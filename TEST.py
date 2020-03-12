import matplotlib.pyplot as plt
import numpy as np
from BayesianRegression import evaluate_performance, predict_dpi

data = np.load('/home/steven/Documents/Python/CryptoBot (3.5)/Trained Variables/2017-02-01 00:00:00 - 2017-10-31 23:59:59_5min.npz')
size = 24
centers = 100
clusters = 20
#X = generate_timeseries(x, size)
x = data['prices1'][20000:20500]
plt.plot(np.transpose(x))
plt.show()

#plt.plot(np.transpose(X))
#plt.show()

center3 = data['center3']
#center1 = find_cluster_centers(X, centers)
#print(center1.shape)
#print(center1[:,0])
#print(center1[:,size])
plt.plot(np.transpose(center3[:,0:size]))
plt.show()

cluster3 = data['cluster3']
#cluster1 = choose_effective_centers(center1, clusters, size)
#print(cluster1.shape)
plt.plot(np.transpose(cluster3[:,0:size]))
plt.show()

print(predict_dpi(x[:size], cluster3), data['prices3'][121] - data['prices3'][120])

dps = data['dps']
plt.plot(dps[0:500])
plt.show()

prices3 = data['prices3']
print(evaluate_performance(prices3, size, dps, t=197*10**-7, step=1))
#for i in range(1, 200, 1):
#    bank = evaluate_performance(prices3, size, dps, t=i*10**-7, step=1)
#    print('Bank balance: ', bank, 'Threshold=t (t^-6):', i)
