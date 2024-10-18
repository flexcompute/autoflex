import pydantic as pd
from pydantic import Field
import autoflex
from autoflex.types import Property, PhysicalProperty, PhysicalFieldInfo, Symbolic
from autoflex.extractors import field_info_to_property, physical_field_info_to_physical_property, auto_field_to_property_type, extract_property_list_from_model
from autoflex.field import PhysicalField

def test_get_field_infos():
    import demo

    basic_class = demo.BasicClass()
    basic_mixed_class = demo.BasicMixedAnnotatedClass()

    basic_class_fields = autoflex.get_field_infos(basic_class)
    basic_mixed_class_fields = autoflex.get_field_infos(basic_mixed_class)

    print(f"Fields: {basic_class_fields}")
    assert len(basic_class_fields) == 3, f"Expected 3 fields, found {len(basic_class_fields)}"
    assert len(basic_mixed_class_fields) == 4, f"Expected 4 fields, found {len(basic_mixed_class_fields)}"




def test_automatic_field_to_property_extractor():
    # help(pd.fields.Field)
    field_json_schema_extras = Field(
        json_schema_extra={
            "unit": "ms",
            "math": "s + 1"
        }
    )

    field_extra = Field(
        extra={
            "unit": "ms",
            "math": "s + 1"
        }
    )


    aufoflex_physical_field_extra = Field(
        json_schema_extra={
            "unit": "ms",
            "math": "s + 1"
        }
    )


def test_physical_field_info_to_physical_property():
    # Create a PhysicalFieldInfo instance
    symbolic = Symbolic(label="Force", math="F = ma")
    unit = "N"
    field_info = PhysicalFieldInfo(
        default=10.0,
        unit=unit,
        math=symbolic,
        description="Force applied",
    )

    field_name = "force"

    physical_property = physical_field_info_to_physical_property(field_info, field_name)

    print(physical_property)

    assert isinstance(physical_property, PhysicalProperty)
    assert physical_property.name == "force"
    # assert physical_property.unit == unit
    # assert physical_property.math == symbolic
    assert physical_property.description == "Force applied"
    assert physical_property.default == "10.0"


def test_field_info_to_property():
    # Create a standard FieldInfo instance
    field_info = pd.Field(
        default=5.0,
        description="Mass of the object",
    )

    field_name = "mass"

    property_instance = field_info_to_property(field_info, field_name)

    print("FieldInfo:")
    print(field_info)
    print("Property instance:", property_instance)
    print(property_instance)

    assert isinstance(property_instance, Property)
    assert property_instance.name == "mass"
    assert property_instance.description == "Mass of the object"
    assert property_instance.default == "5.0"
    # assert property_instance.types == "<class 'float'>"


def test_auto_field_to_property_type_physical():
    # Create a PhysicalFieldInfo instance
    symbolic = Symbolic(label="Force", math="F = ma")
    unit = "N"
    field_info = PhysicalFieldInfo(
        default=15.0,
        unit=unit,
        math=symbolic,
        description="Applied force",
    )

    field_name = "force"

    property_type = auto_field_to_property_type(field_info, field_name)

    print(property_type)

    assert isinstance(property_type, PhysicalProperty)
    assert property_type.name == "force"
    # assert property_type.unit == unit
    # assert property_type.math == symbolic
    assert property_type.description == "Applied force"
    assert property_type.default == "15.0"


def test_auto_field_to_property_type_standard():
    # Create a standard FieldInfo instance
    field_info = pd.Field(
        default=7.5,
        description="Temperature in Celsius",
    )

    field_name = "temperature"

    property_type = auto_field_to_property_type(field_info, field_name)

    assert isinstance(property_type, Property)
    assert property_type.name == "temperature"
    assert property_type.description == "Temperature in Celsius"
    assert property_type.default == "7.5"
    # assert property_type.types == "<class 'float'>"


