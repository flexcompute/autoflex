"""
    sphinxcontrib.autoflex
    ~~~~~~~~~~~~~~~~~~~~~~

    A flexible, nicer way of generating API docs without requiring custom docstrings.

    :copyright: Copyright 2023 by daquintero <dario a quintero at gmail dot com>
    :license: BSD, see LICENSE for details.
"""

from typing import Any, Dict
from .install import install_verification
from .directives import AutoFlexDirective

__version__ = "0.0.1"
__author__ = "Dario Quintero Dominguez"
__email__ = "dario a quintero at gmail dot com"


def setup(app) -> Dict[str, Any]:
    """Add icon node to the sphinx builder."""
    install_verification()
    app.add_directive("autoflex", AutoFlexDirective)
    # load the icon node/role
    # app.add_node(icon_node, **_NODE_VISITORS)  # type: ignore
    # app.add_role("icon", Icon())
    #
    # # load the font
    # font_handler = Fontawesome()
    #
    # # install html related files
    # app.add_css_file(str(font_handler.css_file.resolve()))
    # app.add_js_file(str(font_handler.js_file.resolve()))
    #
    # # install latex files
    # app.add_latex_package("fontspec")
    # app.connect("config-inited", font_handler.add_latex_font)
    # app.connect("config-inited", font_handler.enforce_xelatex)
    # app.connect("builder-inited", font_handler.add_latex_font_files)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
