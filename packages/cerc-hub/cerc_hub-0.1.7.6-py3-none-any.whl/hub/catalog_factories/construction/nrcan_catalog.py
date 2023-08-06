"""
NRCAN construction catalog
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import json
import urllib.request
import xmltodict

from hub.catalog_factories.catalog import Catalog
from hub.catalog_factories.data_models.usages.content import Content
from hub.catalog_factories.construction.construction_helper import ConstructionHelper
from hub.catalog_factories.data_models.construction.construction import Construction
from hub.catalog_factories.data_models.construction.archetype import Archetype


class NrcanCatalog(Catalog):
  def __init__(self, path):
    path = str(path / 'nrcan.xml')
    self._content = None
    self._g_value_per_hdd = []
    self._thermal_transmittance_per_hdd_and_surface = {}
    self._window_ratios = {}
    with open(path) as xml:
      self._metadata = xmltodict.parse(xml.read())
    self._base_url_archetypes = self._metadata['nrcan']['@base_url_archetypes']
    self._base_url_construction = self._metadata['nrcan']['@base_url_construction']
    self._load_window_ratios()
    self._load_construction_values()
    self._content = Content(self._load_archetypes())

  def _load_window_ratios(self):
    for standard in self._metadata['nrcan']['standards_per_function']['standard']:
      url = f'{self._base_url_archetypes}{standard["file_location"]}'
    # todo: read from file
    self._window_ratios = {'Mean': 0.2, 'North': 0.2, 'East': 0.2, 'South': 0.2, 'West': 0.2}

  def _load_construction_values(self):
    for standard in self._metadata['nrcan']['standards_per_period']['standard']:
      g_value_url = f'{self._base_url_construction}{standard["g_value_location"]}'
      punc = '()<?:'
      with urllib.request.urlopen(g_value_url) as json_file:
        text = json.load(json_file)['tables']['SHGC']['table'][0]['formula']
        values = ''.join([o for o in list(text) if o not in punc]).split()
        for index in range(int((len(values) - 1)/3)):
          self._g_value_per_hdd.append([values[3*index+1], values[3*index+2]])
        self._g_value_per_hdd.append(['15000', values[len(values)-1]])

      construction_url = f'{self._base_url_construction}{standard["constructions_location"]}'
      with urllib.request.urlopen(construction_url) as json_file:
        cases = json.load(json_file)['tables']['surface_thermal_transmittance']['table']
        # W/m2K
        for case in cases:
          surface = \
            ConstructionHelper().nrcan_surfaces_types_to_hub_types[f"{case['surface']}_{case['boundary_condition']}"]
          thermal_transmittance_per_hdd = []
          text = case['formula']
          values = ''.join([o for o in list(text) if o not in punc]).split()
          for index in range(int((len(values) - 1)/3)):
            thermal_transmittance_per_hdd.append([values[3*index+1], values[3*index+2]])
          thermal_transmittance_per_hdd.append(['15000', values[len(values)-1]])
          self._thermal_transmittance_per_hdd_and_surface[surface] = thermal_transmittance_per_hdd

  def _load_constructions(self, window_ratio_standard, construction_standard):
    constructions = []
    # todo: we need to save the total transmittance somehow, we don't do it yet in our archetypes
    # todo: it has to be selected the specific thermal_transmittance from
    #  self._thermal_transmittance_per_hdd_and_surface and window_ratios from self._window_ratios for each standard case
    for i, surface_type in enumerate(self._thermal_transmittance_per_hdd_and_surface):
      constructions.append(Construction(i, surface_type, None, None, self._window_ratios))
    return constructions

  def _load_archetypes(self):
    archetypes = []
    archetype_id = 0
    for window_ratio_standard in self._metadata['nrcan']['standards_per_function']['standard']:
      for construction_standard in self._metadata['nrcan']['standards_per_period']['standard']:
        archetype_id += 1
        function = window_ratio_standard['@function']
        climate_zone = 'Montreal'
        construction_period = construction_standard['@period_of_construction']
        constructions = self._load_constructions(window_ratio_standard, construction_standard)
        archetypes.append(Archetype(archetype_id,
                          None,
                          function,
                          climate_zone,
                          construction_period,
                          constructions,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None))
    return archetypes

  def names(self, category=None):
    """
    Get the catalog elements names
    :parm: for usage catalog category filter does nothing as there is only one category (usages)
    """
    _names = {'usages': []}
    for usage in self._content.usages:
      _names['usages'].append(usage.name)
    return _names

  def entries(self, category=None):
    """
    Get the catalog elements
    :parm: for usage catalog category filter does nothing as there is only one category (usages)
    """
    return self._content

  def get_entry(self, name):
    """
    Get one catalog element by names
    :parm: entry name
    """
    for usage in self._content.usages:
      if usage.name.lower() == name.lower():
        return usage
    raise IndexError(f"{name} doesn't exists in the catalog")
