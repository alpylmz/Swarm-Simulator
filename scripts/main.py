from sim import Sim


sim = Sim(4)

while True:
    ret = sim.step()
    if ret == False:
        print("Simulation ended gracefully!")
        break