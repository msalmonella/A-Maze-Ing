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
    model_config = ConfigDict(arbitrary_types_allowed=True)

    algorithm: Algorithm = Field(default=MazerTheMiner())
    solver: Solver = Field(default=BFS())
    renderer: Renderer = Field(default=AsciiRenderer())

    @field_validator("algorithm", "solver", "renderer", mode="before")
    @classmethod
    def _lookup_class(
        cls, value: str | ModuleType, info: ValidationInfo
    ) -> ModuleType:
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
    """Handles validation for the maze attributes"""

    mandatory: Mandatory
    operations: Operations
    seed: str = Field(default="")
    sps: int = Field(default=24, ge=0)


def parse_config(filepath: str) -> Config:
    """Parses the given config file"""

    try:
        config: dict[str, str] = {}
        with open(filepath) as f:
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


if __name__ == "__main__":
    try:
        config = parse_config("config.txt")
        print("-" * 40)
        print("Testing config")
        print("-" * 40)
        print(parse_config("config.txt").model_dump())
    except ConfigError as e:
        print(e)
        if e.validation:
            print()
            for err in e.validation.errors():
                msg = err.get("msg")
                loc = err.get("loc")
                locs = ", ".join([str(lo) for lo in loc])
                print(f"{locs}: {msg}")
