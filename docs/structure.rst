Implementation Structure
=========================

``autoflex`` is divided in the following conceptual structure:

.. code-block::

    Descriptors
    Structures
    Directives

Each of these logical divisions has a different use accordingly.

``Descriptors`` are fundamental data containers. These are defined as basic types that have fundamental information. These data containers individually or in a collection are used as validated-types inputs to a structure constructure.

``Structures`` are the generated documentation output which we interact with. These could be a information-specific table for a set of data container types. In principle, these structures are generated as a functional output of ``constructor(Descriptor)``.

``Directives`` are the integration of these construction flows into specific documentation flows. For example, this could involve a specific methodology for autodocumentation.

For example, a ``Directive`` may operate on a given class. This will then generate a set of doctree structures nodes that are represented in HTML accordingly. The directive will extract the ``Descriptors`` from the given class, and use those validated types to generate the ``Structures`` for which a collection of them are represented for a given implemented full directive.

It can be relatively difficult to test documentation, as it is mainly a visual output. It does have logical elements and the data created by the constructors can be tested. Ultimately, the difficulty is that visually validating the generated HTML output is required if for some reason the generated output does not actually look good.


Descriptors
------------

Part of the objective of ``autoflex`` is to reduce the complexity of defining and extending documentation.
Every time we compile documentation directly from python, it exposes failure points on functionality changes or
data structure changes within ``python``. This can make some functionality very hard to extend, and probably
this has contributed to the complexity of ``doctools`` and ``sphinx``.

This is because it's dealing with `language`
and `content` changes at the same time when rendering a documentation. It is trying to compile `language` within the
`code` into `structures` that can then be built into `HTML` or whatever else. By having a more static schema, it is
possible to perform translations in between the domains in a clearer way.

This is the motivation behind defining the `autoflex` schema in both a generic and extensible manner - to kind of
independize from the `language` but still enable the compilation of base ``python`` and ``pydantic`` data types
functionality into this ``schema`` as defined by the user.

So one of the complexities is how to perform this translation exactly from the existing information within the python
attributes, what is relevant, and what is not relevant from a given declaration. What overlaps with the
existing documentation methodology and what doesn't? This kind of type implementation is meta, because, yes: it can be
automated to be generated directly from the python class implementation. It defines a given translation methodology
directly from the base class definition into this schema. Then from this schema, we can translate into a given
visualization structure accordingly. So in a way, what this is proposing is a strongly-typed validated meta-autodoc.
I guess this is a good idea in principle and enables extension of the docs functionality in a very clear-cut manner.

The idea of this is to create container definitions relevant to our applications, which can then be translated into
structural definitions that actually construct the documentation components. The interactions between these definitions
and the methods documentation can be very lightweight accordingly.

The actual documentation constructors can, and would necessarily, leverage the sphinx doctools constructors within the
extension. But then, what exactly is the ``autoflex`` directive building. It would be building a schema, of a given
defined ``documentation`` attribute. As long as that schema can be translated into a given data structure which can be
constructed within ``autoflex`` then that type of documentation mapping can be implemented.

In a way, it's redefining documentation from a constructor-based documentation into a `API`-based documentation,
especially intended for deeply-nested APIs such as in ``tidy3d`` accordingly. This is bounded to the given data containers
in which we can represent data.

For example, when we have a set group of attributes/parameters they can be declared or inherited. In any case, they are a list
of parameters which can be accessed within a class directly through, say, a dot method or etc. In Physics APIs, these
parameters ultimately represent physical-based mappings to a component representation. In our case, we might have
classes - and constructors within these classes - which we operate on within the states or schema declaration of our other classes.
As such, we have a combination of constructors and physics representations which we might want to combine and represent differently.
Each of our constructors might have a physical meaning assigned to them. This is where we might want to represent units, or
operators as symbolic terms.

As such, we don't want to overwrite the existing documentation functionality we like such as doctree declarations.
