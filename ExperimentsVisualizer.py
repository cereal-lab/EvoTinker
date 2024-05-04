import sys
import pickle
import matplotlib.pyplot as plt

file_core = sys.argv[1]

#root = 'Experiments Logs/'
root = ''
suffix = f'/experiment_best_plot.pickle'
file_name = root + file_core + suffix

with open(file_name, 'rb') as f:
    file_series = pickle.load(f)

x = [i for i in range(len(file_series))]

plt.plot(x, file_series)

# Set the title and labels of the plot
plt.title(f"Plotting average best fitness over number of iterations")
plt.xlabel("Iteration Number")
plt.ylabel(f"Best Fitness")

# Display the plot
plt.show()







