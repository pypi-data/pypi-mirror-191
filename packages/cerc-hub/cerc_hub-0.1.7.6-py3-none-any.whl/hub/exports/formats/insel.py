"""
Insel export models to insel format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from abc import ABC


class Insel(ABC):
  def __init__(self, city, path):
    self._city = city
    self._path = path
    self._results = None

  @staticmethod
  def _add_block(file, block_number, block_type, inputs='', parameters=''):
    file += "S " + str(block_number) + " " + block_type + "\n"
    for block_input in inputs:
      file += str(block_input) + "\n"
    if len(parameters) > 0:
      file += "P " + str(block_number) + "\n"
    for block_parameter in parameters:
      file += str(block_parameter) + "\n"
    return file

  def _export(self):
    raise NotImplementedError
