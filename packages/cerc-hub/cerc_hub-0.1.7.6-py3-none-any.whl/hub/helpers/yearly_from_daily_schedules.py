"""
Yearly from daily schedules module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import calendar as cal
import hub.helpers.constants as cte
from hub.city_model_structure.attributes.schedule import Schedule


class YearlyFromDailySchedules:
  """
  YearlyFromDailySchedules class
  """
  def __init__(self, daily_schedules, year):
    self._daily_schedules = daily_schedules
    self._year = year

  @property
  def yearly_schedule(self) -> Schedule:
    """
    Creates a yearly schedule out of a set of daily schedules
    :return: Schedule
    """
    yearly_schedule = Schedule()
    weekly_schedules = [0, 0, 0, 0, 0, 0, 0]
    day_types = dict({cte.MONDAY: 0, cte.TUESDAY: 1, cte.WEDNESDAY: 2, cte.THURSDAY: 3,
                      cte.FRIDAY: 4, cte.SATURDAY: 5, cte.SUNDAY: 6})
    for daily_schedule in self._daily_schedules:
      for day_type in daily_schedule.day_types:
        weekly_schedules[day_types[day_type]] = daily_schedule.values

    values = []
    for month in range(1, 13):
      _, number_days = cal.monthrange(self._year, month)
      for day in range(1, number_days+1):
        week_day = cal.weekday(self._year, month, day)
        values.extend(weekly_schedules[week_day])
    yearly_schedule.type = self._daily_schedules[0].type
    yearly_schedule.data_type = self._daily_schedules[0].data_type
    yearly_schedule.time_range = cte.YEAR
    yearly_schedule.time_step = cte.HOUR
    yearly_schedule.values = values

    return yearly_schedule
