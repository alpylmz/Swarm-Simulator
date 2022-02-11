import matplotlib.pyplot as plt


average_errors =        [653.62, 232.05, 373.61]
dangerous_event_count = [98.0, 26.0,      27.0]
collision_count =       [25, 8.0,         9]

algos = ["Default", "State Machine", "Sliding Method"]
# draw average errors in a bar chart
plt.bar(algos, average_errors, align='center')
plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)
plt.title("Average Errors for Different Algorithms", fontsize = 20)
plt.xlabel("Algorithms", fontsize = 20)
plt.ylabel("Average Error", fontsize = 20)
plt.show()

#draw_average_errors_graph(["A", "B", "C", "D"], average_errors, "Average errors")