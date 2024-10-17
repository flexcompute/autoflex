

``autoflex`` is divided in the following conceptual structure:

.. raw::

    Descriptors
    Structures
    Directives

Each of these logical divisions has a different use accordingly.

``Descriptors`` are fundamental data containers. These are defined as basic types that have fundamental information. These data containers individually or in a collection are used as validated-types inputs to a structure constructure.

``Structures`` are the generated documentation output which we interact with. These could be a information-specific table for a set of data container types. In principle, these structures are generated as a functional output of ``constructor(Descriptor)``.

``Directives`` are the integration of these construction flows into specific documentation flows. For example, this could involve a specific methodology for autodocumentation.

For example, a ``Directive`` may operate on a given class. This will then generate a set of doctree structures nodes that are represented in HTML accordingly. The directive will extract the ``Descriptors`` from the given class, and use those validated types to generate the ``Structures`` for which a collection of them are represented for a given implemented full directive.
