from grid.relative_grid import RelativeGrid


from vehicle.vehicle_lane import VehicleLane
from vehicle.turning_vehicle import TurningVehicle
from vehicle.straight_vehicle import StraightVehicle

from rectangle import Rectangle

from road_entity import RoadEntity

class TurningVehicleLane(VehicleLane):
    def spawn_vehicle(self, vehicle_grid: RelativeGrid[RoadEntity], vehicle_prot: Rectangle):
        # TurningVehicle(vehicle_grid, vehicle_prot)
        StraightVehicle(vehicle_grid, vehicle_prot)