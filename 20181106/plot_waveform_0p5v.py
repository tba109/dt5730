import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

cf = 0.030257421

fin = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_cfd/FILTERED/0@DT5730 #2-11-586_Data_run_0ns_cfd.csv','r')
reader = csv.reader(fin,delimiter=';')
header = reader.next()
print header

icnt = 1
x2 = np.zeros(496)
for row in reader: 
    x = row[4:]
    x1 = np.array([float(xi) for xi in x])
    x1m = np.mean(x1)
    x1 = [(xi-x1m)*cf for xi in x1]
    t1 = np.arange(0,2*496,2)
    # x2 = [(x2i*(icnt-1) + x1i)/icnt for x2i,x1i in zip(x2,x1)]
    # print len(t1)
    # num = '%03d' % icnt
    # plt.text(120,-6,num,fontsize=20)
    # plt.plot(t1[0:100],x1[0:100])
    # plt.plot(t1,x1)
    plt.plot(t1,x1,'.-')
    # plt.xlim(60,160)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    strt = 'spe_%03d.png' % (icnt-1)
    icnt+=1    
    # fig.savefig(strt)
    plt.show()
    plt.gcf().clear()

plt.xlabel('Time (ns)')
plt.ylabel('Amplitude (mV)')
plt.plot(t1,x2)
plt.show()
