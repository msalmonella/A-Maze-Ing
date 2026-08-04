from pydantic import BaseModel, Field, field_validator, ValidationError
from pydantic_core import PydanticCustomError
from .models import Coordinate
from .generators import Generator, MazerTheMiner
from .solvers import Solver, BFS
from .renderers import Renderer, HexWriter
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
    renderer: type[Renderer] = Field(default=HexWriter)

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

    @field_validator("generator", mode="before")
    @classmethod
    def _str_to_generator(cls, method: str | Generator) -> Generator:
        if isinstance(method, str):
            try:
                return getattr(generators, method)
            except AttributeError as e:
                raise PydanticCustomError(
                    "generator",
                    "No such generator found named '{method}'",
                    {"method": method},
                ) from e
        return method

    @field_validator("solver", mode="before")
    @classmethod
    def _str_to_solver(cls, method: str | Solver) -> Solver:
        if isinstance(method, str):
            try:
                return getattr(solvers, method)
            except AttributeError as e:
                raise PydanticCustomError(
                    "solver",
                    "No such solver found named '{method}'",
                    {"method": method},
                ) from e
        return method

    @field_validator("renderer", mode="before")
    @classmethod
    def _str_to_renderer(cls, method: str | Renderer) -> Renderer:
        if isinstance(method, str):
            try:
                return getattr(renderers, method)
            except AttributeError as e:
                raise PydanticCustomError(
                    "renderer",
                    "No such renderer found named '{method}'",
                    {"method": method},
                ) from e
        return method


def parse_config(filepath: str) -> Config:
    """Parses the given config file"""

    config: dict[str, str] = {}
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config[key.strip().lower()] = value.strip()

    return Config(**config)  # type: ignore


if __name__ == "__main__":
    try:
        config = parse_config("config.txt")
        print("-" * 40)
        print("Testing config")
        print("-" * 40)
        print(parse_config("config.txt").model_dump())
    except ValidationError as e:
        for err in e.errors():
            msg = err.get("msg")
            loc = err.get("loc")
            locs = ", ".join([str(l) for l in loc])
            print(f"{msg}: {locs}")
