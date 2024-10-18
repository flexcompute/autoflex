"""
This contains all the relevant types used for the documentation constructors and base definition.
"""
import pydantic.fields
from pydantic import Field
from typing import Union
from autoflex.types.core import AutoflexBaseModel

class Symbolic(AutoflexBaseModel):
    """
    A class representing a symbolic representation of a label and math formula.

    Attributes:
        label: The label for the symbolic expression (e.g., 'Force').
        math: The mathematical formula or representation (e.g., 'F = ma').
    """
    label: str = Field(..., description="Label of the symbolic representation")
    math: str = Field(..., description="Mathematical representation or equation")


SymbolicTypes = Union[str, Symbolic]

class Unit(AutoflexBaseModel):
    """
    A class representing a physical unit.

    Attributes:
        name: The name of the unit (e.g., 'meter', 'second').
        symbol: The symbol for the unit (e.g., 'm', 's').
        description: An optional description of the unit.
    """
    name: str = Field(..., description="Name of the unit")
    symbol: SymbolicTypes = Field(..., description="Symbol for the unit")
    description: str = Field(None, description="Optional description of the unit")

UnitTypes = Union[str, Unit]
