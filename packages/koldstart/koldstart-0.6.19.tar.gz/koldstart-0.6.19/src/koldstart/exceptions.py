from __future__ import annotations

from typing import Generic, TypeVar

from click import Group
from grpc import Call as RpcCall

ExceptionType = TypeVar("ExceptionType")


class BaseExceptionHandler(Generic[ExceptionType]):
    """Base handler defaults to the string representation of the error"""

    def should_handle(self, _: Exception) -> bool:
        return True

    def handle(self, exception: ExceptionType):
        print(exception.__str__)


class GrpcExceptionHandler(BaseExceptionHandler[RpcCall]):
    """Handle GRPC errors. The user message is part of the `details()`"""

    def should_handle(self, exception: Exception) -> bool:
        return isinstance(exception, RpcCall)

    def handle(self, exception: RpcCall):
        print(exception.details())


class ApplicationExceptionHandler(Group):
    """Handle exceptions of a CLI `click.Group`.

    This exception handler is capable of handling, i.e. customize the output
    and add behavior, of any type of exception. Click handles all `ClickException`
    types by default, but prints the stack for other exception not wrapped in ClickException.

    The handler also allows for central metrics and logging collection.
    """

    handlers: list[BaseExceptionHandler] = [GrpcExceptionHandler()]

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except Exception as e:
            match_handler: BaseExceptionHandler = next(
                (h for h in self.handlers if h.should_handle(e)), BaseExceptionHandler()
            )
            match_handler.handle(e)
