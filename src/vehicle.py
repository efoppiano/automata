from typing import List

from relative_grid import RelativeGrid
from relative_position import RelativePosition
from stoplight import StopLight
from generator.tp_generator import TPGenerator
from rectangle import Rectangle

gen = TPGenerator(4*10**7)

class Vehicle:
  def __init__(self, origin: RelativeGrid, crosswalk_zone: Rectangle, prototype: Rectangle):
    self._repr = gen.choice(["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫"])
    self._vel = 5
    self._crossing = False
    self._crosswalk_zone = crosswalk_zone
    self._desired_movement = None
    # These are swapped on purpose
    self._width = prototype.length
    self._length = prototype.width

    self.build_grids(origin)    
    
  def build_grids(self, origin: RelativeGrid):
    self.relative_origins: List[RelativeGrid] = []
    for i in range(self._width):
      for j in range(self._length):
        origin_ij = origin.new_displaced(
            RelativePosition.right(i) + RelativePosition.forward(j)
            )
        if i == 0 and j == self._length-1:
          self.driver_pos = origin_ij
        else:
          self.relative_origins.insert(0, origin_ij) # We will want to move the last ones first as they're in front
    
    self.driver_pos.fill(RelativePosition.still(),self)
    for rel_grid_i in self.relative_origins:
      part = VehiclePart(self, rel_grid_i, self._repr)
      rel_grid_i.fill(RelativePosition.still(),part)

  def facing(self):
    return self.driver_pos.facing
  
  def can_move(self) -> bool:
    for i in range(self._width):
      dist_to_next = self.driver_pos.calc_dist_to_next(RelativePosition.right(i))
      if dist_to_next is not None and dist_to_next < self._vel:
        return False
      
    return True

  def think(self, pedestrian_stop_light: StopLight):
    if self._crossing or pedestrian_stop_light.is_red():
      self._desired_movement = RelativePosition.forward(self._vel)
    else:
      dist = self.driver_pos.calc_dist_to_zone(RelativePosition.still(), self._crosswalk_zone)
      if dist is None:
        self._desired_movement = RelativePosition.forward(self._vel)
      else:
        self._desired_movement = RelativePosition.forward(min(dist, self._vel))
    
  def move(self):
    if not self.can_move():
      return
    
    if not self.driver_pos.is_inbounds(self._desired_movement):
      self.remove()
      return

    self.driver_pos.move(self._desired_movement)

    for rel_grid_i in self.relative_origins:
      rel_grid_i.move(self._desired_movement)
      
    if not self._desired_movement.is_still():
      self._moved = True
    if not self._crossing:
      self._crossing = self.driver_pos.is_in(self._crosswalk_zone)
    
  
  def __repr__(self):
        return self._repr

  def remove(self):
    self.driver_pos.clear()
    for rel_grid_i in self.relative_origins:
      rel_grid_i.clear()

  
class VehiclePart:
  def __init__(self, parent: Vehicle, relative_origin: RelativeGrid, repr: str):
    self.parent = parent
    self.relative_origin = relative_origin
    self._repr = repr
    self._vel = 0
    
  @property
  def facing(self):
    return self.relative_origin.facing
  
  def think(self, _:StopLight):
    pass
  
  def __repr__(self):
        return self._repr
      
  def move(self):
    pass
  
  def remove(self):
    pass