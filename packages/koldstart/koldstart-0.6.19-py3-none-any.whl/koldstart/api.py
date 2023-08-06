from __future__ import annotations

import os
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field, replace
from functools import partial, wraps
from typing import Any, Callable, ClassVar, Dict, Generic, TypeVar, cast

import dill
import grpc
import isolate
import yaml
from isolate.backends.common import active_python
from isolate.backends.settings import DEFAULT_SETTINGS
from isolate.connections import PythonIPC
from koldstart.sdk import (
    KOLDSTART_DEFAULT_KEEP_ALIVE,
    Credentials,
    HostedRunState,
    KoldstartClient,
    KoldstartConnection,
    MachineRequirements,
    _get_agent_credentials,
    get_default_credentials,
)

dill.settings["recurse"] = True

ReturnT = TypeVar("ReturnT")
BasicConfig = Dict[str, Any]
_UNSET = object()


@dataclass
class KoldstartError(Exception):
    message: str


@dataclass
class InternalKoldstartError(Exception):
    ...


@dataclass
class Host:
    """The physical environment where the isolated code
    is executed."""

    _SUPPORTED_KEYS: ClassVar[frozenset[str]] = frozenset()

    @classmethod
    def parse_key(cls, key: str, value: Any) -> tuple[Any, Any]:
        if key == "env_yml":
            # Conda environment definition should be parsed before sending
            # to koldstart
            with open(value) as f:
                return "env_dict", yaml.safe_load(f)
        else:
            return key, value

    @classmethod
    def parse_options(cls, **config: Any) -> Options:
        """Split the given set of options into host and
        environment options."""

        options = Options()
        for key, value in config.items():
            key, value = cls.parse_key(key, value)
            if key in cls._SUPPORTED_KEYS:
                options.host[key] = value
            else:
                options.environment[key] = value
        return options

    def run(
        self,
        func: Callable[..., ReturnT],
        options: Options,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> ReturnT:
        """Run the given function in the isolated environment."""
        raise NotImplementedError


def _execution_controller(
    func: Callable[..., ReturnT],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> Callable[..., ReturnT]:
    """Handle the execution of the given user function."""

    @wraps(func)
    def wrapper(*remote_args: Any, **remote_kwargs: Any) -> ReturnT:
        return func(*remote_args, *args, **remote_kwargs, **kwargs)

    return wrapper


@dataclass
class LocalHost(Host):
    # The environment which provides the default set of
    # packages for isolate agent to run.
    _AGENT_ENVIRONMENT = isolate.prepare_environment(
        "virtualenv",
        requirements=[f"dill=={dill.__version__}"],
    )

    def run(
        self,
        func: Callable[..., ReturnT],
        options: Options,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> ReturnT:
        settings = replace(DEFAULT_SETTINGS, serialization_method="dill")
        environment = isolate.prepare_environment(
            **options.environment,
            context=settings,
        )
        with PythonIPC(
            environment,
            environment.create(),
            extra_inheritance_paths=[self._AGENT_ENVIRONMENT.create()],
        ) as connection:
            executable = partial(func, *args, **kwargs)
            return connection.run(executable)


KOLDSTART_DEFAULT_URL = os.getenv("KOLDSTART_HOST", "api.alpha.fal.ai:443")
KOLDSTART_DEFAULT_MACHINE_TYPE = "XS"


import threading


# TODO: Should we build all these in fal/dbt-fal packages instead?
@dataclass
class KoldstartHost(Host):
    _SUPPORTED_KEYS = frozenset({"machine_type", "keep_alive", "setup_function"})

    url: str = KOLDSTART_DEFAULT_URL
    credentials: Credentials = field(default_factory=get_default_credentials)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self.credentials = _get_agent_credentials(self.credentials)

    @property
    def _connection(self) -> KoldstartConnection:
        with self._lock:
            client = KoldstartClient(self.url, self.credentials)
            return client.connect()

    def run(
        self,
        func: Callable[..., ReturnT],
        options: Options,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> ReturnT:
        environment_options = options.environment.copy()
        environment_options.setdefault("python_version", active_python())
        environments = [self._connection.define_environment(**environment_options)]

        machine_type = options.host.get("machine_type", KOLDSTART_DEFAULT_MACHINE_TYPE)
        keep_alive = options.host.get("keep_alive", KOLDSTART_DEFAULT_KEEP_ALIVE)
        setup_function = options.host.get("setup_function", None)

        machine_requirements = MachineRequirements(
            machine_type=machine_type, keep_alive=keep_alive
        )

        return_value = _UNSET
        # Allow isolate provided arguments (such as setup function) to take
        # precedence over the ones provided by the user.
        partial_func = _execution_controller(func, args, kwargs)
        for partial_result in self._connection.run(
            partial_func,
            environments,
            machine_requirements=machine_requirements,
            setup_function=setup_function,
        ):
            for log in partial_result.logs:
                print(str(log))

            if partial_result.status.state is not HostedRunState.IN_PROGRESS:
                state = partial_result.status.state
                if state is HostedRunState.INTERNAL_FAILURE:
                    raise InternalKoldstartError(
                        "An internal failure occurred while performing this run."
                    )
                elif state is HostedRunState.SUCCESS:
                    return_value = partial_result.result
                else:
                    raise NotImplementedError("Unknown state: ", state)

        if return_value is _UNSET:
            raise InternalKoldstartError("The input function did not return any value.")

        return cast(ReturnT, return_value)


@dataclass
class Options:
    host: BasicConfig = field(default_factory=dict)
    environment: BasicConfig = field(default_factory=dict)


_DEFAULT_HOST = KoldstartHost()


def isolated(
    kind: str = "virtualenv",
    *,
    host: Host = _DEFAULT_HOST,
    **config: Any,
) -> Callable[[Callable[..., ReturnT]], IsolatedFunction[ReturnT]]:
    options = host.parse_options(kind=kind, **config)

    def wrapper(func: Callable[..., ReturnT]) -> IsolatedFunction[ReturnT]:
        proxy = IsolatedFunction(
            host=host,
            func=func,
            options=options,
        )
        return wraps(func)(proxy)

    return wrapper


@dataclass
class IsolatedFunction(Generic[ReturnT]):
    host: Host
    func: Callable[..., ReturnT]
    options: Options
    executor: ThreadPoolExecutor = field(default_factory=ThreadPoolExecutor)

    def submit(self, *args: Any, **kwargs: Any) -> Future[ReturnT]:
        # TODO: This should probably live inside each host since they can
        # have more optimized Future implementations (e.g. instead of real
        # threads, they can use state observers and detached runs).

        future = self.executor.submit(
            self.host.run,
            func=self.func,  # type: ignore
            options=self.options,
            args=args,
            kwargs=kwargs,
        )
        return cast(Future[ReturnT], future)

    def __call__(self, *args, **kwargs) -> ReturnT:
        try:
            return self.host.run(
                self.func,
                self.options,
                args=args,
                kwargs=kwargs,
            )
        except grpc._channel._MultiThreadedRendezvous as e:
            if (
                e.code() == grpc.StatusCode.UNAVAILABLE
                and type(self.host) == KoldstartHost
            ):
                raise KoldstartError(
                    f"Could not reach koldstart host url: {self.host.url}. "
                    "This is most likely a transient problem. "
                    "Please, try again."
                )
            raise e

    def on(self, host: Host | None = None, **config: Any) -> IsolatedFunction[ReturnT]:
        host = host or self.host
        if isinstance(host, type(self.host)):
            previous_host_options = self.options.host
        else:
            previous_host_options = {}

        # The order of the options is important here (the latter
        # options override the former ones).
        host_options = {**previous_host_options, **config}
        new_options = host.parse_options(**self.options.environment, **host_options)
        return replace(
            self,
            host=host,
            options=new_options,
        )
