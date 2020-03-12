import matplotlib.pyplot as plt
import numpy as np
from BayesianRegression import evaluate_performance

#currencyPair = 'BTC_ETH'
Size1 = 180
Size2 = 360
Size3 = 720
#mapPeriod = 10

DPS = np.load('/home/steven/Documents/Python/CryptoBot (3.5)/Trained Variables/dps_1.npz')
dps = DPS['dps']
data = np.load('/home/steven/Documents/Python/CryptoBot (3.5)/Trained Variables/2017-08-01 00:00:00 - 2017-10-31 23:59:59_v2.npz')
prices3 = data['prices3']
v_buy3 = data['v_buy3']
v_sell3 = data['v_sell3']
cluster1 = data['cluster1']
cluster2 = data['cluster2']
cluster3 = data['cluster3']
w = data['w']
print('Data loaded...')

plt.plot(dps[0:100])
plt.show()

for i in range(1, 200, 1):
    bank = evaluate_performance(prices3, Size3, dps, t=i*10**-7, step=1)
    print('Bank balance: ', bank, 'Threshold=t (t^-6):', i)
