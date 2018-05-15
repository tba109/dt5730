import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys


fin = open('/home/tyler/DAQ/run/UNFILTERED/0@DT5730 #2-11-586_Data_run.csv','r')
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


h1 = TH1F("h1","",100,np.mean(x2)-100,np.mean(x2)+100)
for xi in x2: 
    h1.Fill(xi)

h1.GetXaxis().SetTitle("Flash ADC Samples")
h1.GetXaxis().CenterTitle()
h1.Draw()
f1 = TF1("f1","gaus")
h1.Fit(f1); 
