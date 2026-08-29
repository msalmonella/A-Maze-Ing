"""Configuration parsing and validation for the maze application."""

from types import ModuleType
from typing import cast
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ValidationError,
    ValidationInfo,
    ConfigDict,
)
from pydantic_core import PydanticCustomError
from .models import Mandatory
from .errors import ConfigError
from .algorithms import Algorithm, MazerTheMiner
from .solvers import Solver, BFS
from .renderers import Renderer, AsciiRenderer
from . import algorithms, solvers, renderers


class Operations(BaseModel):
    """Defines the configurable maze operation implementations.

    The operations model specifies the algorithm, solver, and renderer used by
    the maze application. Each operation can be provided either as an instance
    of its corresponding type or as the name of a class available in the
    appropriate module.

    Attributes:
        algorithm (Algorithm): The maze-generation algorithm to use. Defaults
            to `MazerTheMiner`.
        solver (Solver): The maze-solving algorithm to use. Defaults to `BFS`.
        renderer (Renderer): The maze renderer to use. Defaults to
            `AsciiRenderer`.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    algorithm: Algorithm = Field(default=MazerTheMiner())
    solver: Solver = Field(default=BFS())
    renderer: Renderer = Field(default=AsciiRenderer())

    @field_validator("algorithm", "solver", "renderer", mode="before")
    @classmethod
    def _lookup_class(
        cls, value: str | ModuleType, info: ValidationInfo
    ) -> ModuleType:
        """Resolve an operation name to an instantiated implementation.

        String values are interpreted as class names and looked up in the
        module corresponding to the validated field. Non-string values are
        returned unchanged.

        Args:
            value: An operation instance or the name of an operation class.
            info:
                Pydantic validation information containing the field being
                validated.

        Returns:
            The supplied non-string value, or an instantiated operation
            corresponding to the supplied class name.

        Raises:
            PydanticCustomError:
                If no operation with the supplied name exists in the module
                associated
        """

        if not isinstance(value, str):
            return value

        assert info.field_name is not None
        modules: dict[str, ModuleType] = {
            "algorithm": algorithms,
            "solver": solvers,
            "renderer": renderers,
        }
        module = modules[info.field_name]

        try:
            return cast(ModuleType, getattr(module, value)())
        except AttributeError as e:
            raise PydanticCustomError(
                "module_not_found",
                "No such {field_name} found named '{method}'",
                {"method": value, "field_name": info.field_name},
            ) from e


class Config(BaseModel):
    """Stores and validates maze configuration attributes.

    Attributes:
        mandatory (Mandatory): Values required to generate the maze.
        operations (Operations): Represents maze operations.
        seed (str): Seed used for deterministic maze generation.
        sps (int): Steps per second used during maze generation or display.
    """

    mandatory: Mandatory
    operations: Operations
    seed: str = Field(default="")
    sps: int = Field(default=24, ge=0)


def parse_config(filepath: str) -> Config:
    """Parses a configuration file and validates its contents.

    Args:
        filepath (str): Path to the configuration file to read.

    Returns:
        A validated `Config` instance containing the parsed settings.

    Raises:
        ConfigError:
            If the file cannot be read, contains invalid configuration values,
            or has a malformed key/value pair.
    """

    try:
        config: dict[str, str] = {}
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                config[key.strip().lower()] = value.strip()

        return Config(
            mandatory={**config},  # type: ignore
            operations={**config},  # type: ignore
            **config,  # type: ignore
        )
    except OSError as e:
        raise ConfigError("Could not read the file") from e
    except ValidationError as e:
        raise ConfigError("Invalid maze configuration", e) from e
    except ValueError as e:
        raise ConfigError("Bad key/value format (expected 'key=value')") from e


def main() -> None:
    """Parses the configuration file and displays the validated settings.

    Raises:
        ConfigError: If the configuration file is invalid or cannot be read.
    """

    try:
        config = parse_config("config.txt")
        print("-" * 40)
        print("Testing config")
        print("-" * 40)
        print(config.model_dump())
    except ConfigError as e:
        print(e)
        if e.validation:
            print()
            for err in e.validation.errors():
                msg = err.get("msg")
                loc = err.get("loc")
                locs = ", ".join([str(lo) for lo in loc])
                print(f"{locs}: {msg}")


if __name__ == "__main__":
    main()
