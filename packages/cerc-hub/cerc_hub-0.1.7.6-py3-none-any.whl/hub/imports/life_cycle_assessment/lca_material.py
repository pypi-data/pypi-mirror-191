"""
CityGml module parses citygml_classes files and import the geometry into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""
import xmltodict
from pathlib import Path
from hub.city_model_structure.lca_material import LcaMaterial as LMaterial


class LcaMaterial:
  def __init__(self, city, base_path):
    self._city = city
    self._base_path = base_path
    self._lca = None

  def enrich(self):
    self._city.lca_materials = []
    path = Path(self._base_path / 'lca_data.xml').resolve()

    with open(path) as xml:
      self._lca = xmltodict.parse(xml.read())

    for material in self._lca["library"]["building_materials"]['material']:
      _material = LMaterial()
      _material.type = material['@type']
      _material.id = material['@id']
      _material.name = material['@name']
      _material.density = material['density']['#text']
      _material.density_unit = material['density']['@unit']
      _material.embodied_carbon = material['embodied_carbon']['#text']
      _material.embodied_carbon_unit = material['embodied_carbon']['@unit']
      _material.recycling_ratio = material['recycling_ratio']
      _material.onsite_recycling_ratio = material['onsite_recycling_ratio']
      _material.company_recycling_ratio = material['company_recycling_ratio']
      _material.landfilling_ratio = material['landfilling_ratio']
      _material.cost = material['cost']['#text']
      _material._cost_unit = material['cost']['@unit']

      self._city.lca_materials.append(_material)
