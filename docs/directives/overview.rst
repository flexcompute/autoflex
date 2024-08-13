Usage Overview
---------------

.. list-table::
    :header-rows: 1

    * - Extension Command
      - Brief Description
      - Specification
    * - ``flextree``
      - A customizable toctree directive with options to create links with descriptions, custom formatting, and interactive features.
      - https://github.com/flexcompute/autoflex/issues/10
    * - ``autoflex``
      - Our very extensible, automatic API documentation generator for classes.
      -


.. code:: rst

    .. flextree::
        :maxdepth: 2

        mypage1/
            :description: This is the description of the page.
        mypage2/
            :description: This is the description of the page.


Basic Example:

.. code:: rst

   .. autoflex:: somepackage.MyClass
