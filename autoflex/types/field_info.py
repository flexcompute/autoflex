import pydantic as pd
from autoflex.types.descriptors import UnitTypes, SymbolicTypes

class PhysicalFieldInfo(pd.fields.FieldInfo):
    """
    Each field should correspond to an individual physical property field that can represent it completely within the documentation.

    Note that this compiles into a PhysicalProperty accordingly.
    """

    unit: UnitTypes = ""
    """
    """

    math: SymbolicTypes = ""
    """
    """


FieldTypes = PhysicalFieldInfo | pd.fields.FieldInfo
