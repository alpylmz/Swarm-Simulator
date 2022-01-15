# importing libraries
import numpy as np
import time
import matplotlib.pyplot as plt
from sim import Sim

# creating initial data values
# of x and y
sim = Sim(5)
coords = sim.getCoords()

# to run GUI event loop
plt.ion()

# here we are creating sub plots
figure, ax = plt.subplots(figsize=(10, 10))
line1, = ax.plot([coord.x for coord in coords], [coord.y for coord in coords])

# setting title
plt.title("Alp's Simulator", fontsize=20)

# setting x-axis label and y-axis label
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# Loop
while True:
	coords = sim.step()
	
	# updating data values
	line1.set_xdata([coord.x for coord in coords])
	line1.set_ydata([coord.y for coord in coords])

	# drawing updated values
	figure.canvas.draw()

	# This will run the GUI event
	# loop until all UI events
	# currently waiting have been processed
	figure.canvas.flush_events()

	time.sleep(0.01)
