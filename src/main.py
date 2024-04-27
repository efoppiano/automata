import time
from automata import Automata
import os

def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    automata = Automata(animate=True)
    for i in range(600):
        automata.update()
        clear_output()
        automata.show()
        time.sleep(0.2)

    print("Saving animation, this may take a while...")
    automata.save_mp4("animation2.mp4")

if __name__ == "__main__":
    main()