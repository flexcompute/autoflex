``autoflex``
------------

One of the main complexities we have is that managing `rst` code blocks in docstrings is complicated. It involves manually writing and updating parameter descriptions rather than focusing on the actual docstrings.

When we have multiple classes, and multiple inherited classes, it is hard to keep track of each code block and all the added parameters. For example, it would be possible to manually input parameters at each particular stage. However, it would be nice if this could be extracted directly out of each class declaration automatically and rendered in a nice way.

