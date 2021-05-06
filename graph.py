# -*- coding:utf8 -*-

import matplotlib.pyplot as plt
from random import random
import numpy as np
from time import sleep


def updateGraph(list1, list2):
    plt.cla()
    plt.plot(list1)
    plt.plot(list2)
    plt.pause(0.01)


def graph2():
    POINTS = 60
    list1 = [0] * POINTS
    list2 = [0] * POINTS
    indx = 0
    # fig, ax = plt.subplots()
    while True:
        if indx == POINTS:
            indx = 0
        indx += 1
        # 更新绘图数据
        list1 = list1[1:] + [np.sin((indx / 20) * np.pi)]
        list2 = list2[1:] + [random()]
        updateGraph(list1, list2)
        sleep(2)


if __name__ == '__main__':
    graph2()
