import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1, TCanvas
import sys
import itertools

cf = 0.030257421

# analysis case
# ac = "0ns_unfilt_cfd"
# ac = "0ns_filt_cfd"
ac = "1ns_unfilt_cfd"
# ac = "1ns_filt_cfd"
# ac = "0ns_unfilt_led"
# ac = "0ns_filt_led"
# ac = "1ns_unfilt_led"
# ac = "1ns_filt_led"
# ac = "16ns_cable"

if ac == "0ns_unfilt_cfd":
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_cfd/UNFILTERED/0@DT5730 #2-11-586_Data_run_0ns_cfd.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_cfd/UNFILTERED/1@DT5730 #2-11-586_Data_run_0ns_cfd.csv','r')

if ac == "0ns_filt_cfd": 
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_cfd/FILTERED/0@DT5730 #2-11-586_Data_run_0ns_cfd.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_cfd/FILTERED/1@DT5730 #2-11-586_Data_run_0ns_cfd.csv','r')

if ac == "1ns_unfilt_cfd":
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_1ns_cfd/UNFILTERED/0@DT5730 #2-11-586_Data_run_1ns_cfd.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_1ns_cfd/UNFILTERED/1@DT5730 #2-11-586_Data_run_1ns_cfd.csv','r')

if ac == "1ns_filt_cfd": 
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_1ns_cfd/FILTERED/0@DT5730 #2-11-586_Data_run_1ns_cfd.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_1ns_cfd/FILTERED/1@DT5730 #2-11-586_Data_run_1ns_cfd.csv','r')

if ac == "0ns_unfilt_led":
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_led/UNFILTERED/0@DT5730 #2-11-586_Data_run_0ns_led.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_led/UNFILTERED/1@DT5730 #2-11-586_Data_run_0ns_led.csv','r')

if ac == "0ns_filt_led": 
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_led/FILTERED/0@DT5730 #2-11-586_Data_run_0ns_led.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_led/FILTERED/1@DT5730 #2-11-586_Data_run_0ns_led.csv','r')

if ac == "1ns_unfilt_led":
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_1ns_led/UNFILTERED/0@DT5730 #2-11-586_Data_run_1ns_led.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_1ns_led/UNFILTERED/1@DT5730 #2-11-586_Data_run_1ns_led.csv','r')

if ac == "1ns_filt_led": 
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_1ns_led/FILTERED/0@DT5730 #2-11-586_Data_run_1ns_led.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_1ns_led/FILTERED/1@DT5730 #2-11-586_Data_run_1ns_led.csv','r')

if ac == "16ns_cable": 
    fin0 = open('/home/tyler/DAQ/20181106/DAQ/run_cable_cal_16ns/UNFILTERED/0@DT5730 #2-11-586_Data_run_cable_cal_16ns.csv','r')
    fin1 = open('/home/tyler/DAQ/20181106/DAQ/run_cable_cal_16ns/UNFILTERED/1@DT5730 #2-11-586_Data_run_cable_cal_16ns.csv','r')


print ac

# CSV reader
reader0 = csv.reader(fin0,delimiter=';')
header0 = reader0.next()
reader1 = csv.reader(fin1,delimiter=';')
header1 = reader1.next()

icnt = 1
t0 = []
t1 = []
dt = []
nevt = 0
for row0,row1 in itertools.izip(reader0,reader1): 
    # Channel 0
    t0.append(float(row0[0]))
    flags0 = int(row0[3][2:],16)
    # if flags0 != 0x4080 and flags0 != 0x4000:
    #     print '0,%d,%04x' % (nevt,flags0)
    # Channel 1
    t1.append(float(row1[0]))
    flags1 = int(row1[3][2:],16)
    # if flags1 != 0x4080 and flags1 != 0x4000:
    #     print '1,%d,%04x' % (nevt,flags1)
    # print '%d,%04x,%04x' % (nevt,flags0,flags1)
    nevt+=1
    if nevt == 15000: 
        break
    if nevt%1000==0: 
        print nevt
    
i0=0
i1=0
while True: 
    dti = t0[i0] - t1[i1]
    # print dti
    if dti > -30000 and dti < 30000: # Make sure we have a match to 10ns 
        # print '%d,%d,%d' % (dti,i0,i1)
        dt.append(dti)
        i0+=1
        i1+=1        
    else: 
        # print '---------------------------------'
        # print '%d,%d,%d' % (dti,i0,i1)
        # print '---------------------------------'
        if dti > 0:
            i1+=1
        else: 
            i0+=1
    if i0 == len(t0) or i1 == len(t1): 
        # print 'done, %d %d' % (i0,i1)
        break
    
print 'len(dt) = %d' % len(dt)
# for it0,it1,idt in zip(t0,t1,dt):
#    print it0,it1,idt

print nevt
print np.std(dt)
print np.mean(dt)
plt.hist(dt,100)
plt.yscale('log', nonposy='clip')
plt.show()

plt.plot(dt,'o-')
plt.show()

plt.plot(t0,'o-')
plt.plot(t1,'o-')
plt.show()

c1 = TCanvas("c1")
h1 = TH1F("h1","",250,-2000+np.mean(dt),2000+np.mean(dt))
for idt in dt: 
    h1.Fill(idt)
c1.SetLogy()
h1.GetXaxis().SetTitle("Time Difference (ps)")
h1.GetXaxis().CenterTitle()
h1.GetYaxis().SetTitle("Number of Events")
h1.GetYaxis().CenterTitle()
h1.Draw()

raw_input()
