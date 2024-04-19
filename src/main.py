from automata import Automata
import os
import sys
from typing import Optional
from random import randint
from generator.tp_generator import set_seed

from time import sleep

def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_seed() -> Optional[int]:
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except:
            pass
    return None

def main():
    clear_output()

    seed = get_seed()
    if seed is None:
        seed = randint(4*10**6, 4*10**8)
    
    print(f"Using seed {seed}")
    set_seed(seed)

    print("Starting simulation...")

    automata = Automata()

    for i in range(1800):
        automata.update()
        clear_output()
        automata.show()
        sleep(0.05)
    
    print(f"Conflicts: {automata._conflicts}")
    east_facing_pedestrians_generated = automata._waiting_areas[0]._total_generated_pedestrians
    west_facing_pedestrians_generated = automata._waiting_areas[1]._total_generated_pedestrians
    passed_to_west = automata._grid._passed_to_west
    passed_to_east = automata._grid._passed_to_east
    print("Still passing to west:", west_facing_pedestrians_generated - passed_to_west)
    print("Still passing to east:", east_facing_pedestrians_generated - passed_to_east)


if __name__ == "__main__":
    main()