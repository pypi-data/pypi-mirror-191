from __future__ import annotations

import os
from contextlib import ExitStack
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Generic, Iterator, TypeVar

import grpc
import isolate_proto
from isolate.connections.common import is_agent
from isolate.logs import Log
from isolate.server.interface import from_grpc, to_serialized_object
from isolate_proto.configuration import GRPC_OPTIONS
from koldstart import flags
from koldstart.auth import USER

ResultT = TypeVar("ResultT")
InputT = TypeVar("InputT")
UNSET = object()

_DEFAULT_SERIALIZATION_METHOD = "dill"
KOLDSTART_DEFAULT_KEEP_ALIVE = 10


class Credentials:
    def to_grpc(self) -> grpc.ChannelCredentials:
        raise NotImplementedError

    @property
    def extra_options(self) -> list[tuple[str, str]]:
        return GRPC_OPTIONS


class LocalCredentials(Credentials):
    def to_grpc(self) -> grpc.ChannelCredentials:
        return grpc.local_channel_credentials()


@dataclass
class _GRPCMetadata(grpc.AuthMetadataPlugin):
    """Key value metadata bundle for gRPC credentials"""

    _key: str
    _value: str

    def __call__(
        self,
        context: grpc.AuthMetadataContext,
        callback: grpc.AuthMetadataPluginCallback,
    ) -> None:
        callback(((self._key, self._value),), None)


@dataclass
class CloudKeyCredentials(Credentials):
    key_id: str
    key_secret: str

    def to_grpc(self) -> grpc.ChannelCredentials:
        return grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(),
            grpc.metadata_call_credentials(_GRPCMetadata("auth-key", self.key_secret)),
            grpc.metadata_call_credentials(_GRPCMetadata("auth-key-id", self.key_id)),
        )


@dataclass
class AuthenticatedCredentials(Credentials):
    user = USER

    def to_grpc(self) -> grpc.ChannelCredentials:
        return grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(),
            grpc.access_token_call_credentials(USER.access_token),
        )


def _key_credentials() -> CloudKeyCredentials | None:
    if "KOLDSTART_KEY_ID" in os.environ and "KOLDSTART_KEY_SECRET" in os.environ:
        return CloudKeyCredentials(
            os.environ["KOLDSTART_KEY_ID"],
            os.environ["KOLDSTART_KEY_SECRET"],
        )
    else:
        return None


def _get_agent_credentials(original_credentials: Credentials) -> Credentials:
    """If running inside an koldstart box, use the preconfigured credentials
    instead of the user provided ones."""

    key_creds = _key_credentials()
    if is_agent() and key_creds:
        return key_creds
    else:
        return original_credentials


def get_default_credentials() -> Credentials:
    if flags.TEST_MODE:
        return LocalCredentials()
    else:
        key_creds = _key_credentials()
        if key_creds:
            return key_creds
        else:
            return AuthenticatedCredentials()


@dataclass
class KoldstartClient:
    hostname: str
    credentials: Credentials = field(default_factory=get_default_credentials)

    def connect(self) -> KoldstartConnection:
        return KoldstartConnection(self.hostname, self.credentials)


class ScheduledRunState(Enum):
    SCHEDULED = 0
    INTERNAL_FAILURE = 1
    USER_FAILURE = 2


class HostedRunState(Enum):
    IN_PROGRESS = 0
    SUCCESS = 1
    INTERNAL_FAILURE = 2


@dataclass
class HostedRunStatus:
    state: HostedRunState


@dataclass
class ScheduledRun:
    run_id: str
    state: ScheduledRunState
    cron: str


@dataclass
class ScheduledRunActivation:
    run_id: str
    activation_id: str


@dataclass
class HostedRunResult(Generic[ResultT]):
    run_id: str
    status: HostedRunStatus
    logs: list[Log] = field(default_factory=list)
    result: ResultT | None = None


@from_grpc.register(isolate_proto.HostedRunStatus)
def _from_grpc_hosted_run_status(
    message: isolate_proto.HostedRunStatus,
) -> HostedRunStatus:
    return HostedRunStatus(HostedRunState(message.state))


@from_grpc.register(isolate_proto.HostedRunResult)
def _from_grpc_hosted_run_result(
    message: isolate_proto.HostedRunResult,
) -> HostedRunResult[Any]:
    if message.return_value.definition:
        return_value = from_grpc(message.return_value)
    else:
        return_value = UNSET

    return HostedRunResult(
        message.run_id,
        from_grpc(message.status),
        logs=[from_grpc(log) for log in message.logs],
        result=return_value,
    )


_SUPPORTED_MACHINE_TYPES = ["XS", "S", "M", "L", "GPU"]


def _get_run_id(run: ScheduledRun | str) -> str:
    if isinstance(run, ScheduledRun):
        return run.run_id
    else:
        return run


@dataclass
class MachineRequirements:
    machine_type: str
    keep_alive: int = KOLDSTART_DEFAULT_KEEP_ALIVE

    def __post_init__(self):
        assert self.machine_type in _SUPPORTED_MACHINE_TYPES


