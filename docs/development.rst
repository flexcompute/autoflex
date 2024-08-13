Development
===========

The Basics
-----------

Build the local documentation basically:

.. code::

    poetry run python -m sphinx docs/ _docs/


Guidelines
----------

Note that the development of the project should aim to maximize the usage of the directives developed in this package.

Note that because many of these directives are extending `sphinx`-specific ones, then we want to both mantain compatibility whilst guaranteeing extensibility. One way to approach this is by fixing the corresponding versions of Sphinx we support. We can then build upon the Sphinx directive classes by overwriting their class methods accordingly, depending on what needs to be edited.
