import pydantic as pd

def determine_pydantic_version_from_base_model(model: pd.BaseModel):
    """Determine if a BaseModel is from Pydantic v1 or v2."""
    if hasattr(model, 'model_fields'):
        return 2
    elif hasattr(model, '__fields__'):
        return 1
    else:
        raise ValueError("Unknown Pydantic version or incompatible BaseModel class.")
