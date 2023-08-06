"""
DatWeatherParameters class to extract weather parameters from a defined region in .dat format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import sys
from pathlib import Path
import pandas as pd
import hub.helpers.constants as cte


class DatWeatherParameters:
  """
  DatWeatherParameters class
  """

  def __init__(self, city, path):
    self._weather_values = None
    self._city = city
    self._city_name = city.climate_reference_city
    file_name = 'inseldb_' + self._city_name + '.dat'
    self._path = Path(path / file_name)

    if self._weather_values is None:
      try:
        self._weather_values = pd.read_csv(self._path, sep=r'\s+', header=None,
                                           names=['hour', 'global_horiz', 'temperature', 'diffuse', 'beam', 'empty'])
      except SystemExit:
        sys.stderr.write(f'Error: weather file {self._path} not found\n')
        sys.exit()

    for building in self._city.buildings:
      new_value = pd.DataFrame(self._weather_values[['temperature']].to_numpy(), columns=['inseldb'])
      if cte.HOUR not in building.external_temperature:
        building.external_temperature[cte.HOUR] = new_value
      else:
        pd.concat([building.external_temperature[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['global_horiz']].to_numpy(), columns=['inseldb'])
      if cte.HOUR not in building.global_horizontal:
        building.global_horizontal[cte.HOUR] = new_value
      else:
        pd.concat([building.global_horizontal[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['diffuse']].to_numpy(), columns=['inseldb'])
      if cte.HOUR not in building.diffuse:
        building.diffuse[cte.HOUR] = new_value
      else:
        pd.concat([building.diffuse[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['beam']].to_numpy(), columns=['inseldb'])
      if cte.HOUR not in building.beam:
        building.beam[cte.HOUR] = new_value
      else:
        pd.concat([building.beam[cte.HOUR], new_value], axis=1)
