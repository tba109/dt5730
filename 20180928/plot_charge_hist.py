import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1, TCanvas
import sys

# Channel 0
# fin = open('/home/tyler/dt5730/20180928/watchman_pmt_data/20180928/F2--F2_peak_minus_ped--00000.txt','r')
fin = open('/home/tyler/dt5730/20180928/watchman_pmt_data/20181001/F2--waveforms--00000.txt','r')
reader = csv.reader(fin,delimiter=',')
for i in range(6): 
    header = reader.next()
    print header

q0 = []
nevt = 0
for row in reader: 
    q0.append(float(row[1])/(-50.*1.6E-19))
    nevt+=1

# print nevt
# print np.std(q0)
# print np.mean(q0)
# plt.hist(q0,100)
# plt.show()

c1 = TCanvas("c1")
h1 = TH1F("h1","",100,-1.E6,20.E6)
for iq0 in q0: 
    h1.Fill(iq0)
c1.SetLogy()
h1.GetXaxis().SetTitle("SPE Gain")
h1.GetXaxis().CenterTitle()
h1.GetYaxis().SetTitle("Number of Events")
h1.GetYaxis().CenterTitle()
h1.Draw()

raw_input()
