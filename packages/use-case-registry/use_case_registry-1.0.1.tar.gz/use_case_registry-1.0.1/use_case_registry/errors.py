"""Custom defined errors."""
import abc


class NotIdentifiedError(Exception):
    """Error placeholder to be used when an not identified error is raised."""

    def __init__(self, error: Exception) -> None:  # noqa: D107
        super().__init__(f"Not indentified error. {error}")


class IdentifiedError(abc.ABC, Exception):
    """Parent class for all defined errors at application level."""


class CommandInputValidationError(IdentifiedError):
    """Raised when command input values does pass validation check."""
