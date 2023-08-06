"""
EnergySystemsFactory exports energy systems into several formats
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from pathlib import Path
from hub.exports.energy_systems.air_source_hp_export import AirSourceHPExport
from hub.exports.energy_systems.water_to_water_hp_export import WaterToWaterHPExport


class EnergySystemsExportFactory:
  """
  Exports factory class for energy systems
  """

  def __init__(self, city, user_input, hp_model, output_path, sim_type=0, data_type='heat', base_path=None,
               demand_path=None):
    """

    :param city: the city object
    :param user_input: user provided input from UI
    :param hp_model: the heat pump model to run
    :param output_path: the file to hold simulation results
    :param sim_type: the simulation type, 0 for series 1 for parallel
    :param data_type: indicates whether cooling or heating data is used
    :param base_path: the data directory of energy systems
    :param demand_path: path to hourly energy dempand file
    """

    self._city = city
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/energy_systems')
    self._base_path = base_path
    self._user_input = user_input
    self._hp_model = hp_model
    self._data_type = data_type
    self._output_path = output_path
    self._sim_type = sim_type
    self._demand_path = demand_path

  def _export_heat_pump(self, source):
    """
    Exports heat pump performance data as coefficients
    of some objective function
    :return: None
    """
    if source == 'air':
      return AirSourceHPExport(self._base_path, self._city, self._output_path, self._sim_type, self._demand_path)\
        .execute_insel(self._user_input, self._hp_model, self._data_type)
    elif source == 'water':
      return WaterToWaterHPExport(self._base_path, self._city, self._output_path, self._sim_type, self._demand_path)\
        .execute_insel(self._user_input, self._hp_model)

  def export(self, source='air'):
    """
    Export the city given to the class using the given export type handler
    :return: None
    """
    return getattr(self, '_export_heat_pump', lambda: None)(source)
