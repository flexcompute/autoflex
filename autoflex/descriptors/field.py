from dataclasses import field
from typing import Any, Optional
from pydantic import Field
from autoflex.types import AutoflexFieldInfo, AutoflexParameterTypes


def AutoflexField(
    default: Any = ...,
    *,
    autoflex_parameters: Optional[AutoflexParameterTypes] = None,
    **kwargs
) -> AutoflexFieldInfo:
    """
    A wrapper around pydantic's Field function that returns an instance of AutoflexFieldInfo
    instead of FieldInfo.

    Args:
        default: The default value of the field.
        autoflex_parameters: An additional argument specific to AutoflexFieldInfo.
        **kwargs: Any other keyword arguments passed to pydantic's Field.

    Returns:
        AutoflexFieldInfo: Custom field info object.
    """

    field_info = Field(default=default, **kwargs)  # Call pydantic's Field internally

    # Return an instance of AutoflexFieldInfo instead of the default FieldInfo
    return AutoflexFieldInfo(
        default=default,
        autoflex=autoflex_parameters,
        **field_info.dict(exclude_none=True)
    )
