from __future__ import annotations

import warnings
from typing import Any, Callable, Dict, List, Optional, Type

from pydantic import BaseModel, ConfigDict, create_model, Field
from pydantic.fields import FieldInfo
from typing_extensions import TypeGuard

# Define constants
ASTERISK_FIELD_NAME = 'all fields'

# ----------------------------
# Helper Functions and Types
# ----------------------------

def is_pydantic_model(obj: Any) -> TypeGuard[Type[BaseModel]]:
    """Determine if the object is a valid Pydantic model."""
    try:
        return issubclass(obj, BaseModel)
    except TypeError:
        return False


def is_pydantic_field(parent: Any, field_name: str) -> bool:
    """Determine if the given `field_name` is a Pydantic field of the `parent` model."""
    if not is_pydantic_model(parent):
        return False
    return field_name in parent.model_fields


def get_field_names(model: Type[BaseModel]) -> List[str]:
    """Return the field names of the Pydantic model while keeping ordering."""
    return list(model.model_fields.keys())


def get_field_info(model: Type[BaseModel], name: str) -> FieldInfo:
    """Get the instance of `FieldInfo` for the given field `name`."""
    return model.model_fields[name]


def get_alias_or_name(model: Type[BaseModel], field_name: str) -> str:
    """Get the alias of a Pydantic field if set; otherwise, return the field name."""
    if field_name == ASTERISK_FIELD_NAME:
        return field_name
    alias = get_field_info(model, field_name).alias
    return alias if alias is not None else field_name


def get_property_from_field_info(model: Type[BaseModel], field_name: str, property_name: str) -> Any:
    """Get a specific property value from Pydantic's `FieldInfo`."""
    field = get_field_info(model, field_name)
    return getattr(field, property_name, None)


def _get_meta_items(meta_class: Any) -> Dict[str, Any]:
    """Helper method to extract constraint names and values from different
    Pydantic Metadata objects such as `pydantic.types.Strict`."""
    try:
        return meta_class.__dataclass_fields__
    except AttributeError:
        return meta_class.__dict__


def get_constraints(model: Type[BaseModel], field_name: str) -> Dict[str, Any]:
    """Get constraints for the given `field_name`."""
    metadata = model.model_fields[field_name].metadata
    available = [meta for meta in metadata if meta is not None]

    constraints = {}
    for meta in available:
        meta_items = _get_meta_items(meta)
        for key in meta_items:
            attr = getattr(meta, key, None)
            if attr is not None:
                constraints[key] = attr
    return constraints


def is_required(model: Type[BaseModel], field_name: str) -> bool:
    """Check if the given Pydantic field is required/mandatory."""
    return get_field_info(model, field_name).is_required()


def has_default_factory(model: Type[BaseModel], field_name: str) -> bool:
    """Check if the field has a `default_factory` set."""
    return get_field_info(model, field_name).default_factory is not None


def _test_field_serializability(field: FieldInfo) -> bool:
    """Test JSON serializability for the given Pydantic `FieldInfo`."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    try:
        field_args = (field.annotation, field.default)
        model = create_model('_', __config__=model_config, test_field=field_args)
        model.model_json_schema()
    except Exception:  # noqa: BLE001
        return False
    else:
        return True


def _is_json_serializable(field: FieldInfo) -> bool:
    """Ensure JSON serializability for the given Pydantic `FieldInfo`."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        return _test_field_serializability(field)


def is_json_serializable(model: Type[BaseModel], field_name: str) -> bool:
    """Check if the given Pydantic field is JSON serializable."""
    field = get_field_info(model, field_name)
    return _is_json_serializable(field)


def get_non_json_serializable_fields(model: Type[BaseModel]) -> List[str]:
    """Get all fields that can't be safely JSON serialized."""
    return [name for name in get_field_names(model) if not is_json_serializable(model, name)]


def _extract_class_name(func: Callable) -> Optional[str]:
    """Extract the class name from a function's qualified name, if applicable."""
    qualname_parts = func.__qualname__.split('.')
    if len(qualname_parts) > 1:
        return qualname_parts[-2]
    return None


if __name__ is "__main__":
    # ----------------------------
    # Example Usage
    # ----------------------------

    # Assuming you have a Pydantic model like this:
    class ExampleModel(BaseModel):
        name: str
        age: int = Field(..., ge=0)
        email: Optional[str] = None

    # Retrieve field names
    field_names = get_field_names(ExampleModel)
    print("Field Names:", field_names)

    # Get field info
    field_info = get_field_info(ExampleModel, 'age')
    print("Field Info for 'age':", field_info)

    # Get alias or name
    alias_or_name = get_alias_or_name(ExampleModel, 'age')
    print("Alias or Name for 'age':", alias_or_name)

    # Get constraints
    constraints = get_constraints(ExampleModel, 'age')
    print("Constraints for 'age':", constraints)

    # Check if a field is required
    required = is_required(ExampleModel, 'name')
    print("Is 'name' required?", required)

    # Check if a field has a default factory
    default_factory = has_default_factory(ExampleModel, 'email')
    print("Does 'email' have a default factory?", default_factory)

    # Check JSON serializability
    json_serializable = is_json_serializable(ExampleModel, 'email')
    print("Is 'email' JSON serializable?", json_serializable)

    # Get non-JSON serializable fields
    non_serializable = get_non_json_serializable_fields(ExampleModel)
    print("Non-JSON Serializable Fields:", non_serializable)

    # Get validators
    validators = get_validators(ExampleModel)
    for validator in validators:
        print(f"Validator: {validator['name']}, Module: {validator['module']}")

    # Get validator-field mappings
    validator_field_maps = get_validator_field_maps(ExampleModel)
    for mapping in validator_field_maps:
        print(f"Field: {mapping['field_name']}, Validator: {mapping['validator_name']}, "
              f"Field Ref: {mapping['field_ref']}, Validator Ref: {mapping['validator_ref']}")

    # Check if a specific validator exists
    has_name_validator = is_validator_by_name('name_must_not_be_empty', ExampleModel)
    print("Has 'name_must_not_be_empty' validator:", has_name_validator)
