from sim import Sim
from time import sleep
from tqdm import tqdm
import matplotlib.pyplot as plt

multi_sim = False
if multi_sim == False:
    sim = Sim(4, plot_sim=True, beautiful_output=True)

    while True:
        ret = sim.step()
        if ret == False:
            break

else:
    repeat_count = 1000
    agent_count = 4
    average_error = dangerous_event_count = collision_count = 0.0

    for i in tqdm(range(repeat_count)):
        sim = Sim(agent_count, plot_sim = False, beautiful_output = None)

        while True:
            ret = sim.step()
            if ret == False:
                break

        output = sim.getSimOutput()
        try:
            average_error           += output["average error"]
            dangerous_event_count   += output["dangerous event count"]
            collision_count         += output["collision count"]
        except:
            pass

    print("average error is", average_error/repeat_count)
    print("dangerous event count is", dangerous_event_count)
    print("dangerous event probability is", dangerous_event_count/repeat_count)
    print("collision count is", collision_count)
    print("collision probability is", collision_count/repeat_count)
    