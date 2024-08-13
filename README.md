# `autoflex` Sphinx Documentation Extension

A flexible, nicer way of generating API docs without requiring custom docstrings.

## Overview

One of the main complexities we have is that managing `rst` code blocks in docstrings is complicated. It involves manually writing and updating parameter descriptions rather than focusing on the actual docstrings.

When we have multiple classes, and multiple inherited classes, it is hard to keep track of each code block and all the added parameters. For example, it would be possible to manually input parameters at each particular stage. However, it would be nice if this could be extracted directly out of each class declaration automatically and render it in a nice way.

This extension aims to do that.

### Objectives

- Improve the API template for `autodoc` which can be limited.
- For each class, such as `tidy3d` complex classes, properly generate a nicer template of the parameters and methods that extends how autodoc works.
- Generate an index of each API directive that can be easily searched by corresponding themes like the `sphinx_book_theme`.
- For inherited classes, have the option to easily define the methods and parameters that we want to generate documentation for.
- Have the option to generate custom HTML relevant to each class in a way defined by the class docstring.
- Make sure the docstrings don't interfere with help messages such as ipython, etc. (Maybe explore how to compile relevant docstrings into the help messages).

**API Docstrings Improvements**

When we have highly complex classes that have multiple inherited parameters, it is desired to have a clear definition of each specific class and its parameters, types and defaults. Whilst this can be done manually for an individual class or method, as a project increases in complexity, it is desired to understand the relevant docstrings for each class and method.

## Usage

The idea is that we can use the `autoflex` directive to improve the data structure generated during the `autosummary` process instead of the `automodule` or `autoclass` directive.

Install the package in `development` mode:
```bash
poetry install -E dev
```

Build the local basic documentation with the extension linked:

```bash
poetry run python -m sphinx docs/ _docs/
```

Basic Example:

```rst
.. autoflex:: somepackage.MyClass # CURRENTLY NOT WORKING
```

## Links

-   Source: <https://github.com/sphinx-contrib/sphinxcontrib-autoflex />
-   Bugs: <https://github.com/sphinx-contrib/sphinxcontrib-autoflex/issues />
