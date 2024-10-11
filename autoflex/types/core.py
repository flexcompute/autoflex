from pydantic import BaseModel

class AutoflexBaseModel(BaseModel):
    """
    A base class that can be used for any model within the system.
    It inherits from Pydantic's BaseModel to leverage data validation
    and parsing features.
    """
