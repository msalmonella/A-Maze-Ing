from types import ModuleType
from typing import cast, Self
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ValidationError,
    ValidationInfo,
)
from pydantic_core import PydanticCustomError, InitErrorDetails
from .models import Coordinate
from .errors import ConfigError
from .generators import Generator, MazerTheMiner
from .solvers import Solver, BFS
from .renderers import Renderer, AsciiRenderer
from . import generators, solvers, renderers


class Config(BaseModel):
    """Handles validation for the maze attributes"""

    width: int = Field(ge=2)
    height: int = Field(ge=2)
    entry: Coordinate
    exit: Coordinate
    output_file: str = Field(min_length=1)
    perfect: bool

    seed: str = Field(default="")
    generator: type[Generator] = Field(default=MazerTheMiner)
    solver: type[Solver] = Field(default=BFS)
    renderer: type[Renderer] = Field(default=AsciiRenderer)

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def _str_to_coordinate(cls, value: str | Coordinate) -> Coordinate:
        if isinstance(value, str):
            try:
                x, y = value.split(",")
                return Coordinate(int(x), int(y))
            except ValueError as e:
                raise ValueError(
                    "Coordinates must be two comma-separated integers"
                ) from e
        return value

    @field_validator("generator", "solver", "renderer", mode="before")
    @classmethod
    def _lookup_class(
        cls, value: str | ModuleType, info: ValidationInfo
    ) -> ModuleType:
        if not isinstance(value, str):
            return value

        assert info.field_name is not None
        modules: dict[str, ModuleType] = {
            "generator": generators,
            "solver": solvers,
            "renderer": renderers,
        }
        module = modules[info.field_name]

        try:
            return cast(ModuleType, getattr(module, value))
        except AttributeError as e:
            raise PydanticCustomError(
                "module_not_found",
                "No such {field_name} found named '{method}'",
                {"method": value, "field_name": info.field_name},
            ) from e

    @model_validator(mode="after")
    def _validate_entry_exit(self) -> Self:
        errors: list[InitErrorDetails] = []

        if self.entry == self.exit:
            errors.append(
                {
                    "type": PydanticCustomError(
                        "identical_points",
                        "Entry and exit points must be different",
                    ),
                    "input": (self.entry, self.exit),
                }
            )

        for name, point in [("entry", self.entry), ("exit", self.exit)]:
            if point.x >= self.width or point.y >= self.height:
                errors.append(
                    {
                        "type": PydanticCustomError(
                            "point_out_of_bounds",
                            "The {name} point is out of bounds",
                            {"name": name},
                        ),
                        "loc": (name,),
                        "input": point,
                    }
                )

        if errors:
            raise ValidationError.from_exception_data(
                self.__class__.__name__, errors
            )

        return self


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

        return Config(**config)  # type: ignore
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
