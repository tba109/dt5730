#######################################################################################
# Tyler Anderson Fri May 18 09:57:58 EDT 2018
# Update for Watchman PMT data: Wed Oct  3 11:46:42 EDT 2018
# Plot data from the channels and do some timing analysis
# 
#
#######################################################################################

import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys
import itertools

###############################################################################################
# Program parameters
cf = 0.030257421 # 0.5V range LSB to mV conversion factor
NCNT = 5000
icnt = 0
inspect = False
iinspect = 15
force_plot = False

###############################################################################################
# Box car averager
def box_car(x,n): 
    x1 = np.zeros(len(x)-n)
    for i in range(len(x1)): 
        xsum = 0
        for j in range(n): 
            xsum += x[n+i-j]
        x1[i]=float(xsum)/float(n)
        # print i-n+1
    # sys.exit()    
    return x1

###############################################################################################
# Constant fraction discriminator
def cfd(x,d=1,n=4,plot=False,ch=0,icnt=0): 
    x1 = x
    t1 = np.arange(0,2*len(x1),2)

    # Box car average
    x2 = box_car(x1,n)
    t2 = np.arange(2.*n,2*(len(x1)),2)
    
    num = '%03d, %03d' % (icnt,ch)
    plt.text(200,-4,num,fontsize=20)
    plt.plot(t1,x1,marker='o',color='b')
    plt.plot(t2,x2,marker='o',color='g')
    # plt.ylim(-10,5)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    # fig.savefig(strt)
    # if(plot):
    #    plt.show()
    # plt.gcf().clear()

    # Differentiate
    x3 = [xi - xj for xi,xj in zip(x2[:-1*d],x2[d:])]
    t3 = t2[d:]
    plt.plot(t3,x3,marker='o',color='r')
    plt.ylim(-10,5)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    strt = 'spe_%03d.png' % icnt

    # average again
    # x4 = box_car(x3,n)
    x4 = x3
    t4 = t3

    # average again
    # x5 = box_car(x4,n)
    x5 = x4
    t5 = t4

    # Find the 0 crossing time
    peaking = False
    i = 0
    for xi in x5: 
        if(xi > 1.):
            peaking = True
        if(peaking and xi < 0):
            break
        i+=1
    
    if(i > len(x5)-1):
        tz = 2.*i
    else:
        tz = -x5[i-1]/(x5[i] - x5[i-1])*2. + t5[i-1]
    
    tzstr = '%.3fns' % tz
    plt.text(200,-5,tzstr,fontsize=20)
    plt.xlim(0,400)
    plt.axhline()
    plt.axvline(tz)

    # plt.ylim(-8,4)
    if(plot): 
        plt.show()
        # fig.savefig(strt)
    plt.gcf().clear()

    return  tz

###############################################################################################
# Trigger and Time Filter
# x: float representing waveform samples (units = mV)
# thr: threshold for detection (negative edge, mV)
# d: number of samples for CFD delay
# n: number of samples for boxcar averager
# plot: bool representing whether the data should be plotted
# ch: channel number
# icnt: loop number
# force: bool which forces analysis (good when found in one of the channels)
# Return: True and zero time crossing
#         False and -1000
def ttf(x,thr=-2.1,d=1,n=4,plot=False,ch=0,icnt=0,force=False):
    bsln = np.mean([xi for xi in x[0:10]])
    x1 = np.array([xi - bsln for xi in x])
    if(force): 
        return True, cfd(x1,d,n,True,ch,icnt), bsln
    else:     
        for xi in x1:
            if(xi <= thr):
                cfd_res = cfd(x1,d,n,plot,ch,icnt)
                return True, cfd_res, bsln
    return False, -1000, bsln

###############################################################################################
# main    
tzero1 = np.array([])
tzero2 = np.array([])
iw1 = np.array([])
iw2 = np.array([])

