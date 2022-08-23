from cell_properties import PyramidalCell
import neuron
from neuron import h
import matplotlib.pyplot as plt
import os

# Simulation parameters	
tstop = 1600 #* ms simulation time (ms)
h.dt = 0.1 #* ms # integration step (ms)
vinit = -65 #* mV  # initial voltage (mV)

#pyr_cells = [PyramidalCell(i) for i in range(5)]
#pyr_cells[0].apic1(0.5)

#create cells 
pyr_cells = [PyramidalCell(i) for i in range(5)]

#create synapses
apic_synapses = []
tuft_synapses = []
for i in range(5):
    apic_synapses.append(h.Exp2Syn(pyr_cells[i].tuft1(0.5)))
    apic_synapses[-1].tau1 = 0.2
    apic_synapses[-1].tau2  = 5
    #tuft_synapses[-1].tau1 = 0.2
    #tuft_synapses[-1].tau2 = 5

apic_NMDA_synapses = []
tuft_NMDA_synapses = []

for i in range(5):
    tuft_NMDA_synapses.append(h.NMDA(pyr_cells[i].tuft1(0.5)))
    #apic_NMDA_synapses[-1].tau1 = 10
    #apic_NMDA_synapses[-1].tau2 = 75
    tuft_NMDA_synapses[-1].tau1 = 10
    tuft_NMDA_synapses[-1].tau2  = 75

# netcon objects to connect typical synapses
ncon_apic_synapses = []
for i in range(len(apic_synapses)-1):    
    ncon_apic_synapses.append(h.NetCon(pyr_cells[i + 1].soma(0.5)._ref_v, apic_synapses[i], sec=pyr_cells[i + 1].soma))
    ncon_apic_synapses[-1].threshold = -10
    ncon_apic_synapses[-1].delay = 2 #make 2 because adds delay of axon
    ncon_apic_synapses[-1].weight[0] = 0.001
#netcon objects to connect NMDA synapses 
ncon_tuft_NMDA_synapses = []
for i in range(len(tuft_NMDA_synapses)-1):
    ncon_tuft_NMDA_synapses.append(h.NetCon(pyr_cells[i + 1].soma(0.5)._ref_v, tuft_NMDA_synapses[i], sec = pyr_cells[i + 1].soma))
    ncon_tuft_NMDA_synapses[-1].threshold = -10
    ncon_tuft_NMDA_synapses[-1].delay = 2 #make 2 because adds delay of axon, presynaptic effect so must be the same as AMPA 
    ncon_tuft_NMDA_synapses[-1].weight[0] = 0.003
#should cell 5 and cell 0 be connected through synapse?
ncon_apic_synapses.append(h.NetCon(pyr_cells[0].soma(0.5)._ref_v, apic_synapses[-1], sec = pyr_cells[0].soma))
ncon_apic_synapses[-1].threshold = -10
ncon_apic_synapses[-1].delay = 2 #make 2 because adds delay of axon
ncon_apic_synapses[-1].weight[0] = 0.001
ncon_tuft_NMDA_synapses.append(h.NetCon(pyr_cells[0].soma(0.5)._ref_v, tuft_NMDA_synapses[-1], sec = pyr_cells[0].soma))
ncon_tuft_NMDA_synapses[-1].threshold = -10
ncon_tuft_NMDA_synapses[-1].delay = 2 #make 2 because adds delay of axon, presynaptic effect so must be the same as AMPA 
ncon_tuft_NMDA_synapses[-1].weight[0] = 0.003

# Create a current Clamp starting at 200 ms and with duration 5ms. Amplitude is an argument.     
ic = h.IClamp(pyr_cells[0].soma(0.5))
ic.delay = 200  # ms
ic.dur = 5  # ms
ic.amp = 0.000  # nA

#========== ...create an artificial spike (an "event" to be delivered to the synapse)...
tsignal = 20
ns = h.NetStim(0.5) # do you input the spike vector here?
ns.start = 200  # stimulus onset
ns.number = 20  # number of events
ns.noise = 0.5

stim1 = h.NetCon(ns, apic_synapses[0])
stim1.weight[0] = 0.0001*8 #if weight is less than than 8 then spikes do not fire 
stim2 = h.NetCon(ns, tuft_NMDA_synapses[0])
stim2.weight[0] = 0.0001*8
#add conductances

recording_variables = []
for i in range(len(apic_synapses)):
    recording_variables.append(h.Vector().record(pyr_cells[i].soma(0.5)._ref_v))

dend_recording = h.Vector().record(pyr_cells[0].tuft1(0.5)._ref_v)
t_vec = h.Vector().record(h._ref_t)  # Time stamp vector

# Run the simulation
h.finitialize(vinit)
h.continuerun(tstop)

# Remove the first 20ms to avoid artifacts
tremove = 200
for vec in recording_variables:
    vec.remove(0, int(tremove/h.dt))
t_vec.remove(0, int(tremove/h.dt))
dend_recording.remove(0, int(tremove/h.dt))

plt.figure(figsize=(8, 6))
for i, vec in enumerate(recording_variables):
    plt.plot(t_vec, vec, label=f'soma {i}')
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.legend()
plt.show()

plt.figure()
plt.plot(t_vec, dend_recording)
plt.show()



