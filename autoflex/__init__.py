"""
    sphinxcontrib.autoflex
    ~~~~~~~~~~~~~~~~~~~~~~

    A flexible, nicer way of generating API docs without requiring custom docstrings.

    :copyright: Copyright 2023 by daquintero <dario a quintero at gmail dot com>
    :license: BSD, see LICENSE for details.
"""

from typing import Any, Dict
import pathlib

from .install import install_verification
from autoflex.directives import AutoFlex, FlexTree
from autoflex.styles.setup import copy_autoflex_styles_to_static
from autoflex.directives.flextree import desc_tocnode, depart_desc_tocnode, depart_desc_tocnode_html, visit_desc_tocnode_html, visit_desc_tocnode

__version__ = "0.0.1"
__author__ = "Dario Quintero Dominguez"
__email__ = "dario a quintero at gmail dot com"


def setup(app) -> Dict[str, Any]:
    """
    Configure the ``autoflex`` extension onto your project.
    """
    print("Started loading `autoflex` extension.")
    # DIRECTIVES
    app.add_directive("autoflex", AutoFlex)
    app.add_directive("flextree", FlexTree)
    app.add_node(desc_tocnode,
                 html=(visit_desc_tocnode_html, depart_desc_tocnode_html),
                 latex=(visit_desc_tocnode, depart_desc_tocnode),
                 text=(visit_desc_tocnode, depart_desc_tocnode))
    # load the icon node/role
    # app.add_node(icon_node, **_NODE_VISITORS)  # type: ignore
    # app.add_role("icon", Icon())

    # STYLES
    app.connect('build-finished', copy_autoflex_styles_to_static)
    app.add_css_file("css/autoflex.css")

    print("Finished loading `autoflex` extension.")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
