"""
User repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from hub.persistence import Repository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from hub.persistence.models import User as Model
from hub.persistence.models import UserRoles
from hub.helpers.auth import Auth
from typing import Union, Dict
from hub.hub_logger import logger
import datetime


class User(Repository):
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(User, cls).__new__(cls)
    return cls._instance

  def insert(self, name: str, password: str, role: UserRoles, application_id: int) -> Union[Model, Dict]:
    """
    Inserts a new user
    :param name: user name
    :param password: user password
    :param role: user rol [Admin or Hub_Reader]
    :param application_id: user application id
    :return: [User, Dictionary]
    """
    user = self.get_by_name_and_application(name, application_id)
    if user is None:
      try:
        user = Model(name=name, password=Auth.hash_password(password), role=role, application_id=application_id)
        self.session.add(user)
        self.session.flush()
        self.session.commit()
        return user
      except SQLAlchemyError as err:
        logger.error(f'An error occurred while creating user: {err}')
    else:
      return {'message': f'user {name} already exists for that application'}

  def update(self, user_id: int, name: str, password: str, role: UserRoles) -> Union[Dict, None]:
    """
    Updates a user
    :param user_id: the id of the user to be updated
    :param name: the name of the user
    :param password: the password of the user
    :param role: the role of the user
    :return:
    """
    try:
      self.session.query(Model).filter(Model.id == user_id).update({
        'name': name,
        'password': Auth.hash_password(password),
        'role': role,
        'updated': datetime.datetime.utcnow()
      })
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while updating user: {err}')
      return {'err_msg': 'Error occurred while updated user'}

  def delete(self, user_id: int):
    """
    Deletes a user with the id
    :param user_id: the user id
    :return: None
    """
    try:
      self.session.query(Model).filter(Model.id == user_id).delete()
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching user: {err}')

  def get_by_name_and_application(self, name: str, application_id: int) -> [Model]:
    """
    Fetch user based on the email address
    :param name: User name
    :param application_id: User application name
    :return: [User] matching the search criteria
    """
    try:
      return self.session.execute(
        select(Model).where(Model.name == name, Model.application_id == application_id)
      ).first()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching user by name and application: {err}')

  def get_by_name_application_and_password(self, name: str, password: str, application_id: int) -> [Model]:
    """
    Fetch user based on the email and password
    :param name: User name
    :param password: User password
    :param application_id: User password

    :return: [User] with the provided email and password
    """
    try:
      user = self.session.execute(
        select(Model).where(Model.name == name, Model.application_id == application_id)
      ).first()
      if user:
        if Auth.check_password(password, user[0].password):
          return user[0]
      return {'message': 'invalid login information'}
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching user by email: {err}')
