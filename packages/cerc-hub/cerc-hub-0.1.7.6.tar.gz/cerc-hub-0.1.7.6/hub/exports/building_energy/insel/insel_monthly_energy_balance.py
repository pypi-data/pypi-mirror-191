"""
InselMonthlyEnergyBalance exports models to insel format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import numpy as np
from pathlib import Path

from hub.exports.formats.insel import Insel
from hub.imports.weather.helpers.weather import Weather
import hub.helpers.constants as cte

_CONSTRUCTION_CODE = {
    cte.WALL: '1',
    cte.GROUND: '2',
    cte.ROOF: '3',
    cte.INTERIOR_WALL: '5',
    cte.GROUND_WALL: '6',
    cte.ATTIC_FLOOR: '7',
    cte.INTERIOR_SLAB: '8'
  }


class InselMonthlyEnergyBalance(Insel):

  def __init__(self, city, path, radiation_calculation_method='sra', weather_format='epw'):
    super().__init__(city, path)
    self._radiation_calculation_method = radiation_calculation_method
    self._weather_format = weather_format
    self._contents = []
    self._insel_files_paths = []
    for building in city.buildings:
      self._insel_files_paths.append(building.name + '.insel')
      file_name_out = building.name + '.out'
      output_path = Path(self._path / file_name_out).resolve()
      self._contents.append(self.generate_meb_template(building, output_path, self._radiation_calculation_method,
                                                       self._weather_format))
    self._export()

  def _export(self):
    for i_file, content in enumerate(self._contents):
      file_name = self._insel_files_paths[i_file]
      with open(Path(self._path / file_name).resolve(), 'w') as insel_file:
        insel_file.write(content)
    return

  @staticmethod
  def generate_meb_template(building, insel_outputs_path, radiation_calculation_method, weather_format):
    file = ""
    i_block = 1
    parameters = ["1", "12", "1"]
    file = Insel._add_block(file, i_block, 'DO', parameters=parameters)

    i_block = 4
    inputs = ["1.1", "20.1", "21.1"]
    surfaces = building.surfaces
    for i in range(1, len(surfaces) + 1):
      inputs.append(f"{str(100 + i)}.1 % Radiation surface {str(i)}")

    # BUILDING PARAMETERS
    parameters = [f'{0.85 * building.volume} % BP(1) Heated Volume (m3)',
                  f'{building.average_storey_height} % BP(2) Average storey height (m)',
                  f'{building.storeys_above_ground} % BP(3) Number of storeys above ground',
                  f'{building.attic_heated} % BP(4) Attic heating type (0=no room, 1=unheated, 2=heated)',
                  f'{building.basement_heated} % BP(5) Cellar heating type (0=no room, 1=unheated, 2=heated, '
                  f'99=invalid)']

    # todo: this method and the insel model have to be reviewed for more than one internal zone
    internal_zone = building.internal_zones[0]
    thermal_zone = internal_zone.thermal_zones[0]
    parameters.append(f'{thermal_zone.indirectly_heated_area_ratio} % BP(6) Indirectly heated area ratio')
    parameters.append(f'{thermal_zone.effective_thermal_capacity / 3600} % BP(7) Effective heat capacity (Wh/m2K)')
    parameters.append(f'{thermal_zone.additional_thermal_bridge_u_value} '
                      f'% BP(8) Additional U-value for heat bridge (Wh/m2K)')
    parameters.append('1 % BP(9) Usage type (0=standard, 1=IWU)')

    # ZONES AND SURFACES
    parameters.append(f'{len(internal_zone.usages)} %  BP(10) Number of zones')

    for i, usage in enumerate(internal_zone.usages):
      percentage_usage = usage.percentage
      parameters.append(f'{float(internal_zone.area) * percentage_usage}  % BP(11) #1 Area of zone {i + 1} (m2)')
      total_internal_gain = 0
      for ig in usage.internal_gains:
        total_internal_gain += float(ig.average_internal_gain) * \
                                (float(ig.convective_fraction) + float(ig.radiative_fraction))
      parameters.append(f'{total_internal_gain} % BP(12) #2 Internal gains of zone {i + 1}')
      parameters.append(f'{usage.thermal_control.mean_heating_set_point} % BP(13) #3 Heating setpoint temperature '
                        f'zone {i + 1} (degree Celsius)')
      parameters.append(f'{usage.thermal_control.heating_set_back} % BP(14) #4 Heating setback temperature '
                        f'zone {i + 1} (degree Celsius)')
      parameters.append(f'{usage.thermal_control.mean_cooling_set_point} % BP(15) #5 Cooling setpoint temperature '
                        f'zone {i + 1} (degree Celsius)')
      parameters.append(f'{usage.hours_day} %  BP(16) #6 Usage hours per day zone {i + 1}')
      parameters.append(f'{usage.days_year} %  BP(17) #7 Usage days per year zone {i + 1}')
      parameters.append(f'{usage.mechanical_air_change} % BP(18) #8 Minimum air change rate zone {i + 1} (ACH)')

    parameters.append(f'{len(thermal_zone.thermal_boundaries)}  % Number of surfaces = BP(11+8z) \n'
                      f'% 1. Surface type (1=wall, 2=ground 3=roof, 4=flat roof)\n'
                      f'% 2. Areas above ground (m2)\n'
                      f'% 3. Areas below ground (m2)\n'
                      f'% 4. U-value (W/m2K)\n'
                      f'% 5. Window area (m2)\n'
                      f'% 6. Window frame fraction\n'
                      f'% 7. Window U-value (W/m2K)\n'
                      f'% 8. Window g-value\n'
                      f'% 9. Short-wave reflectance\n'
                      f'% #1     #2       #3      #4      #5     #6     #7     #8     #9\n')

    for thermal_boundary in thermal_zone.thermal_boundaries:
      type_code = _CONSTRUCTION_CODE[thermal_boundary.type]
      window_area = thermal_boundary.opaque_area * thermal_boundary.window_ratio / (1 - thermal_boundary.window_ratio)

      parameters.append(type_code)
      if thermal_boundary.type != cte.GROUND:
        parameters.append(thermal_boundary.opaque_area + window_area)
        parameters.append('0.0')
      else:
        parameters.append('0.0')
        parameters.append(thermal_boundary.opaque_area + window_area)
      parameters.append(thermal_boundary.u_value)
      parameters.append(window_area)

      if window_area <= 0.001:
        parameters.append(0.0)
        parameters.append(0.0)
        parameters.append(0.0)
      else:
        thermal_opening = thermal_boundary.thermal_openings[0]
        parameters.append(thermal_opening.frame_ratio)
        parameters.append(thermal_opening.overall_u_value)
        parameters.append(thermal_opening.g_value)
      if thermal_boundary.type is not cte.GROUND:
        parameters.append(thermal_boundary.parent_surface.short_wave_reflectance)
      else:
        parameters.append(0.0)

    file = Insel._add_block(file, i_block, 'd18599', inputs=inputs, parameters=parameters)

    i_block = 20
    inputs = ['1']
    parameters = ['12 % Monthly ambient temperature (degree Celsius)']

    external_temperature = building.external_temperature[cte.MONTH]

    for i in range(0, len(external_temperature)):
      parameters.append(f'{i + 1} {external_temperature.at[i, weather_format]}')

    file = Insel._add_block(file, i_block, 'polyg', inputs=inputs, parameters=parameters)

    i_block = 21
    inputs = ['1']
    parameters = ['12 % Monthly sky temperature']

    sky_temperature = Weather.sky_temperature(external_temperature[[weather_format]].to_numpy().T[0])
    for i, temperature in enumerate(sky_temperature):
      parameters.append(f'{i + 1} {temperature}')

    file = Insel._add_block(file, i_block, 'polyg', inputs=inputs, parameters=parameters)

    for i, surface in enumerate(surfaces):
      i_block = 101 + i
      inputs = ['1 % Monthly surface radiation (W/m2)']
      parameters = [f'12 % Azimuth {np.rad2deg(surface.azimuth)}, '
                    f'inclination {np.rad2deg(surface.inclination)} (degrees)']

      if surface.type != 'Ground':
        if cte.MONTH not in surface.global_irradiance:
          raise ValueError(f'surface: {surface.name} from building {building.name} has no global irradiance!')
        global_irradiance = surface.global_irradiance[cte.MONTH]
        for j in range(0, len(global_irradiance)):
          parameters.append(f'{j + 1} {global_irradiance.at[j, radiation_calculation_method]}')
      else:
        for j in range(0, 12):
          parameters.append(f'{j + 1} 0.0')

      file = Insel._add_block(file, i_block, 'polyg', inputs=inputs, parameters=parameters)

    i_block = 300 + len(surfaces)
    inputs = ['4.1', '4.2']
    file = Insel._add_block(file, i_block, 'cum', inputs=inputs)

    in_1 = f'{i_block}.1'
    in_2 = f'{i_block}.2'
    i_block = 303 + len(surfaces)
    inputs = [in_1, in_2]
    file = Insel._add_block(file, i_block, 'atend', inputs=inputs)

    i_block = 310 + len(surfaces)
    inputs = ['4.1', '4.2']
    parameters = ['1 % Mode',
                  '0 % Suppress FNQ inputs',
                  f"'{str(insel_outputs_path)}' % File name",
                  "'*' % Fortran format"]
    file = Insel._add_block(file, i_block, 'WRITE', inputs=inputs, parameters=parameters)

    return file
