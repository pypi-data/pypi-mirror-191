"""
TestCityMerge test and validate the merge of several cities into one
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""
from pathlib import Path
from unittest import TestCase

from hub.imports.geometry_factory import GeometryFactory


class TestCityMerge(TestCase):
  """
  Functional TestCityMerge
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()

  def _get_citygml(self, file):
    file_path = (self._example_path / file).resolve()
    city = GeometryFactory('citygml', path=file_path).city
    self.assertIsNotNone(city, 'city is none')
    return city

  def test_merge(self):
    city_1 = self._get_citygml('one_building_in_kelowna.gml')
    city_2 = self._get_citygml('pluto_building.gml')
    city = city_1.merge(city_2)
    self.assertEqual(len(city_1.city_objects), 1, 'Wrong amount of city_objects found in city_1')
    self.assertEqual(len(city_2.city_objects), 1, 'Wrong amount of city_objects found in city_2')
    self.assertEqual(len(city.city_objects), 2, 'Wrong amount of city_objects found in city')