@dataclass
class KoldstartConnection:
    hostname: str
    credentials: Credentials

    _stack: ExitStack = field(default_factory=ExitStack)
    _stub: isolate_proto.IsolateControllerStub | None = None

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._stack.close()

    def close(self):
        self._stack.close()

    @property
    def stub(self) -> isolate_proto.IsolateControllerStub:
        if self._stub:
            return self._stub

        options = self.credentials.extra_options
        channel_creds = self.credentials.to_grpc()
        channel = self._stack.enter_context(
            grpc.secure_channel(self.hostname, channel_creds, options)
        )
        self._stub = isolate_proto.IsolateControllerStub(channel)
        return self._stub

    def create_user_key(self) -> tuple[str, str]:
        request = isolate_proto.CreateUserKeyRequest()
        response = self.stub.CreateUserKey(request)
        return response.key_secret, response.key_id

    def list_user_keys(self) -> list[isolate_proto.UserKeyInfo]:
        request = isolate_proto.ListUserKeysRequest()
        response: isolate_proto.ListUserKeysResponse = self.stub.ListUserKeys(request)
        return list(response.user_keys)

    def revoke_user_key(self, key_id) -> None:
        request = isolate_proto.RevokeUserKeyRequest(key_id=key_id)
        self.stub.RevokeUserKey(request)

    # TODO: get rid of this in favor of define_environment
    def create_environment(
        self,
        kind: str,
        configuration_options: dict[str, Any],
    ) -> isolate_proto.EnvironmentDefinition:
        assert isinstance(
            configuration_options, dict
        ), "configuration_options must be a dict"

        struct = isolate_proto.Struct()
        struct.update(configuration_options)

        return isolate_proto.EnvironmentDefinition(
            kind=kind,
            configuration=struct,
        )

    def define_environment(
        self, kind: str, **options: Any
    ) -> isolate_proto.EnvironmentDefinition:
        return self.create_environment(
            kind=kind,
            configuration_options=options,
        )

    def run(
        self,
        function: Callable[..., ResultT],
        environments: list[isolate_proto.EnvironmentDefinition],
        *,
        serialization_method: str = _DEFAULT_SERIALIZATION_METHOD,
        machine_requirements: MachineRequirements | None = None,
        setup_function: Callable[[], InputT] | None = None,
    ) -> Iterator[HostedRunResult[ResultT]]:
        wrapped_function = to_serialized_object(function, serialization_method)
        if machine_requirements:
            wrapped_requirements = isolate_proto.MachineRequirements(
                machine_type=machine_requirements.machine_type,
                keep_alive=machine_requirements.keep_alive,
            )
        else:
            wrapped_requirements = None

        request = isolate_proto.HostedRun(
            function=wrapped_function,
            environments=environments,
            machine_requirements=wrapped_requirements,
        )
        if setup_function:
            request.setup_func.MergeFrom(
                to_serialized_object(setup_function, serialization_method)
            )
        for partial_result in self.stub.Run(request):
            yield from_grpc(partial_result)

    def schedule_run(
        self,
        function: Callable[[], ResultT],
        environments: list[isolate_proto.EnvironmentDefinition],
        cron: str,
        *,
        serialization_method: str = _DEFAULT_SERIALIZATION_METHOD,
        machine_requirements: MachineRequirements | None = None,
    ) -> ScheduledRun:
        wrapped_function = to_serialized_object(function, serialization_method)
        if machine_requirements:
            wrapped_requirements = isolate_proto.MachineRequirements(
                machine_type=machine_requirements.machine_type
            )
        else:
            wrapped_requirements = None

        request = isolate_proto.HostedRunCron(
            function=wrapped_function,
            environments=environments,
            cron=cron,
            machine_requirements=wrapped_requirements,
        )
        response = self.stub.Schedule(request)
        return ScheduledRun(
            response.run_id,
            state=ScheduledRunState(response.state),
            cron=cron,
        )

    def list_scheduled_runs(self) -> list[ScheduledRun]:
        request = isolate_proto.ListScheduledRunsRequest()
        response = self.stub.ListScheduledRuns(request)
        return [
            ScheduledRun(
                run.run_id,
                state=ScheduledRunState(run.state),
                cron=run.cron,
            )
            for run in response.scheduled_runs
        ]

    def cancel_scheduled_run(self, run: ScheduledRun | str) -> None:
        request = isolate_proto.CancelScheduledRunRequest(run_id=_get_run_id(run))
        self.stub.CancelScheduledRun(request)

    def list_run_activations(
        self, run: ScheduledRun | str
    ) -> list[ScheduledRunActivation]:
        request = isolate_proto.ListScheduledRunActivationsRequest(
            run_id=_get_run_id(run)
        )
        response = self.stub.ListScheduledRunActivations(request)
        return [
            ScheduledRunActivation(
                run_id=_get_run_id(run),
                activation_id=activation_id,
            )
            for activation_id in response.activation_ids
        ]

    def get_activation_logs(self, activation: ScheduledRunActivation) -> bytes:
        request = isolate_proto.GetScheduledActivationLogsRequest(
            run_id=activation.run_id,
            activation_id=activation.activation_id,
        )
        response = self.stub.GetScheduledActivationLogs(request)
        return response.raw_logs
