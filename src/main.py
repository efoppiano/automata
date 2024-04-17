from automata import Automata
import os

from time import sleep

def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Starting simulation...")
    clear_output()

    automata = Automata(8, 42)
    
    for i in range(1000):
        automata.update()
        clear_output()
        automata.show()
        # print()
        sleep(1)
    
    east_facing_pedestrians_generated = automata._waiting_area_west._total_generated_pedestrians
    west_facing_pedestrians_generated = automata._waiting_area_east._total_generated_pedestrians
    passed_to_west = automata._grid._passed_to_west
    passed_to_east = automata._grid._passed_to_east
    print("Still passing to west:", west_facing_pedestrians_generated - passed_to_west)
    print("Still passing to east:", east_facing_pedestrians_generated - passed_to_east)


if __name__ == "__main__":
    main()