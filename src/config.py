import os
from dotenv import load_dotenv

from rectangle import Rectangle
from stoplight import StopLight

DEFAULT_CROSSWALK_ROWS = 8
DEFAULT_CROSSWALK_COLS = 42
DEFAULT_WAITING_AREA_COLS = 1
DEFAULT_VEHICLE_LANES = 6
DEFAULT_VEHICLE_ROWS = 6
DEFAULT_VEHICLE_COLS = 5
DEFAULT_STOP_LIGHT_CYCLE = 90
DEFAULT_GREEN_LIGHT_TIME = 20
DEFAULT_PEDESTRIAN_ARRIVAL_RATE = 1000/3600
DEFAULT_VEHICLE_ARRIVAL_RATE = 1400/(6*3600)



class Config:
    @classmethod
    def new_from_env_file(cls) -> "Config":
        load_dotenv()

        crosswalk_rows = os.environ.get("crosswalk_rows", DEFAULT_CROSSWALK_ROWS)
        crosswalk_cols = os.environ.get("crosswalk_cols", DEFAULT_CROSSWALK_COLS)
        waiting_area_cols = os.environ.get("waiting_area_cols", DEFAULT_WAITING_AREA_COLS)
        vehicle_lanes = os.environ.get("vehicle_lanes", DEFAULT_VEHICLE_LANES)
        vehicle_rows = os.environ.get("vehicle_rows", DEFAULT_VEHICLE_ROWS)
        vehicle_cols = os.environ.get("vehicle_cols", DEFAULT_VEHICLE_COLS)
        stop_light_cycle = os.environ.get("stop_light_cycle", DEFAULT_STOP_LIGHT_CYCLE)
        green_light_time = os.environ.get("green_light_time", DEFAULT_GREEN_LIGHT_TIME)
        pedestrian_stop_light = StopLight(stop_light_cycle, green_light_time, "green")
        pedestrian_arrival_rate = os.environ.get("pedestrian_arrival_rate", DEFAULT_PEDESTRIAN_ARRIVAL_RATE)
        vehicle_arrival_rate = os.environ.get("vehicle_arrival_rate", DEFAULT_VEHICLE_ARRIVAL_RATE)

        vehicle_lane_cols = crosswalk_cols // vehicle_lanes
        crosswalk_prototype = Rectangle(crosswalk_rows, crosswalk_cols)
        vehicle_lane_prototype = Rectangle(3*vehicle_rows+crosswalk_prototype.rows, vehicle_lane_cols)
        waiting_area_prototype = Rectangle(crosswalk_rows, waiting_area_cols)
        vehicle_prototype = Rectangle(vehicle_rows, vehicle_cols)

        return cls(crosswalk_prototype,
                   vehicle_lane_prototype, 
                   waiting_area_prototype, 
                   vehicle_prototype, 
                   pedestrian_stop_light,
                   pedestrian_arrival_rate, 
                   vehicle_arrival_rate)

    def __init__(self,
                 crosswalk_prot: Rectangle,
                 vehicle_lane_prot: Rectangle,
                 waiting_area_prot: Rectangle,
                 vehicle_prot: Rectangle,
                 pedestrian_stop_light: StopLight,
                 pedestrian_arrival_rate: float,
                 vehicle_arrival_rate: float):
        self.crosswalk_prot = crosswalk_prot
        self.vehicle_lane_prot = vehicle_lane_prot
        self.waiting_area_prot = waiting_area_prot
        self.vehicle_prot = vehicle_prot
        self.pedestrian_stop_light = pedestrian_stop_light
        self.pedestrian_arrival_rate = pedestrian_arrival_rate
        self.vehicle_arrival_rate = vehicle_arrival_rate

    @property
    def total_cols(self) -> int:
        return self.crosswalk_prot.cols + 2*self.waiting_area_prot.cols
    
    @property
    def total_rows(self) -> int:
        return self.vehicle_lane_prot.rows

    @property
    def walking_zone_prot(self) -> Rectangle:
        return Rectangle(self.crosswalk_prot.rows, self.total_cols)
    
    def show(self):
        print(f"Crosswalk prototype: {self.crosswalk_prot}")
        print(f"Vehicle lane prototype: {self.vehicle_lane_prot}")
        print(f"Waiting area prototype: {self.waiting_area_prot}")
        print(f"Vehicle prototype: {self.vehicle_prot}")
        print(f"Pedestrian stop light: {self.pedestrian_stop_light}")
        print(f"Pedestrian arrival rate: {self.pedestrian_arrival_rate}")
        print(f"Vehicle arrival rate: {self.vehicle_arrival_rate}")
        print(f"Total rows: {self.total_rows}")
        print(f"Total cols: {self.total_cols}")
        print(f"Walking zone prototype: {self.walking_zone_prot}")