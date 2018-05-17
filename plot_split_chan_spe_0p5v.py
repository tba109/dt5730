import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

cf = 0.030257421

fin1 = open('/home/tyler/DAQ/DAQ/DAQ/split_chan_spe/UNFILTERED/0@DT5730 #2-11-586_Data_split_chan_spe.csv','r')
fin2 = open('/home/tyler/DAQ/DAQ/DAQ/split_chan_spe/UNFILTERED/1@DT5730 #2-11-586_Data_split_chan_spe.csv','r')
reader1 = csv.reader(fin1,delimiter=';')
reader2 = csv.reader(fin2,delimiter=';')
header1 = reader1.next()
header2 = reader2.next()
print header1
print header2

def cfd(x,d=1,n=4,plot=False): 

    bsln = np.mean([float(xi) for xi in x])
    x1 = np.array([float(xi) - bsln for xi in x])

    x1 = [(xi)*cf for xi in x1]
    t1 = np.arange(0,2*len(x1),2)
    

    x2 = np.zeros(len(t1)-n)
    t2 = np.arange(0,2*(len(x1)-n),2)
    for i in range(len(x2)): 
        xsum = 0
        for j in range(n-1): 
            xsum += x1[i+j]
        x2[i]=float(xsum)/float(n)

    num = '%03d' % icnt
    plt.text(120,-6,num,fontsize=20)
    plt.plot(t1,x1,'b')
    plt.plot(t2,x2,'g')
    # plt.ylim(-10,5)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    # fig.savefig(strt)
    # if(plot):
    #    plt.show()
    # plt.gcf().clear()

    x3 = [xi - xj for xi,xj in zip(x2[:-1*d],x2[d:])]
    t3 = t2[2:]
    plt.plot(t3,x3,'r')
    # plt.ylim(-10,5)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    strt = 'spe_%03d.png' % icnt
    
    # Find the 0 crossing time
    peaking = False
    i = 0
    for xi in x3: 
        if(xi > 0.5):
            peaking = True
        if(peaking and xi < 0):
            break
        i+=1
    
    if(i > len(x3)-1):
        tz = 2.*i
    else:
        # tz = (-2.*((x3[i] - (x3[i] - x3[i-1])*i)/(x3[i] - x3[i-1])))
        tz = (-2.* ( (i-1) - ( x3[i-1]/(x3[i]-x3[i-1]) ) ) )
    
    tzstr = '%f' % tz
    plt.text(240,-6,tzstr,fontsize=20)
    plt.ylim(-8,4)
    # fig.savefig(strt)
    if(plot): 
        plt.show()
    plt.gcf().clear()

    return  tz


# main    
NCNT = 10000
icnt = 0
tzero1 = np.array([])
for row1 in reader1: 
    # SPE
    x = row1[4:]
    bsln = np.mean([float(xi) for xi in x])
    x1 = np.array([float(xi) - bsln for xi in x])
    x1 = [(xi)*cf for xi in x1]
    if(icnt%100==0): print 'icnt=%d' % icnt
    icnt+=1
    for xi in x1:
        if(xi <= -2.1):
            if(False):
                tzero1 = np.append(tzero1,cfd(x,d=2,n=8,plot=True))
            else:    
                tzero1 = np.append(tzero1,cfd(x,d=2,n=8,plot=False))
            # print tzero1[-1]
            break
    if(icnt == NCNT): 
        break

icnt = 0
tzero2 = np.array([])
for row2 in reader2: 
    # SPE
    x = row2[4:]
    bsln = np.mean([float(xi) for xi in x])
    x1 = np.array([float(xi) - bsln for xi in x])
    x1 = [(xi)*cf for xi in x1]
    if(icnt%100==0): print 'icnt=%d' % icnt
    icnt+=1
    for xi in x1:
        if(xi <= -2.1):
            tzero2 = np.append(tzero2,cfd(x,d=2,n=8,plot=False))
            # print tzero2[-1]
            break
    if(icnt == NCNT): 
        break

print len(tzero1), len(tzero2)
    
td = [tz1 - tz2 for tz1,tz2 in zip(tzero1,tzero2)]
# plt.plot(td)
# plt.show()
print np.std(td)
# print td
h1 = TH1F("h1","",1000,-50,50)
for tdi in td: 
    h1.Fill(tdi)

h1.Draw()

