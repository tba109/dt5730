import matplotlib.pyplot as plt
import numpy as np
import csv
from ROOT import TH1F, TF1
import sys

fname = './watchman_pmt_data/20181001/C1--waveforms--'

for i in range(500): 
    istr = '%05d' % i
    fname = './watchman_pmt_data/20181001/C1--waveforms--' + istr + '.txt'
    fscope = open(fname)
    rscope = csv.reader(fscope,delimiter=',')
    for i in range(5): 
        print rscope.next()
    tscope = []
    xscope = []
    for row in rscope: 
        tscope.append(float(row[0])*1.E9)
        xscope.append(float(row[1])*1.E3)

    if(min(xscope) < -1.):
        plt.plot(tscope,xscope)
        plt.ylabel('Amplitude (mV)')
        plt.xlim(500,650)
        plt.ylim(-10,1)
        plt.xlabel('Time (ns)')
        # plt.show()
        plt.savefig("scope_spe_gif/" + istr + ".png")
        plt.gcf().clear()
    fscope.close()
    
sys.exit()
