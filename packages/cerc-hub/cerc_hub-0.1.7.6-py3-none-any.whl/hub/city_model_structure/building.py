"""
Building module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import sys
from typing import List, Union
import numpy as np
from hub.hub_logger import logger
import hub.helpers.constants as cte
from hub.city_model_structure.building_demand.surface import Surface
from hub.city_model_structure.city_object import CityObject
from hub.city_model_structure.building_demand.household import Household
from hub.city_model_structure.building_demand.internal_zone import InternalZone
from hub.city_model_structure.attributes.polyhedron import Polyhedron


class Building(CityObject):
  """
  Building(CityObject) class
  """
  def __init__(self, name, surfaces, year_of_construction, function, terrains=None):
    super().__init__(name, surfaces)
    self._households = None
    self._basement_heated = None
    self._attic_heated = None
    self._terrains = terrains
    self._year_of_construction = year_of_construction
    self._function = function
    self._average_storey_height = None
    self._storeys_above_ground = None
    self._floor_area = None
    self._roof_type = None
    self._internal_zones = None
    self._shell = None
    self._alias = None
    self._type = 'building'
    self._heating = dict()
    self._cooling = dict()
    self._lighting_electrical_demand = dict()
    self._appliances_electrical_demand = dict()
    self._domestic_hot_water_heat_demand = dict()
    self._eave_height = None
    self._grounds = []
    self._roofs = []
    self._walls = []
    self._internal_walls = []
    self._ground_walls = []
    self._attic_floors = []
    self._interior_slabs = []
    for surface_id, surface in enumerate(self.surfaces):
      self._min_x = min(self._min_x, surface.lower_corner[0])
      self._min_y = min(self._min_y, surface.lower_corner[1])
      self._min_z = min(self._min_z, surface.lower_corner[2])
      surface.id = surface_id
      if surface.type == cte.GROUND:
        self._grounds.append(surface)
      elif surface.type == cte.WALL:
        self._walls.append(surface)
      elif surface.type == cte.ROOF:
        self._roofs.append(surface)
      elif surface.type == cte.INTERIOR_WALL:
        self._internal_walls.append(surface)
      elif surface.type == cte.GROUND_WALL:
        self._ground_walls.append(surface)
      elif surface.type == cte.ATTIC_FLOOR:
        self._attic_floors.append(surface)
      elif surface.type == cte.INTERIOR_SLAB:
        self._interior_slabs.append(surface)
      else:
        logger.error(f'Building {self.name} [alias {self.alias}]  has an unexpected surface type {surface.type}.\n')
        sys.stderr.write(f'Building {self.name} [alias {self.alias}]  has an unexpected surface type {surface.type}.\n')

  @property
  def shell(self) -> Polyhedron:
    """
    Get building's external polyhedron
    :return: [Polyhedron]
    """
    polygons = []
    for surface in self.surfaces:
      if surface.type is not cte.INTERIOR_WALL:
        polygons.append(surface.solid_polygon)
        if surface.holes_polygons is not None:
          for hole in surface.holes_polygons:
            polygons.append(hole)
    if self._shell is None:
      self._shell = Polyhedron(polygons)
    return self._shell

  @property
  def internal_zones(self) -> List[InternalZone]:
    """
    Get building internal zones
    For Lod up to 3, there is only one internal zone which corresponds to the building shell.
    In LoD 4 there can be more than one. In this case the definition of surfaces and floor area must be redefined.
    :return: [InternalZone]
    """
    if self._internal_zones is None:
      self._internal_zones = [InternalZone(self.surfaces, self.floor_area)]
    return self._internal_zones

  @property
  def grounds(self) -> List[Surface]:
    """
    Get building ground surfaces
    :return: [Surface]
    """
    return self._grounds

  @property
  def roofs(self) -> List[Surface]:
    """
    Get building roof surfaces
    :return: [Surface]
    """
    return self._roofs

  @property
  def walls(self) -> List[Surface]:
    """
    Get building wall surfaces
    :return: [Surface]
    """
    return self._walls

  @property
  def internal_walls(self) -> List[Surface]:
    """
    Get building internal wall surfaces
    :return: [Surface]
    """
    return self._internal_walls

  @property
  def terrains(self) -> Union[None, List[Surface]]:
    """
    Get city object terrain surfaces
    :return: [Surface]
    """
    return self._terrains

  @property
  def attic_heated(self) -> Union[None, int]:
    """
    Get if the city object attic is heated
    0: no attic in the building
    1: attic exists but is not heated
    2: attic exists and is heated
    :return: None or int
    """
    return self._attic_heated

  @attic_heated.setter
  def attic_heated(self, value):
    """
    Set if the city object attic is heated
    0: no attic in the building
    1: attic exists but is not heated
    2: attic exists and is heated
    :param value: int
    """
    if value is not None:
      self._attic_heated = int(value)

  @property
  def basement_heated(self) -> Union[None, int]:
    """
    Get if the city object basement is heated
    0: no basement in the building
    1: basement exists but is not heated
    2: basement exists and is heated
    :return: None or int
    """
    return self._basement_heated

  @basement_heated.setter
  def basement_heated(self, value):
    """
    Set if the city object basement is heated
    0: no basement in the building
    1: basement exists but is not heated
    2: basement exists and is heated
    :param value: int
    """
    if value is not None:
      self._basement_heated = int(value)

  @property
  def heated_volume(self):
    """
    Raises not implemented error
    """
    # todo: this need to be calculated based on the basement and attic heated values
    raise NotImplementedError

  @property
  def year_of_construction(self):
    """
    Get building year of construction
    :return: int
    """
    return self._year_of_construction

  @year_of_construction.setter
  def year_of_construction(self, value):
    """
    Set building year of construction
    :param value: int
    """
    if value is not None:
      self._year_of_construction = int(value)

  @property
  def function(self) -> Union[None, str]:
    """
    Get building function
    :return: None or str
    """
    return self._function

  @function.setter
  def function(self, value):
    """
    Set building function
    :param value: str
    """
    if value is not None:
      self._function = str(value)

  @property
  def average_storey_height(self) -> Union[None, float]:
    """
    Get building average storey height in meters
    :return: None or float
    """
    return self._average_storey_height

  @average_storey_height.setter
  def average_storey_height(self, value):
    """
    Set building average storey height in meters
    :param value: float
    """
    if value is not None:
      self._average_storey_height = float(value)

  @property
  def storeys_above_ground(self) -> Union[None, int]:
    """
    Get building storeys number above ground
    :return: None or int
    """
    return self._storeys_above_ground

  @storeys_above_ground.setter
  def storeys_above_ground(self, value):
    """
    Set building storeys number above ground
    :param value: int
    """
    if value is not None:
      self._storeys_above_ground = int(value)

  @property
  def heating(self) -> dict:
    """
    Get heating demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._heating

  @heating.setter
  def heating(self, value):
    """
    Set heating demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._heating = value

  @property
  def cooling(self) -> dict:
    """
    Get cooling demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._cooling

  @cooling.setter
  def cooling(self, value):
    """
    Set cooling demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._cooling = value

  @property
  def lighting_electrical_demand(self) -> dict:
    """
    Get lighting electrical demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._lighting_electrical_demand

  @lighting_electrical_demand.setter
  def lighting_electrical_demand(self, value):
    """
    Set lighting electrical demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._lighting_electrical_demand = value

  @property
  def appliances_electrical_demand(self) -> dict:
    """
    Get appliances electrical demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._appliances_electrical_demand

  @appliances_electrical_demand.setter
  def appliances_electrical_demand(self, value):
    """
    Set appliances electrical demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._appliances_electrical_demand = value

  @property
  def domestic_hot_water_heat_demand(self) -> dict:
    """
    Get domestic hot water heat demand in Wh
    :return: dict{DataFrame(float)}
    """
    return self._domestic_hot_water_heat_demand

  @domestic_hot_water_heat_demand.setter
  def domestic_hot_water_heat_demand(self, value):
    """
    Set domestic hot water heat demand in Wh
    :param value: dict{DataFrame(float)}
    """
    self._domestic_hot_water_heat_demand = value

  @property
  def eave_height(self):
    """
    Get building eave height in meters
    :return: float
    """
    if self._eave_height is None:
      self._eave_height = 0
      for wall in self.walls:
        self._eave_height = max(self._eave_height, wall.upper_corner[2])
    return self._eave_height

  @property
  def roof_type(self):
    """
    Get roof type for the building flat or pitch
    :return: str
    """
    if self._roof_type is None:
      self._roof_type = 'flat'
      for roof in self.roofs:
        grads = np.rad2deg(roof.inclination)
        if 355 > grads > 5:
          self._roof_type = 'pitch'
          break
    return self._roof_type

  @roof_type.setter
  def roof_type(self, value):
    """
    Set roof type for the building flat or pitch
    :return: str
    """
    self._roof_type = value

  @property
  def floor_area(self):
    """
    Get building floor area in square meters
    :return: float
    """
    if self._floor_area is None:
      self._floor_area = 0
      for surface in self.surfaces:
        if surface.type == 'Ground':
          self._floor_area += surface.perimeter_polygon.area
    return self._floor_area

  @property
  def households(self) -> List[Household]:
    """
    Get the list of households inside the building
    :return: List[Household]
    """
    return self._households

  @property
  def is_conditioned(self):
    """
    Get building heated flag
    :return: Boolean
    """
    if self.internal_zones is None:
      return False
    for internal_zone in self.internal_zones:
      if internal_zone.usages is not None:
        for usage in internal_zone.usages:
          if usage.thermal_control is not None:
            return True
    return False

  @property
  def alias(self):
    """
    Get the alias name for the building
    :return: str
    """
    return self._alias

  @alias.setter
  def alias(self, value):
    """
    Set the alias name for the building
    """
    self._alias = value

  @property
  def usages_percentage(self):
    """
    Get the usages and percentages for the building
    """
    _usage = ''
    for internal_zone in self.internal_zones:
      for usage in internal_zone.usages:
        _usage = f'{_usage}{usage.name}_{usage.percentage} '
    return _usage.rstrip()
