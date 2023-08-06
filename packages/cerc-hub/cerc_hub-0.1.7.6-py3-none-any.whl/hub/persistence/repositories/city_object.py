"""
City Object repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

import datetime
from typing import Union, Dict

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from hub.hub_logger import logger
from hub.persistence import Repository
from hub.persistence.models import CityObject as Model
from hub.city_model_structure.building import Building


class CityObject(Repository):
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(CityObject, cls).__new__(cls)
    return cls._instance

  def insert(self, city_id:int, building: Building) -> Union[Model, Dict]:
    """
    Inserts a new city object
    :param city_id: city id for the city owning this city object
    :param building: the city object (only building for now) to be inserted
    return CityObject model and dictionary
    """
    city_object = self.get_by_name_and_city(building.name, city_id)
    if city_object is None:
      try:
        object_usage = ''
        for internal_zone in building.internal_zones:
          for usage in internal_zone.usages:
            object_usage = f'{object_usage}{usage.name}_{usage.percentage} '
        object_usage = object_usage.rstrip()
        city_object = Model(city_id=city_id,
                            name=building.name,
                            alias=building.alias,
                            object_type=building.type,
                            year_of_construction=building.year_of_construction,
                            function=building.function,
                            usage=object_usage,
                            volume=building.volume,
                            area=building.floor_area)
        self.session.add(city_object)
        self.session.flush()
        self.session.commit()
        return city_object
      except SQLAlchemyError as err:
        logger.error(f'An error occurred while creating city_object: {err}')
    else:
      return {'message': f'A city_object named {building.name} already exists in that city'}

  def update(self,city_id: int, building: Building) -> Union[Dict, None]:
    """
    Updates an application
    :param city_id: the city id of the city owning the city object
    :param building: the city object
    :return:
    """
    try:
      object_usage = ''
      for internal_zone in building.internal_zones:
        for usage in internal_zone.usages:
          object_usage = f'{object_usage}{usage.name}_{usage.percentage} '
      object_usage = object_usage.rstrip()
      self.session.query(Model).filter(Model.name == building.name, Model.city_id == city_id).update(
        {'name': building.name,
         'alias': building.alias,
         'object_type': building.type,
         'year_of_construction': building.year_of_construction,
         'function': building.function,
         'usage': object_usage,
         'volume': building.volume,
         'area': building.floor_area,
         'updated': datetime.datetime.utcnow()})
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while updating city object: {err}')
      return {'message': 'Error occurred while updating application'}

  def delete(self, city_id: int, name: str):
    """
    Deletes an application with the application_uuid
    :param city_id: The id for the city owning the city object
    :param name: The city object name
    :return: None
    """
    try:
      self.session.query(Model).filter(Model.city_id == city_id, Model.name == name).delete()
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while deleting application: {err}')

  def get_by_name_and_city(self, name, city_id) -> [Model]:
    """
    Fetch a city object based on name and city id
    :param name: city object name
    :param city_id: a city identifier
    :return: [CityObject] with the provided name belonging to the city with id city_id
    """
    try:
      _city_object = self.session.execute(select(Model).where(
        Model.name == name, Model.city_id == city_id
      )).first()
      if _city_object is None:
        return None
      return _city_object[0]
    except SQLAlchemyError as err:
      print(err)
      logger.error(f'Error while fetching application by application_uuid: {err}')
