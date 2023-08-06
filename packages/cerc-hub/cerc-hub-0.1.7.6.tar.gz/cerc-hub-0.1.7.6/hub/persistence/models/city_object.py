"""
Model representation of a city object
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

import datetime

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Float
from sqlalchemy import DateTime
from hub.persistence.configuration import Models

class CityObject(Models):
  """
  A model representation of an application
  """
  __tablename__ = 'city_object'
  id = Column(Integer, Sequence('city_object_id_seq'), primary_key=True)
  city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
  name = Column(String, nullable=False)
  alias = Column(String, nullable=True)
  type = Column(String, nullable=False)
  year_of_construction = Column(Integer, nullable=True)
  function = Column(String, nullable=True)
  usage = Column(String, nullable=True)
  volume = Column(Float, nullable=False)
  area = Column(Float, nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, city_id, name, alias, object_type, year_of_construction, function, usage, volume, area):
    self.city_id = city_id
    self.name = name
    self.alias = alias
    self.type = object_type
    self.year_of_construction = year_of_construction
    self.function = function
    self.usage = usage
    self.volume = volume
    self.area = area
