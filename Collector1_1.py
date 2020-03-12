#from urllib.request import Request, urlopen
#import json
import requests
import time
#import bigfloat as bg
from datetime import datetime
from datetime import timedelta

def collector(currencyPair, start, end, mapPeriod):

    unixStart = int(time.mktime(start.timetuple()))
    unixEnd = int(time.mktime(end.timetuple()))
    unixPeriod = 86400         #seconds in a day (limit<max pull from url)

    #Collect tick-data in JSON list
    for i in range(unixStart, unixEnd, unixPeriod):
        endPeriod = i + unixPeriod
        url = 'https://poloniex.com/public?command=returnTradeHistory&currencyPair=' + currencyPair + '&start=' + str(i) + '&end=' + str(endPeriod)
        response = requests.get(url)        
        #req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        #webURL = urlopen(req)
        #response = webURL.read()
        #encoding = webURL.info().get_content_charset('utf-8')
        if i == unixStart:
            data = response.json()
            #ata = json.loads(response.decode(encoding))
        else:
            data = data + response.json()
            #data = data + json.loads(response.decode(encoding))
    #Sort data
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'))
    
    #Initialize variables to map to nearest (map)period
    listPrice = []
    listSellVolume = []
    listBuyVolume = []         
    rate = 0            #initialize rate
    sellVolume = 0      #initialize sellvolume
    buyVolume = 0       #initialize buyvolume
    mappedDate = datetime.strptime(sorted_data[0]['date'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds=mapPeriod) #initialize map period
    #Map tick-data to nearest mapPeriod interval
    for i in sorted_data:
        loopDate = datetime.strptime(i['date'], '%Y-%m-%d %H:%M:%S')
        if loopDate < mappedDate:
            rate = rate + float(i['rate'])*float(i['amount'])
            if i['type']=='buy': buyVolume = buyVolume + float(i['amount'])
            if i['type']=='sell': sellVolume = sellVolume + float(i['amount'])
        else:
            if buyVolume > 0 or sellVolume > 0: weightedRate = rate/(buyVolume + sellVolume)
            listPrice.append(weightedRate)
            listBuyVolume.append(buyVolume)
            listSellVolume.append(sellVolume)
            rate = 0
            buyVolume = 0
            sellVolume = 0
            mappedDate = mappedDate + timedelta(seconds=mapPeriod)    #2017-10-31 21:59:37
            
    return listPrice, listBuyVolume, listSellVolume