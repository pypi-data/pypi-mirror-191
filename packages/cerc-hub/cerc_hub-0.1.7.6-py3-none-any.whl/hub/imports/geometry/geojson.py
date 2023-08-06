"""
Geojson module parses geojson files and import the geometry into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guillermo Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""
import json

import trimesh.creation

from pyproj import Transformer
from shapely.geometry import Polygon as ShapelyPolygon

import hub.helpers.constants as cte
from hub.imports.geometry.helpers.geometry_helper import GeometryHelper
from hub.city_model_structure.attributes.polygon import Polygon
from hub.city_model_structure.building import Building
from hub.city_model_structure.building_demand.surface import Surface
from hub.city_model_structure.city import City


class Geojson:
  """
  Geojson class
  """
  X = 0
  Y = 1

  def __init__(self,
               path,
               extrusion_height_field=None,
               year_of_construction_field=None,
               function_field=None,
               function_to_hub=None):
    # todo: destination epsg should change according actual the location
    self._transformer = Transformer.from_crs('epsg:4326', 'epsg:26911')
    self._min_x = cte.MAX_FLOAT
    self._min_y = cte.MAX_FLOAT
    self._max_x = cte.MIN_FLOAT
    self._max_y = cte.MIN_FLOAT
    self._max_z = 0
    self._city = None
    self._extrusion_height_field = extrusion_height_field
    self._year_of_construction_field = year_of_construction_field
    self._function_field = function_field
    self._function_to_hub = function_to_hub
    with open(path) as json_file:
      self._geojson = json.loads(json_file.read())

  def _save_bounds(self, x, y):
    if x > self._max_x:
      self._max_x = x
    if x < self._min_x:
      self._min_x = x
    if y > self._max_y:
      self._max_y = y
    if y < self._min_y:
      self._min_y = y

  @staticmethod
  def _create_buildings_lod0(name, year_of_construction, function, surfaces_coordinates):
    surfaces = []
    buildings = []
    for zone, surface_coordinates in enumerate(surfaces_coordinates):
      points = GeometryHelper.points_from_string(GeometryHelper.remove_last_point_from_string(surface_coordinates))
      polygon = Polygon(points)
      surfaces.append(Surface(polygon, polygon))
      buildings.append(Building(f'{name}_zone_{zone}', surfaces, year_of_construction, function))
    return buildings

  @staticmethod
  def _create_buildings_lod1(name, year_of_construction, function, height, surface_coordinates):
    lod0_buildings = Geojson._create_buildings_lod0(name, year_of_construction, function, surface_coordinates)
    surfaces = []
    buildings = []
    for zone, lod0_building in enumerate(lod0_buildings):
      for surface in lod0_building.surfaces:
        shapely_polygon = ShapelyPolygon(surface.solid_polygon.coordinates)
        if not shapely_polygon.is_valid:
          print(surface.solid_polygon.area)
          print('error?', name, surface_coordinates)
          continue
        mesh = trimesh.creation.extrude_polygon(shapely_polygon, height)
        for face in mesh.faces:
          points = []
          for vertex_index in face:
            points.append(mesh.vertices[vertex_index])
          polygon = Polygon(points)
          surface = Surface(polygon, polygon)
          surfaces.append(surface)
        buildings.append(Building(f'{name}_zone_{zone}', surfaces, year_of_construction, function))
    return buildings

  def _get_polygons(self, polygons, coordinates):
    if type(coordinates[0][self.X]) != float:
      polygons = []
      for element in coordinates:
        polygons = self._get_polygons(polygons, element)
      return polygons
    else:
      transformed_coordinates = ''
      for coordinate in coordinates:
        transformed = self._transformer.transform(coordinate[self.Y], coordinate[self.X])
        self._save_bounds(transformed[self.X], transformed[self.Y])
        transformed_coordinates = f'{transformed_coordinates} {transformed[self.X]} {transformed[self.Y]} 0.0'
      polygons.append(transformed_coordinates.lstrip(' '))
      return polygons

  @property
  def city(self) -> City:
    """
    Get city out of a Geojson file
    """
    if self._city is None:
      buildings = []
      building_id = 0
      for feature in self._geojson['features']:
        extrusion_height = 0
        if self._extrusion_height_field is not None:
          extrusion_height = float(feature['properties'][self._extrusion_height_field])
        year_of_construction = None
        if self._year_of_construction_field is not None:
          year_of_construction = int(feature['properties'][self._year_of_construction_field])
        function = None
        if self._function_field is not None:
          function = feature['properties'][self._function_field]
          if self._function_to_hub is not None:
            # use the transformation dictionary to retrieve the proper function
            function = self._function_to_hub[function]
        geometry = feature['geometry']
        if 'id' in feature:
          building_name = feature['id']
        else:
          building_name = f'building_{building_id}'
          building_id += 1
        polygons = []
        lod = 1
        for part, coordinates in enumerate(geometry['coordinates']):
          polygons = self._get_polygons(polygons, coordinates)
          for zone, polygon in enumerate(polygons):
            if extrusion_height == 0:
              buildings = buildings + Geojson._create_buildings_lod0(f'{building_name}_part_{part}_zone{zone}',
                                                                     year_of_construction,
                                                                     function,
                                                                     [polygon])
              lod = 0
            else:
              if self._max_z < extrusion_height:
                self._max_z = extrusion_height
              buildings = buildings + Geojson._create_buildings_lod1(f'{building_name}_part_{part}',
                                                                     year_of_construction,
                                                                     function,
                                                                     extrusion_height,
                                                                     [polygon])

      self._city = City([self._min_x, self._min_y, 0.0], [self._max_x, self._max_y, self._max_z], 'epsg:26911')
      for building in buildings:
        self._city.add_city_object(building)
      self._city.level_of_detail.geometry = lod
    return self._city
