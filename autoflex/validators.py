from pydantic.fields import FieldInfo

def check_json_schema_extra(field: FieldInfo) -> bool:
    """Check if the FieldInfo contains a 'json_schema_extra' parameter."""
    return hasattr(field, 'json_schema_extra') and field.json_schema_extra is not None
