"""Various exceptions managed in this module."""

from pydantic import ValidationError


class MazeError(Exception):
    """Base MazeGenerator error."""


class ConfigError(MazeError):
    """Invalid configuration.

    Attributes:
        validation (ValidationError):
            Stores the ValidationError object raised by 'pydantic'
    """

    def __init__(
        self, message: str, validation: ValidationError | None = None
    ):
        """Initializes a ConfigError.

        Args:
            message (str):
                A message describing the main problem.
            validation (ValidationError, optional):
                ValidationError object raised by 'pydantic'
        """
        errors = (
            [
                f"{' - '.join(str(loc).upper() for loc in err['loc'])}: "
                f"{err['msg']}"
                for err in validation.errors(
                    include_url=False,
                    include_input=False,
                    include_context=False,
                )
            ]
            if validation
            else []
        )

        super().__init__(message, *errors)
        self.validation = validation


class LockedWallError(MazeError):
    """Attempt to modify a locked wall."""


class PatternError(MazeError):
    """Invalid attempt to place the 42 pattern."""
