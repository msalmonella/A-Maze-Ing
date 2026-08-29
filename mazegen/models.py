from typing import NamedTuple, Self
from enum import IntFlag
from pydantic import (
    Field,
    field_validator,
    model_validator,
    ValidationError,
)
from pydantic_core import PydanticCustomError, InitErrorDetails
from pydantic.dataclasses import dataclass as pydantic_dataclass


class Direction(IntFlag):
    """Binary representation of closed walls."""

    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000


class Coordinate(NamedTuple):
    """Indicates a position on a maze grid."""

    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


Path = list[Coordinate]


@pydantic_dataclass
class Mandatory:

    entry: Coordinate
    exit: Coordinate
    perfect: bool
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    output_file: str = Field(min_length=1)

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
