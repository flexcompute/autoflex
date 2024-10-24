from typing import Any, List
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger
from pydantic import BaseModel
from pydantic.v1 import BaseModel as BaseModelV1
import importlib
import json

from autoflex.types import Property
from autoflex.constructors.parameter_table import create_property_table, model_to_property_table_nodes

logger = getLogger(__name__)

class AutoFlex(SphinxDirective):
    """
    Extension of the ``.. autoflex::`` directive.

    In order to maintain compatibility and extensibility with all versions of Pydantic,
    this tool uses the interconnected JSON definition of the data structure instead of the
    internal Pydantic class representation. From this generic data structure, the tool can
    generate documentation compatible with the Pydantic version in use or any generic data structure
    schema derived from a class definition.

    The ``autoflex`` directive improves the data structure generated during the `autosummary` process
    instead of the `automodule` or `autoclass` directive.

    There are three components to the autoflex class:
    - Extract the relevant docs schema
    - Convert that docs schema into a documentation structure data type
    - Construct those into doctree nodes within sphinx. These are then returned to the directive declaration.

    Usage
    -----

    .. code::

        .. autoflex:: my_package.BasicClass
            :title: BasicClass Schema
            :description: This schema represents the basic structure of the BasicClass.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'title': directives.unchanged,
        'description': directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        import_path = self.arguments[0]
        logger.debug(f"AutoFlex processing import path: {import_path}")

        try:
            module_path, class_name = import_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            print(cls)
            # if (not issubclass(cls, BaseModel)) or (not issubclass(cls, BaseModelV1)):
            #     raise TypeError(f"{import_path} is not a subclass of pydantic.BaseModel")
        except (ImportError, AttributeError, ValueError, TypeError) as e:
            logger.error(f"AutoFlex directive error: {e}")
            error = self.state_machine.reporter.error(
                f'AutoFlex directive error: {e}',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            # return [error]
            pass

        # Generate documentation nodes from the schema
        nodes_list = []

        # Create a unique section ID to prevent conflicts
        section_id = f'autoflex-{class_name.lower()}'
        section_node = nodes.section(ids=[section_id])

        # Title
        title_text = self.options.get('title', f"Schema for `{class_name}`")
        title_node = nodes.title(text=title_text)
        section_node += title_node

        # Description
        description = self.options.get('description', cls.__doc__)
        if description:
            description_node = nodes.paragraph(text=description)
            section_node += description_node
        #
        # # JSON Schema as a literal block
        # try:
        #     schema_json = json.dumps(schema_dict, indent=2)
        # except (TypeError, ValueError) as e:
        #     logger.error(f"Error serializing schema for {import_path}: {e}")
        #     error = self.state_machine.reporter.error(
        #         f'Error serializing schema for {import_path}: {e}',
        #         nodes.literal_block(self.block_text, self.block_text),
        #         line=self.lineno
        #     )
        #     return [error]
        #
        # literal = nodes.literal_block(schema_json, schema_json)
        # literal['language'] = 'json'
        # section_node += literal
        #
        # # Generate the property table if applicable
        # properties = []
        # for prop_name, prop_info in schema_dict.get('properties', {}).items():
        #     if 'type' in prop_info:
        #         properties.append(Property(
        #             name=prop_name,
        #             types=prop_info['type'],
        #             description=prop_info.get('description', ''),
        #             default=str(prop_info.get('default', ''))
        #         ))

        logger.debug("Before building property table.")
        table_node = model_to_property_table_nodes(cls)
        logger.debug("After building property table.")
        section_node += table_node

        nodes_list.append(section_node)

        return nodes_list
