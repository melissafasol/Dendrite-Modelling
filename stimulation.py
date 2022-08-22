from cell_properties import PyramidalCell
import neuron
from neuron import h
import matplotlib as plt

# Simulation parameters	
tstop = 600 #* ms simulation time (ms)
h.dt = 0.1 #* ms # integration step (ms)
vinit = -65 #* mV  # initial voltage (mV)

cell_0 = PyramidalCell(0)
cell_1 = PyramidalCell(1)
cell_2 = PyramidalCell(2)
cell_3 = PyramidalCell(3)
cell_4 = PyramidalCell(4)

#create a new synapse on cell 2 that will connect cell 1 and t 
#put synapse of cell 0 on apical dendrites 
syn_0 = h.ExpSyn(cell_0.apic1(0.5)) #two synapses - one with x_syn and one with NMDA
syn_0_NMDA = h.NMDA(cell_0.tuft(0.5))
syn_1 = h.ExpSyn(cell_1.apic1(0.5))
syn_1_NMDA = h.NMDA(cell_1.tuft(0.5))
syn_2 = h.ExpSyn(cell_2.apic1(0.5))
syn_2_NMDA = h.NMDA(cell_2.tuft1(0.5))
syn_3 = h.ExpSyn(cell_3.apic1(0.5))
syn_3_NMDA = h.NMDA(cell_3.apic1(0.5)) 
syn_4 = h.ExpSyn(cell_4.tuft1(0.5))
syn_4_NMDA = h.NMDA(cell_4.apic1(0.5))

# netcon object to connect cell 0 and 1 
ncon_0 = h.NetCon(cell_1.soma(0.5)._ref_v, syn_0, sec= cell_1.soma) #measure from the soma because this is what is typically done during ephys recordings
ncon_0_NMDA = h.NetCon(cell_1.soma(0.5)._ref_v, syn_0_NMDA, sec = cell_1.soma)
ncon_1 = h.Netcon(cell_2.soma(0.5)._ref_v, syn_1, sec = cell_2.soma)
ncon_1_NMDA = h.NetCon(cell_2.soma(0.5)._ref_v, syn_1_NMDA, sec = cell_2.soma)
ncon_2 = h.NetCon(cell_3.soma(0.5)._ref_v, syn_3, sec= cell_3.soma)
ncon_2_NMDA = h.NetCon(cell_3.soma(0.5)._ref_v, syn_2_NMDA, sec = cell_3.soma)
ncon_3 = h.Netcon(cell_4.soma(0.5)._ref_v, syn_2, sec = cell_4.soma)
ncon_3_NMDA = h.NetCon(cell_4.soma(0.5)._ref_v, syn_3_NMDA, sec = cell_4.soma)

#should cell 5 and cell 0 be connected through synapse?

#spike threshold to decide whether spike will be transmitted to the next cell 
ncon_0.threshold = -10
ncon_0_NMDA.threshold = -10 #is this threshold the same
ncon_1.threshold = -10
ncon_1_NMDA.threshold = -10
ncon_2.threshold = -10
ncon_2_NMDA.threshold = -10
ncon_3.threshold = -10
ncon_3_NMDA.threshold = -10

#delay of spike to next cell 
weight_NMDA = 0.03
weight_syn = 0.01

ncon_0.delay = 0
ncon_0.weight = weight_syn
ncon_0_NMDA.delay = 20
ncon_0_NMDA.weight[0] = weight_NMDA
ncon_1.delay = 0
ncon_1_NMDA.delay = 20
ncon_1.weight[0] = weight_syn
ncon_1_NMDA.weight[0] = weight_NMDA
ncon_2.delay = 0
ncon_2_NMDA.delay = 20
ncon_2.weight[0] = weight_syn
ncon_2_NMDA.weight[0] = weight_NMDA
ncon_3.delay = 0
ncon_3_NMDA.delay = 20
ncon_3.weight[0] = weight_syn
ncon_3_NMDA.weight[0] = weight_NMDA

