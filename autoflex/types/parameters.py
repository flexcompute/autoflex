from pydantic import Field
from autoflex.types.core import AutoflexBaseModel
from autoflex.types.descriptors import Unit, SymbolicTypes

class PhysicalParameter(AutoflexBaseModel):
    """
    This structure instance is a representation of the relevant information that might want to represent in a parameter
    row or in another container.

    We need the parameter name, the type definition in a format we might want to represent (or even interact with)
    a description which may be
    """
    name: str = ""
    types: str = ""
    description: str = ""
    math: SymbolicTypes = Field(..., description="The mathematical representation defining the physical parameter in raw string latex")
    unit: Unit = Field(..., description="The unit of the physical parameter")


AutoflexParameterTypes = PhysicalParameter
