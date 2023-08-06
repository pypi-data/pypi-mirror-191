"""
TestGeometryFactory test and validate the city model structure geometric parameters
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from pathlib import Path
from unittest import TestCase

from numpy import inf

import hub.exports.exports_factory
from hub.imports.construction_factory import ConstructionFactory
from hub.imports.geometry_factory import GeometryFactory


class TestGeometryFactory(TestCase):
  """
  Non-functional TestGeometryFactory
  Load testing
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._city = None
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()
    self._output_path = (Path(__file__).parent / 'tests_outputs').resolve()

  def _get_city(self, file, file_type, height_field=None, year_of_construction_field=None, function_field=None):
    file_path = (self._example_path / file).resolve()
    self._city = GeometryFactory(file_type,
                                 path=file_path,
                                 height_field=height_field,
                                 year_of_construction_field=year_of_construction_field,
                                 function_field=function_field).city
    self.assertIsNotNone(self._city, 'city is none')
    return self._city

  def _check_buildings(self, city):
    for building in city.buildings:
      self.assertIsNotNone(building.name, 'building name is none')
      self.assertIsNotNone(building.type, 'building type is none')
      self.assertIsNotNone(building.volume, 'building volume is none')
      self.assertIsNotNone(building.detailed_polyhedron, 'building detailed polyhedron is none')
      self.assertIsNotNone(building.simplified_polyhedron, 'building simplified polyhedron is none')
      self.assertIsNotNone(building.surfaces, 'building surfaces is none')
      self.assertIsNotNone(building.max_height, 'building max_height is none')
      self.assertEqual(len(building.external_temperature), 0, 'building external temperature is calculated')
      self.assertEqual(len(building.global_horizontal), 0, 'building global horizontal is calculated')
      self.assertEqual(len(building.diffuse), 0, 'building diffuse is calculated')
      self.assertEqual(len(building.beam), 0, 'building beam is calculated')
      self.assertIsNotNone(building.lower_corner, 'building lower corner is none')
      self.assertEqual(len(building.sensors), 0, 'building sensors are assigned')
      self.assertIsNotNone(building.internal_zones, 'no internal zones created')
      self.assertIsNotNone(building.grounds, 'building grounds is none')
      self.assertIsNotNone(building.walls, 'building walls is none')
      self.assertIsNotNone(building.roofs, 'building roofs is none')
      self.assertIsNotNone(building.internal_zones, 'building internal zones is none')
      for internal_zone in building.internal_zones:
        self.assertIsNone(internal_zone.usages, 'usage zones are defined')
        self.assertIsNone(internal_zone.thermal_zones, 'thermal zones are defined')
      self.assertIsNone(building.basement_heated, 'building basement_heated is not none')
      self.assertIsNone(building.attic_heated, 'building attic_heated is not none')
      self.assertIsNone(building.terrains, 'building terrains is not none')
      self.assertIsNone(building.average_storey_height, 'building average_storey_height is not none')
      self.assertIsNone(building.storeys_above_ground, 'building storeys_above_ground is not none')
      self.assertEqual(len(building.heating), 0, 'building heating is not none')
      self.assertEqual(len(building.cooling), 0, 'building cooling is not none')
      self.assertIsNotNone(building.eave_height, 'building eave height is none')
      self.assertIsNotNone(building.roof_type, 'building roof type is none')
      self.assertIsNotNone(building.floor_area, 'building floor_area is none')
      self.assertIsNone(building.households, 'building households is not none')
      self.assertFalse(building.is_conditioned, 'building is_conditioned is conditioned')

  def _check_surfaces(self, building):
    for surface in building.surfaces:
      self.assertIsNotNone(surface.name, 'surface name is none')
      self.assertIsNotNone(surface.id, 'surface id is none')
      self.assertIsNotNone(surface.lower_corner, 'surface envelope_lower_corner is none')
      self.assertIsNotNone(surface.upper_corner, 'surface envelope_upper_corner is none')
      self.assertIsNotNone(surface.perimeter_area, 'surface area_above_ground is none')
      self.assertIsNotNone(surface.azimuth, 'surface azimuth is none')
      self.assertIsNotNone(surface.inclination, 'surface inclination is none')
      self.assertIsNotNone(surface.type, 'surface type is none')
      self.assertEqual(len(surface.global_irradiance), 0, 'global irradiance is calculated')
      self.assertIsNotNone(surface.perimeter_polygon, 'surface perimeter_polygon is none')
      self.assertIsNone(surface.holes_polygons, 'surface hole_polygons is not none')
      self.assertIsNotNone(surface.solid_polygon, 'surface solid_polygon is none')
      self.assertIsNone(surface.short_wave_reflectance, 'surface short_wave_reflectance is not none')
      self.assertIsNone(surface.long_wave_emittance, 'surface long_wave_emittance is not none')
      self.assertIsNotNone(surface.inverse, 'surface inverse is none')
      self.assertEqual(len(surface.associated_thermal_boundaries), 0, 'associated_thermal_boundaries are assigned')
      self.assertIsNone(surface.vegetation, 'surface vegetation is not none')

  # citygml_classes
  def test_import_citygml(self):
    """
    Test city objects in the city
    :return: None
    """
    file = 'FZK_Haus_LoD_2.gml'
    city = self._get_city(file, 'citygml', year_of_construction_field='yearOfConstruction')
    self.assertTrue(len(city.buildings) == 1)
    self._check_buildings(city)
    for building in city.buildings:
      self._check_surfaces(building)
      building.year_of_construction = 2006
      city = ConstructionFactory('nrel', city).enrich()

  def test_import_rhino(self):
    """
    Test rhino import
    """
    file = 'dompark.3dm'
    city = self._get_city(file, 'rhino')
    self.assertIsNotNone(city, 'city is none')
    self.assertTrue(len(city.buildings) == 36)
    i = 0
    for building in city.buildings:
      self.assertIsNot(building.volume, inf, 'open volume')
      i += 1

  def test_import_obj(self):
    """
    Test obj import
    """
    file = 'kelowna.obj'
    city = self._get_city(file, 'obj')
    self.assertTrue(len(city.buildings) == 1)
    self._check_buildings(city)
    for building in city.buildings:
      self._check_surfaces(building)

  def test_import_geojson(self):
    """
    Test geojson import
    """
    file = 'concordia.geojson'
    city = self._get_city(file, 'geojson',
                          height_field='citygml_me',
                          year_of_construction_field='ANNEE_CONS',
                          function_field='LIBELLE_UT')

    hub.exports.exports_factory.ExportsFactory('obj', city, self._output_path).export()
    self.assertEqual(207, len(city.buildings), 'wrong number of buildings')
    self._check_buildings(city)
