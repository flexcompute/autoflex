from pydantic.fields import FieldInfo
from pydantic import BaseModel

def check_json_schema_extra(field: FieldInfo) -> bool:
    """Check if the FieldInfo contains a 'json_schema_extra' parameter."""
    return hasattr(field, 'json_schema_extra') and field.json_schema_extra is not None



def determine_pydantic_version_from_base_model(model: BaseModel):
    """Determine if a BaseModel is from Pydantic v1 or v2."""
    if hasattr(model, 'model_fields'):
        return 2
    elif hasattr(model, '__fields__'):
        return 1
    else:
        raise ValueError("Unknown Pydantic version or incompatible BaseModel class.")


def get_field_infos(model: BaseModel):
    """Get all FieldInfo instances from a Pydantic model, compatible with v1 and v2."""
    version = determine_pydantic_version_from_base_model(model)

    field_infos = []

    # Handle Pydantic v2
    if version == 2:
        for field_name, field in model.model_fields.items():
            field_infos.append(field)

    # Handle Pydantic v1
    elif version == 1:
        for field_name, field in model.__fields__.items():
            field_infos.append(field)

    return field_infos
