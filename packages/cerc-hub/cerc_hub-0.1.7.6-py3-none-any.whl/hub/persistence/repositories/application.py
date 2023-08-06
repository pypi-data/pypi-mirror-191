"""
Application repository with database CRUD operations
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
from hub.persistence.models import Application as Model


class Application(Repository):
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(Application, cls).__new__(cls)
    return cls._instance

  def insert(self, name: str, description: str, application_uuid: str) -> Union[Model, Dict]:
    """
    Inserts a new application
    :param name: Application name
    :param description: Application description
    :param application_uuid: Unique identifier for the application
    :return: application and dictionary
    """
    application = self.get_by_uuid(application_uuid)
    if application is None:
      try:
        application = Model(name=name, description=description, application_uuid=application_uuid)
        self.session.add(application)
        self.session.commit()
        return application
      except SQLAlchemyError as err:
        logger.error(f'An error occurred while creating application: {err}')
    else:
      return {'message': f'An application with {application_uuid} application uuid, already exists'}

  def update(self, application_uuid: str, name: str, description: str) -> Union[Dict, None]:
    """
    Updates an application
    :param application_uuid: the application uuid of the application to be updated
    :param name: the application name
    :param description: the application description
    :return:
    """
    try:
      self.session.query(Model).filter(
        Model.application_uuid == application_uuid
      ).update({'name': name, 'description': description, 'updated': datetime.datetime.utcnow()})
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while updating application: {err}')
      return {'message': 'Error occurred while updating application'}

  def delete(self, application_uuid: str):
    """
    Deletes an application with the application_uuid
    :param application_uuid: The application uuid
    :return: None
    """
    try:
      self.session.query(Model).filter(Model.application_uuid == application_uuid).delete()
      self.session.flush()
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while deleting application: {err}')

  def get_by_uuid(self, application_uuid: str) -> Union[Model, None]:
    """
    Fetch Application based on the application uuid
    :param application_uuid: the application uuid
    :return: Application with the provided application_uuid or None
    """
    try:
      result_set = self.session.execute(select(Model).where(
        Model.application_uuid == application_uuid)
      ).first()
      if result_set is None:
        return None
      return result_set[0]
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching application by application_uuid: {err}')

