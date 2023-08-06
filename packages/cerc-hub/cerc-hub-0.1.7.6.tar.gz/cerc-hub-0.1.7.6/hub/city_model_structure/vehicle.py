"""
LifeCycleAssessment retrieve the specific Life Cycle Assessment module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""

class Vehicle:
  """
  Vehicle class
  """

  def __init__(self, vehicle_id, name, fuel_consumption_rate, fuel_consumption_unit, carbon_emission_factor,
               carbon_emission_factor_unit):
    self._vehicle_id = vehicle_id
    self._name = name
    self._fuel_consumption_rate = fuel_consumption_rate
    self._fuel_consumption_unit = fuel_consumption_unit
    self._carbon_emission_factor = carbon_emission_factor
    self._carbon_emission_factor_unit = carbon_emission_factor_unit

  @property
  def id(self) -> int:
    """
    Get vehicle id
    :return: int
    """
    return self._vehicle_id

  @property
  def name(self) -> str:
    """
    Get vehicle name
    :return: str
    """
    return self._name

  @property
  def fuel_consumption_rate(self) -> float:
    """
    Get vehicle fuel consumption rate
    :return: float
    """
    return self._fuel_consumption_rate

  @property
  def fuel_consumption_unit(self) -> str:
    """
    Get fuel consumption unit
    :return: str
    """
    return self._fuel_consumption_unit

  @property
  def carbon_emission_factor(self) -> float:
    """
    Get vehicle carbon emission factor
    :return: float
    """
    return self._carbon_emission_factor

  @property
  def carbon_emission_factor_unit(self) -> str:
    """
    Get carbon emission units
    :return: str
    """
    return self._carbon_emission_factor_unit
