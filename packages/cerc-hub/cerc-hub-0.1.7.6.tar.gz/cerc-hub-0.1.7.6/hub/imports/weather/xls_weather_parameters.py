"""
XlsWeatherParameters class to extract weather parameters from a defined region in .xls format
defined and used by the norm iso 52016-1:2017
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import sys
from pathlib import Path
import pandas as pd
import hub.helpers.constants as cte


class XlsWeatherParameters:
  """
  XlsWeatherParameters class
  """
  def __init__(self, city, path, name):
    self._weather_values = None
    self._city = city
    self._file_name = name
    file_name = self._file_name + '.xls'
    self._path = Path(path / file_name)

    if self._weather_values is None:
      try:
        self._weather_values = pd.read_excel(self._path, skiprows=4, nrows=9504,
                                             names=['hours_calc', 'month', 'week', 'day_of_week', 'hours_of_day',
                                                    'temperature', 'I_sol_vertical_N', 'I_sol_vertical_E',
                                                    'I_sol_vertical_S', 'I_sol_vertical_W', 'I_sol_45_N', 'I_sol_45_S',
                                                    'void', 'global_horiz', 'wind_velocity', 'humidity'])
      except SystemExit:
        sys.stderr.write(f'Error reading weather file {self._path}\n')
        sys.exit()

    for building in self._city.buildings:
      new_value = pd.DataFrame(self._weather_values[['temperature']].to_numpy(), columns=['iso52016'])
      if cte.HOUR not in building.external_temperature:
        building.external_temperature[cte.HOUR] = new_value
      else:
        pd.concat([building.external_temperature[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['global_horiz']].to_numpy(), columns=['iso52016'])
      if cte.HOUR not in building.global_horizontal:
        building.global_horizontal[cte.HOUR] = new_value
      else:
        pd.concat([building.global_horizontal[cte.HOUR], new_value], axis=1)
