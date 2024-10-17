import pydantic as pd
from autoflex.types.parameters import AutoflexParameterTypes

class AutoflexFieldInfo(pd.fields.FieldInfo):
    """
    Each field should correspond to an individual parameter field that can represent it completely within the documentation.
    """
    autoflex: AutoflexParameterTypes