fin1 = open('/home/tyler/DAQ/DAQ/watchman_spe/DAQ/run/FILTERED/0@DT5730 #2-11-586_Data_run.csv','r')
fin2 = open('/home/tyler/DAQ/DAQ/watchman_spe/DAQ/run/FILTERED/1@DT5730 #2-11-586_Data_run.csv','r')
reader1 = csv.reader(fin1,delimiter=';')
reader2 = csv.reader(fin2,delimiter=';')
header1 = reader1.next()
header2 = reader2.next()
print header1
print header2

b1 = []
b2 = []

for row1,row2 in itertools.izip(reader1,reader2): 
    x1 = row1[4:]
    x1 = np.array([float(xi)*cf for xi in x1])
    x2 = row2[4:]
    x2 = np.array([float(xi)*cf for xi in x2])
    # print row1[0:4],row2[0:4]
    iw1i = int(row1[0])
    iw2i = int(row2[0])
    # print '%012x %012x' % (iw1i, iw2i)
    if(icnt%100==0): print 'icnt=%d' % icnt    

    # plt.plot(x1); plt.plot(x2); tx = '%d' % icnt; plt.text(120,244,tx,fontsize=20); plt.show()
    plot = False
    if((inspect and icnt==iinspect) or force_plot): 
        plot = True

    # processing ch0
    found1 = False
    found1,tz1,b1i = ttf(x1,thr=-1,d=4,n=2,plot=plot,ch=0,icnt=icnt,force=False)
    if(found1): 
        # tzero1 = np.append(tzero1,tz1 + float(int(iw1i) >> 10))
        tzero1 = np.append(tzero1,tz1)
        iw1 = np.append(iw1,iw1i)
        b1.append(b1i)

    found2 = False
    found2,tz2,b2i = ttf(x2,thr=-1,d=4,n=2,plot=plot,ch=1,icnt=icnt,force=False)
    if(found2): 
        # tzero2 = np.append(tzero2,tz2 + float(int(iw2i) >> 10))
        tzero2 = np.append(tzero2,tz2)
        iw2 = np.append(iw2,iw2i)
        b2.append(b2i)
    
    # if(tz1-tz2 > 0): 
    #     ttf(x1,thr=-1,d=4,n=2,plot=True,ch=0,icnt=icnt,force=False)
    #     ttf(x2,thr=-1,d=4,n=2,plot=True,ch=0,icnt=icnt,force=False)

    icnt+=1
    if(icnt == NCNT): 
        break
    
print len(tzero1), len(tzero2), len(iw1), len(iw2)

td = [tz1i - tz2i for tz1i,tz2i in zip(tzero1,tzero2)]

h1 = TH1F("h1","",1000,-50,50)
i = 0
for tdi,iw1i,iw2i in zip(td,iw1,iw2): 
    h1.Fill(tdi)
    i+=1

# h2 = TH1F("h2","",1000,-50,50)
h2 = TH1F("h2","",1000,-50,50)
# h2.SetLineColor(2)
h2.GetXaxis().CenterTitle()
i = 0
for tdi,iw1i,iw2i in zip(td,iw1,iw2): 
    if((int(iw1i) & 0xffff0000) == (int(iw2i) & 0xffff0000)):
        h2.Fill(tdi)
        i+=1
    else: 
        "time word difference"

diw12 = []
for iw1i, iw2i in zip(iw1,iw2): 
    diw12.append(float(iw1i-iw2i)/1000.)

plt.plot(td,'o')
plt.plot(diw12,'o')
plt.show()

plt.plot(b1,'-o')
plt.plot(b2,'-o')
plt.show()

plt.plot(b1,iw1)
plt.show()

plt.plot(b2,iw2)
plt.show()

h2.GetXaxis().SetTitle("CFD CH0-CH1 #deltaT (ns)")
h2.GetXaxis().CenterTitle()
# h1.Draw()
# h2.Draw("same")

plt.plot([(int(iw1i) >> 10) - (int(iw2i) >> 10) for iw1i,iw2i in zip(iw1,iw2)],'-o')
plt.ylim(-5,5)
plt.show()

h2.Draw("")
f1 = TF1("f1","gaus")
h2.Fit(f1)

raw_input()
