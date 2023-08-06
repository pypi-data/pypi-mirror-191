"""
CityGml module parses citygml_classes files and import the geometry into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""
import xmltodict
from pathlib import Path
from hub.city_model_structure.vehicle import Vehicle


class LcaVehicle:
  def __init__(self, city, base_path):
    self._city = city
    self._base_path = base_path
    self._lca = None

  def enrich(self):
    self._city.vehicles = []
    path = Path(self._base_path / 'lca_data.xml').resolve()

    with open(path) as xml:
      self._lca = xmltodict.parse(xml.read())
    for vehicle in self._lca["library"]["vehicles"]['vehicle']:
      self._city.vehicles.append(Vehicle(vehicle['@id'], vehicle['@name'], vehicle['fuel_consumption_rate']['#text'],
                                         vehicle['fuel_consumption_rate']['@unit'],
                                         vehicle['carbon_emission_factor']['#text'],
                                         vehicle['carbon_emission_factor']['@unit']))
