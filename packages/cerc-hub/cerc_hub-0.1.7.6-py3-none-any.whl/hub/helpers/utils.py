"""
Constant module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""


def validate_import_export_type(cls_name: type):
  """
  Retrieves all the function names in a class which are property types (decoration)
  and normal functions
  :param cls_name: the class name
  :return: [str], a list of functions in the class
  """
  return [func for func in dir(cls_name)
          if (type(getattr(cls_name, func)) is property or callable(getattr(cls_name, func)))
          and func in cls_name.__dict__ and func[0] == '_' and func != '__init__']
