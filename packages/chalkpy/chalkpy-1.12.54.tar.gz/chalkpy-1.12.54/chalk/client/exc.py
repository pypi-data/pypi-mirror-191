from typing import List

from chalk.client.models import ChalkError


class ChalkBaseException(Exception):
    """The base type for Chalk exceptions.

    This exception makes error handling easier, as you can
    look only for this exception class.
    """

    ...


class ChalkOfflineQueryException(ChalkBaseException):
    message: str
    """A readable message describing the overall error."""

    errors: List[ChalkError]
    """The errors from running the offline query.

    These errors contain more detailed information about
    why the exception occurred.
    """

    def __init__(self, message: str, errors: List[ChalkError]):
        self.message = message
        self.errors = errors
        super().__init__(message + "\n" + "\n".join(["\t" + e.message for e in errors[0:3]]))


class ChalkResolverRunException(ChalkBaseException):
    message: str
    """A readable message describing the overall error."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ChalkDatasetDownloadException(ChalkBaseException):
    message: str
    """A readable message describing the overall error."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


__all__ = [
    "ChalkBaseException",
    "ChalkOfflineQueryException",
    "ChalkResolverRunException",
    "ChalkDatasetDownloadException",
]
