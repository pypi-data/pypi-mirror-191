"""
Usage helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import sys
import hub.helpers.constants as cte
from typing import Dict


class UsageHelper:
  """
  Usage helper class
  """
  _nrcan_schedule_type_to_hub_schedule_type = {
    'Lighting': cte.LIGHTING,
    'Occupancy': cte.OCCUPANCY,
    'Equipment': cte.APPLIANCES,
    'Thermostat Setpoint Cooling': cte.COOLING_SET_POINT,  # Compose 'Thermostat Setpoint' + 'Cooling'
    'Thermostat Setpoint Heating': cte.HEATING_SET_POINT,  # Compose 'Thermostat Setpoint' + 'Heating'
    'Fan': cte.HVAC_AVAILABILITY
  }
  _nrcan_data_type_to_hub_data_type = {
    'FRACTION': cte.FRACTION,
    'ON_OFF': cte.ON_OFF,
    'TEMPERATURE': cte.ANY_NUMBER
  }

  _nrcan_time_to_hub_time = {
    'Hourly': cte.HOUR,
    'Constant': cte.CONSTANT
  }

  _nrcan_day_type_to_hub_days = {
    'Default|Wkdy': [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY],
    'Sun|Hol': [cte.SUNDAY, cte.HOLIDAY],
    'Sat': [cte.SATURDAY],
    'Default|WntrDsn|SmrDsn': [cte.MONDAY,
                               cte.TUESDAY,
                               cte.WEDNESDAY,
                               cte.THURSDAY,
                               cte.FRIDAY,
                               cte.SATURDAY,
                               cte.SUNDAY,
                               cte.HOLIDAY,
                               cte.WINTER_DESIGN_DAY,
                               cte.SUMMER_DESIGN_DAY],
    'Default': [cte.MONDAY,
                cte.TUESDAY,
                cte.WEDNESDAY,
                cte.THURSDAY,
                cte.FRIDAY,
                cte.SATURDAY,
                cte.SUNDAY,
                cte.HOLIDAY,
                cte.WINTER_DESIGN_DAY,
                cte.SUMMER_DESIGN_DAY]

  }

  _comnet_days = [cte.MONDAY,
                  cte.TUESDAY,
                  cte.WEDNESDAY,
                  cte.THURSDAY,
                  cte.FRIDAY,
                  cte.SATURDAY,
                  cte.SUNDAY,
                  cte.HOLIDAY]

  _comnet_data_type_to_hub_data_type = {
    'Fraction': cte.FRACTION,
    'OnOff': cte.ON_OFF,
    'Temperature': cte.ANY_NUMBER
  }

  _comnet_schedules_key_to_comnet_schedules = {
    'C-1 Assembly': 'C-1 Assembly',
    'C-2 Public': 'C-2 Health',
    'C-3 Hotel Motel': 'C-3 Hotel',
    'C-4 Manufacturing': 'C-4 Manufacturing',
    'C-5 Office': 'C-5 Office',
    'C-7 Restaurant': 'C-7 Restaurant',
    'C-8 Retail': 'C-8 Retail',
    'C-9 Schools': 'C-9 School',
    'C-10 Warehouse': 'C-10 Warehouse',
    'C-11 Laboratory': 'C-11 Lab',
    'C-12 Residential': 'C-12 Residential',
    'C-14 Gymnasium': 'C-14 Gymnasium'
  }

  @property
  def nrcan_day_type_to_hub_days(self):
    return self._nrcan_day_type_to_hub_days

  @property
  def nrcan_schedule_type_to_hub_schedule_type(self):
    return self._nrcan_schedule_type_to_hub_schedule_type

  @property
  def nrcan_data_type_to_hub_data_type(self):
    return self._nrcan_data_type_to_hub_data_type

  @property
  def nrcan_time_to_hub_time(self):
    return self._nrcan_time_to_hub_time

  @property
  def comnet_data_type_to_hub_data_type(self):
    return self._comnet_data_type_to_hub_data_type

  @property
  def comnet_schedules_key_to_comnet_schedules(self) -> Dict:
    return self._comnet_schedules_key_to_comnet_schedules

  @property
  def comnet_days(self):
    return self._comnet_days

  @staticmethod
  def schedules_key(usage):
    """
    Get Comnet schedules key from the list found in the Comnet usage file
    :param usage: str
    :return: str
    """
    try:
      return UsageHelper._comnet_schedules_key_to_comnet_schedules[usage]
    except KeyError:
      sys.stderr.write('Error: Comnet keyword not found. An update of the Comnet files might have been '
                       'done changing the keywords.\n')
