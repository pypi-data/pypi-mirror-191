"""
Persistence (Postgresql) configuration
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from hub.hub_logger import logger

Models = declarative_base()

class Configuration:
  """
  Configuration class to hold common persistence configuration
  """

  def __init__(self, db_name: str, dotenv_path: str, app_env='TEST'):
    """
      :param db_name: database name
      :param app_env: application environment, test or production
      :param dotenv_path: the absolute path to dotenv file
      """
    try:
      # load environmental variables
      load_dotenv(dotenv_path=dotenv_path)
      self._db_name = db_name
      self._db_host = os.getenv(f'{app_env}_DB_HOST')
      self._db_user = os.getenv(f'{app_env}_DB_USER')
      self._db_pass = os.getenv(f'{app_env}_DB_PASSWORD')
      self._db_port = os.getenv(f'{app_env}_DB_PORT')
      self.hub_token = os.getenv('HUB_TOKEN')
    except KeyError as err:
      logger.error(f'Error with credentials: {err}')

  def conn_string(self):
    """
      Returns a connection string postgresql
      :return: connection string
      """
    if self._db_pass:
      return f'postgresql://{self._db_user}:{self._db_pass}@{self._db_host}:{self._db_port}/{self._db_name}'
    return f'postgresql://{self._db_user}@{self._db_host}:{self._db_port}/{self._db_name}'

  def get_db_user(self):
    return self._db_user
