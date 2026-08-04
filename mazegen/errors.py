from pydantic import ValidationError


class MazeError(Exception):
    """Base MazeGenerator error."""


class ConfigError(MazeError):
    """Invalid configuration."""

    def __init__(self, message: str, validation: ValidationError):
        super().__init__(message)
        self.validation = validation


class LockedWallError(MazeError):
    """Attempt to modify a locked wall."""
