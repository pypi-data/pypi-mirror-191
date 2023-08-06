"""
ConstructionFactory (before PhysicsFactory) retrieve the specific construction module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""

class Fuel:
  def __init__(self, fuel_id, name, carbon_emission_factor, unit):
    self._fuel_id = fuel_id
    self._name = name
    self._carbon_emission_factor = carbon_emission_factor
    self._unit = unit

  @property
  def id(self) -> int:
    """
    Get fuel id
    :return: int
    """
    return self._fuel_id

  @property
  def name(self) -> str:
    """
    Get fuel name
    :return: str
    """
    return self._name

  @property
  def carbon_emission_factor(self) -> float:
    """
    Get fuel carbon emission factor
    :return: float
    """
    return self._carbon_emission_factor

  @property
  def unit(self) -> str:
    """
    Get fuel units
    :return: str
    """
    return self._unit
