import pydantic
from docutils.parsers import rst
from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.ext.autodoc import ClassDocumenter
from sphinx.util.docutils import SphinxDirective

class AutoFlex(ClassDocumenter):
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

    has_content = True



