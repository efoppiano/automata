import time
import numpy as np
from automata import Automata
from typing import List
from generator.tp_generator import set_seed
from multiprocessing import Pool
from config import Config

def run(args):
    i, config = args
    
    print(f"Starting automata...")
    start = time.time()
    results = []
    for j in range(3):
        set_seed(9*10**6 + i*10 + j)
        automata = Automata(config)
        automata.advance_to(3600)
        results.append(automata._conflicts)
    print(f"Scenario finished in {time.time() - start} seconds")

    pedestrian_arrival_rate = config.pedestrian_arrival_rate
    vehicle_arrival_rate = config.vehicle_arrival_rate
    return pedestrian_arrival_rate, vehicle_arrival_rate, sum(results)/len(results)

def build_configs() -> List[Config]:
    config = Config.new_from_env_file()
    configs = []
    for pedestrian_arrival_rate in np.linspace(1000/(2*3600), 6000/(2*3600), 30):
        for vehicle_arrival_rate in np.linspace(200/(6*3600), 1400/(6*3600), 30):
            config_dup = config.duplicate()
            config_dup.pedestrian_arrival_rate = pedestrian_arrival_rate
            config_dup.vehicle_arrival_rate = vehicle_arrival_rate
            configs.append(config_dup)
    return configs

def main():
    print("Starting simulation...")
    configs = build_configs()

    with Pool() as p:
       results = p.map(run, zip(range(len(configs)), configs))
    
    print(f"Average conflicts: {sum([r[2] for r in results])/len(results)}")

    t = time.localtime()
    file_name = f"{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}-{t.tm_sec}.csv"
    with open(f"results/{file_name}", "w") as f:
        f.write("pedestrian_arrival_rate,vehicle_arrival_rate,conflicts\n")
        for r in results:
            f.write(f"{int(r[0]*2*3600)},{int(r[1]*6*3600)},{r[2]}\n")
    print(f"Results saved in results/{file_name}")


if __name__ == "__main__":
    main()