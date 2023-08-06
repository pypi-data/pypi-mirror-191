"""
export a city into Obj format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

from pathlib import Path
import trimesh.exchange.obj
from hub.exports.formats.triangular import Triangular
from hub.imports.geometry_factory import GeometryFactory


class Obj(Triangular):
  """
  Export to obj format
  """
  def __init__(self, city, path):
    super().__init__(city, path, 'obj')

  def to_ground_points(self):
    """
    Move closer to the origin
    """
    file_name_in = self._city.name + '.' + self._triangular_format
    file_name_out = self._city.name + '_ground.' + self._triangular_format
    file_path_in = (Path(self._path).resolve() / file_name_in).resolve()
    file_path_out = (Path(self._path).resolve() / file_name_out).resolve()
    obj = GeometryFactory('obj', path=file_path_in)
    scene = obj.scene
    scene.rezero()
    obj_file = trimesh.exchange.obj.export_obj(scene)
    with open(file_path_out, 'w') as file:
      file.write(obj_file)
