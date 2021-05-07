# -*- coding:utf8 -*-

import matplotlib.pyplot as plt
from random import random
import numpy as np
from time import sleep
from datetime import datetime
from pytz import timezone
import csv
import serial

headers = ['Timestamp', 'Time', 'Pm25', 'Tvoc', 'Hcho', 'Co2', 'Temp', 'Hum']

def updateGraph(list1, list2):
    plt.cla()
    plt.plot(list1)
    plt.plot(list2)
    plt.pause(0.01)
    plt.draw()

def createCsv():
    now = datetime.now()
    central = timezone('Asia/Shanghai')
    loc_d = central.localize(now)
    csvname = str(loc_d) + '.csv'

    f = open(csvname,'w')
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    return f_csv

def openSerial():
    serial0 = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)  #/dev/ttyUSB0
    if serial0.isOpen() :
        print("open success")
    else :
        print("open failed")
    return serial0

def wrserial(serial0):
    serial0.write([0x42, 0x4D, 0xAB, 0x00, 0x00, 0x01, 0x3A])
    sleep(0.1)
    data = serial0.read_all()
    return data

def dealReplyAB(data):
    # 查找到数据.
    # print(len(data),':',data)
    datalen = len(data)
    if datalen < 4:
        return

    cmdpos = -1
    for i in range(datalen):
        if (i+1) < datalen: 
            if data[i] == 0x42 and data[i+1] == 0x4D:
                cmdpos = i
    # if(cmdpos >= 0):
    #     print('find cmd ' + str(cmdpos))
    # 获取命令长度
    cmdlen = (data[cmdpos+2] << 8) + data[cmdpos+3] + 4
    if cmdpos + cmdlen > datalen:
        print('错误!命令起始%d+命令长度%d>数据长度%d'%(cmdpos, cmdlen, datalen))
        return
    # print('cmdpos:%d, cmdlen:%d'%(cmdpos, cmdlen))
    # 校验
    checksum = 0
    for i in range(cmdlen-2):
        checksum += data[cmdpos+i]
    checksum = checksum & 0xffff
    checksum2 = (data[cmdpos+cmdlen-2]<<8) + data[cmdpos+cmdlen-1]
    # print('checksum:%04x, cal:%04x'%(checksum2, checksum))
    # print(data)
    if (checksum != checksum2):
        print('错误!校验和不一致!')
        return
    # 读取数据.
    dict = {}
    # dict['Pm25'] = random() * 1000
    # dict['Tvoc'] = random() * 100
    dict['Pm25'] = (data[cmdpos+4]<<8) + data[cmdpos+5]
    dict['Tvoc'] = ((data[cmdpos+6]<<8) + data[cmdpos+7])/100
    dict['Hcho'] = ((data[cmdpos+9]<<8) + data[cmdpos+10])/100
    dict['Co2'] = (data[cmdpos+12]<<8) + data[cmdpos+13]
    dict['Temp'] = ((data[cmdpos+14]<<8) + data[cmdpos+15])/10
    dict['Hum'] = ((data[cmdpos+16]<<8) + data[cmdpos+17])/10
    print(dict)
    return dict


if __name__ == '__main__':
    # 初始化.
    stream0 = createCsv()
    serial0 = openSerial()

    POINTS = 90
    list1 = [0] * POINTS
    list2 = [0] * POINTS
    indx = 0
    # fig, ax = plt.subplots()
    while True:
        if indx == POINTS:
            # 监测时间到,退出
            indx = 0
            break
        # 从传感器读数据.
        data = wrserial(serial0)
        # data = [0x42, 0x4D, 0x00, 0x14, 0x01, 0x02, 0x00, 0x00, 
        #         0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 
        #         0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA9]
        # 解析数据
        data0 = dealReplyAB(data)
        if not data0:
            continue
        dt = datetime.now()
        timestamp = dt.timestamp()
        data0['Timestamp'] = timestamp
        data0['Time'] = dt
        # 写入csv
        stream0.writerow(data0)
        # 更新绘图数据
        list1 = list1[1:] + [data0['Tvoc']]
        list2 = list2[1:] + [data0['Hcho']]
        updateGraph(list1, list2)
        sleep(20)
        indx += 1

