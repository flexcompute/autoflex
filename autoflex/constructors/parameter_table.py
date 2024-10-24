"""
This file contains the structure of a ParameterTable.
"""
from pydantic import BaseModel
from autoflex.types import PropertyCollectionTable
from autoflex.extractors import extract_property_list_from_model
from docutils import nodes

def model_to_property_table_nodes(model: BaseModel) -> nodes.table:
    """
    This method converts from a given class or schema declaration into a container of data required for a ParameterTable
    in its intended implementation.
    """
    property_list = extract_property_list_from_model(model)
    table_nodes = create_property_table(property_list)
    return table_nodes


def create_property_table(properties: PropertyCollectionTable):
    # Define a list of table columns
    table_head = [
        ["Name", "Description", "Units", "Symbolic", "Types", "Default"]
    ]

    # Create the table node
    table = nodes.table()
    tgroup = nodes.tgroup(cols=6)
    table += tgroup

    # Define column specifications
    for _ in range(6):
        tgroup += nodes.colspec(colwidth=1)

    thead = nodes.thead()
    tgroup += thead
    tbody = nodes.tbody()
    tgroup += tbody

    # Fill in the header row
    row = nodes.row()
    for header in table_head[0]:
        entry = nodes.entry()
        entry += nodes.paragraph(text=header)
        row += entry
    thead += row

    # Fill in the property rows
    for prop in properties:
        row = nodes.row()

        # Add property name
        entry = nodes.entry()
        entry += nodes.paragraph(text=prop.name)
        row += entry

        # Add property description
        entry = nodes.entry()
        entry += nodes.paragraph(text=prop.description)
        row += entry

        # Check if it's a PhysicalProperty by checking for `math` and `unit` attributes
        if hasattr(prop, 'math') and hasattr(prop, 'unit'):
            # Add units
            entry = nodes.entry()
            entry += nodes.paragraph(text=str(prop.unit))
            row += entry

            # Add symbolic
            entry = nodes.entry()
            entry += nodes.paragraph(text=str(prop.math))
            row += entry
        else:
            # Add empty cells for units and symbolic if it's not a PhysicalProperty
            for _ in range(2):
                entry = nodes.entry()
                entry += nodes.paragraph(text="")
                row += entry

        # Add types
        entry = nodes.entry()
        entry += nodes.paragraph(text=prop.types)
        row += entry

        # Add default
        entry = nodes.entry()
        entry += nodes.paragraph(text=prop.default)
        row += entry

        # Append row to the body
        tbody += row

    return table

