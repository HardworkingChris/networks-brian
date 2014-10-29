'''
Hodgkin-Huxley model
Assuming area 1*cm**2
'''

from brian import *
from brian.library.ionic_currents import *

defaultclock.dt=.01*ms # more precise
# Parameters
Cm=1*uF # /cm**2
Iapp=2*uA
gL=0.1*msiemens
EL=-65*mV
ENa=55*mV
EK=-90*mV
gNa=35*msiemens
gK=9*msiemens

eqs = MembraneEquation(Cm) + leak_current(gL, EL)
eqs += K_current_HH(gK, EK) + Na_current_HH(gNa, ENa)
eqs += Current('Ia:amp')

eqs2='''
dv/dt=(-gNa*m**3*h*(v-ENa)-gK*n**4*(v-EK)-gL*(v-EL)+Iapp)/Cm : volt
m=alpham/(alpham+betam) : 1
alpham=-0.1/mV*(v+35*mV)/(exp(-0.1/mV*(v+35*mV))-1)/ms : Hz
betam=4*exp(-(v+60*mV)/(18*mV))/ms : Hz
dh/dt=5*(alphah*(1-h)-betah*h) : 1
alphah=0.07*exp(-(v+58*mV)/(20*mV))/ms : Hz
betah=1./(exp(-0.1/mV*(v+28*mV))+1)/ms : Hz
dn/dt=5*(alphan*(1-n)-betan*n) : 1
alphan=-0.01/mV*(v+34*mV)/(exp(-0.1/mV*(v+34*mV))-1)/ms : Hz
betan=0.125*exp(-(v+44*mV)/(80*mV))/ms : Hz
'''

neuron = NeuronGroup(1, eqs)
neuron2 = NeuronGroup(1, eqs2)

neuron.vm=-65*mV
neuron2.v=-65*mV
neuron2.h=1

trace = StateMonitor(neuron, 'vm', record=True)
trace2 = StateMonitor(neuron2, 'v', record=True)

neuron.Ia = Iapp
run(50 * ms, report='text')
subplot(2,1,1)
plot(trace.times / ms, trace[0] / mV)
subplot(2,1,2)
plot(trace2.times/ms, trace2[0]/mV)
show()
