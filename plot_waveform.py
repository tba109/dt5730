import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

# fin = open('/home/tyler/DAQ/run/UNFILTERED/0@DT5730 #2-11-586_Data_run.csv','r')
# fin = open('/home/tyler/DAQ/run/FILTERED/0@DT5730 #2-11-586_Data_run.csv','r')
fin = open('/home/tyler/DAQ/DAQ/pulse_100mV_100ns_2v/UNFILTERED/0@DT5730 #2-11-586_Data_pulse_100mV_100ns_2v.csv','r')
reader = csv.reader(fin,delimiter=';')
header = reader.next()
print header

x2 = []
i = 0
for row in reader: 
    x = row[4:]
    x1 = np.array([float(xi) for xi in x])
    plt.plot(x1)
    plt.show()

