from sim import Sim
from time import sleep


sim = Sim(4, plot_sim=True)

while True:
    ret = sim.step()
    if ret == False:
        print("Simulation ended gracefully!")
        break