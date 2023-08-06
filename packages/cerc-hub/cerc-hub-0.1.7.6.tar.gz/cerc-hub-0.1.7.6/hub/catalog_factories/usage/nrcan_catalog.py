"""
NRCAN usage catalog
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import json
import urllib.request
import xmltodict

import hub.helpers.constants as cte
from hub.catalog_factories.catalog import Catalog
from hub.catalog_factories.data_models.usages.appliances import Appliances
from hub.catalog_factories.data_models.usages.content import Content
from hub.catalog_factories.data_models.usages.lighting import Lighting
from hub.catalog_factories.data_models.usages.ocupancy import Occupancy
from hub.catalog_factories.data_models.usages.schedule import Schedule
from hub.catalog_factories.data_models.usages.thermal_control import ThermalControl
from hub.catalog_factories.data_models.usages.usage import Usage
from hub.catalog_factories.usage.usage_helper import UsageHelper


class NrcanCatalog(Catalog):
  def __init__(self, path):
    path = str(path / 'nrcan.xml')
    self._content = None
    self._schedules = {}
    with open(path) as xml:
      self._metadata = xmltodict.parse(xml.read())
    self._base_url = self._metadata['nrcan']['@base_url']
    self._load_schedules()
    self._content = Content(self._load_archetypes())

  @staticmethod
  def _extract_schedule(raw):
    nrcan_schedule_type = raw['category']
    if 'Heating' in raw['name']:
      nrcan_schedule_type = f'{nrcan_schedule_type} Heating'
    elif 'Cooling' in raw['name']:
      nrcan_schedule_type = f'{nrcan_schedule_type} Cooling'
    if nrcan_schedule_type not in UsageHelper().nrcan_schedule_type_to_hub_schedule_type:
      return None
    hub_type = UsageHelper().nrcan_schedule_type_to_hub_schedule_type[nrcan_schedule_type]
    data_type = UsageHelper().nrcan_data_type_to_hub_data_type[raw['units']]
    time_step = UsageHelper().nrcan_time_to_hub_time[raw['type']]
    # nrcan only uses yearly range for the schedules
    time_range = cte.YEAR
    day_types = UsageHelper().nrcan_day_type_to_hub_days[raw['day_types']]
    return Schedule(hub_type, raw['values'], data_type, time_step, time_range, day_types)

  def _load_schedules(self):
    usage = self._metadata['nrcan']
    url = f'{self._base_url}{usage["schedules_location"]}'
    _schedule_types = []
    with urllib.request.urlopen(url) as json_file:
      schedules_type = json.load(json_file)
    for schedule_type in schedules_type['tables']['schedules']['table']:
      schedule = NrcanCatalog._extract_schedule(schedule_type)
      if schedule_type['name'] not in _schedule_types:
        _schedule_types.append(schedule_type['name'])
        if schedule is not None:
          self._schedules[schedule_type['name']] = [schedule]
      else:
        if schedule is not None:
          _schedules = self._schedules[schedule_type['name']]
          _schedules.append(schedule)
          self._schedules[schedule_type['name']] = _schedules

  def _get_schedules(self, name):
    if name in self._schedules:
      return self._schedules[name]

  def _load_archetypes(self):
    usages = []
    name = self._metadata['nrcan']
    url = f'{self._base_url}{name["space_types_location"]}'
    with urllib.request.urlopen(url) as json_file:
      space_types = json.load(json_file)['tables']['space_types']['table']
#    space_types = [st for st in space_types if st['building_type'] == 'Space Function']
    space_types = [st for st in space_types if st['space_type'] == 'WholeBuilding']
    for space_type in space_types:
#      usage_type = space_type['space_type']
      usage_type = space_type['building_type']
      occupancy_schedule_name = space_type['occupancy_schedule']
      lighting_schedule_name = space_type['lighting_schedule']
      appliance_schedule_name = space_type['electric_equipment_schedule']
      hvac_schedule_name = space_type['exhaust_schedule']
      if 'FAN' in hvac_schedule_name:
        hvac_schedule_name = hvac_schedule_name.replace('FAN', 'Fan')
      heating_setpoint_schedule_name = space_type['heating_setpoint_schedule']
      cooling_setpoint_schedule_name = space_type['cooling_setpoint_schedule']
      occupancy_schedule = self._get_schedules(occupancy_schedule_name)
      lighting_schedule = self._get_schedules(lighting_schedule_name)
      appliance_schedule = self._get_schedules(appliance_schedule_name)
      heating_schedule = self._get_schedules(heating_setpoint_schedule_name)
      cooling_schedule = self._get_schedules(cooling_setpoint_schedule_name)
      hvac_availability = self._get_schedules(hvac_schedule_name)

      occupancy_density = space_type['occupancy_per_area']

      # ACH
      mechanical_air_change = space_type['ventilation_air_changes']
      # cfm/ft2 to m3/m2.s
      ventilation_rate = space_type['ventilation_per_area'] / (cte.METERS_TO_FEET * cte.MINUTES_TO_SECONDS)
      if ventilation_rate == 0:
        # cfm/person to m3/m2.s
        ventilation_rate = space_type['ventilation_per_person'] / occupancy_density\
                           / (cte.METERS_TO_FEET * cte.MINUTES_TO_SECONDS)

      # W/sqft to W/m2
      lighting_density = space_type['lighting_per_area'] * cte.METERS_TO_FEET * cte.METERS_TO_FEET
      lighting_radiative_fraction = space_type['lighting_fraction_radiant']
      lighting_convective_fraction = 0
      if lighting_radiative_fraction is not None:
        lighting_convective_fraction = 1 - lighting_radiative_fraction
      lighting_latent_fraction = 0
      # W/sqft to W/m2
      appliances_density = space_type['electric_equipment_per_area'] * cte.METERS_TO_FEET * cte.METERS_TO_FEET
      appliances_radiative_fraction = space_type['electric_equipment_fraction_radiant']
      appliances_latent_fraction = space_type['electric_equipment_fraction_latent']
      appliances_convective_fraction = 0
      if appliances_radiative_fraction is not None and appliances_latent_fraction is not None:
        appliances_convective_fraction = 1 - appliances_radiative_fraction - appliances_latent_fraction

      occupancy = Occupancy(occupancy_density,
                            None,
                            None,
                            None,
                            occupancy_schedule)
      lighting = Lighting(lighting_density,
                          lighting_convective_fraction,
                          lighting_radiative_fraction,
                          lighting_latent_fraction,
                          lighting_schedule)
      appliances = Appliances(appliances_density,
                              appliances_convective_fraction,
                              appliances_radiative_fraction,
                              appliances_latent_fraction,
                              appliance_schedule)
      thermal_control = ThermalControl(None,
                                       None,
                                       None,
                                       hvac_availability,
                                       heating_schedule,
                                       cooling_schedule)
      hours_day = None
      days_year = None
      usages.append(Usage(usage_type,
                          hours_day,
                          days_year,
                          mechanical_air_change,
                          ventilation_rate,
                          occupancy,
                          lighting,
                          appliances,
                          thermal_control))
    return usages

  def names(self, category=None):
    """
    Get the catalog elements names
    :parm: for usage catalog category filter does nothing as there is only one category (usages)
    """
    _names = {'usages': []}
    for usage in self._content.usages:
      _names['usages'].append(usage.name)
    return _names

  def entries(self, category=None):
    """
    Get the catalog elements
    :parm: for usage catalog category filter does nothing as there is only one category (usages)
    """
    return self._content

  def get_entry(self, name):
    """
    Get one catalog element by names
    :parm: entry name
    """
    for usage in self._content.usages:
      if usage.name.lower() == name.lower():
        return usage
    raise IndexError(f"{name} doesn't exists in the catalog")
