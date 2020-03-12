#from urllib.request import Request, urlopen
#import json
import requests
import time
import csv
#import bigfloat as bg
from datetime import datetime
from datetime import timedelta

currencyPair = 'BTC_ETH'
start = datetime(2017, 8, 1, 0, 0, 0)    #date(yyyy, mm, dd), NOTE: max 3 months
end = datetime(2017, 8, 31, 23, 59, 59)
unixStart = int(time.mktime(start.timetuple()))
unixEnd = int(time.mktime(end.timetuple()))
unixPeriod = 86400         #seconds in a day (limit<max pull from url)
mapPeriod = 60

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
        #data = json.loads(response.decode(encoding))
    else:
        data = data + response.json()
#Sort data
sorted_data = sorted(data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'))

#Initialize variables to map to nearest (map)period
mapped_data = []           
rate = 0            #initialize rate
volume = 0          #initialize volume
mappedDate = datetime.strptime(sorted_data[0]['date'], '%Y-%m-%d %H:%M:%S') + timedelta(seconds=mapPeriod) #initialize map period
#Map tick-data to nearest mapPeriod interval
for i in sorted_data:
    loopDate = datetime.strptime(i['date'], '%Y-%m-%d %H:%M:%S')
    if loopDate < mappedDate:
        rate = rate + float(i['rate'])*float(i['amount'])
        volume = volume + float(i['amount'])
    else:
        if volume > 0: weightedRate = rate/volume
        entry = {'date':mappedDate.strftime('%Y-%m-%d %H:%M:%S'),'rate':weightedRate,'volume':volume}
        mapped_data.append(entry)
        
        rate = 0
        volume = 0
        mappedDate = mappedDate + timedelta(seconds=mapPeriod)    #2017-10-31 21:59:37


#Save JSON data to CSV
fname = '/home/steven/Documents/Charts' + start.strftime('%Y-%m-%d') + ' - ' + end.strftime('%Y-%m-%d') + ' ' + currencyPair + ' ' + str(mapPeriod) + 's.csv'
with open(fname,'w', newline='') as outf:
    outcsv = csv.DictWriter(outf, fieldnames=['date', 'rate', 'volume'])
    outcsv.writeheader()
    outcsv.writerows(mapped_data)