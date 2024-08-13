import pydantic
from docutils.parsers import rst
from typing import Any


class AutoFlex(rst.Directive):
    """
    Extension of the ``.. automodule::`` directive.

     In order to mantain compatibility and extensibility with all the versions of pydantic,
     it makes sense that this tool uses, rather than the internal pydantic class representation of the class,
     the interconnected JSON definition of the data structure. From this generic data structure, the tool can
        generate the documentation in a way that is compatible with the version of pydantic that is being used, or even
        any generic data structure schema that can be generated from a given class definition.

     The idea is that we can use the ``autoflex`` directive to improve the data structure generated during the
      `autosummary` process instead of the `automodule` or `autoclass` directive.


    Usage
    -----

    .. code::

        .. autoflex:: my_package.MyClass

    """

    # Directive information
    has_content: bool = True

    # name: str = "autoflex"
    # arguments: Any = None
    # options: Any = None
    # content: Any = None
    # lineno: Any = None
    # content_offset: Any = None
    # block_text: Any = None
    # state: Any = None
    # state_machine: Any = None
    # reporter: Any = None
    #
    # required_arguments: int = 1
    # optional_arguments: int = 0

    def run(self):
        print("AutoFlex directive running.")
        print(self.name)
        return []
