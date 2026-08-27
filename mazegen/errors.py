from pydantic import ValidationError


class MazeError(Exception):
    """Base MazeGenerator error."""


class ConfigError(MazeError):
    """Invalid configuration."""

    def __init__(
        self, message: str, validation: ValidationError | None = None
    ):
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
