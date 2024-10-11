from autoflex.types.core import AutoflexBaseModel
from autoflex.types.descriptors import AutoflexParameterTypes


class ParameterTable(AutoflexBaseModel):
    name: str
    types: str
    description: str
    special_parameters: AutoflexParameterTypes
