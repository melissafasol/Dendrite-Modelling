from cell_properties import PyramidalCell
import neuron
from neuron import h
import matplotlib.pyplot as plt

# Simulation parameters	
tstop = 600 #* ms simulation time (ms)
h.dt = 0.1 #* ms # integration step (ms)
vinit = -65 #* mV  # initial voltage (mV)

#pyr_cells = [PyramidalCell(i) for i in range(5)]
#pyr_cells[0].apic1(0.5)

pyr_cells = [PyramidalCell(i) for i in range(5)]
print(pyr_cells)

#create a new synapse on cell 2 that will connect cell 1 and t 
#put synapse of cell 0 on apical dendrites 

synapses = h.ExpSyn(pyr_cells[i].apic1(0.5) for i in range(5))
print(synapses)
NMDA_synapses = h.NMDA(pyr_cells[i].tuft1(0.5) for i in range(5))
print(NMDA_synapses)

# netcon object to connect cell 0 and 1 

ncon_0 = h.NetCon(cell_1.soma(0.5)._ref_v, syn_0, sec= cell_1.soma) #measure from the soma because this is what is typically done during ephys recordings
ncon_0_NMDA = h.NetCon(cell_1.soma(0.5)._ref_v, syn_0_NMDA, sec = cell_1.soma)
ncon_1 = h.NetCon(cell_2.soma(0.5)._ref_v, syn_1, sec = cell_2.soma)
ncon_1_NMDA = h.NetCon(cell_2.soma(0.5)._ref_v, syn_1_NMDA, sec = cell_2.soma)
ncon_2 = h.NetCon(cell_3.soma(0.5)._ref_v, syn_3, sec= cell_3.soma)
ncon_2_NMDA = h.NetCon(cell_3.soma(0.5)._ref_v, syn_2_NMDA, sec = cell_3.soma)
ncon_3 = h.NetCon(cell_4.soma(0.5)._ref_v, syn_2, sec = cell_4.soma)
ncon_3_NMDA = h.NetCon(cell_4.soma(0.5)._ref_v, syn_3_NMDA, sec = cell_4.soma)
ncon_4 = h.NetCon(cell_0.soma(0.5)._ref_v, syn_4, sec = cell_0.soma)
#should cell 5 and cell 0 be connected through synapse?

#spike threshold to decide whether spike will be transmitted to the next cell 

# assume a list ncon_list
for ncon in ncon_list:
    ncon.threshold = -10

ncon_0.threshold = -10
ncon_0_NMDA.threshold = -10 #is this threshold the same
ncon_1.threshold = -10
ncon_1_NMDA.threshold = -10
ncon_2.threshold = -10
ncon_2_NMDA.threshold = -10
ncon_3.threshold = -10
ncon_3_NMDA.threshold = -10
ncon_4.threshold = -10

#delay of spike to next cell 
weight_NMDA = 0.03
weight_syn = 0.01

ncon_0.delay = 0
ncon_0.weight[0] = weight_syn
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
ncon_4.weight[0] = weight_syn

# Create a current Clamp starting at 200 ms and with duration 5ms. Amplitude is an argument.     
ic = h.IClamp(cell_0.soma(0.5))
ic.delay = 200  # ms
ic.dur = 5  # ms
ic.amp = 0.2  # nA

# Include an EPSP

syn_tau1 = 0.1
syn_tau2 = 20
syn_NMDA_tau1 = 10
syn_NMDA_tau2 = 75

