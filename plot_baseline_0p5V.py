import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

fin = open('/home/tyler/DAQ/DAQ/baseline_0p5v/UNFILTERED/0@DT5730 #2-11-586_Data_baseline_0p5v.csv','r')
reader = csv.reader(fin,delimiter=';')
header = reader.next()
print header

h1 = TH1F("h1","",1000,8080-100,8080+100)

x2 = []
i = 0
for row in reader: 
    x = row[4:]
    x1 = np.array([float(xi) for xi in x])
    for xi in x1: 
        x2.append(xi)

xmu = np.mean(x2)
cf = 0.030257421
x3 = [(xi - xmu)*cf for xi in x2]

lo = np.mean(x3) - 2
hi = np.mean(x3) + 2
nb = int((hi-lo)/cf) + 1
h1 = TH1F("h1","",nb,lo,hi)
for xi in x3: 
    h1.Fill(xi)

h1.GetXaxis().SetTitle("Baseline (mV)")
h1.GetXaxis().CenterTitle()
h1.Draw()
f1 = TF1("f1","gaus")
f1.SetNpx(10000)
h1.Fit(f1); 
