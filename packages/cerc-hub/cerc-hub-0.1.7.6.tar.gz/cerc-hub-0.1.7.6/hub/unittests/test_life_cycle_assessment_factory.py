"""
Building test
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""
from pathlib import Path
from unittest import TestCase
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.life_cycle_assessment_factory import LifeCycleAssessment


class TestLifeCycleAssessment(TestCase):
  """
  TestBuilding TestCase 1
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._city_gml = None
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()

  def test_fuel(self):
    city_file = "tests_data/C40_Final.gml"
    city = GeometryFactory('citygml', path=city_file).city
    LifeCycleAssessment('fuel', city).enrich()
    for fuel in city.fuels:
      self.assertTrue(len(city.fuels) > 0)

  def test_vehicle(self):
    city_file = "tests_data/C40_Final.gml"
    city = GeometryFactory('citygml', path=city_file).city
    LifeCycleAssessment('vehicle', city).enrich()
    for vehicle in city.vehicles:
      self.assertTrue(len(city.vehicles) > 0)

  def test_machine(self):
    city_file = "tests_data/C40_Final.gml"
    city = GeometryFactory('citygml', path=city_file).city
    LifeCycleAssessment('machine', city).enrich()
    for machine in city.machines:
      self.assertTrue(len(city.machines) > 0)

  def test_material(self):
    city_file = "tests_data/C40_Final.gml"
    city = GeometryFactory('citygml', path=city_file).city
    LifeCycleAssessment('material', city).enrich()
    for material in city.lca_materials:
      self.assertTrue(len(city.lca_materials) > 0)




