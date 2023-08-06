"""
LifeCycleAssessment retrieve the specific Life Cycle Assessment module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""


class Machine:
  """
  Machine class
  """

  def __init__(self, machine_id, name, work_efficiency, work_efficiency_unit, energy_consumption_rate,
               energy_consumption_unit, carbon_emission_factor, carbon_emission_unit):
    self._machine_id = machine_id
    self._name = name
    self._work_efficiency = work_efficiency
    self._work_efficiency_unit = work_efficiency_unit
    self._energy_consumption_rate = energy_consumption_rate
    self._energy_consumption_unit = energy_consumption_unit
    self._carbon_emission_factor = carbon_emission_factor
    self._carbon_emission_unit = carbon_emission_unit

  @property
  def id(self) -> int:
    """
    Get machine id
    :return: int
    """
    return self._machine_id

  @property
  def name(self) -> str:
    """
    Get machine name
    :return: str
    """
    return self._name

  @property
  def work_efficiency(self) -> float:
    """
    Get machine work efficiency
    :return: float
    """
    return self._work_efficiency

  @property
  def work_efficiency_unit(self) -> str:
    """
    Get machine work efficiency unit
    :return: str
    """
    return self._work_efficiency_unit

  @property
  def energy_consumption_rate(self) -> float:
    """
    Get energy consumption rate
    :return: float
    """
    return self._energy_consumption_rate

  @property
  def energy_consumption_unit(self) -> str:
    """
    Get energy consumption unit
    :return: str
    """
    return self._energy_consumption_unit

  @property
  def carbon_emission_factor(self) -> float:
    """
    Get carbon emission factor
    :return: float
    """
    return self._carbon_emission_factor

  @property
  def carbon_emission_unit(self) -> str:
    """
    Get carbon emission unit
    :return: str
    """
    return self._carbon_emission_unit
