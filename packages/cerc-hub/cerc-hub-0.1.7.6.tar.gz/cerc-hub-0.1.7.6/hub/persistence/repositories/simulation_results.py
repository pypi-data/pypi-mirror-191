"""
Simulation results repository with database CRUD operations
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
from hub.persistence.models import SimulationResults as Model
from hub.persistence.models import City
from hub.persistence.models import CityObject

from hub.city_model_structure.building import Building


class SimulationResults(Repository):
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(SimulationResults, cls).__new__(cls)
    return cls._instance

  def insert(self, name: str, values: str, city_id=None, city_object_id=None) -> Union[Model, Dict]:
    """
    Inserts simulations results linked either with a city as a whole or with a city object
    :param name: results name
    :param values: the simulation results in json format
    :param city_id: optional city id
    :param city_object_id: optional city object id
    :return SimulationResults or Dictionary
    """
    if city_id is not None:
      city = self.get_city(city_id)
      if city is None:
        return {'message': f'City does not exists'}
    else:
      city_object = self.get_city_object(city_object_id)
      if city_object is None:
        return {'message': f'City object does not exists'}
    try:
      simulation_result = Model(name=name,
                                values=values,
                                city_id=city_id,
                                city_object_id=city_object_id)
      self.session.add(simulation_result)
      self.session.flush()
      self.session.commit()
      return simulation_result
    except SQLAlchemyError as err:
      logger.error(f'An error occurred while creating city_object: {err}')

  def update(self, name: str, values: str, city_id=None, city_object_id=None) -> Union[Dict, None]:
    """
    Updates simulation results for a city or a city object
    :param name: The simulation results tool and workflow name
    :param values: the simulation results in json format
    :param city_id: optional city id
    :param city_object_id: optional city object id
    :return: None or dictionary
    """
    try:
      if city_id is not None:
        self.session.query(Model).filter(Model.name == name, Model.city_id == city_id).update(
          {
            'values': values,
            'updated': datetime.datetime.utcnow()
          })
        self.session.commit()
      elif city_object_id is not None:
        self.session.query(Model).filter(Model.name == name, Model.city_object_id == city_object_id).update(
          {
            'values': values,
            'updated': datetime.datetime.utcnow()
          })
        self.session.commit()
      else:
        return {'message': 'Missing either city_id or city_object_id'}
    except SQLAlchemyError as err:
      logger.error(f'Error while updating city object: {err}')
      return {'message': 'Error occurred while updating application'}

  def delete(self, name: str, city_id=None, city_object_id=None):
    """
    Deletes an application with the application_uuid
    :param name: The simulation results tool and workflow name
    :param city_id: The id for the city owning the simulation results
    :param city_object_id: the id for the city_object ownning these simulation results

    :return: None
    """
    try:
      if city_id is not None:
        self.session.query(Model).filter(Model.name == name, Model.city_id == city_id).delete()
        self.session.commit()
      elif city_object_id is not None:
        self.session.query(Model).filter(Model.name == name, Model.city_object_id == city_object_id).delete()
        self.session.commit()
      else:
        return {'message': 'Missing either city_id or city_object_id'}
    except SQLAlchemyError as err:
      logger.error(f'Error while deleting application: {err}')

  def get_city(self, city_id) -> [City]:
    """
    Fetch a city object based city id
    :param city_id: a city identifier
    :return: [City] with the provided city_id
    """
    try:
      return self.session.execute(select(City).where(City.id == city_id)).first()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city by city_id: {err}')

  def get_city_object(self, city_object_id) -> [CityObject]:
    """
    Fetch a city object based city id
    :param city_object_id: a city object identifier
    :return: [CityObject] with the provided city_object_id
    """
    try:
      return self.session.execute(select(CityObject).where(CityObject.id == city_object_id)).first()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city by city_id: {err}')
