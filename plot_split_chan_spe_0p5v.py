import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

# 0.5V range LSB to mV conversion factor
cf = 0.030257421

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

def cfd(x,d=1,n=4,plot=False): 

    bsln = np.mean([float(xi) for xi in x[0:100]])
    x1 = np.array([float(xi) - bsln for xi in x])

    x1 = [(xi)*cf for xi in x1]
    t1 = np.arange(0,2*len(x1),2)

    # Box car average
    x2 = box_car(x1,n)
    t2 = np.arange(2.*n,2*(len(x1)),2)
    # for i in range(n-1,len(x2)): 
    #     xsum = 0
    #     for j in range(n): 
    #         xsum += x1[i-j]
    #     x2[i]=float(xsum)/float(n)

    num = '%03d' % icnt
    plt.text(200,-6,num,fontsize=20)
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

    # Differentiate
    x3 = [xi - xj for xi,xj in zip(x2[:-1*d],x2[d:])]
    t3 = t2[d:]
    plt.plot(t3,x3,'r')
    # plt.ylim(-10,5)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    strt = 'spe_%03d.png' % icnt

    # average again
    # x4 = box_car(x3,n)
    x4 = x3

    # average again
    # x5 = box_car(x4,n)
    x5 = x4

    # Find the 0 crossing time
    peaking = False
    i = 0
    for xi in x5: 
        if(xi > 0.5):
            peaking = True
        if(peaking and xi < 0):
            break
        i+=1
    
    if(i > len(x5)-1):
        tz = 2.*i
    else:
        tz = (-2.* ( (i-1) - ( x5[i-1]/(x5[i]-x5[i-1]) ) ) )
    
    tzstr = '%.3fns' % tz
    plt.text(320,-6,tzstr,fontsize=20)
    plt.xlim(150,400)
    plt.ylim(-8,4)
    if(plot): 
        plt.show()
        # fig.savefig(strt)
    plt.gcf().clear()

    return  tz


fin1 = open('/home/tyler/DAQ/DAQ/DAQ/split_chan_spe/UNFILTERED/0@DT5730 #2-11-586_Data_split_chan_spe.csv','r')
fin2 = open('/home/tyler/DAQ/DAQ/DAQ/split_chan_spe/UNFILTERED/1@DT5730 #2-11-586_Data_split_chan_spe.csv','r')
reader1 = csv.reader(fin1,delimiter=';')
reader2 = csv.reader(fin2,delimiter=';')
header1 = reader1.next()
header2 = reader2.next()
print header1
print header2


# main    
NCNT = 20000
icnt = 0
tzero1 = np.array([])
iw1 = np.array([])
inspect = False
iinspect = 55
for row1 in reader1: 
    # SPE
    x = row1[4:]
    bsln = np.mean([float(xi) for xi in x[0:100]])
    x1 = np.array([float(xi) - bsln for xi in x])
    x1 = [(xi)*cf for xi in x1]
    if(icnt%100==0): print 'icnt=%d' % icnt    
    if(inspect and icnt==iinspect): cfd(x,d=4,n=8,plot=True)
    for xi in x1:
        if(xi <= -2.1):
            tzero1 = np.append(tzero1,cfd(x,d=4,n=8,plot=False))
            iw1 = np.append(iw1,icnt)
            break
    icnt+=1
    if(icnt == NCNT): 
        break
    
icnt = 0
tzero2 = np.array([])
iw2 = np.array([])
for row2 in reader2: 
    # SPE
    x = row2[4:]
    bsln = np.mean([float(xi) for xi in x[0:100]])
    x1 = np.array([float(xi) - bsln for xi in x])
    x1 = [(xi)*cf for xi in x1]
    if(icnt%100==0): print 'icnt=%d' % icnt
    if(inspect and icnt==iinspect): cfd(x,d=4,n=8,plot=True)
    for xi in x1:
        if(xi <= -2.1):
            tzero2 = np.append(tzero2,cfd(x,d=4,n=8,plot=False))
            iw2 = np.append(iw2,icnt)
            break
    icnt+=1
    if(icnt == NCNT): 
        break

print len(tzero1), len(tzero2), len(iw1)

fout = open("fout.txt",'w')    
td = [tz1 - tz2 for tz1,tz2 in zip(tzero1,tzero2)]
plt.plot(td)
plt.show()
print np.std(td)
# print td
h1 = TH1F("h1","",1000,-50,50)
i = 0
for tdi,iwi in zip(td,iw1): 
    h1.Fill(tdi)
    if(tdi > 0.5 or tdi < -0.5):
        strout = "%d %f\n" % (iwi,tdi)
        fout.write(strout)
    i+=1

fout.close()

h1.GetXaxis().SetTitle("CFD CH0-CH1 #deltaT (ns)")
h1.Draw()
f1 = TF1("f1","gaus")
h1.Fit(f1)
