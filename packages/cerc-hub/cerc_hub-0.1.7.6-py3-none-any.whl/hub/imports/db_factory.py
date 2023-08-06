"""
DBFactory performs database create, delete and update operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project CoderPeter Yefi peteryefi@gmail.com
"""
from hub.city_model_structure.city import City
from hub.persistence import City as CityRepository
from hub.persistence import SimulationResults


class DBFactory:
  """
  DBFactory class
  """

  def __init__(self, db_name, dotenv_path, app_env):
    self._city_repository = CityRepository(db_name=db_name, dotenv_path=dotenv_path, app_env=app_env)
    self._simulation_results = SimulationResults(db_name=db_name, dotenv_path=dotenv_path, app_env=app_env)

  def persist_city(self, city: City, pickle_path, application_id: int, user_id: int):
    """
    Persist city into postgres database
    :param city: City to be stored
    :param pickle_path: Path to save the pickle file
    :param application_id: Application id owning this city
    :param user_id: User who create the city
    """
    return self._city_repository.insert(city, pickle_path, application_id, user_id)

  def update_city(self, city_id, city):
    """
   Update an existing city in postgres database
   :param city_id: the id of the city to update
   :param city: the updated city object
    """
    return self._city_repository.update(city_id, city)

  def delete_city(self, city_id):
    """
    Deletes a single city from postgres
    :param city_id: the id of the city to get
    """
    self._city_repository.delete(city_id)

  def add_simulation_results(self, name, values, city_id=None, city_object_id=None):
    """
    Add simulation results to the city or to the city_object
    :param name: simulation and simulation engine name
    :param values: simulation values in json format
    :param city_id: city id or None
    :param city_object_id: city object id or None
    """
    self._simulation_results.insert(name, values,city_id, city_object_id)
