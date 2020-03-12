'''
Trainer fits variables of the Bayesian Regression on collected data, to be used to forecast future price movements
'''

#import bigfloat as bg
import numpy as np
from datetime import datetime
from BayesianRegression import generate_timeseries, find_cluster_centers, choose_effective_centers, linear_regression_vars, find_parameters_w, predict_dps #, evaluate_performance
from Collector import collector

###########
#VARIABLES#
###########
currencyPair = 'BTC_ETH'
mapPeriod = 60          #interval length between ticks in seconds
Size1 = 30             #Size of first pattern (=SizeI * mapPeriod)
Size2 = 60             #Size of second pattern
Size3 = 120             #Size of third pattern
Clusters = 100          #Amount of clusters
EffectiveClusters = 20  #Amount of effective clusters
#1st Period
start1 = datetime(2017, 2, 1, 0, 0, 0)    #date(yyyy, mm, dd), NOTE: max 3 months
end1 = datetime(2017, 4, 30, 23, 59, 59)
#2nd Period
start2 = datetime(2017, 5, 1, 0, 0, 0)
end2 = datetime(2017, 7, 31, 23, 59, 59)
#3rd Period
start3 = datetime(2017, 8, 1, 0, 0, 0)
end3 = datetime(2017, 10, 31, 23, 59, 59)

##############
#COLLECT DATA#
##############
'''
Collector has difficulty handling large arrays: MemoryError (NOT on LINUX)
Collector sometimes encounters server errors
'''
prices1, v_buy1, v_sell1 = collector(currencyPair, start1, end1, mapPeriod)
prices2, v_buy2, v_sell2 = collector(currencyPair, start2, end2, mapPeriod)
prices3, v_buy3, v_sell3 = collector(currencyPair, start3, end3, mapPeriod)
print('Data Collected')

#####################
#GENERATE TIMESERIES#
#####################

timeseries1 = generate_timeseries(prices1, Size1)
timeseries2 = generate_timeseries(prices1, Size2)
timeseries3 = generate_timeseries(prices1, Size3)
print('Timeseries Generated')

#########################
#FIND EFFECTIVE CLUSTERS#
#########################

center1 = find_cluster_centers(timeseries1, Clusters)
center2 = find_cluster_centers(timeseries2, Clusters)
center3 = find_cluster_centers(timeseries3, Clusters)

cluster1 = choose_effective_centers(center1, EffectiveClusters, Size1)
cluster2 = choose_effective_centers(center2, EffectiveClusters, Size2)
cluster3 = choose_effective_centers(center3, EffectiveClusters, Size3)
print('Effective Clusters Found')

#####################
#ESTIMATE PARAMETERS#
#####################

X, Y = linear_regression_vars(prices2, v_buy2, v_sell2, Size1, Size2, Size3, cluster1, cluster2, cluster3)
w = find_parameters_w(X, Y)
print('Parameters Estimated:', w)

##########
#EVALUATE# (OPTIONAL)
##########

dps = predict_dps(prices3, v_buy3, v_sell3, Size1, Size2, Size3, cluster1, cluster2, cluster3, w)
'''
for i in range(0, 5, 1):
    bank = evaluate_performance(prices3, Size3, dps, t=0.0001*10**i, step=1)
    print('Bank balance: ', bank)
'''

#############
#SAVE OUTPUT#
#############

outfile = '/home/steven/Documents/Python/CryptoBot (3.5)/Trained Variables/' + str(start1) + ' - ' + str(end3) + '_60s.npz'
np.savez(outfile,timeseries1=timeseries1, timeseries2=timeseries2, timeseries3=timeseries3, prices1=prices1, prices2=prices2, prices3=prices3, v_buy3=v_buy3, v_sell3=v_sell3, center1=center1, center2=center2, center3=center3, cluster1=cluster1, cluster2=cluster2, cluster3=cluster3, X=X, Y=Y, w=w, dps=dps)
print('Output Saved')




