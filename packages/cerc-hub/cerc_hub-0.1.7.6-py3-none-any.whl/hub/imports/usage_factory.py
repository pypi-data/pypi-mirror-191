"""
UsageFactory retrieve the specific usage module for the given region
This factory can only be called after calling the construction factory so the thermal zones are created.
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from pathlib import Path
from hub.imports.usage.comnet_usage_parameters import ComnetUsageParameters
from hub.imports.usage.nrcan_usage_parameters import NrcanUsageParameters
from hub.hub_logger import logger
from hub.helpers.utils import validate_import_export_type


class UsageFactory:
  """
  UsageFactory class
  """
  def __init__(self, handler, city, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/usage')
    self._handler = '_' + handler.lower().replace(' ', '_')
    class_funcs = validate_import_export_type(UsageFactory)
    if self._handler not in class_funcs:
      err_msg = f"Wrong import type [{self._handler}]. Valid functions include {class_funcs}"
      logger.error(err_msg)
      raise Exception(err_msg)
    self._city = city
    self._base_path = base_path

  def _comnet(self):
    """
    Enrich the city with COMNET usage library
    """
    self._city.level_of_detail.usage = 2
    ComnetUsageParameters(self._city, self._base_path).enrich_buildings()

  def _nrcan(self):
    """
    Enrich the city with NRCAN usage library
    """
    self._city.level_of_detail.usage = 2
    NrcanUsageParameters(self._city, self._base_path).enrich_buildings()

  def enrich(self):
    """
    Enrich the city given to the class using the usage factory given handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()