# Create a current Clamp starting at 200 ms and with duration 5ms. Amplitude is an argument.     
ic = h.IClamp(cell_0.soma(0.5))
ic.delay = 200  # ms
ic.dur = 5  # ms
ic.amp = 0.2  # nA

# Include an EPSP
syn_0 = h.Exp2Syn(cell_0.apic1(0.5))
syn_0.tau1 = 0.1  # rise time #if synapse is NMDA tau1 = 10
syn_0.tau2 = 20  # decay time #if synapse is NMDA tau2 = 75ms - because takes much more current and time for magnesium ion to be removed from channel
syn_0.e = 0  # reversal potential of the synapse

syn_0_NMDA = h.NMDA


#========== ...create an artificial spike (an "event" to be delivered to the synapse)...
tsignal = 20
ns = h.NetStim(0.5)
ns.start = 200  # stimulus onset
ns.number = 1  # number of events

#... and connect the event to the synapse.
nc = h.NetCon(ns, syn)
nc.delay = 0  # synaptic delay (ms)
nc.weight[0] = 0.002  # synaptic weight (strength) - importance of synapse in overall potential 


cell_0_soma_vec = h.Vector().record(cell_0.soma(0.5)._ref_v)  #membrane potential vector
cell_0_trunk3_vec = h.Vector().record(cell_0.trunk3(0.5)._ref_v)  
cell_1_soma_vec = h.Vector().record(cell_1.soma(0.5)._ref_v)  
cell_1_trunk3_vec = h.Vector().record(cell_1.trunk3(0.5)._ref_v)  
cell_2_soma_vec = h.Vector().record(cell_2.soma(0.5)._ref_v)  
cell_2_trunk3_vec = h.Vector().record(cell_2.trunk3(0.5)._ref_v)  
cell_3_soma_vec = h.Vector().record(cell_3.soma(0.5)._ref_v)  
cell_3_trunk3_vec = h.Vector().record(cell_3.trunk3(0.5)._ref_v) 
cell_4_soma_vec = h.Vector().record(cell_4.soma(0.5)._ref_v)  
cell_4_trunk3_vec = h.Vector().record(cell_4.trunk3(0.5)._ref_v)  

t_vec = h.Vector().record(h._ref_t)  # Time stamp vector


# Run the simulation
h.finitialize(vinit)
h.continuerun(tstop)

# Remove the first 20ms to avoid artifacts
tremove = 20
cell_0_soma_vec.remove(0, int(tremove/h.dt))
cell_0_trunk3_vec.remove(0, int(tremove/h.dt))
cell_1_soma_vec.remove(0, int(tremove/h.dt))
cell_1_trunk3_vec.remove(0, int(tremove/h.dt))
cell_2_soma_vec.remove(0, int(tremove/h.dt))
cell_2_trunk3_vec.remove(0, int(tremove/h.dt))
cell_3_soma_vec.remove(0, int(tremove/h.dt))
cell_3_trunk3_vec.remove(0, int(tremove/h.dt))
cell_4_soma_vec.remove(0, int(tremove/h.dt))
cell_4_trunk3_vec.remove(0, int(tremove/h.dt))
t_vec.remove(0, int(tremove/h.dt))

plt.figure(figsize=(8, 6))
plt.plot(t_vec, cell_0_soma_vec, label='soma 0 ')
plt.plot(t_vec, cell_0_trunk3_vec, label='trunk3 0')
plt.plot(t_vec, cell_1_soma_vec, label='soma 1')
plt.plot(t_vec, cell_1_trunk3_vec, label='trunk3 1')
plt.plot(t_vec, cell_2_soma_vec, label='soma 2 ')
plt.plot(t_vec, cell_2_trunk3_vec, label='trunk3 2')
plt.plot(t_vec, cell_3_soma_vec, label='soma 3')
plt.plot(t_vec, cell_3_trunk3_vec, label='trunk3 3')
plt.plot(t_vec, cell_4_soma_vec, label='soma 4')
plt.plot(t_vec, cell_4_trunk3_vec, label='trunk3 4')

plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.legend()
plt.show()