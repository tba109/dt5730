import matplotlib.pyplot as plt
import numpy as np

x = [-69   , -142  , -216  , -289  , -363  , -463   , -508, -582]
y = [ 375.2,  299.8,  226.9,  154.5,   81.7,    9.76,    0,    0]

y2 = [np.abs(yi - 375.2 -69) for yi in y]
x2 = [np.abs(xi) for xi in x]

plt.plot(x2,y2,'.-')
plt.xlabel('Pulser Amplitude (mV)')
plt.ylabel('Digitizer Amplitude (mV)')
plt.xlim(0,650)
plt.ylim(0,500)
plt.show()
