import time
import numpy as np
from automata import Automata
from typing import List, Tuple
from generator.tp_generator import set_seed
from multiprocessing import Pool
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

INITIAL_PEDESTRIAN_ARRIVAL_RATE_HR = os.environ.get("pedestrian_arrival_rate", 1000)
FINAL_PEDESTRIAN_ARRIVAL_RATE_HR = os.environ.get("pedestrian_arrival_rate", 6000)
INITIAL_VEHICLE_ARRIVAL_RATE_HR = os.environ.get("vehicle_arrival_rate", 200)
FINAL_VEHICLE_ARRIVAL_RATE_HR = os.environ.get("vehicle_arrival_rate", 1400)
# Amount of times each scenario will be run
# The average of the conflicts will be taken as the final result
# The original paper runs 30 times each scenario, but for this
# python implementation, that would take a long time
RUNS_PER_SCENARIO = os.environ.get("runs_per_scenario", 3)
# Data is recorded every 3600 time steps
SIMULATION_TIME = os.environ.get("simulation_time", 3600)

# The simulation will run for 30 different pedestrian and vehicle arrival rates,
# making a total of 900 scenarios
PEDESTRIAN_ARRIVAL_RATES = np.linspace(INITIAL_PEDESTRIAN_ARRIVAL_RATE_HR/(2*3600), FINAL_PEDESTRIAN_ARRIVAL_RATE_HR/(2*3600), 30)
VEHICLE_ARRIVAL_RATES = np.linspace(INITIAL_VEHICLE_ARRIVAL_RATE_HR/(6*3600), FINAL_VEHICLE_ARRIVAL_RATE_HR/(6*3600), 30)

def print_simulation_config():
    print("Running with the following configuration:")
    print(f"Initial pedestrian arrival rate: {INITIAL_PEDESTRIAN_ARRIVAL_RATE_HR} cap/hr")
    print(f"Final pedestrian arrival rate: {FINAL_PEDESTRIAN_ARRIVAL_RATE_HR} cap/hr")
    print(f"Initial vehicle arrival rate: {INITIAL_VEHICLE_ARRIVAL_RATE_HR} veh/hr")
    print(f"Final vehicle arrival rate: {FINAL_VEHICLE_ARRIVAL_RATE_HR} veh/hr")
    print(f"Runs per scenario: {RUNS_PER_SCENARIO}")
    print(f"Simulation time: {SIMULATION_TIME} steps")
    print(f"Green light time: {os.environ['GREEN_LIGHT_TIME']} seconds")
    print(f"Crosswalk width: {float(os.environ['CROSSWALK_ROWS']) / 2: .1f} meters")

def run(i: int, config: Config) -> Tuple[float, float, float]:    
    print(f"Starting automata...")
    start = time.time()
    results = []
    for j in range(RUNS_PER_SCENARIO):
        set_seed(9*10**6 + i*10 + j)
        automata = Automata(config)
        automata.advance_to(SIMULATION_TIME)
        results.append(automata._conflicts)
    print(f"Scenario finished in {time.time() - start} seconds")

    pedestrian_arrival_rate = config.pedestrian_arrival_rate
    vehicle_arrival_rate = config.vehicle_arrival_rate
    return pedestrian_arrival_rate, vehicle_arrival_rate, sum(results)/len(results)

def build_configs() -> List[Config]:
    config = Config.new_from_env_file()
    configs = []
    for pedestrian_arrival_rate in PEDESTRIAN_ARRIVAL_RATES:
        for vehicle_arrival_rate in VEHICLE_ARRIVAL_RATES:
            config_dup = config.duplicate()
            config_dup.pedestrian_arrival_rate = pedestrian_arrival_rate
            config_dup.vehicle_arrival_rate = vehicle_arrival_rate
            configs.append(config_dup)
    return configs

def run_parallel(configs: List[Config]) -> List[Tuple[float, float, float]]:
    with Pool() as p:
       results = p.starmap(run, zip(range(len(configs)), configs))
    return results

def save_results(results: List[Tuple[float, float, float]]):
    t = time.localtime()
    file_name = f"{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}-{t.tm_sec}.csv"
    with open(f"results/{file_name}", "w") as f:
        f.write("pedestrian_arrival_rate,vehicle_arrival_rate,conflicts\n")
        for r in results:
            f.write(f"{int(r[0]*2*3600)},{int(r[1]*6*3600)},{r[2]}\n")
    print(f"Results saved in results/{file_name}")

def main():
    print_simulation_config()
    configs = build_configs()
    results = run_parallel(configs)
    save_results(results)

if __name__ == "__main__":
    main()