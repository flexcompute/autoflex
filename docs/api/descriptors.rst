Descriptors
------------

Part of the goal of using dedicated ``AutoflexField`` definitions is that we can compile this data into a nice way
to visualise it both in the terminal and on the web. It can be used as a more helpful visualisation tool than the standard
type descriptions.

We want to provide the implementation of the Field functionality so that an `AutoflexField` compiles into a standard
Pydantic Field whilst using the ``json_schema_extra`` to encode the information accordingly.


