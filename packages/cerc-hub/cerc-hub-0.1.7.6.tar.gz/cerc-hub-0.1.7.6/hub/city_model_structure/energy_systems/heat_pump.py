"""
heat_pump module defines a heat pump
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""


class HeatPump:
  """
  HeatPump class
  """

  def __init__(self):
    self._model = None

  @property
  def model(self) -> str:
    """
    Get model name
    :return: str
    """
    return self._model

  @model.setter
  def model(self, value):
    """
    Set model (name, indicated in capacity)
    :param value: str
    """
    if self._model is None:
      self._model = value
