"""
Base repository class to establish db connection
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from hub.persistence.configuration import Configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class Repository:

  def __init__(self, db_name, dotenv_path: str, app_env='TEST'):
    try:
      self.configuration = Configuration(db_name, dotenv_path, app_env)
      self.engine = create_engine(self.configuration.conn_string())
      self.session = Session(self.engine)
    except ValueError as err:
      print(f'Missing value for credentials: {err}')
