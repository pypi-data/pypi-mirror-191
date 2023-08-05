import inspect
from typing import Any, Callable, List, Literal, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from typing_extensions import ParamSpec

from chalk.state import KeyedState
from chalk.streams._file_source import FileSource
from chalk.streams._kafka_source import KafkaSource
from chalk.streams._windows import Windowed, get_duration_secs, get_name_with_duration, windowed
from chalk.streams.base import StreamSource
from chalk.utils import MachineType

__all__ = [
    "FileSource",
    "KafkaSource",
    "KeyedState",
    "StreamSource",
    "Windowed",
    "stream",
    "windowed",
    "get_name_with_duration",
    "get_duration_secs",
]

P = ParamSpec("P")
T = TypeVar("T")

MessageType = TypeVar("MessageType", bound=BaseModel)


def stream(
    *,
    source: StreamSource,
    mode: Optional[Literal["continuous", "tumbling"]] = None,
    environment: Optional[Union[List[str], str]] = None,
    machine_type: Optional[MachineType] = None,
    message: Optional[Type[Any]] = None,
    owner: Optional[str] = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to create a stream resolver.

    Parameters
    ----------
    source
        The streaming source, e.g. `KafkaSource()`
    mode
        The streaming mode, either "continuous" or "tumbling".
    environment
        Environments are used to trigger behavior in different deployments
        such as staging, production, and local development.

        Environment can take one of three types:
            - None (default) - candidate to run in every environment
            - str - run only in this environment
            - list[str] - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    machine_type
        You can optionally specify that resolvers need to run
        on a machine other than the default. Must be configured
        in your deployment.
    message
        A `dataclass` describing the JSON format of the messages on
        the topic.
    owner
        Allows you to specify an individual or team who is responsible
        for this resolver. The Chalk Dashboard will display this field,
        and alerts can be routed to owners.

    Returns
    -------
    Callable[[Any, ...], Any]
        A callable function! You can unit-test resolvers as you would
        unit-test any other code.

        Read more at https://docs.chalk.ai/docs/unit-tests
    """
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_globals = caller_frame.frame.f_globals
    caller_locals = caller_frame.frame.f_locals
    from chalk.features.resolver import parse_and_register_stream_resolver

    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        return parse_and_register_stream_resolver(
            caller_globals=caller_globals,
            caller_locals=caller_locals,
            fn=fn,
            source=source,
            mode=mode,
            caller_filename=caller_filename,
            environment=environment,
            machine_type=machine_type,
            message=message,
            owner=owner,
        )

    return decorator
