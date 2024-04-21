import time
import numpy as np
from automata import Automata
import os
import sys
from typing import Optional, List
import random as rd
from generator.tp_generator import set_seed
from multiprocessing import Pool
import multiprocessing
from config import Config

from time import sleep

def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

def run(args):
    i, config = args
    
    print(f"Starting automata...")
    config.show()
    results = []
    for j in range(3):
        set_seed(9*10**6 + i*10 + j)
        automata = Automata(config)
        automata.advance_to(3600)
        results.append(automata._conflicts)

    pedestrian_arrival_rate = config.pedestrian_arrival_rate
    vehicle_arrival_rate = config.vehicle_arrival_rate
    return pedestrian_arrival_rate, vehicle_arrival_rate, sum(results)/len(results)

def build_configs() -> List[Config]:
    config = Config.new_from_env_file()
    configs = []
    for pedestrian_arrival_rate in np.linspace(50/(2*3600), 6000/(2*3600), 20):
        for vehicle_arrival_rate in np.linspace(50/(6*3600), 1400/(6*3600), 20):
            config_dup = config.duplicate()
            config_dup.pedestrian_arrival_rate = pedestrian_arrival_rate
            config_dup.vehicle_arrival_rate = vehicle_arrival_rate
            configs.append(config_dup)
    return configs

def main():
    print("Starting simulation...")
   
    configs = build_configs()

    with Pool(8) as p:
       results = p.map(run, zip(range(len(configs)), configs))
    
    print(f"Conflicts: {[r[2] for r in results]}")
    print(f"Average conflicts: {sum([r[2] for r in results])/len(results)}")

    t = time.localtime()
    with open(f"results/{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}-{t.tm_sec}.csv", "w") as f:
        f.write("pedestrian_arrival_rate,vehicle_arrival_rate,conflicts\n")
        for r in results:
            f.write(f"{int(r[0]*2*3600)},{int(r[1]*6*3600)},{r[2]}\n")


if __name__ == "__main__":
    main()