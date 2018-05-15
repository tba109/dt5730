import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

# Read the waveform from the scope. Averaged over 1000 traces
fscope = open('/home/tyler/Scope_Waveforms/F1--Trace--00000.txt')
rscope = csv.reader(fscope,delimiter=',')
for i in range(5): 
    print rscope.next()

tscope = []
xscope = []
for row in rscope: 
    tscope.append(float(row[0])*1.E9)
    xscope.append(float(row[1])*1.E3-6.78)
    
# plt.plot(tscope,xscope)
# plt.show()
# sys.exit()

# Read the waveform from caen
fcaen = open('/home/tyler/DAQ/DAQ/pulse_100mV_100ns_2v/UNFILTERED/0@DT5730 #2-11-586_Data_pulse_100mV_100ns_2v.csv','r')
rcaen = csv.reader(fcaen,delimiter=';')
hcaen = rcaen.next()
print hcaen
i=0
for row in rcaen: 
    xcaen = row[4:]
    xcaen = np.array([float(xi) for xi in xcaen])
    xcaen = [(xi - 8142)*(95./795.)*(94.76/93.55) for xi in xcaen]
    tcaen = np.arange(0,len(xcaen)*2,2)
    tcaen = [ti - 94.75 for ti in tcaen]
    plt.plot(tscope,xscope,'b')
    plt.plot(tcaen,xcaen,'r.-')
    # plt.xlim(tscope[0],tscope[-1])
    plt.xlim(tscope[0],200.)
    plt.xlabel("Time (ns)")
    plt.ylabel("Amplitude (mV)")
    fig = plt.gcf()
    strt = 'scope_vs_caen_%03d.png' % i
    fig.savefig(strt)
    # plt.show()
    plt.gcf().clear()
    print i
    i+=1

