"""
CityGml module parses citygml_classes files and import the geometry into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""
import xmltodict
from pathlib import Path
from hub.city_model_structure.fuel import Fuel

class LcaFuel:
  def __init__(self, city, base_path):
    self._city = city
    self._base_path = base_path
    self._lca = None

  def enrich(self):
    self._city.fuels = []
    path = Path(self._base_path / 'lca_data.xml').resolve()

    with open(path) as xml:
      self._lca = xmltodict.parse(xml.read())
    for fuel in self._lca["library"]["fuels"]['fuel']:
      self._city.fuels.append(Fuel(fuel['@id'], fuel['@name'], fuel['carbon_emission_factor']['#text'],
                                    fuel['carbon_emission_factor']['@unit']))
