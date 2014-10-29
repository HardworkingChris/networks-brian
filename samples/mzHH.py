from brian import *
import brian_no_units
from time import time
from numpy import *
from scipy import *

Cm = 1
gL = 0.3
gK = 36
gNa = 120
VL = -54.402
VK = -77
VNa = 50
J1=10

eqs=Equations('''
dv/dt = (-gL*(v-VL)-gK*n*n*n*n*(v-VK)-gNa*h*m*m*m*(v-VNa)+J1)/Cm
dm/dt = (minfty-m)/(taum)
dn/dt = (ninfty-n)/(taun)
dh/dt = (hinfty-h)/(tauh)
alpham = 0.1*(v+40)/(1-exp(-0.1*(v+40)))
alphah = 0.07*exp(-0.05*(v+65))
alphan = 0.01*(v+55)/(1-exp(-0.1*(v+55)))
betam = 4.0*exp(-0.0556*(v+65))
betah = 1.0/(1+exp(-0.1*(v+35)))
betan = 0.125*exp(-0.0125*(v+65))
taum = 1.0/(alpham+betam)
taun = 1.0/(alphan+betan)
tauh = 1.0/(alphah+betah)
minfty = alpham*taum
ninfty = alphan*taun
hinfty = alphah*tauh
''')


P = NeuronGroup(1, model=eqs, method='RK', freeze=True)


M = SpikeMonitor(neuron1)
rate = PopulationRateMonitor(neuron1)

trace = StateMonitor(neuron1, 'v', record=True)
start_time=time()
run(duration)
print "Simulation time:",time()-start_time
clf()
figure(1)
subplot(221)
plot(rate.times,rate.rate)

run(100 * ms)
neuron.I = 10 * uA
run(100 * ms)
plot(trace.times / ms, trace[0] / mV)
plot(trace.times,trace[0])
show()


