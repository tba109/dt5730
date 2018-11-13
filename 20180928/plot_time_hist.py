import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1, TCanvas
import sys

cf = 0.030257421

# Channel 0
fin0 = open('/home/tyler/DAQ/DAQ/watchman_spe/DAQ/run/FILTERED/0@DT5730 #2-11-586_Data_run.csv','r')
reader0 = csv.reader(fin0,delimiter=';')
header0 = reader0.next()
print header0

# Channel 1
fin1 = open('/home/tyler/DAQ/DAQ/watchman_spe/DAQ/run/FILTERED/1@DT5730 #2-11-586_Data_run.csv','r')
reader1 = csv.reader(fin1,delimiter=';')
header1 = reader1.next()
print header1

icnt = 1
t0 = []
t1 = []
dt = []
nevt = 0
for row0,row1 in zip(reader0,reader1): 
    # Channel 0
    t0.append(float(row0[0]))
        
    # Channel 1
    t1.append(float(row1[0]))
    dti = t0[-1] - t1[-1]
    if dti > -10000 and dti < 10000: 
        dt.append(dti)
    nevt+=1

# for it0,it1,idt in zip(t0,t1,dt):
#    print it0,it1,idt

print nevt
print np.std(dt)
print np.mean(dt)
# plt.hist(dt,100)
# plt.show()

c1 = TCanvas("c1")
h1 = TH1F("h1","",250,-2000,2000)
for idt in dt: 
    h1.Fill(idt)
c1.SetLogy()
h1.GetXaxis().SetTitle("Time Difference (ps)")
h1.GetXaxis().CenterTitle()
h1.GetYaxis().SetTitle("Number of Events")
h1.GetYaxis().CenterTitle()
h1.Draw()

raw_input()
