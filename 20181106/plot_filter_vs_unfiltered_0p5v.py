import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys
import itertools

cf = 0.030257421

fin_f = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_cfd/FILTERED/0@DT5730 #2-11-586_Data_run_0ns_cfd.csv','r')
reader_f = csv.reader(fin_f,delimiter=';')
header_f = reader_f.next()
print header_f

fin_u = open('/home/tyler/DAQ/20181106/DAQ/run_0ns_cfd/UNFILTERED/0@DT5730 #2-11-586_Data_run_0ns_cfd.csv','r')
reader_u = csv.reader(fin_u,delimiter=';')
header_u = reader_u.next()
print header_u

icnt = 1
x2 = np.zeros(496)
for row_f,row_u in itertools.izip(reader_f,reader_u): 
    x_f = row_f[4:]
    x1_f = np.array([float(xi) for xi in x_f])
    x1m_f = np.mean(x1_f)
    x1_f = [(xi-x1m_f)*cf for xi in x1_f]
    t1_f = np.arange(0,2*496,2)

    x_u = row_u[4:]
    x1_u = np.array([float(xi) for xi in x_u])
    x1m_u = np.mean(x1_u)
    x1_u = [(xi-x1m_u)*cf for xi in x1_u]
    t1_u = np.arange(0,2*496,2)
    
    plt.plot(t1_f,x1_f,'o-')
    plt.plot(t1_u,x1_u,'.')
    # plt.xlim(60,160)
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (mV)')
    fig = plt.gcf()
    strt = 'spe_%03d.png' % (icnt-1)
    icnt+=1    
    # fig.savefig(strt)
    plt.show()
    plt.gcf().clear()
