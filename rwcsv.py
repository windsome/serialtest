# -*- coding:utf8 -*-
import csv
from datetime import datetime
from pytz import timezone

headers = ['Timestamp', 'Time', 'Pm25', 'Tvoc', 'Hcho', 'Co2', 'Temp', 'Hum']

def createCsv():
    now = datetime.now()
    central = timezone('Asia/Shanghai')
    loc_d = central.localize(now)
    csvname = str(loc_d) + '.csv'

    f = open(csvname,'w')
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    return f_csv

    # with open(csvname,'w') as f:
    #     f_csv = csv.DictWriter(f, headers)
    #     f_csv.writeheader()
    # return csvname

    
def writeCsv(csvname, rows):
    with open(csvname,'w+') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerows(rows)



if __name__ == '__main__':
    stream = createCsv()
    # csvname = createCsv()
    dt = datetime.now()
    timestamp = dt.timestamp()

    rows = [
        {'Timestamp':timestamp, 'Time': dt, 'Pm25':39.48, 'Tvoc':92.1, 'Hcho':92.1, 'Co2':0.18, 'Temp':18.1, 'Hum':50.1},
    ]
    stream.writerows(rows)

    # writeCsv( csvname, rows)