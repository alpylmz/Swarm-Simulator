from sim import Sim
from time import sleep


sim = Sim(4)

while True:
    print("step")
    ret = sim.step()
    if ret == False:
        print("Simulation ended gracefully!")
        break