"""
Concordia file report
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

import io
import json
from pathlib import Path
import pandas as pd


class ConcordiaFileReport:
  """
  Concordia file report for sensors base class
  """
  def __init__(self, city, end_point, base_path, db_file):
    self._city_object = []
    self._city_objects_cluster = []
    self._sensors = []
    self._sensor_point = {}
    self._city = city
    self._end_point = end_point
    self._sensor_database = base_path
    metadata = True
    content = False
    with open(Path(base_path / db_file).resolve()) as concordia_db:
      self._sensor_database = json.load(concordia_db)

    for city_object in self._sensor_database['sensors']:
      city_object_name = city_object['city_object']
      for sensor in city_object['sensors']:
        self._city_object.append(city_object_name)
        self._sensors.append(sensor)

    buffer = ""
    with open(end_point.resolve()) as data:
      for line in data:
        line = ConcordiaFileReport._clean_line(line)
        if metadata:
          fields = line.split(',')
          if len(fields) > 2:
            point = fields[0].replace(":", "")
            key = fields[1]
            if fields[1] in self._sensors:
              self._sensor_point[key] = point
        if "End of Report" in line:
          content = False
        if content:
          line = ConcordiaFileReport._merge_date_time(line)
          buffer = buffer + line + '\n'
        if line == '':
          metadata = False
          content = True
    measures = pd.read_csv(io.StringIO(buffer), sep=',')
    measures["Date time"] = pd.to_datetime(measures["Date time"])
    self._measures = ConcordiaFileReport._force_format(measures)

  @staticmethod
  def _clean_line(line):
    return line.replace('"', '').replace('\n', '')

  @staticmethod
  def _merge_date_time(line):
    fields = line.split(',')
    date = fields[0]
    time = fields[1]
    if '<>' in date:
      return line.replace(f'{date},{time}', 'Date time')
    date_fields = date.split('/')
    format_date_time = f'"{int(date_fields[2])}-{int(date_fields[0]):02d}-{int(date_fields[1]):02d} {time}"'
    return line.replace(f'{date},{time}', format_date_time)

  @staticmethod
  def _force_format(df):
    for head in df.head():
      if 'Date time' not in head:
        df = df.astype({head: 'float64'})
    return df
