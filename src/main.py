import time
from automata import Automata
import os

def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    automata = Automata()
    for i in range(3600):
        automata.update()
        clear_output()
        automata.show()
        time.sleep(0.3)

if __name__ == "__main__":
    main()