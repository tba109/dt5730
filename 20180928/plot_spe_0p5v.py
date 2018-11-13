import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

cf = 0.030257421

fin0 = open('/home/tyler/DAQ/DAQ/watchman_spe/DAQ/run/FILTERED/0@DT5730 #2-11-586_Data_run.csv','r')
reader0 = csv.reader(fin,delimiter=';')
header0 = reader.next()
print header

icnt = 0
for row in reader: 
    x = row[4:]
    x1 = np.array([float(xi) for xi in x])
    x1 = [(xi - xpc)*cf for xi,xpc in zip(x1,xp)]
    for i in np.arange(40,43,1): 
        if x1[i] < -1.25:
            t1 = np.arange(0,2*496,2)
            # print len(t1)
            num = '%03d' % icnt
            plt.text(120,-6,num,fontsize=20)
            plt.plot(t1[0:100],x1[0:100])
            plt.ylim(-10,5)
            plt.xlabel('Time (ns)')
            plt.ylabel('Amplitude (mV)')
            fig = plt.gcf()
            strt = 'spe_%03d.png' % icnt
            icnt+=1
            fig.savefig(strt)
            # plt.show()
            plt.gcf().clear()
            break
