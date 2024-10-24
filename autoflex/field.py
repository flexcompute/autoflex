from typing import Any, Optional
from pydantic import Field
from autoflex.types import PhysicalFieldInfo, UnitTypes, SymbolicTypes


def PhysicalField(
    default: Any = ...,
    *,
    unit: UnitTypes,
    math: SymbolicTypes,
    **kwargs
) -> PhysicalFieldInfo:
    """
    A wrapper around pydantic's Field function that returns an instance of AutoflexFieldInfo
    instead of FieldInfo.

    Args:
        default: The default value of the field.
        unit: The UnitType to represent.
        math: The SymbolicType to represent.
        **kwargs: Any other keyword arguments passed to pydantic's Field.

    Returns:
        AutoflexFieldInfo: Custom field info object.
    """

    # Need to compile this into a FieldInfo in order to extract the correct kwargs.
    field_info = Field(default=default, **kwargs)

    # Return an instance of AutoflexFieldInfo instead of the default FieldInfo
    return PhysicalFieldInfo(
        default=default,
        unit=unit,
        math=math,

    )
