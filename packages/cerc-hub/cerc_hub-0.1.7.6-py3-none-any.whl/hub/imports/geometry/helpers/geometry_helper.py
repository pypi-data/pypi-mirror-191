"""
Geometry helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import numpy as np


class GeometryHelper:
  """
  Geometry helper
  """
  @staticmethod
  def to_points_matrix(points):
    """
    Transform a point vector into a point matrix
    :param points: [x, y, z, x, y, z ...]
    :return: [[x,y,z],[x,y,z]...]
    """
    rows = points.size // 3
    points = points.reshape(rows, 3)
    return points

  @staticmethod
  def gml_surface_to_libs(surface):
    """
    Transform citygml surface names into hub names
    """
    if surface == 'WallSurface':
      return 'Wall'
    if surface == 'GroundSurface':
      return 'Ground'
    return 'Roof'

  @staticmethod
  def points_from_string(coordinates) -> np.ndarray:
    points = np.fromstring(coordinates, dtype=float, sep=' ')
    points = GeometryHelper.to_points_matrix(points)
    return points

  @staticmethod
  def remove_last_point_from_string(points):
    array = points.split(' ')
    res = " "
    return res.join(array[0:len(array) - 3])
