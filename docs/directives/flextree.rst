``flextree``
-------------

This should be a drop in replacement to ``toctree`` with more customizable options.


Development Information
^^^^^^^^^^^^^^^^^^^^^^^

The main ``toctree`` code can be found under ``sphinx.ext.other``. It is defined as a ``SphinxDirective`` subclass.

.. code:: python

    def run(self) -> list[Node]:
        subnode = addnodes.toctree()
        ...
        ret = self.parse_content(subnode)
        ret.append(wrappernode)
        return ret


It's also important to understand that that a ``Node`` is a representation of a generated doctree element which is
an extension of ``docutils.nodes``. This is also the case for ``AutoDocumenter`` extensions.


.. code:: python

    class Node:
        """Abstract base class of nodes in a document tree."""

        parent = None
        """Back-reference to the Node immediately containing this Node."""

        source = None
        """Path or description of the input source which generated this Node."""

        line = None
        """The line number (1-based) of the beginning of this Node in `source`."""

        _document = None


We also know there are multiple sub-elements that get generated accordingly in ``docutils.nodes``:


.. code::

    class Text(Node, str)
    class Element(Node)
    ...

Sphinx is written in this class-inheritance based approach for all the elements.
Based on these classes, the resulting output doctype gets constructed accordingly.

In our case, we want to extend the existing directives functionality without actually making the commands incompatible
with the original structure.

A very good way to understand how to extend nodes is to go deeper into the way the themes are created, as some are part extension and html theming.

One of the main complexities is that we don't want the ``flextree`` extension interfering with the theme settings either,
so this involves understanding where it goes wrong in terms of the interface point. We probably want to find a
theme-agnostic implementation of this, but this may prove tricky.
