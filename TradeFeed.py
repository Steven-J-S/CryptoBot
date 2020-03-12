import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
from Collector import collector

#Currencypair
currencyBTC = 'BTC'         #always BTC
currencyX = 'ETH'          #variable currency
currencyPair = currencyBTC + '_' + currencyX
#TIMER VARIABLES
startTime = time.time()
runPeriod = 60*60*0.25 #seconds*minutes*hours (total in seconds)
endTime = startTime + runPeriod
freq = 10 #frequency of data refresh NOTE: doesn't have to be the same as MapPeriod
#THRESHOLD
t = 197*10**-7
#Data Mapping Variables
mapPeriod = 60
Size = 24

while True :
    
    #COLLECTION TIME VARIABLES
    end = datetime.now()
    start = end - timedelta(seconds=(Size + 2)*mapPeriod)
    prices, v_buy, v_sell = collector(currencyPair, start, end, mapPeriod)
    
    #Live Feed Prices
    plt.close()
    plt.plot(prices)
    plt.show()
    
    #TIMER BREAK CONDITION
    if time.time() > endTime:
        break
    #TIMER
    time.sleep(freq - ((time.time() - startTime) % freq))
    