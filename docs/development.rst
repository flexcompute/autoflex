Development
===========

The Basics
-----------

Build the local documentation basically:

.. code::

    poetry run python -m sphinx docs/ _docs/

It helps to be able to debug inside the ``sphinx-extension``, for this we use the ``logging`` python package, and this
just needs to be activated in the ``conf.py`` options of a given project.


Guidelines
----------

Note that the development of the project should aim to maximize the usage of the directives developed in this package.

Note that because many of these directives are extending `sphinx`-specific ones, then we want to both mantain compatibility whilst guaranteeing extensibility. One way to approach this is by fixing the corresponding versions of Sphinx we support. We can then build upon the Sphinx directive classes by overwriting their class methods accordingly, depending on what needs to be edited.


Logging
--------

We use the ``logging`` base python module to create a record of the operations occuring internally in the code.

The formalism used is declaring a ``logger`` at the top of the file.

.. code:

    import logging
    logger = logging.getLogger(__name__)
