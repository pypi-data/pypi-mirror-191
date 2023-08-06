"""
Test EnergySystemsFactory and various heatpump models
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
from unittest import TestCase
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.energy_systems_factory import EnergySystemsFactory
from hub.exports.energy_systems_factory import EnergySystemsExportFactory
from hub.imports.db_factory import DBFactory
from hub.exports.db_factory import DBFactory as ExportDBFactory
from hub.persistence.base_repo import BaseRepo
from sqlalchemy import create_engine
from hub.persistence.models import City
from hub.persistence.models import SimulationTypes
from hub.persistence.models import HeatPumpTypes
from hub.persistence.models import HeatPumpSimulation
from hub.persistence.models import User
from sqlalchemy.exc import ProgrammingError
from hub.imports.user_factory import UserFactory
from hub.persistence.models import UserRoles

# User defined paramenters
hp_sim_data = {
  'StartYear': 2020,
  'EndYear': 2021,
  'MaximumHPEnergyInput': 8000,
  'HoursOfStorageAtMaxDemand': 1,
  'BuildingSuppTemp': 40,
  'TemperatureDifference': 15,
  'FuelLHV': 47100,
  'FuelPrice': 0.12,
  'FuelEF': 1887,
  'FuelDensity': 0.717,
  'HPSupTemp': 60
}


class TestHeatPumpSimulation(TestCase):
  """
  Heat pump simulation test cases
  """
  @classmethod
  def setUpClass(cls) -> None:
    """
    Test setup
    :return: None
    """
    repo = BaseRepo(db_name='test_db', app_env='TEST', dotenv_path='../.env')
    eng = create_engine(f'postgresql://{repo.config.get_db_user()}@/{repo.config.get_db_user()}')

    try:
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

    # Create test tables if they do not exit
    User.__table__.create(bind=repo.engine, checkfirst=True)
    City.__table__.create(bind=repo.engine, checkfirst=True)
    HeatPumpSimulation.__table__.create(bind=repo.engine, checkfirst=True)


    city_file = "tests_data/C40_Final.gml"
    cls._city = GeometryFactory('citygml', city_file).city
    EnergySystemsFactory('air source hp', cls._city).enrich()

    cls._db_factory = DBFactory(db_name='test_db', app_env='TEST', dotenv_path='../.env')
    cls._export_db_factory = ExportDBFactory(db_name='test_db', app_env='TEST', dotenv_path='../.env')
    user_factory = UserFactory(db_name='test_db', app_env='TEST', dotenv_path='../.env')
    cls._user = user_factory.create_user("Admin", "admin@hub.com", "Admin@123", UserRoles.Admin)

  def test_heat_pump_simulation_persistence(self):
    output = EnergySystemsExportFactory(city=self._city, user_input=hp_sim_data, hp_model='018',
                                        output_path=None, sim_type=1).export()
    hp_sim_data["HeatPumpModel"] = '018'
    hp_sim_data["SimulationType"] = SimulationTypes.Parallel
    hp_sim_data["HeatPumpType"] = HeatPumpTypes.Air
    hp_sim_data["HourlyElectricityDemand"] = output["hourly_electricity_demand"]
    hp_sim_data["DailyElectricityDemand"] = output["daily_electricity_demand"]
    hp_sim_data["MonthlyElectricityDemand"] = output["monthly_electricity_demand"]
    hp_sim_data["DailyFossilFuelConsumption"] = output["daily_fossil_consumption"]
    hp_sim_data["MonthlyFossilFuelConsumption"] = output["monthly_fossil_consumption"]

    saved_city = self._db_factory.persist_city(self._user.id, self._city)
    hp_sim = self._db_factory.persist_hp_simulation(hp_sim_data, saved_city.id)
    self.assertEqual(hp_sim.heat_pump_type, HeatPumpTypes.Air)
    self.assertEqual(hp_sim.simulation_type, SimulationTypes.Parallel)
    self.assertEqual(hp_sim.fuel_efficiency, hp_sim_data["FuelEF"])
    self.assertEqual(hp_sim.monthly_electricity_demand, output["monthly_electricity_demand"])
    self._db_factory.delete_hp_simulation(hp_sim.id)
    self._db_factory.delete_city(saved_city.id)

  def test_get_heat_pump_simulation_by_city(self):
    output = EnergySystemsExportFactory(city=self._city, user_input=hp_sim_data, hp_model='012',
                                        output_path=None, sim_type=0).export()
    hp_sim_data["HeatPumpModel"] = '012'
    hp_sim_data["SimulationType"] = SimulationTypes.Series
    hp_sim_data["HeatPumpType"] = HeatPumpTypes.Air
    hp_sim_data["HourlyElectricityDemand"] = output["hourly_electricity_demand"]
    hp_sim_data["DailyElectricityDemand"] = output["daily_electricity_demand"]
    hp_sim_data["MonthlyElectricityDemand"] = output["monthly_electricity_demand"]
    hp_sim_data["DailyFossilFuelConsumption"] = output["daily_fossil_consumption"]
    hp_sim_data["MonthlyFossilFuelConsumption"] = output["monthly_fossil_consumption"]

    saved_city = self._db_factory.persist_city(self._user.id, self._city)
    self._db_factory.persist_hp_simulation(hp_sim_data, saved_city.id)

    # retrieved saved simulation by city id
    hp_sim = self._export_db_factory.get_hp_simulation_by_city(saved_city.id)
    self.assertEqual(hp_sim[0].heat_pump_type, HeatPumpTypes.Air)
    self.assertEqual(hp_sim[0].simulation_type, SimulationTypes.Series)
    self.assertEqual(hp_sim[0].fuel_price, hp_sim_data["FuelPrice"])
    self.assertEqual(hp_sim[0].hourly_electricity_demand, output["hourly_electricity_demand"])
    self._db_factory.delete_hp_simulation(hp_sim[0].id)
    self._db_factory.delete_city(saved_city.id)

