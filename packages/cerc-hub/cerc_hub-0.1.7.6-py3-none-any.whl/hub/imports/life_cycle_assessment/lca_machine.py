"""
CityGml module parses citygml_classes files and import the geometry into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""
import xmltodict
from pathlib import Path
from hub.city_model_structure.machine import Machine


class LcaMachine:
  def __init__(self, city, base_path):
    self._city = city
    self._base_path = base_path
    self._lca = None

  def enrich(self):
    self._city.machines = []
    path = Path(self._base_path / 'lca_data.xml').resolve()

    with open(path) as xml:
      self._lca = xmltodict.parse(xml.read())
    for machine in self._lca["library"]["machines"]['machine']:
      self._city.machines.append(Machine(machine['@id'], machine['@name'], machine['work_efficiency']['#text'],
                                         machine['work_efficiency']['@unit'],
                                         machine['energy_consumption_rate']['#text'],
                                         machine['energy_consumption_rate']['@unit'],
                                         machine['carbon_emission_factor']['#text'],
                                         machine['carbon_emission_factor']['@unit']))
