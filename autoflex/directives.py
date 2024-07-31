import pydantic
from docutils.parsers import rst
from typing import Any


class AutoFlexDirective(pydantic.BaseModel, rst.Directive):
    """
    Extension of the ``.. automodule::`` directive.

    Usage
    -----

    .. code::

        .. autoflex:: my_package.MyClass

    """

    # Directive information
    name: str = "autoflex"
    arguments: Any = None
    options: Any = None
    content: Any = None
    lineno: Any = None
    content_offset: Any = None
    block_text: Any = None
    state: Any = None
    state_machine: Any = None
    reporter: Any = None

    required_arguments: int = 0
    optional_arguments: int = 0

    def run(self):
        print("AutoFlex directive running.")
        print(self.name)
