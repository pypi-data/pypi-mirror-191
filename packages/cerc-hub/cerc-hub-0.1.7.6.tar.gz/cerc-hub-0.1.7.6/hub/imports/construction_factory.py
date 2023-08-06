"""
ConstructionFactory (before PhysicsFactory) retrieve the specific construction module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from pathlib import Path
from hub.hub_logger import logger
from hub.helpers.utils import validate_import_export_type
from hub.imports.construction.nrel_physics_parameters import NrelPhysicsParameters
from hub.imports.construction.nrcan_physics_parameters import NrcanPhysicsParameters


class ConstructionFactory:
  """
  ConstructionFactory class
  """
  def __init__(self, handler, city, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/construction')
    self._handler = '_' + handler.lower().replace(' ', '_')
    class_funcs = validate_import_export_type(ConstructionFactory)
    if self._handler not in class_funcs:
      err_msg = f"Wrong import type [{self._handler}]. Valid functions include {class_funcs}"
      logger.error(err_msg)
      raise Exception(err_msg)
    self._city = city
    self._base_path = base_path

  def _nrel(self):
    """
    Enrich the city by using NREL information
    """
    NrelPhysicsParameters(self._city, self._base_path).enrich_buildings()
    self._city.level_of_detail.construction = 2

  def _nrcan(self):
    """
    Enrich the city by using NRCAN information
    """
    NrcanPhysicsParameters(self._city, self._base_path).enrich_buildings()
    self._city.level_of_detail.construction = 2

  def enrich(self):
    """
    Enrich the city given to the class using the class given handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()

  def enrich_debug(self):
    """
    Enrich the city given to the class using the class given handler
    :return: None
    """
    NrelPhysicsParameters(self._city, self._base_path).enrich_buildings()
