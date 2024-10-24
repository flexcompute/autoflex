"""
This file contains the structure of a ParameterTable.
"""
from pydantic import BaseModel
from autoflex.types import PropertyCollectionTable
from autoflex.extractors import extract_property_list_from_model


def property_table_to_nodes(
    property_table: PropertyCollectionTable
) -> list:
    """
    This function converts the data container within a parameter table to sphinx nodes which can be used within both
    a given directive as the automated construction of a class based on an internal function.

    Should be a list of nodes that convert to sphinx.
    """
    return []

def extract_class_to_property_table_nodes(model: BaseModel) -> list:
    """
    This method converts from a given class or schema declaration into a container of data required for a ParameterTable
    in its intended implementation.
    """
    property_list = extract_property_list_from_model(model)
    nodes = property_table_to_nodes(property_list)
    return nodes



