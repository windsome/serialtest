# -*- coding:utf8 -*-
import csv
from datetime import datetime
from pytz import timezone
import sys
import matplotlib.pyplot as plt
from random import random
import numpy as np
from time import sleep


headers = ['Timestamp', 'Time', 'Pm25', 'Tvoc', 'Hcho', 'Co2', 'Temp', 'Hum']

def openCsv(csvname):
    pm25 = []
    tvoc = []
    with open(csvname) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            print(row, row['Pm25'], row['Tvoc'])
            pm25 += [float(row['Pm25'])]
            tvoc += [float(row['Tvoc'])]
    return tvoc

def updateGraph2(list1, list2):
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签 
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    plt.title(u'tvoc对比(启动设备前后)')
    plt.xlabel(u'时间')
    plt.ylabel('tvoc')
    plt.cla()
    plt.plot(list1, label=u"tvoc-before")
    plt.plot(list2, label=u"tvoc-after")
    # plt.pause(0.01)
    plt.legend()
    plt.show()

def updateGraph1(list1):
    plt.title('tvoc值')
    plt.xlabel(u'时间')
    plt.ylabel(u'tvoc值')
    plt.cla()
    plt.plot(list1, label="tvoc")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    print ('参数个数为:', len(sys.argv), '个参数。')
    print ('参数列表:', str(sys.argv))
    file1 = sys.argv[1]
    print (file1)
    if len(sys.argv) > 2:
        file2 = sys.argv[2]
        tvoc2 = openCsv(file2)
        print (file2)
        tvoc1 = openCsv(file1)
        updateGraph2(tvoc1, tvoc2)
    else: 
        tvoc1 = openCsv(file1)
        updateGraph1(tvoc1)
    input('输入回车退出')

