import time
import poloniex
import numpy as np
from datetime import datetime
from datetime import timedelta
from Collector import collector
from BayesianRegression import predict_dps as DPS

#TRADE VARIABLES
orderType = 'fillOrKill'    #fillOrKill, immediateOrCancel, postOnly
currencyBTC = 'BTC'         #always BTC
currencyX = 'ETH'          #variable currency
currencyPair = currencyBTC + '_' + currencyX

#DATA FETCH VARIABLES
mapPeriod = 300
Size1 = 6
Size2 = 12
Size3 = 24

#LOAD DATA
data = np.load('/home/steven/Documents/Python/CryptoBot (3.5)/Trained Variables/2017-02-01 00:00:00 - 2017-10-31 23:59:59_5min.npz')
w = data['w']
cluster1 = data['cluster1']
cluster2 = data['cluster2']
cluster3 = data['cluster3']

#RESET API KEYS REGULARLY
polo = poloniex.Poloniex('SECRET-POST-TOKEN','SECRET-GET-TOKEN')

#Fetch balances and rates
balances    = polo('returnBalances')
balanceBTC  = balances[currencyBTC]
balanceX    = balances[currencyX]

#for i in range(5, 50, 3):    #Possibility to loop over thresholds
    
#SET TRADE MARKER
position = 1
pl = 0
#TIMER VARIABLES
startTime = time.time()
runPeriod = 60*60*0.25 #seconds*minutes*hours (total in seconds)
endTime = startTime + runPeriod
freq = 290 #frequency of data refresh NOTE: doesn't have to be the same as MapPeriod
#THRESHOLD
t = 197*10**-7
while True:

    #COLLECTION TIME VARIABLES
    end = datetime.now()
    start = end - timedelta(seconds=(Size3 + 2)*mapPeriod)
    
    #GET DATA
    prices, v_buy, v_sell = collector(currencyPair, start, end, mapPeriod)
    #trueDps = prices[0] - prices[1]
    
    #FORECAST DPS
    dps = DPS(prices, v_buy, v_sell, Size1, Size2, Size3, cluster1, cluster2, cluster3, w)
    #print('Dps:', dps, 'Actual', trueDps)
    
    #TRADING STRATEGY
    if dps < -t and position == 1: #SELL
        bid = float(polo('returnTicker')[currencyPair]['highestBid'])   #what you pay (converted to float)
        position = -1
        pl = pl + bid
        print('P/L:', pl)
        
    if dps > t and position == -1: #BUY
        ask = float(polo('returnTicker')[currencyPair]['lowestAsk'])  #what you get (converted to float)
        position = 1
        pl = pl - ask
        print('P/L:', pl)
    
    #TIMER BREAK CONDITION
    if time.time() > endTime:
        if position == -1: pl = pl - float(polo('returnTicker')[currencyPair]['lowestAsk'])
        print('BOT TERMINATED')
        print('P/L:', pl, 'Threshold:', t)
        break
    #TIMER
    time.sleep(freq - ((time.time() - startTime) % freq))
