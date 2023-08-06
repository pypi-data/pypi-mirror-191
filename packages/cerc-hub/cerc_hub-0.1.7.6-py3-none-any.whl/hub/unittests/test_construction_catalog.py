"""
TestConstructionCatalog
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

from unittest import TestCase
from hub.catalog_factories.construction_catalog_factory import ConstructionCatalogFactory


class TestConstructionCatalog(TestCase):

  def test_nrel_catalog(self):
    catalog = ConstructionCatalogFactory('nrel').catalog
    catalog_categories = catalog.names()
    constructions = catalog.names('constructions')
    windows = catalog.names('windows')
    materials = catalog.names('materials')
    self.assertTrue(len(constructions['constructions']), 24)
    self.assertTrue(len(windows['windows']), 4)
    self.assertTrue(len(materials['materials']), 19)
    with self.assertRaises(ValueError):
      catalog.names('unknown')

    # retrieving all the entries should not raise any exceptions
    for category in catalog_categories:
      for value in catalog_categories[category]:
        catalog.get_entry(value)

    with self.assertRaises(IndexError):
      catalog.get_entry('unknown')

