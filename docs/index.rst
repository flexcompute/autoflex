**********************
autoflex
**********************

A flexible, nicer way of generating API docs without requiring custom docstrings.

This extension aims to do that.


.. include:: get_started.rst
.. include:: directives/overview.rst

Objectives
==========

- Improve the API template for `autodoc` which can be limited.
- For each class, such as `tidy3d` complex classes, properly generate a nicer template of the parameters and methods that extends how autodoc works.
- Generate an index of each API directive that can be easily searched by corresponding themes like the ``sphinx_book_theme``.
- For inherited classes, have the option to easily define the methods and parameters that we want to generate documentation for.
- Have the option to generate custom HTML relevant to each class in a way defined by the class docstring.
- Make sure the docstrings don't interfere with help messages such as ipython, etc. (Maybe explore how to compile relevant docstrings into the help messages).

**API Docstrings Improvements**

When we have highly complex classes that have multiple inherited parameters, it is desired to have a clear definition of each specific class and its parameters, types, and defaults. Whilst this can be done manually for an individual class or method, as a project increases in complexity, it is desired to understand the relevant docstrings for each class and method.


Indices and tables
==================

.. flextree::
   :maxdepth: 2

   get_started/ :description: Hello
   directives/index
   examples/index
   configuration/index
   development


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Links
=====

- Source: `<https://github.com/flexcompute/autoflex />`_
- Bugs: `<https://github.com/flexcompute/autoflex/issues />`_
