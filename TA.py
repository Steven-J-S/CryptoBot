import numpy as np
import talib
from talib import MA_Type
import matplotlib.pyplot as plt
#from datetime import datetime
#from Collector import collector

#print(talib.get_functions())

data = np.load('/home/steven/Documents/Python/CryptoBot (3.5)/Trained Variables/2017-02-01 00:00:00 - 2017-10-31 23:59:59_5min.npz')
prices1 = data['prices1'][24633:25633]
upper, middle, lower = talib._ta_lib.BBANDS(prices1, MA_Type.T3)
mom = talib._ta_lib.MOM(prices1)
print(len(prices1))
plt.plot(prices1)
#plt.plot(upper)
#plt.plot(middle)
#plt.plot(lower)
#plt.plot(mom)
plt.show()