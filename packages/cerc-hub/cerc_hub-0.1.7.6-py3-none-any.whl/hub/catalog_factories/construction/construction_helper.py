from hub.helpers import constants as cte


class ConstructionHelper:
  """
  Construction helper class
  """
  _reference_standard_to_construction_period = {
    'non_standard_dompark': '1900 - 2004',
    'ASHRAE 90.1_2004': '2004 - 2009',
    'ASHRAE 189.1_2009': '2009 - PRESENT'
  }

  _nrel_surfaces_types_to_hub_types = {
    'exterior wall': cte.WALL,
    'interior wall': cte.INTERIOR_WALL,
    'ground wall': cte.GROUND_WALL,
    'exterior slab': cte.GROUND,
    'attic floor': cte.ATTIC_FLOOR,
    'interior slab': cte.INTERIOR_SLAB,
    'roof': cte.ROOF
  }

  _nrcan_surfaces_types_to_hub_types = {
    'Wall_Outdoors': cte.WALL,
    'RoofCeiling_Outdoors': cte.ROOF,
    'Floor_Outdoors': cte.ATTIC_FLOOR,
    'Window_Outdoors': cte.WINDOW,
    'Skylight_Outdoors': cte.SKYLIGHT,
    'Door_Outdoors': cte.DOOR,
    'Wall_Ground': cte.GROUND_WALL,
    'RoofCeiling_Ground': cte.GROUND_WALL,
    'Floor_Ground': cte.GROUND
  }

  @property
  def reference_standard_to_construction_period(self):
    return self._reference_standard_to_construction_period

  @property
  def nrel_surfaces_types_to_hub_types(self):
    return self._nrel_surfaces_types_to_hub_types

  @property
  def nrcan_surfaces_types_to_hub_types(self):
    return self._nrcan_surfaces_types_to_hub_types
