"""
DBFactory performs read related operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project CoderPeter Yefi peteryefi@gmail.com
"""
from hub.persistence import City
from hub.persistence import Application
from hub.persistence import User
from hub.persistence import CityObject


class DBFactory:
  """
  DBFactory class
  """

  def __init__(self, db_name, app_env, dotenv_path):
    self._city = City(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._application = Application(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._user = User(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._city_object = CityObject(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)

  def get_city(self, city_id):
    """
    Retrieve a single city from postgres
    :param city_id: the id of the city to get
    """
    return self._city.get_by_id(city_id)

  def get_city_by_name(self, city_name):
    """
    Retrieve a single city from postgres
    :param city_name: the name of the city to get
    """
    return self._city.get_by_name(city_name)

  def get_city_by_user(self, user_id):
    """
    Retrieve cities created by user
    :param user_id: the id of the user
    """
    return self._city.get_by_user(user_id)

  def application_info(self, application_uuid):
    return self._application.get_by_uuid(application_uuid)

  def user_info(self, name, password, application_id):
    return self._user.get_by_name_application_and_password(name, password, application_id)

  def building_info(self, name, city_id):
    return self._city_object.get_by_name_and_city(name, city_id)

