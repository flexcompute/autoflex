"""
Note that the compilation flow is as follows:

.. code::

    FieldTypes -> PropertyTypes
    PhysicalFieldInfo -> PhysicalProperty
    pd.FieldInfo -> Property

Then, this automated flow can be run for a given BaseModel and the properties can be extracted accordingly.
"""
import pydantic as pd
from autoflex.types import PropertyTypes, FieldTypes, PhysicalProperty, PhysicalFieldInfo, Property
from autoflex.version_manager import determine_pydantic_version_from_base_model

def get_field_infos(model: pd.BaseModel):
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


def physical_field_info_to_physical_property(field: PhysicalFieldInfo, field_name: str) -> PhysicalProperty:
    """
    Convert a PhysicalFieldInfo instance to a PhysicalProperty.

    Args:
        field: The PhysicalFieldInfo instance.
        field_name: The name of the field.

    Returns:
        PhysicalProperty: The corresponding PhysicalProperty instance.
    """
    # Extract unit and math information
    unit = field.unit
    math = field.math

    # Extract other field attributes
    description = field.description or ""
    default = field.default if field.default is not None else ""

    # Assuming 'types' can be inferred from the field's type
    types = str(field.outer_type_) if hasattr(field, 'outer_type_') else ""

    return PhysicalProperty(
        name=field_name,
        types=types,
        description=description,
        default=str(default),
        unit=unit,
        math=math
    )


def field_info_to_property(field: pd.fields.FieldInfo, field_name: str) -> Property:
    """
    Convert a standard FieldInfo instance to a Property.

    Args:
        field: The FieldInfo instance.
        field_name: The name of the field.

    Returns:
        Property: The corresponding Property instance.
    """
    description = field.description or ""
    default = field.default if field.default is not None else ""
    types = str(field.outer_type_) if hasattr(field, 'outer_type_') else ""

    return Property(
        name=field_name,
        types=types,
        description=description,
        default=str(default)
    )


def auto_field_to_property_type(field: FieldTypes, field_name: str) -> PropertyTypes:
    """
    Convert a FieldTypes instance to a PropertyTypes instance.

    Args:
        field: The FieldTypes instance (PhysicalFieldInfo or FieldInfo).
        field_name: The name of the field.

    Returns:
        PropertyTypes: The corresponding PropertyTypes instance.
    """
    if isinstance(field, PhysicalFieldInfo):
        return physical_field_info_to_physical_property(field, field_name)
    else:
        return field_info_to_property(field, field_name)


def extract_property_list_from_model(model: pd.BaseModel) -> list[PropertyTypes]:
    """
    Extract a list of PropertyTypes from a Pydantic model.

    Args:
        model: The Pydantic BaseModel instance.

    Returns:
        List[PropertyTypes]: A list of PropertyTypes instances extracted from the model.
    """
    field_infos = get_field_infos(model)
    properties = []

    # Get field names based on Pydantic version
    version = determine_pydantic_version_from_base_model(model)
    if version == 2:
        field_names = list(model.model_fields.keys())
    elif version == 1:
        field_names = list(model.__fields__.keys())
    else:
        field_names = []

    for field, field_name in zip(field_infos, field_names):
        property_item = auto_field_to_property_type(field, field_name)
        properties.append(property_item)

    return properties

