
import numpy as np
import matplotlib.pyplot as plt

data = np.load('/home/steven/Documents/Python/CryptoBot (3.5)/Trained Variables/2017-02-01 00:00:00 - 2017-10-31 23:59:59_5min.npz')
x = data['prices1'][-1000:]

x_min = [0]
for i in range(1, len(x)-1):
    if x[i]<x[i-1] and x[i]<x[i+1]:
        x_min.append(x[i])
    else :
        x_min.append(0)

x_max = [0]
for i in range(1, len(x)-1):
    if x[i]>x[i-1] and x[i]>x[i+1]:
        x_max.append(x[i])
    else :
        x_max.append(0)

#for i in range(1, len(x)):
    

plt.plot(x)
plt.plot(x_min)
plt.plot(x_max)
plt.show()