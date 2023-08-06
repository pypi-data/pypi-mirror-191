import abc
from typing import List, Optional

from chalk.client.models import ChalkError


class ChalkBaseException(Exception, abc.ABC):
    """The base type for Chalk exceptions.

    This exception makes error handling easier, as you can
    look only for this exception class.
    """

    message: str
    """A message describing the specific type of exception raised."""

    full_message: str
    """A message that describes the specific type of exception raised
    and contains the readable representation of each error in the
    errors attribute.
    """

    errors: List[ChalkError]
    """The errors from executing a Chalk operation.

    These errors contain more detailed information about
    why the exception occurred.
    """

    def __init__(self, errors: Optional[List[ChalkError]] = None):
        if errors is None:
            errors = []

        self.errors = errors

        super().__init__(self.full_message)

    @property
    def message(self) -> str:
        raise NotImplementedError

    @property
    def full_message(self) -> str:
        if self.errors:
            return self.message + "\n" + "\n".join(["\t" + e.message for e in self.errors])

        return self.message


class ChalkWhoAmIException(ChalkBaseException):
    @property
    def message(self) -> str:
        return "Failed to retrieve current user information during who-am-I check"


class ChalkOnlineQueryException(ChalkBaseException):
    @property
    def message(self) -> str:
        return "Failed to execute online query"


class ChalkOfflineQueryException(ChalkBaseException):
    @property
    def message(self) -> str:
        return "Failed to execute offline query"

    @property
    def full_message(self) -> str:
        return self.message + "\n" + "\n".join(["\t" + e.message for e in self.errors[0:3]])


class ChalkComputeResolverException(ChalkOfflineQueryException):
    @property
    def message(self) -> str:
        return "Failed to compute resolver output"


class ChalkResolverRunException(ChalkBaseException):
    @property
    def message(self) -> str:
        return "Resolver run failed"


class ChalkDatasetDownloadException(ChalkBaseException):
    @property
    def message(self) -> str:
        return "Failed to download dataset"


__all__ = [
    "ChalkBaseException",
    "ChalkOnlineQueryException",
    "ChalkOfflineQueryException",
    "ChalkResolverRunException",
    "ChalkDatasetDownloadException",
    "ChalkComputeResolverException",
    "ChalkWhoAmIException",
]