syn_0 = h.Exp2Syn(cell_0.apic1(0.5))
syn_0.tau1 = syn_tau1  # rise time #if synapse is NMDA tau1 = 10
syn_0.tau2 = syn_tau2  # decay time #if synapse is NMDA tau2 = 75ms - because takes much more current and time for magnesium ion to be removed from channel
syn_0_NMDA.tau1 = syn_NMDA_tau1
syn_0_NMDA.tau2 = syn_NMDA_tau2
syn_1 = h.Exp2Syn(cell_1.apic1(0.5))
syn_1.tau1 = syn_tau1
syn_1.tau2 = syn_tau2
syn_1_NMDA = h.NMDA(cell_1.tuft1(0.5))
syn_1_NMDA.tau1 = syn_NMDA_tau1
syn_1_NMDA.tau2 = syn_NMDA_tau2
syn_2 = h.Exp2Syn(cell_2.apic1(0.5))
syn_2.tau1 = syn_NMDA_tau1
syn_2.tau2 = syn_NMDA_tau2
syn_2_NMDA = h.NMDA(cell_2.tuft1(0.5))
syn_2_NMDA.tau1 = syn_NMDA_tau1
syn_2_NMDA.tau2 = syn_NMDA_tau2
syn_3 = h.Exp2Syn(cell_3.apic1(0.5))
syn_3.tau1 = syn_tau1
syn_3.tau2 = syn_tau2
syn_3_NMDA = h.NMDA(cell_3.apic1(0.5)) 
syn_3_NMDA.tau1 = syn_NMDA_tau1
syn_3_NMDA.tau2 = syn_NMDA_tau2
syn_4 = h.Exp2Syn(cell_4.tuft1(0.5))
syn_4.tau1 = syn_tau1
syn_4.tau2 = syn_tau2
syn_4_NMDA = h.NMDA(cell_4.apic1(0.5))
syn_4_NMDA.tau1 = syn_NMDA_tau1
syn_4_NMDA.tau2 = syn_NMDA_tau2

syn_0.e = 0  # reversal potential of the synapse
syn_0_NMDA.e = 0
syn_1.e = 0
syn_1_NMDA.e = 0
syn_2.e = 0
syn_2_NMDA.e = 0
syn_3.e = 0
syn_3_NMDA.e = 0
syn_4.e = 0
syn_4_NMDA.e = 0


#========== ...create an artificial spike (an "event" to be delivered to the synapse)...
tsignal = 20
ns = h.NetStim(0.5) # do you input the spike vector here?
ns.start = 200  # stimulus onset
ns.number = 1  # number of events

#... and connect the event to the synapse.
nc = h.NetCon(ns, syn_0)
nc.delay = 0  # synaptic delay (ms)
nc.weight[0] = 0.01  # synaptic weight (strength) - importance of synapse in overall potential 

#add conductances

cell_0_soma_vec = h.Vector().record(cell_0.soma(0.5)._ref_v)  #membrane potential vector 
cell_1_soma_vec = h.Vector().record(cell_1.soma(0.5)._ref_v)  
cell_2_soma_vec = h.Vector().record(cell_2.soma(0.5)._ref_v)  
cell_3_soma_vec = h.Vector().record(cell_3.soma(0.5)._ref_v)  
cell_4_soma_vec = h.Vector().record(cell_4.soma(0.5)._ref_v)  

t_vec = h.Vector().record(h._ref_t)  # Time stamp vector

# Run the simulation
h.finitialize(vinit)
h.continuerun(tstop)

# Remove the first 20ms to avoid artifacts
tremove = 20
cell_0_soma_vec.remove(0, int(tremove/h.dt))
cell_1_soma_vec.remove(0, int(tremove/h.dt))
cell_2_soma_vec.remove(0, int(tremove/h.dt))
cell_3_soma_vec.remove(0, int(tremove/h.dt))
cell_4_soma_vec.remove(0, int(tremove/h.dt))
t_vec.remove(0, int(tremove/h.dt))

plt.figure(figsize=(8, 6))
plt.plot(t_vec, cell_0_soma_vec, label='soma 0 ')
plt.plot(t_vec, cell_1_soma_vec, label='soma 1')
plt.plot(t_vec, cell_2_soma_vec, label='soma 2')
plt.plot(t_vec, cell_3_soma_vec, label='soma 3')
plt.plot(t_vec, cell_4_soma_vec, label='soma 4')

plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.legend()
plt.show()