def test_extract_property_list_from_model():
    class TestModel(pd.BaseModel):
        mass: float = pd.Field(5.0, description="Mass of the object")
        velocity: float = pd.Field(10.0, description="Velocity of the object")
        force: float = PhysicalField(
            default=20.0,
            description="Force applied",
            unit="N",
            math="F = ma"
        )
        acceleration: float = pd.Field(9.8, description="Acceleration of the object")

    model = TestModel()

    properties = extract_property_list_from_model(model)

    assert len(properties) == 4, f"Expected 4 properties, found {len(properties)}"

    # Check each property
    mass_prop = properties[0]
    assert isinstance(mass_prop, Property)
    assert mass_prop.name == "mass"
    assert mass_prop.description == "Mass of the object"
    assert mass_prop.default == "5.0"

    velocity_prop = properties[1]
    assert isinstance(velocity_prop, Property)
    assert velocity_prop.name == "velocity"
    assert velocity_prop.description == "Velocity of the object"
    assert velocity_prop.default == "10.0"

    force_prop = properties[2]
    print(force_prop)
    assert isinstance(force_prop, PhysicalProperty)
    assert force_prop.name == "force"
    # assert force_prop.description == "Force applied"
    assert force_prop.default == "20.0"
    # assert force_prop.unit == "N"
    # assert force_prop.math == "F = ma"

    acceleration_prop = properties[3]
    assert isinstance(acceleration_prop, Property)
    assert acceleration_prop.name == "acceleration"
    assert acceleration_prop.description == "Acceleration of the object"
    # assert acceleration_prop.default == "9.81"


def test_automatic_field_to_property_extractor():
    # Create FieldInfo instances with different extras
    field_json_schema_extras = Field(
        default=100,
        description="Time in milliseconds",
        json_schema_extra={
            "unit": "ms",
            "math": "t = 1000 * s"
        }
    )

    field_extra = Field(
        default=200,
        description="Distance in meters",
        extra={
            "unit": "m",
            "math": "d = vt"
        }
    )

    # For the purpose of this test, we'll manually create PhysicalFieldInfo if extras are present
    # In a real scenario, you might have logic to detect and convert based on extras
    physical_field_info_json = PhysicalFieldInfo(
        default=100,
        unit="ms",
        math="t = 1000 * s",
        description="Time in milliseconds",
    )

    physical_field_info_extra = PhysicalFieldInfo(
        default=200,
        unit="m",
        math="d = vt",
        description="Distance in meters",
    )

    # Convert to PropertyTypes
    property_json = auto_field_to_property_type(field_json_schema_extras, "time")
    property_extra = auto_field_to_property_type(field_extra, "distance")
    property_physical_json = auto_field_to_property_type(physical_field_info_json, "time_physical")
    property_physical_extra = auto_field_to_property_type(physical_field_info_extra, "distance_physical")

    # Assertions
    assert isinstance(property_json, Property)
    assert property_json.name == "time"
    assert property_json.description == "Time in milliseconds"
    assert property_json.default == "100"
    # assert property_json.types == "<class 'int'>"

    assert isinstance(property_extra, Property)
    assert property_extra.name == "distance"
    assert property_extra.description == "Distance in meters"
    assert property_extra.default == "200"
    # assert property_extra.types == "<class 'int'>"

    assert isinstance(property_physical_json, PhysicalProperty)
    assert property_physical_json.name == "time_physical"
    assert property_physical_json.description == "Time in milliseconds"
    assert property_physical_json.default == "100"
    # assert property_physical_json.unit == "ms"
    # assert property_physical_json.math == "t = 1000 * s"

    assert isinstance(property_physical_extra, PhysicalProperty)
    assert property_physical_extra.name == "distance_physical"
    assert property_physical_extra.description == "Distance in meters"
    assert property_physical_extra.default == "200"
    # assert property_physical_extra.unit == "m"
    # assert property_physical_extra.math == "d = vt"


