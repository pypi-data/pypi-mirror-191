"""
weather helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import math
import hub.helpers.constants as cte
import pandas as pd
import calendar as cal
import numpy as np


class Weather:
  """
  Weather class
  """

  @staticmethod
  def sky_temperature(ambient_temperature):
    """
    Get sky temperature from ambient temperature in Celsius
    :return: float
    """
    # Swinbank - Source sky model approximation(1963) based on cloudiness statistics(32 %) in United States
    # ambient temperatures( in °C)
    # sky temperatures( in °C)
    values = []
    for temperature in ambient_temperature:
      value = 0.037536 * math.pow((temperature + cte.KELVIN), 1.5) \
              + 0.32 * (temperature + cte.KELVIN) - cte.KELVIN
      values.append(value)
    return values

  def get_monthly_mean_values(self, values):
    out = None
    if values is not None:
      if 'month' not in values.columns:
        values = pd.concat([self.month_hour, pd.DataFrame(values)], axis=1)
      out = values.groupby('month', as_index=False).mean()
      del out['month']
    return out

  def get_yearly_mean_values(self, values):
    return values.mean()

  def get_total_month(self, values):
    out = None
    if values is not None:
      if 'month' not in values.columns:
        values = pd.concat([self.month_hour, pd.DataFrame(values)], axis=1)
      out = pd.DataFrame(values).groupby('month', as_index=False).sum()
      del out['month']
    return out

  @property
  def month_hour(self):
    """
    returns a DataFrame that has x values of the month number (January = 1, February = 2...),
    being x the number of hours of the corresponding month
    :return: DataFrame(int)
    """
    array = []
    for i in range(0, 12):
      days_of_month = cal.monthrange(2015, i+1)[1]
      total_hours = days_of_month * 24
      array = np.concatenate((array, np.full(total_hours, i + 1)))
    return pd.DataFrame(array, columns=['month'])
