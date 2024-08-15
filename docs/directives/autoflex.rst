``autoflex``
------------

One of the main complexities we have is that managing `rst` code blocks in docstrings is complicated. It involves manually writing and updating parameter descriptions rather than focusing on the actual docstrings.

When we have multiple classes, and multiple inherited classes, it is hard to keep track of each code block and all the added parameters. For example, it would be possible to manually input parameters at each particular stage. However, it would be nice if this could be extracted directly out of each class declaration automatically and rendered in a nice way.




Development Logic
^^^^^^^^^^^^^^^^^

All extensions onto a ``sphinx`` project, extend the ``def setup(app)`` where ``app`` is the ``sphinx`` app.
Including a project in the conf.py ``extensions = [...]`` declaration means that the extension will operate onto the sphinx app at the corresponding location of the extension in the extensions list.

It is pretty valuable to understand how the existing autodocumentation works. Let's go through some of the theory
of the components that we want to replace:

``sphinx.ext.autodoc`` contains a `Documenter <https://github.com/sphinx-doc/sphinx/blob/49c3b21c60a1d376c41aa2715061039cf854fbaa/sphinx/ext/autodoc/__init__.py#L324-L347>`_, which when initialized contains the following information:

.. code:: python

        def __init__(self, directive: DocumenterBridge, name: str, indent: str = '') -> None:
            self.directive = directive
            self.config: Config = directive.env.config
            self.env: BuildEnvironment = directive.env
            self.options = directive.genopt
            self.name = name
            self.indent = indent
            # the module and object path within the module, and the fully
            # qualified name (all set after resolve_name succeeds)
            self.modname: str = ''
            self.module: ModuleType | None = None
            self.objpath: list[str] = []
            self.fullname = ''
            # extra signature items (arguments and return annotation,
            # also set after resolve_name succeeds)
            self.args: str | None = None
            self.retann: str = ''
            # the object to document (set after import_object succeeds)
            self.object: Any = None
            self.object_name = ''
            # the parent/owner of the object to document
            self.parent: Any = None
            # the module analyzer to get at attribute docs, or None
            self.analyzer: ModuleAnalyzer | None = None

This means that every directive has got a ``BuildEnvironment`` and information about the states. So, the ``autodoc/__init__.py`` extension is loaded by adding the corresponding documenters and configuration variables at these points. Note that ``Sphinx``
is a class that we can hence, extend through classmethods accordingly - and it aims to represent at a higher level the
data relationships of our classes.


.. code:: python

    def setup(app: Sphinx) -> ExtensionMetadata:
        app.add_autodocumenter(ModuleDocumenter)

        app.add_config_value('autoclass_content', 'class', 'env', ENUM('both', 'class', 'init'))



Each documenter class:

.. code:: python

    class ClassLevelDocumenter(Documenter):

        def resolve_name(self, modname: str | None, parents: Any, path: str, base: str,
                     ) -> tuple[str | None, list[str]]
            return modname, [*parents, base]

It is also possible simply to:

.. raw:: python

        def add_autodocumenter(self, cls: type[Documenter], override: bool = False) -> None:
            """Register a new documenter class for the autodoc extension.

            Add *cls* as a new documenter class for the :mod:`sphinx.ext.autodoc`
            extension.  It must be a subclass of
            :class:`sphinx.ext.autodoc.Documenter`.  This allows auto-documenting
            new types of objects.  See the source of the autodoc module for
            examples on how to subclass :class:`~sphinx.ext.autodoc.Documenter`.

            If *override* is True, the given *cls* is forcedly installed even if
            a documenter having the same name is already installed.

            See :ref:`autodoc_ext_tutorial`.

            .. versionadded:: 0.6
            .. versionchanged:: 2.2
               Add *override* keyword.
            """
            logger.debug('[app] adding autodocumenter: %r', cls)
            from sphinx.ext.autodoc.directive import AutodocDirective
            self.registry.add_documenter(cls.objtype, cls)
            self.add_directive('auto' + cls.objtype, AutodocDirective, override=override)

In our case, we want to document all our classes. We also want to do this in a `pydantic-agnositic` way,
but we also want to represent all the relevant methods accordingly. It would be ideal, if rather than documenting directly
from the parameters, fields or classmethods, we could extract this from the serialized output which is unlikely to change.
For applications keen on documenting the validators, this could be done with ease by extending `autodoc-pydantic`.

The goal of `pydantic` is to serialize `python`, and in a way, `sphinx` is also trying to achieve a similar functionalty
by documenting the members corresponding to python objects. Hence, if we can provide a defined interconnect between
the data types in `pydantic` and `sphinx`, there is a possibility for more flexible documentation accordingly.
This would be mainly applicable primarily to serialized APIs.
