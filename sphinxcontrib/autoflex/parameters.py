"""
This is what we had before in terms of our parameter extraction.

Other relevant references are:
- autodoc_pydantic parameter visualisation.
"""


# @classmethod
# def generate_docstring(cls) -> str:
#     """Generates a docstring for a Tidy3D mode and saves it to the __doc__ of the class."""
#
#     # store the docstring in here
#     doc = ""
#
#     # if the model already has a docstring, get the first lines and save the rest
#     original_docstrings = []
#     if cls.__doc__:
#         original_docstrings = cls.__doc__.split("\n\n")
#         class_description = original_docstrings.pop(0)
#         doc += class_description
#     original_docstrings = "\n\n".join(original_docstrings)
#
#     # create the list of parameters (arguments) for the model
#     doc += "\n\n    Parameters\n    ----------\n"
#     for field_name, field in cls.__fields__.items():
#         # ignore the type tag
#         if field_name == TYPE_TAG_STR:
#             continue
#
#         # get data type
#         data_type = field._type_display()
#
#         # get default values
#         default_val = field.get_default()
#         if "=" in str(default_val):
#             # handle cases where default values are pydantic models
#             default_val = f"{default_val.__class__.__name__}({default_val})"
#             default_val = (", ").join(default_val.split(" "))
#             default_val = default_val.replace("=", "")
#
#         # make first line: name : type = default
#         default_str = "" if field.required else f" = {default_val}"
#         doc += f"\n\t\t``{field_name}``: Attribute: :attr:`{field_name}` \n"
#         doc += "\n\t\t\t .. list-table::"
#         doc += "\n\t\t\t\t:widths: 20 80\n"
#         doc += "\n\t\t\t\t* -    ``Type``"
#         doc += f"\n\t\t\t\t  -    *{data_type}*"
#         doc += "\n\t\t\t\t* -    ``Default``"
#         doc += f"\n\t\t\t\t  -     {default_str}"
#
#         # get field metadata
#         field_info = field.field_info
#         # doc += "        "
#
#         # add units (if present)
#         units = field_info.extra.get("units")
#         if units is not None:
#             if isinstance(units, (tuple, list)):
#                 unitstr = "("
#                 for unit in units:
#                     unitstr += str(unit)
#                     unitstr += ", "
#                 unitstr = unitstr[:-2]
#                 unitstr += ")"
#             else:
#                 unitstr = units
#             doc += "\n\t\t\t\t* -    ``Units``"
#             doc += f"\n\t\t\t\t  -    `{unitstr}`"
#
#         # add description
#         description_str = field_info.description
#         if description_str is not None:
#             doc += "\n\t\t\t\t* -    ``Description``"
#             doc += f"\n\t\t\t\t  -    {description_str}\n"
#
#     # add in remaining things in the docs
#     if original_docstrings:
#         doc += "\n"
#         doc += original_docstrings
#
#     doc += "\n"
#     cls.__doc__ = doc
