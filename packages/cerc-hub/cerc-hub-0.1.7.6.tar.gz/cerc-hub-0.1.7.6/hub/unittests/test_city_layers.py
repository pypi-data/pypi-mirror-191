"""
CityLayersTest
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2023 Concordia CERC group
Project Coder:  Milad Aghamohamadnia --- milad.aghamohamadnia@concordia.ca

"""

from unittest import TestCase
import json
import os
import time
import uuid
from pathlib import Path
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.usage_factory import UsageFactory
from hub.imports.construction_factory import ConstructionFactory
from hub.exports.energy_building_exports_factory import EnergyBuildingsExportsFactory
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Polygon


class CityLayerTest(TestCase):

  @staticmethod
  def _prepare_buildings(bldgs_group):
    target_json = bldgs_group['target']
    adjacent_json = bldgs_group['adjacent']
    target_buildings = [f"building_{target_json['index']}"]
    adjacent_buildings = [f"building_{el}" for el in adjacent_json['Ids']]
    target_dict = [dict(
      name=f"building_{target_json['index']}",
      height=target_json['height_max'],
      idx=target_json['index'],
      uid=target_json['uid'],
      year_built=2005,
      # year_built= 2005 if target_json['year_built']==9999 else target_json['year_built'],
      coords=target_json['coords'],
      function="residential",
      # function= "residential" if target_json['year_built']>2000 else "industry",
    )]
    adjacent_dict = [dict(
      name=f"building_{el['index']}",
      height=el['height_max'],
      idx=el['index'],
      uid=el['uid'],
      year_built=2005,
      # year_built=2005 if el['year_built']==9999 else el['year_built'],
      coords=el['geom']['coordinates'],
      function="residential",
      # function= "residential" if el['year_built']>2000 else "industry",
    ) for el in adjacent_json['data']]
    df = pd.DataFrame(target_dict + adjacent_dict)
    geometries = [Polygon(row['coords'][0]) for ix, row in df.iterrows()]
    gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometries)
    gdf = gdf.set_crs('EPSG:4326')
    gdf = gdf.to_crs('EPSG:26911')
    return gdf, target_buildings, adjacent_buildings

  def _genidf(self, bldgs_group):
    t0 = time.time()
    buildings_df, target_buildings, adjacent_buildings = self._prepare_buildings(bldgs_group)
    output_path = (Path(__file__).parent / 'tests_outputs').resolve()
    city = GeometryFactory('gpandas', data_frame=buildings_df).city
    ConstructionFactory('nrel', city).enrich()
    UsageFactory('comnet', city).enrich()
    EnergyBuildingsExportsFactory('idf', city, output_path, target_buildings=target_buildings,
                                  adjacent_buildings=adjacent_buildings).export_debug()
    filepath = os.path.join(output_path, city.name + ".idf")
    newfilepath = filepath[:-4] + "_" + uuid.uuid4().hex[:10] + ".idf"
    os.rename(filepath, newfilepath)
    print(f"It took {round((time.time() - t0), 0)} seconds")
    return newfilepath

  def test_city_layers(self):
    json_path = str((Path(__file__).parent / 'tests_data' / 'city_layers.json').resolve())
    with open(json_path) as json_file:
      data = json.loads(json_file.read())
    self._genidf(data)
