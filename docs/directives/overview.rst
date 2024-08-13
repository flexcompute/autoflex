Usage Overview
---------------

.. list-table::
    :header-rows: 1

    * - Extension Command
      - Brief Description
      - Specification
    * - ``autoflex``
      - Our very extensible, automatic API documentation generator for classes.
      -
    * - ``flextree``
      - A customizable ``toctree`` directive with options to create links with descriptions, custom formatting, and interactive features.
      - https://github.com/flexcompute/autoflex/issues/10
    * - ``flexsummary``
      - A customizable ``autosummary`` directive.
      - https://github.com/flexcompute/autoflex/issues/10



Basic ``autoflex`` Usage
^^^^^^^^^^^^^^^^^^^^^^^^^

If you just want to automatically generate the API documentation for a class with the default configuration by the extension.
You need to make sure you've delclared the relevant top path of the module you're in.

.. code:: rst

   .. currentmodule:: tidy3d

   .. autoflex:: tidy3d.Simulation


Basic ``flextree`` Usage
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: rst

    .. flextree::
        :maxdepth: 2

        mypage1/
            :description: This is the description of the page.
        mypage2/
            :description: This is the description of the page.


Basic ``flexsummary`` Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Custom ``autosummary`` implementation, based on ``autoflex`` directives.

.. code:: rst

    .. flexsummary::
