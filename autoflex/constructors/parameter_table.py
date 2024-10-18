"""
This file contains the structure of a ParameterTable.
"""
from autoflex.types import PropertyTypes

def extract_class_to_parameter_table(physcial_parameter: PropertyTypes) -> ParameterTable:
    """
    This method converts from a given class or schema declaration into a container of data required for a ParameterTable
    in its intended implementation.
    """

def parameter_table_to_nodes() -> list:
    """
    This function converts the data container within a parameter table to sphinx nodes which can be used within both
    a given directive as the automated construction of a class based on an internal function.

    Should be a list of nodes that convert to sphinx.
    """
