import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

cf = 0.030257421

# Channel 0
fin_0 = open('/home/tyler/DAQ/DAQ/watchman_spe/DAQ/run/FILTERED/0@DT5730 #2-11-586_Data_run.csv','r')
reader_0 = csv.reader(fin_0,delimiter=';')
header_0 = reader_0.next()
print header_0

# Channel 1
fin_1 = open('/home/tyler/DAQ/DAQ/watchman_spe/DAQ/run/FILTERED/1@DT5730 #2-11-586_Data_run.csv','r')
reader_1 = csv.reader(fin_1,delimiter=';')
header_1 = reader_1.next()
print header_1

icnt = 1
for row_0,row_1 in zip(reader_0,reader_1): 
    # Channel 0
    x_0 = row_0[4:]
    x1_0 = np.array([float(xi) for xi in x_0])
    x1m_0 = np.mean(x1_0)
    x1_0 = [(xi-x1m_0)*cf for xi in x1_0]
    t1_0 = np.arange(0,2*len(x1_0),2.0)
    
    # Channel 1
    x_1 = row_1[4:]
    x1_1 = np.array([float(xi) for xi in x_1])
    x1m_1 = np.mean(x1_1)
    x1_1 = [(xi-x1m_1)*cf for xi in x1_1]
    t1_1 = np.arange(0,2*len(x1_1),2.0)
        
    plt.plot(t1_0,x1_0)
    plt.plot(t1_1,x1_1)
    # plt.xlim(60,160)
    plt.ylim(-10,2)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    strt = './caen_spe_png/%05d.png' % (icnt-1)
    icnt+=1    
    fig.savefig(strt)
    # plt.show()
    plt.gcf().clear()

