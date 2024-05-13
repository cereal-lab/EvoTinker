import sys
import pickle
import matplotlib.pyplot as plt

file_core1 = sys.argv[1]
if sys.arv[2]:
    file_core2 = sys.argv[2]

#root = 'Experiments Logs/'
root = ''
suffix = f''
file_name1 = root + file_core1 + suffix
if sys.argv[2]:
    file_name2 = root + file_core2 + suffix

with open(file_name1, 'rb') as f1:
    file_series1 = pickle.load(f1)

if sys.argv[2]:
    with open(file_name2, 'rb') as f2:
        file_series2 = pickle.load(f2)

x = [i for i in range(len(file_series1))]

plt.plot(x, file_series1, label='SSGA')
if sys.argv[2]:
    plt.plot(x, file_series2, label='RI-original')

#plt.title(f"Experiment 0a: Fitness vs. iterations")
plt.xlabel("Iteration Number")
plt.ylabel(f"Best Fitness (averaged)")
#plt.ylim(80,92)
#plt.xlim(49980, 50400)
plt.legend(loc='lower right')
#plt.savefig('exp0b.png')
plt.show()







