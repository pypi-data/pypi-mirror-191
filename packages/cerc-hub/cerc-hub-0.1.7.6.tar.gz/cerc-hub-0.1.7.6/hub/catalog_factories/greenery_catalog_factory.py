"""
Greenery catalog publish the greenery information
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

from pathlib import Path
from typing import TypeVar
from hub.catalog_factories.greenery.greenery_catalog import GreeneryCatalog
from hub.hub_logger import logger
from hub.helpers.utils import validate_import_export_type
Catalog = TypeVar('Catalog')


class GreeneryCatalogFactory:
  """
  GreeneryCatalogFactory class
  """
  def __init__(self, file_type, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/greenery')
    self._catalog_type = '_' + file_type.lower()
    class_funcs = validate_import_export_type(GreeneryCatalogFactory)
    if self._catalog_type not in class_funcs:
      err_msg = f"Wrong import type. Valid functions include {class_funcs}"
      logger.error(err_msg)
      raise Exception(err_msg)
    self._path = base_path

  @property
  def _nrel(self):
    """
    Return a greenery catalog based in NREL using ecore as datasource
    :return: GreeneryCatalog
    """
    return GreeneryCatalog((self._path / 'ecore_greenery_catalog.xml').resolve())

  @property
  def catalog(self) -> Catalog:
    """
    Enrich the city given to the class using the class given handler
    :return: Catalog
    """
    return getattr(self, self._catalog_type, lambda: None)
