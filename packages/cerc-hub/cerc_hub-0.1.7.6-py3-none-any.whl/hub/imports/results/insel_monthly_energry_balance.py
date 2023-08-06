"""
Insel monthly energy balance
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guillermo.GutierrezMorote@concordia.ca
"""

from pathlib import Path
import pandas as pd
import csv
import hub.helpers.constants as cte

class InselMonthlyEnergyBalance:
  """
  Import SRA results
  """
  def __init__(self, city, base_path):

    self._city = city
    self._base_path = base_path

  @staticmethod
  def _demand(insel_output_file_path):
    heating = []
    cooling = []
    with open(Path(insel_output_file_path).resolve()) as csv_file:
      csv_reader = csv.reader(csv_file)
      for line in csv_reader:
        demand = str(line).replace("['", '').replace("']", '').split()
        for i in range(0, 2):
          if demand[i] != 'NaN':
            aux = float(demand[i]) * 1000  # kWh to Wh
            demand[i] = str(aux)
          else:
            demand[i] = '0'
        heating.append(demand[0])
        cooling.append(demand[1])
    monthly_heating = pd.DataFrame(heating, columns=[cte.INSEL_MEB])
    monthly_cooling = pd.DataFrame(cooling, columns=[cte.INSEL_MEB])
    return monthly_heating, monthly_cooling

  def enrich(self):
    for building in self._city.buildings:
      file_name = building.name + '.out'
      insel_output_file_path = Path(self._base_path / file_name).resolve()
      if insel_output_file_path.is_file():
        building.heating[cte.MONTH], building.cooling[cte.MONTH] = self._demand(insel_output_file_path)
        building.heating[cte.YEAR] = pd.DataFrame(
          [building.heating[cte.MONTH][cte.INSEL_MEB].sum()], columns=[cte.INSEL_MEB]
        )
        building.cooling[cte.YEAR] = pd.DataFrame(
          [building.cooling[cte.MONTH][cte.INSEL_MEB].sum()], columns=[cte.INSEL_MEB]
        )
