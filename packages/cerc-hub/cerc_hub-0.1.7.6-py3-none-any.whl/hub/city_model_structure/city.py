"""
City module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Peter Yefi peteryefi@gmail.com
"""
from __future__ import annotations

import bz2
import sys
import pickle
import math
import copy
import pyproj
from typing import List, Union
from pyproj import Transformer
from pathlib import Path
from hub.city_model_structure.building import Building
from hub.city_model_structure.city_object import CityObject
from hub.city_model_structure.city_objects_cluster import CityObjectsCluster
from hub.city_model_structure.buildings_cluster import BuildingsCluster
from hub.city_model_structure.fuel import Fuel
from hub.city_model_structure.iot.station import Station
from hub.city_model_structure.level_of_detail import LevelOfDetail
from hub.city_model_structure.machine import Machine
from hub.city_model_structure.parts_consisting_building import PartsConsistingBuilding
from hub.helpers.geometry_helper import GeometryHelper
from hub.helpers.location import Location
from hub.city_model_structure.energy_system import EnergySystem
from hub.city_model_structure.lca_material import LcaMaterial


class City:
  """
  City class
  """

  def __init__(self, lower_corner, upper_corner, srs_name):
    self._name = None
    self._lower_corner = lower_corner
    self._upper_corner = upper_corner
    self._buildings = None
    self._srs_name = srs_name
    self._location = None
    self._country_code = None
    self._climate_reference_city = None
    self._climate_file = None
    self._latitude = None
    self._longitude = None
    self._time_zone = None
    self._buildings_clusters = None
    self._parts_consisting_buildings = None
    self._city_objects_clusters = None
    self._city_objects = None
    self._energy_systems = None
    self._fuels = None
    self._machines = None
    self._stations = []
    self._lca_materials = None
    self._level_of_detail = LevelOfDetail()

  @property
  def fuels(self) -> [Fuel]:
    return self._fuels

  @fuels.setter
  def fuels(self, value):
    self._fuels = value

  @property
  def machines(self) -> [Machine]:
    return self._machines

  @machines.setter
  def machines(self, value):
    self._machines = value

  def _get_location(self) -> Location:
    if self._location is None:
      gps = pyproj.CRS('EPSG:4326')  # LatLon with WGS84 datum used by GPS units and Google Earth
      try:
        if self._srs_name in GeometryHelper.srs_transformations.keys():
          self._srs_name = GeometryHelper.srs_transformations[self._srs_name]
        input_reference = pyproj.CRS(self.srs_name)  # Projected coordinate system from input data
      except pyproj.exceptions.CRSError:
        sys.stderr.write('Invalid projection reference system, please check the input data. '
                         '(e.g. in CityGML files: srs_name)\n')
        sys.exit()
      transformer = Transformer.from_crs(input_reference, gps)
      coordinates = transformer.transform(self.lower_corner[0], self.lower_corner[1])
      self._location = GeometryHelper.get_location(coordinates[0], coordinates[1])
    return self._location

  @property
  def country_code(self):
    """
    Get models country code
    :return: str
    """
    return self._get_location().country

  @property
  def location(self):
    return self._get_location().city

  @property
  def name(self):
    """
    Get city name
    :return: str
    """
    if self._name is None:
      return self._get_location().city
    return self._name

  @property
  def climate_reference_city(self) -> Union[None, str]:
    """
    Get the name for the climatic information reference city
    :return: None or str
    """
    return self._climate_reference_city

  @climate_reference_city.setter
  def climate_reference_city(self, value):
    """
    Set the name for the climatic information reference city
    :param value: str
    """
    if value is not None:
      self._climate_reference_city = str(value)

  @property
  def climate_file(self) -> Union[None, Path]:
    """
    Get the climate file full path
    :return: None or Path
    """
    return self._climate_file

  @climate_file.setter
  def climate_file(self, value):
    """
    Set the climate file full path
    :param value: Path
    """
    if value is not None:
      self._climate_file = Path(value)

  @property
  def city_objects(self) -> Union[List[CityObject], None]:
    """
    Get the city objects belonging to the city
    :return: None or [CityObject]
    """
    if self._city_objects is None:
      if self.city_objects_clusters is None:
        self._city_objects = []
      else:
        self._city_objects = self.city_objects_clusters
      if self.buildings is not None:
        for building in self.buildings:
          self._city_objects.append(building)
      if self.energy_systems is not None:
        for energy_system in self.energy_systems:
          self._city_objects.append(energy_system)
    return self._city_objects

  @property
  def buildings(self) -> Union[List[Building], None]:
    """
    Get the buildings belonging to the city
    :return: None or [Building]
    """
    return self._buildings

  @property
  def lower_corner(self) -> List[float]:
    """
    Get city lower corner
    :return: [x,y,z]
    """
    return self._lower_corner

  @property
  def upper_corner(self) -> List[float]:
    """
    Get city upper corner
    :return: [x,y,z]
    """
    return self._upper_corner

  def city_object(self, name) -> Union[CityObject, None]:
    """
    Retrieve the city CityObject with the given name
    :param name:str
    :return: None or CityObject
    """
    for city_object in self.buildings:
      if str(city_object.name) == str(name):
        return city_object
    return None

  def add_city_object(self, new_city_object):
    """
    Add a CityObject to the city
    :param new_city_object:CityObject
    :return: None or not implemented error
    """
    if new_city_object.type == 'building':
      if self._buildings is None:
        self._buildings = []
      self._buildings.append(new_city_object)
    elif new_city_object.type == 'energy_system':
      if self._energy_systems is None:
        self._energy_systems = []
      self._energy_systems.append(new_city_object)
    else:
      raise NotImplementedError(new_city_object.type)

  def remove_city_object(self, city_object):
    """
    Remove a CityObject from the city
    :param city_object:CityObject
    :return: None
    """
    if city_object.type != 'building':
      raise NotImplementedError(city_object.type)
    if self._buildings is None or self._buildings == []:
      sys.stderr.write('Warning: impossible to remove city_object, the city is empty\n')
    else:
      if city_object in self._buildings:
        self._buildings.remove(city_object)

  @property
  def srs_name(self) -> Union[None, str]:
    """
    Get city srs name
    :return: None or str
    """
    return self._srs_name

  @name.setter
  def name(self, value):
    """
    Set city name
    :param value:str
    """
    if value is not None:
      self._name = str(value)

  @staticmethod
  def load(city_filename) -> City:
    """
    Load a city saved with city.save(city_filename)
    :param city_filename: city filename
    :return: City
    """
    with open(city_filename, 'rb') as file:
      return pickle.load(file)

  def save(self, city_filename):
    """
    Save a city into the given filename
    :param city_filename: destination city filename
    :return: None
    """
    with open(city_filename, 'wb') as file:
      pickle.dump(self, file)

  def save_compressed(self, city_filename):
    """
    Save a city into the given filename
    :param city_filename: destination city filename
    :return: None
    """
    with bz2.BZ2File(city_filename, 'wb') as f:
      pickle.dump(self, f)

  def region(self, center, radius) -> City:
    """
    Get a region from the city
    :param center: specific point in space [x, y, z]
    :param radius: distance to center of the sphere selected in meters
    :return: selected_region_city
    """
    selected_region_lower_corner = [center[0] - radius, center[1] - radius, center[2] - radius]
    selected_region_upper_corner = [center[0] + radius, center[1] + radius, center[2] + radius]
    selected_region_city = City(selected_region_lower_corner, selected_region_upper_corner, srs_name=self.srs_name)
    selected_region_city.climate_file = self.climate_file
    #    selected_region_city.climate_reference_city = self.climate_reference_city
    for city_object in self.city_objects:
      location = city_object.centroid
      if location is not None:
        distance = math.sqrt(math.pow(location[0] - center[0], 2) + math.pow(location[1] - center[1], 2)
                             + math.pow(location[2] - center[2], 2))
        if distance < radius:
          selected_region_city.add_city_object(city_object)
    return selected_region_city

  @property
  def latitude(self) -> Union[None, float]:
    """
    Get city latitude in degrees
    :return: None or float
    """
    return self._latitude

  @latitude.setter
  def latitude(self, value):
    """
    Set city latitude in degrees
    :parameter value: float
    """
    if value is not None:
      self._latitude = float(value)

  @property
  def longitude(self) -> Union[None, float]:
    """
    Get city longitude in degrees
    :return: None or float
    """
    return self._longitude

  @longitude.setter
  def longitude(self, value):
    """
    Set city longitude in degrees
    :parameter value: float
    """
    if value is not None:
      self._longitude = float(value)

  @property
  def time_zone(self) -> Union[None, float]:
    """
    Get city time_zone
    :return: None or float
    """
    return self._time_zone

  @time_zone.setter
  def time_zone(self, value):
    """
    Set city time_zone
    :parameter value: float
    """
    if value is not None:
      self._time_zone = float(value)

  @property
  def buildings_clusters(self) -> Union[List[BuildingsCluster], None]:
    """
    Get buildings clusters belonging to the city
    :return: None or [BuildingsCluster]
    """
    return self._buildings_clusters

  @property
  def parts_consisting_buildings(self) -> Union[List[PartsConsistingBuilding], None]:
    """
    Get parts consisting buildings belonging to the city
    :return: None or [PartsConsistingBuilding]
    """
    return self._parts_consisting_buildings

  @property
  def energy_systems(self) -> Union[List[EnergySystem], None]:
    """
    Get energy systems belonging to the city
    :return: None or [EnergySystem]
    """
    return self._energy_systems

  @property
  def stations(self) -> [Station]:
    """
    Get the sensors stations belonging to the city
    :return: [Station]
    """
    return self._stations

  @property
  def city_objects_clusters(self) -> Union[List[CityObjectsCluster], None]:
    """
    Get city objects clusters belonging to the city
    :return: None or [CityObjectsCluster]
    """
    if self.buildings_clusters is None:
      self._city_objects_clusters = []
    else:
      self._city_objects_clusters = self.buildings_clusters
    if self.parts_consisting_buildings is not None:
      self._city_objects_clusters.append(self.parts_consisting_buildings)
    return self._city_objects_clusters

  def add_city_objects_cluster(self, new_city_objects_cluster):
    """
    Add a CityObject to the city
    :param new_city_objects_cluster:CityObjectsCluster
    :return: None or NotImplementedError
    """
    if new_city_objects_cluster.type == 'buildings':
      if self._buildings_clusters is None:
        self._buildings_clusters = []
      self._buildings_clusters.append(new_city_objects_cluster)
    elif new_city_objects_cluster.type == 'building_parts':
      if self._parts_consisting_buildings is None:
        self._parts_consisting_buildings = []
      self._parts_consisting_buildings.append(new_city_objects_cluster)
    else:
      raise NotImplementedError

  @property
  def lca_materials(self) -> Union[List[LcaMaterial], None]:
    """
    Get life cycle materials for the city
    :return: [LcaMaterial] or
    """
    return self._lca_materials

  @lca_materials.setter
  def lca_materials(self, value):
    """
    Set life cycle materials for the city
    """
    self._lca_materials = value

  def lca_material(self, lca_id) -> Union[LcaMaterial, None]:
    """
    Get the lca material matching the given Id
    :return: LcaMaterial or None
    """
    for lca_material in self.lca_materials:
      if str(lca_material.id) == str(lca_id):
        return lca_material
    return None

  @property
  def copy(self) -> City:
    """
    Get a copy of the current city
    """
    return copy.deepcopy(self)

  def merge(self, city) -> City:
    _merge_city = self.copy
    for city_object in city.city_objects:
      _merge_city.add_city_object(city_object)
    return _merge_city

  @property
  def level_of_detail(self) -> LevelOfDetail:
    """
    Get level of detail of different aspects of the city: geometry, construction and usage
    :return: LevelOfDetail
    """
    return self._level_of_detail
