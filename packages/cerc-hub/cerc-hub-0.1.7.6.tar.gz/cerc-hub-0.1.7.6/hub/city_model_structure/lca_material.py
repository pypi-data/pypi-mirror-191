"""
LCA Material module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder atiya.atiya@mail.concordia.ca
"""

from typing import Union

class LcaMaterial:
  def __init__(self):
    self._id = None
    self._type = None
    self._name = None
    self._density = None
    self._density_unit = None
    self._embodied_carbon = None
    self._embodied_carbon_unit = None
    self._recycling_ratio = None
    self._company_recycling_ratio = None
    self._onsite_recycling_ratio = None
    self._landfilling_ratio = None
    self._cost = None
    self._cost_unit = None

  @property
  def id(self):
    """
    Get material id
    :return: int
    """
    return self._id

  @id.setter
  def id(self, value):
    """
    Set material id
    :param value: int
    """
    self._id = int(value)

  @property
  def type(self):
    """
    Get material type
    :return: str
    """
    return self._type

  @type.setter
  def type(self, value):
    """
    Set material type
    :param value: string
    """
    self._type = str(value)

  @property
  def name(self):
    """
    Get material name
    :return: str
    """
    return self._name

  @name.setter
  def name(self, value):
    """
    Set material name
    :param value: string
    """
    self._name = str(value)

  @property
  def density(self) -> Union[None, float]:
    """
    Get material density in kg/m3
    :return: None or float
    """
    return self._density

  @density.setter
  def density(self, value):
    """
    Set material density
    :param value: float
    """
    if value is not None:
      self._density = float(value)

  @property
  def density_unit(self) -> Union[None, str]:
    """
    Get material density unit
    :return: None or string
    """
    return self._density_unit

  @density_unit.setter
  def density_unit(self, value):
    """
    Set material density unit
    :param value: string
    """
    if value is not None:
      self._density_unit = str(value)

  @property
  def embodied_carbon(self) -> Union[None, float]:
    """
    Get material embodied carbon
    :return: None or float
    """
    return self._embodied_carbon

  @embodied_carbon.setter
  def embodied_carbon(self, value):
    """
    Set material embodied carbon
    :param value: float
    """
    if value is not None:
      self._embodied_carbon = float(value)

  @property
  def embodied_carbon_unit(self) -> Union[None, str]:
    """
    Get material embodied carbon unit
    :return: None or string
    """
    return self._embodied_carbon

  @embodied_carbon_unit.setter
  def embodied_carbon_unit(self, value):
    """
    Set material embodied carbon unit
    :param value: string
    """
    if value is not None:
      self._embodied_carbon_unit = str(value)

  @property
  def recycling_ratio(self) -> Union[None, float]:
    """
    Get material recycling ratio
    :return: None or float
    """
    return self._recycling_ratio

  @recycling_ratio.setter
  def recycling_ratio(self, value):
    """
    Set material recycling ratio
    :param value: float
    """
    if value is not None:
      self._recycling_ratio = float(value)

  @property
  def onsite_recycling_ratio(self) -> Union[None, float]:
    """
    Get material onsite recycling ratio
    :return: None or float
    """
    return self._onsite_recycling_ratio

  @onsite_recycling_ratio.setter
  def onsite_recycling_ratio(self, value):
    """
    Set material onsite recycling ratio
    :param value: float
    """
    if value is not None:
      self._onsite_recycling_ratio = float(value)

  @property
  def company_recycling_ratio(self) -> Union[None, float]:
    """
    Get material company recycling ratio
    :return: None or float
    """
    return self._company_recycling_ratio

  @company_recycling_ratio.setter
  def company_recycling_ratio(self, value):
    """
    Set material company recycling ratio
    :param value: float
    """
    if value is not None:
      self._company_recycling_ratio = float(value)

  @property
  def landfilling_ratio(self) -> Union[None, float]:
    """
    Get material landfilling ratio
    :return: None or float
    """
    return self._landfilling_ratio

  @landfilling_ratio.setter
  def landfilling_ratio(self, value):
    """
    Set material landfilling ratio
    :param value: float
    """
    if value is not None:
      self._landfilling_ratio = float(value)

  @property
  def cost(self) -> Union[None, float]:
    """
    Get material cost
    :return: None or float
    """
    return self._cost

  @cost.setter
  def cost(self, value):
    """
    Set material cost
    :param value: float
    """
    if value is not None:
      self._cost = float(value)

  @property
  def cost_unit(self) -> Union[None, str]:
    """
    Get material cost unit
    :return: None or string
    """
    return self._cost_unit

  @cost_unit.setter
  def cost_unit(self, value):
    """
    Set material cost unit
    :param value: string
    """
    if value is not None:
      self._cost_unit = float(value)
