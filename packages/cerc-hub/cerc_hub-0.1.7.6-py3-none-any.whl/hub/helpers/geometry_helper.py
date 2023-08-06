"""
Geometry helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import math
import numpy as np
import requests
from trimesh import Trimesh
from trimesh import intersections
from hub.city_model_structure.attributes.polygon import Polygon
from hub.city_model_structure.attributes.polyhedron import Polyhedron
from hub.helpers.location import Location
from hub.helpers.configuration_helper import ConfigurationHelper


class GeometryHelper:
  """
  Geometry helper class
  """
  srs_transformations = {
    'urn:adv:crs:ETRS89_UTM32*DE_DHHN92_NH': 'epsg:25832'
  }

  def __init__(self, delta=0, area_delta=0):
    self._delta = delta
    self._area_delta = area_delta

  @staticmethod
  def adjacent_locations(location1, location2):
    """
    Determine when two attributes may be adjacent or not based in the dis
    :param location1:
    :param location2:
    :return: Boolean
    """
    max_distance = ConfigurationHelper().max_location_distance_for_shared_walls
    return GeometryHelper.distance_between_points(location1, location2) < max_distance

  @staticmethod
  def segment_list_to_trimesh(lines) -> Trimesh:
    """
    Transform a list of segments into a Trimesh
    """
    # todo: trimesh has a method for this
    line_points = [lines[0][0], lines[0][1]]
    lines.remove(lines[0])
    while len(lines) > 1:
      i = 0
      for line in lines:
        i += 1
        if GeometryHelper.distance_between_points(line[0], line_points[len(line_points) - 1]) < 1e-8:
          line_points.append(line[1])
          lines.pop(i - 1)
          break
        if GeometryHelper.distance_between_points(line[1], line_points[len(line_points) - 1]) < 1e-8:
          line_points.append(line[0])
          lines.pop(i - 1)
          break
    polyhedron = Polyhedron(Polygon(line_points).triangles)
    trimesh = Trimesh(polyhedron.vertices, polyhedron.faces)
    return trimesh

  @staticmethod
  def _merge_meshes(mesh1, mesh2):
    v_1 = mesh1.vertices
    f_1 = mesh1.faces
    v_2 = mesh2.vertices
    f_2 = mesh2.faces
    length = len(v_1)
    v_merge = np.concatenate((v_1, v_2))
    f_merge = np.asarray(f_1)

    for item in f_2:
      point1 = item.item(0) + length
      point2 = item.item(1) + length
      point3 = item.item(2) + length
      surface = np.asarray([point1, point2, point3])
      f_merge = np.concatenate((f_merge, [surface]))

    mesh_merge = Trimesh(vertices=v_merge, faces=f_merge)
    mesh_merge.fix_normals()

    return mesh_merge

  @staticmethod
  def divide_mesh_by_plane(trimesh, normal_plane, point_plane):
    """
    Divide a mesh by a plane
    :param trimesh: Trimesh
    :param normal_plane: [x, y, z]
    :param point_plane: [x, y, z]
    :return: [Trimesh]
    """
    # The first mesh returns the positive side of the plane and the second the negative side.
    # If the plane does not divide the mesh (i.e. it does not touch it or it is coplanar with one or more faces),
    # then it returns only the original mesh.
    # todo: review split method in https://github.com/mikedh/trimesh/issues/235,
    #  once triangulate_polygon in Polygon class is solved

    normal_plane_opp = [None] * len(normal_plane)
    for i in range(0, len(normal_plane)):
      normal_plane_opp[i] = - normal_plane[i]

    section_1 = intersections.slice_mesh_plane(trimesh, normal_plane, point_plane)
    if section_1 is None:
      return [trimesh]
    lines = list(intersections.mesh_plane(trimesh, normal_plane, point_plane))
    cap = GeometryHelper.segment_list_to_trimesh(lines)
    trimesh_1 = GeometryHelper._merge_meshes(section_1, cap)

    section_2 = intersections.slice_mesh_plane(trimesh, normal_plane_opp, point_plane)
    if section_2 is None:
      return [trimesh_1]
    trimesh_2 = GeometryHelper._merge_meshes(section_2, cap)

    return [trimesh_1, trimesh_2]

  @staticmethod
  def get_location(latitude, longitude) -> Location:
    """
    Get Location from latitude and longitude
    """
    url = 'https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json'
    response = requests.get(url.format(latitude=latitude, longitude=longitude))
    if response.status_code != 200:
      # This means something went wrong.
      raise Exception('GET /tasks/ {}'.format(response.status_code))

    response = response.json()
    city = 'Unknown'
    country = 'ca'
    if 'city' in response['address']:
      city = response['address']['city']
    if 'country_code' in response['address']:
      country = response['address']['country_code']
    return Location(country, city)

  @staticmethod
  def distance_between_points(vertex1, vertex2):
    """
    distance between points in an n-D Euclidean space
    :param vertex1: point or vertex
    :param vertex2: point or vertex
    :return: float
    """
    power = 0
    for dimension in range(0, len(vertex1)):
      power += math.pow(vertex2[dimension]-vertex1[dimension], 2)
    distance = math.sqrt(power)
    return distance
