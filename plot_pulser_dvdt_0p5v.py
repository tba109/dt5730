import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

fin = open('/home/tyler/DAQ/DAQ/pulser_noise_0p5v/UNFILTERED/0@DT5730 #2-11-586_Data_pulser_noise_0p5v.csv','r')
reader = csv.reader(fin,delimiter=';')
header = reader.next()
print header

x2 = []
xmean = np.zeros(496)
i = 0
for row in reader: 
    x = row[4:]
    # print len(x)
    x1 = np.array([float(xi) for xi in x])
    i+=1
    xmean = [(xm*(i-1) + xi)/i for xm,xi in zip(xmean,x1)] 
    # print xmean[0:10]
    # plt.plot(xmean[0:100])
    # plt.ylim(8080-100,8080+20)
    # plt.show()

print i
plt.plot(x1[0:100])
plt.ylim(8080-100,8080+20)
plt.show()

fout = open('./pulse_coupling.txt','w')
for xm in xmean: 
    strout = '%f\n' % xm
    fout.write(strout)
