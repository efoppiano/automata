from typing import List

from relative_grid import RelativeGrid
from relative_position import RelativePosition
from stoplight import StopLight



class Vehicle:
  def __init__(self, rel_grid: RelativeGrid, width: int, length: int):
    self._repr = "️ ⇩ " if rel_grid.facing == "South" else "⇧" # Por alguna razón este necesita los espacios
    self._vel = 5
    self._desired_movement = None

    self.relative_origins: List[RelativeGrid] = []
    for i in range(width):
      for j in range(length):
        origin_ij = rel_grid.new_displaced(
            RelativePosition.right(i) + RelativePosition.forward(j)
            )
        if i == 0 and j == length-1:
          self.driver_pos = origin_ij
        else:
          self.relative_origins.insert(0, origin_ij) # We will want to move the last ones first as they're in front
    
    self.driver_pos.fill(RelativePosition.still(),self)
    for rel_grid_i in self.relative_origins:
      part = VehiclePart(self, rel_grid_i)
      rel_grid_i.fill(RelativePosition.still(),part)
      
  def facing(self):
    return self.driver_pos.facing
  
  def think(self, pedestrian_stop_light: StopLight):
    if pedestrian_stop_light.is_green():
      self._desired_movement = RelativePosition.still()
    else:
      self._desired_movement = RelativePosition.forward(self._vel)
  
  def move(self):
    self.driver_pos.move(self._desired_movement)
    for rel_grid_i in self.relative_origins:
      rel_grid_i.move(self._desired_movement)
  
  def __repr__(self):
        return self._repr
  
class VehiclePart:
  def __init__(self, parent: Vehicle, relative_origin: RelativeGrid):
    self.parent = parent
    self.relative_origin = relative_origin
    self._repr = "⇩" if relative_origin.facing == "South" else "⇧"
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
  
  