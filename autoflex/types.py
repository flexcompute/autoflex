import pydantic

class AutoflexBaseClass(pydantic.BaseModel):
    pass



class Unit:
    pass

class AttributeDocumentation(AutoflexBaseClass):
    name: str
    units: Unit
    types: pydantic.BaseModel

class MethodDocumentationSchema(AutoflexBaseClass):
    name: str
    description: str


class ClassDocumentation(AutoflexBaseClass):
    """

    """
    attribute_list = list[AttributeDocumentation]
    method_list = list[MethodDocumentationSchema]

class ParameterTable(AutoflexBaseClass):
    pass
