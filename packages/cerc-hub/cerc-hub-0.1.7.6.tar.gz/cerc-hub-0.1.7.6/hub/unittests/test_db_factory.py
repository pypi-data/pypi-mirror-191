"""
Test EnergySystemsFactory and various heatpump models
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
from unittest import TestCase
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.db_factory import DBFactory
from hub.imports.user_factory import UserFactory
from hub.exports.db_factory import DBFactory as ExportDBFactory
from hub.persistence.base_repo import BaseRepo
from sqlalchemy import create_engine
from hub.persistence.models import City
from hub.persistence.models import User, UserRoles
from pickle import loads
from sqlalchemy.exc import ProgrammingError


class TestDBFactory(TestCase):
  """
  TestDBFactory
  """

  @classmethod
  def setUpClass(cls) -> None:
    """
    Test setup
    :return: None
    """
    # Create test database
    repo = BaseRepo(db_name='test_db', app_env='TEST', dotenv_path='/usr/local/etc/hub/.env')
    eng = create_engine(f'postgresql://{repo.config.get_db_user()}@/{repo.config.get_db_user()}')

    try:
      # delete test database if it exists
      conn = eng.connect()
      conn.execute('commit')
      conn.execute('DROP DATABASE test_db')
      conn.close()
    except ProgrammingError as err:
      print(f'Database does not exist. Nothing to delete')

    cnn = eng.connect()
    cnn.execute('commit')
    cnn.execute("CREATE DATABASE test_db")
    cnn.close()
    User.__table__.create(bind=repo.engine, checkfirst=True)
    City.__table__.create(bind=repo.engine, checkfirst=True)

    city_file = "tests_data/C40_Final.gml"
    cls.city = GeometryFactory('citygml', city_file).city
    cls._db_factory = DBFactory(db_name='test_db', app_env='TEST', dotenv_path='../.env')
    cls._export_db_factory = ExportDBFactory(db_name='test_db', app_env='TEST', dotenv_path='../.env')
    user_factory = UserFactory(db_name='test_db', app_env='TEST', dotenv_path='../.env')
    cls._user = user_factory.create_user("Admin", "admin@hub.com", "Admin@123", UserRoles.Admin)

  def test_save_city(self):
    saved_city = self._db_factory.persist_city(self._user.id, self.city)
    self.assertEqual(saved_city.name, 'Montréal')
    pickled_city = loads(saved_city.city)
    self.assertEqual(len(pickled_city.buildings), 10)
    self.assertEqual(pickled_city.buildings[0].floor_area, 1990.9913970530033)
    self._db_factory.delete_city(saved_city.id)

  def test_save_same_city_with_same_hub_version(self):
    first_city = self._db_factory.persist_city(self._user.id, self.city)
    second_city = self._db_factory.persist_city(self._user.id, self.city)
    self.assertEqual(second_city['message'], f'Same version of {self.city.name} exist')
    self.assertEqual(first_city.name, 'Montréal')
    self.assertEqual(first_city.country_code, 'ca')
    self._db_factory.delete_city(first_city.id)

  def test_get_city_by_name(self):
    city = self._db_factory.persist_city(self._user.id, self.city)
    retrieved_city = self._export_db_factory.get_city_by_name(city.name)
    self.assertEqual(retrieved_city[0].lower_corner[0], 610610.7547462888)
    self._db_factory.delete_city(city.id)

  def test_get_city_by_user(self):
    city = self._db_factory.persist_city(self._user.id, self.city)
    retrieved_city = self._export_db_factory.get_city_by_user(self._user.id)
    self.assertEqual(retrieved_city[0].user_id, self._user.id)
    self._db_factory.delete_city(city.id)

  def test_get_city_by_id(self):
    city = self._db_factory.persist_city(self._user.id, self.city)
    retrieved_city = self._export_db_factory.get_city(city.id)
    self.assertEqual(retrieved_city.upper_corner[0], 610818.6731258357)
    self._db_factory.delete_city(city.id)

  def test_get_update_city(self):
    city = self._db_factory.persist_city(self._user.id, self.city)
    self.city.longitude = 1.43589
    self.city.latitude = -9.38928339
    self._db_factory.update_city(city.id, self.city)
    updated_city = self._export_db_factory.get_city(city.id)
    self.assertEqual(updated_city.longitude, 1.43589)
    self.assertEqual(updated_city.latitude, -9.38928339)
    self._db_factory.delete_city(city.id)
