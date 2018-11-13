import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

# These were pulses going in a 100Hz, 100ns wide
# Result says 1bit = 1ps

cf = 0.121042459

fin = open('/home/tyler/DAQ/DAQ/tsamp_check/DAQ/run/FILTERED/0@DT5730 #2-11-586_Data_run.csv','r')
reader = csv.reader(fin,delimiter=';')
header = reader.next()
print header

icnt = 1
for row in reader: 
    iw1i = int(row[0])
    print iw1i
    x = row[4:]
    x1 = np.array([float(xi) for xi in x])
    x1 = [cf*xi for xi in x1]
    t1 = np.arange(0,2.*len(x1),2)
    # print len(t1)
    num = '%03d' % icnt
    plt.plot(t1,x1)
    # plt.ylim(-0.2,0.2)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    strt = 'spe_%03d.png' % (icnt-1)
    icnt+=1    
    # fig.savefig(strt)
    plt.show()
    plt.gcf().clear()
