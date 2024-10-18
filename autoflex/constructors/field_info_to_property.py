"""
This file contains all the functionality to convert from a compiled `AutoflexFieldInfo` or standard pydantic `FieldInfo`
into a AutoflexPropertyType. This way all the fields and annotations can be compiled into a standardized data type
"""
from autoflex.types import FieldTypes

def compile_field_into_property(
    field: FieldTypes
):
    """
    """
