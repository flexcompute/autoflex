from docutils.parsers.rst import Directive
from sphinx.directives.other import TocTree
from docutils import nodes


class FlexTree(TocTree):
    """
    Extension of the ``.. toctree::`` sphinx directive.

    Notes
    -----

    A customizable toctree directive with options to create
     links with descriptions, custom formatting, and interactive features. Ideally this feature should be developed
    in an extensible way building on top of the existing ``toctree`` directive.

    Usage
    -----

    The usage should be broadly compatible with the existing ``.. toctree::`` directive in the structures they represent.
    However, there is more flexibility in the way the tree is generated and the parameters that can be passed.

    To add descriptions below the given generated links, the following syntax can be used:

    .. code::

        .. flextree::
            :maxdepth: 2

            mypage1/
                :description: This is the description of the page.
            mypage2/
                :description: This is the description of the page.


    """

    # Directive information
    has_content: bool = True

    name: str = "flextree"

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
        # Process the toctree as usual
        env = self.state.document.settings.env
        titles = TocTree.run(self)

        # Additional processing to handle the description field
        descriptions = self.options.get('descriptions', [])
        description_nodes = []

        # Create custom nodes with descriptions
        for title, desc in zip(titles, descriptions):
            title_node = nodes.Text(title, title)
            description_node = nodes.Text(desc, desc)
            description_nodes.append((title_node, description_node))

        # Create a custom node to store title and description
        custom_node = desc_tocnode()
        custom_node['entries'] = description_nodes

        return [custom_node]


class desc_tocnode(nodes.General, nodes.Element):
    pass


def visit_desc_tocnode_html(self, node):
    self.body.append('<div class="custom-toctree">')


def depart_desc_tocnode_html(self, node):
    self.body.append('</div>')


def visit_desc_tocnode(self, node):
    pass


def depart_desc_tocnode(self, node):
    pass
