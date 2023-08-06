"""Interface for concrete commands."""
import abc

from result import Result

from .errors import CommandInputValidationError


class ICommand(abc.ABC):
    """Command interface."""

    @abc.abstractmethod
    def validate(self) -> Result[None, CommandInputValidationError]:
        """Validate command input values."""
