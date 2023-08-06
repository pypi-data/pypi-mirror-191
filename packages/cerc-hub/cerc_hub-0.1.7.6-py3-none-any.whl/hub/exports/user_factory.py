"""
User performs user related crud operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project CoderPeter Yefi peteryefi@gmail.com
"""
from hub.persistence import UserRepo


class UserFactory:
  """
  UserFactory class
  """

  def __init__(self, db_name, app_env, dotenv_path):
    self._user_repo = UserRepo(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)

  def login_user(self, email: str, password: str):
    """
    Retrieve a single city from postgres
    :param email: the email of the user
    :param password: the password of the user
    """
    return self._user_repo.get_user_by_email_and_password(email, password)

  def get_user_by_email(self, email):
    """
    Retrieve a single user
    :param email: the email of the user to get
    """
    return self._user_repo.get_by_email(email)
