"""
ExportsFactory export a city into several formats
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

from pathlib import Path
from hub.exports.formats.obj import Obj
from hub.exports.formats.simplified_radiosity_algorithm import SimplifiedRadiosityAlgorithm
from hub.exports.formats.stl import Stl
from hub.hub_logger import logger
from hub.helpers.utils import validate_import_export_type


class ExportsFactory:
  """
  Exports factory class
  """
  def __init__(self, export_type, city, path,
               target_buildings=None,
               adjacent_buildings=None,
               weather_file=None,
               weather_format=None):
    self._city = city
    self._export_type = '_' + export_type.lower()
    class_funcs = validate_import_export_type(ExportsFactory)
    if self._export_type not in class_funcs:
      err_msg = f"Wrong export type [{self._export_type}]. Valid functions include {class_funcs}"
      logger.error(err_msg)
      raise Exception(err_msg)
    if isinstance(path, str):
      path = Path(path)
    self._path = path
    self._target_buildings = target_buildings
    self._adjacent_buildings = adjacent_buildings
    self._weather_file = weather_file
    self._weather_format = weather_format

  @property
  def _citygml(self):
    """
    Export to citygml
    :return: None
    """
    raise NotImplementedError

  @property
  def _collada(self):
    raise NotImplementedError

  @property
  def _stl(self):
    """
    Export the city geometry to stl
    :return: None
    """
    return Stl(self._city, self._path)

  @property
  def _obj(self):
    """
    Export the city geometry to obj
    :return: None
    """
    return Obj(self._city, self._path)

  @property
  def _grounded_obj(self):
    """
    Export the city geometry to obj with grounded coordinates
    :return: None
    """
    return Obj(self._city, self._path).to_ground_points()

  @property
  def _sra(self):
    """
    Export the city to Simplified Radiosity Algorithm xml format
    :return: None
    """
    return SimplifiedRadiosityAlgorithm(self._city,
                                        (self._path / f'{self._city.name}_sra.xml'),
                                        self._weather_file,
                                        self._weather_format,
                                        target_buildings=self._target_buildings)

  def export(self):
    """
    Export the city given to the class using the given export type handler
    :return: None
    """
    return getattr(self, self._export_type, lambda: None)

  def export_debug(self):
    """
    Export the city given to the class using the given export type handler
    :return: None
    """
    return Obj(self._city, self._path)
