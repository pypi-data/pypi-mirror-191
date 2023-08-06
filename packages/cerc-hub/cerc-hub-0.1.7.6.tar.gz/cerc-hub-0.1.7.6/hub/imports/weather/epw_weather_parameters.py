"""
EpwWeatherParameters class to extract weather parameters from a defined region in .epw format (EnergyPlus Weather)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import sys
from pathlib import Path
import pandas as pd
import hub.helpers.constants as cte
from hub.imports.weather.helpers.weather import Weather as wh


class EpwWeatherParameters:
  """
  EpwWeatherParameters class
  """
  def __init__(self, city, path, file_name):
    self._weather_values = None
    self._city = city
    self._path = Path(path / file_name)

    try:
      file = open(self._path, 'r')
      line = file.readline().split(',')
      city.climate_reference_city = line[1]
      city.latitude = line[6]
      city.longitude = line[7]
      city.time_zone = line[8]
      for i in range(0, 2):
        _ = file.readline().split(',')
      line = file.readline().split(',')
      number_records = int(line[1])
      depth_measurement_ground_temperature = []
      ground_temperature = []
      for i in range(0, number_records):
        depth_measurement_ground_temperature.append(line[i*16+2])
        temperatures = []
        for j in range(0, 12):
          temperatures.append(line[i*16+j+6])
        ground_temperature.append(temperatures)
      file.close()
    except SystemExit:
      sys.stderr.write(f'Error: weather file {self._path} not found. Please download it from '
                       f'https://energyplus.net/weather and place it in folder data\\weather\\epw\n')
      sys.exit()

    try:
      self._weather_values = pd.read_csv(self._path, header=0, skiprows=7,
                                         names=['year', 'month', 'day', 'hour', 'minute',
                                                'data_source_and_uncertainty_flags',
                                                'dry_bulb_temperature_c', 'dew_point_temperature_c',
                                                'relative_humidity_perc',
                                                'atmospheric_station_pressure_pa',
                                                'extraterrestrial_horizontal_radiation_wh_m2',
                                                'extraterrestrial_direct_normal_radiation_wh_m2',
                                                'horizontal_infrared_radiation_intensity_wh_m2',
                                                'global_horizontal_radiation_wh_m2', 'direct_normal_radiation_wh_m2',
                                                'diffuse_horizontal_radiation_wh_m2',
                                                'global_horizontal_illuminance_lux',
                                                'direct_normal_illuminance_lux', 'diffuse_horizontal_illuminance_lux',
                                                'zenith_luminance_cd_m2',
                                                'wind_direction_deg', 'wind_speed_m_s', 'total_sky_cover',
                                                'opaque_sky_cover', 'visibility_km',
                                                'ceiling_heigh_m_s', 'present_weather_observation',
                                                'present_weather_codes',
                                                'precipitable_water_mm', 'aerosol_optical_depth_10_3_ths',
                                                'snow_depth_cm',
                                                'days_since_last_snowfall', 'albedo', 'liquid_precipitation_depth_mm',
                                                'liquid_precipitation_quality_hr'])
    except SystemExit:
      sys.stderr.write(f'Error: wrong formatting of weather file {self._path}\n')
      sys.exit()

    for building in self._city.buildings:
      if cte.HOUR in building.external_temperature:
        del building.external_temperature[cte.HOUR]
      new_value = pd.DataFrame(self._weather_values[['dry_bulb_temperature_c']].to_numpy(), columns=['epw'])
      number_invalid_records = new_value[new_value.epw == 99.9].count().epw
      if number_invalid_records > 0:
        sys.stderr.write(f'Warning: {self._path} invalid records (value of 99.9) in dry bulb temperature\n')
      if cte.HOUR not in building.external_temperature:
        building.external_temperature[cte.HOUR] = new_value
      else:
        pd.concat([building.external_temperature[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['global_horizontal_radiation_wh_m2']].to_numpy(), columns=['epw'])
      number_invalid_records = new_value[new_value.epw == 9999].count().epw
      if number_invalid_records > 0:
        sys.stderr.write(f'Warning: {self._path} invalid records (value of 9999) in global horizontal radiation\n')
      if cte.HOUR not in building.global_horizontal:
        building.global_horizontal[cte.HOUR] = new_value
      else:
        pd.concat([building.global_horizontal[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['diffuse_horizontal_radiation_wh_m2']].to_numpy(), columns=['epw'])
      number_invalid_records = new_value[new_value.epw == 9999].count().epw
      if number_invalid_records > 0:
        sys.stderr.write(f'Warning: {self._path} invalid records (value of 9999) in diffuse horizontal radiation\n')
      if cte.HOUR not in building.diffuse:
        building.diffuse[cte.HOUR] = new_value
      else:
        pd.concat([building.diffuse[cte.HOUR], new_value], axis=1)

      new_value = pd.DataFrame(self._weather_values[['direct_normal_radiation_wh_m2']].to_numpy(), columns=['epw'])
      number_invalid_records = new_value[new_value.epw == 9999].count().epw
      if number_invalid_records > 0:
        sys.stderr.write(f'Warning: {self._path} invalid records (value of 9999) in direct horizontal radiation\n')
      if cte.HOUR not in building.beam:
        building.beam[cte.HOUR] = new_value
      else:
        pd.concat([building.beam[cte.HOUR], new_value], axis=1)
    # create the monthly and yearly values out of the hourly
    for building in self._city.buildings:
      if cte.MONTH not in building.external_temperature:
        building.external_temperature[cte.MONTH] = wh().get_monthly_mean_values(building.external_temperature[cte.HOUR][['epw']])
      if cte.YEAR not in building.external_temperature:
        building.external_temperature[cte.YEAR] = wh(). get_yearly_mean_values(building.external_temperature[cte.HOUR][['epw']])
    self._city.level_of_detail.weather = 2
