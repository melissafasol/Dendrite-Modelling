from cell_properties import PyramidalCell, InhibitoryCell
import neuron
from neuron import h
import matplotlib.pyplot as plt
import os
from spike_trains import poisson_spikes

# Simulation parameters	
tstop = 1600 #* ms simulation time (ms)
h.dt = 0.1 #* ms # integration step (ms)
vinit = -65 #* mV  # initial voltage (mV)

#pyr_cells = [PyramidalCell(i) for i in range(5)]
#pyr_cells[0].apic1(0.5)

#create cells 
Ncells = 5
pyr_cells = [PyramidalCell(i) for i in range(Ncells)]

#create inhibitory cell 
inhibitory_cell = InhibitoryCell(0)

#create synapses
apic_synapses, tuft_NMDA_synapses, inhibitory_synapses = [], [], []
for i in range(Ncells):
    apic_synapses.append(h.Exp2Syn(pyr_cells[i].tuft1(0.5)))
    apic_synapses[-1].tau1 = 0.2
    apic_synapses[-1].tau2  = 5

    tuft_NMDA_synapses.append(h.NMDA(pyr_cells[i].tuft1(0.5)))
    tuft_NMDA_synapses[-1].tau1 = 10
    tuft_NMDA_synapses[-1].tau2  = 75
    
    inhibitory_synapses.append(h.Exp2Syn(pyr_cells[i].soma(0.5)))
    inhibitory_synapses[-1].tau1 = 3
    inhibitory_synapses[-1].tau2  = 15
    inhibitory_synapses[-1].e  = -80
    
pyr_to_in_synapses = h.Exp2Syn(inhibitory_cell.dendrite1(0.5))
pyr_to_in_synapses.tau1 = 0.2
pyr_to_in_synapses.tau2 = 5

# netcon objects to connect typical synapses
ncon_apic_synapses = []
for i in range(len(apic_synapses)-1):    
    ncon_apic_synapses.append(h.NetCon(pyr_cells[i + 1].soma(0.5)._ref_v, apic_synapses[i], sec=pyr_cells[i + 1].soma))
    ncon_apic_synapses[-1].threshold = -10
    ncon_apic_synapses[-1].delay = 2 #make 2 because adds delay of axon
    ncon_apic_synapses[-1].weight[0] = 0.001
    
ncon_pyr_in_synapse, ncon_inh_syn = [], []
for i in range(Ncells):
    ncon_pyr_in_synapse.append(h.NetCon(pyr_cells[i].soma(0.5)._ref_v, pyr_to_in_synapses, sec=pyr_cells[i].soma))
    ncon_pyr_in_synapse[-1].threshold = -10
    ncon_pyr_in_synapse[-1].delay = 2.5 #make 2 because adds delay of axon
    ncon_pyr_in_synapse[-1].weight[0] = 0.01
    
    ncon_inh_syn.append(h.NetCon(inhibitory_cell.soma(0.5)._ref_v, inhibitory_synapses[i], sec=inhibitory_cell.soma))
    ncon_inh_syn[-1].threshold = -10
    ncon_inh_syn[-1].delay = 4 #make 2 because adds delay of axon
    ncon_inh_syn[-1].weight[0] = 0.001
    
    
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
#poisson generated spikes 
spikes = poisson_spikes(t1 = 0, t2 = tstop, N=1, rate=25)
input_spikes_as_list = spikes[spikes[:,0]==0][:, 1] #takes first column of vector object as a list


tsignal = 20
ns = h.NetStim(0.5) # do you input the spike vector here?
ns.start = 200  # stimulus onset
ns.number = 20  # number of events
ns.noise = 0.5

vs = h.Vector(input_spikes_as_list)
vstim = h.VecStim()
vstim.play(vs)


stim1 = h.NetCon(vstim, apic_synapses[0])
stim1.weight[0] = 0.0001*8 #if weight is less than than 8 then spikes do not fire 
stim2 = h.NetCon(vstim, tuft_NMDA_synapses[0])
stim2.weight[0] = 0.0001*8
#add conductances

recording_variables = []
for i in range(len(apic_synapses)):
    recording_variables.append(h.Vector().record(pyr_cells[i].soma(0.5)._ref_v))

dend_recording = h.Vector().record(pyr_cells[0].tuft1(0.5)._ref_v)
t_vec = h.Vector().record(h._ref_t)  # Time stamp vector
inh_recording = h.Vector().record(inhibitory_cell.soma(0.5)._ref_v)

# for i in range(5):  #list to test what happens if active currents are taken out and only passive currents remain
#     for sec in pyr_cells[i].apic:
#         for seg in sec:
#             seg.hh.gnabar = 0 
#             seg.hh.gkbar = 0

# Run the simulation
h.finitialize(vinit)
h.continuerun(tstop)

# Remove the first 20ms to avoid artifacts
tremove = 200
for vec in recording_variables:
    vec.remove(0, int(tremove/h.dt))
t_vec.remove(0, int(tremove/h.dt))
dend_recording.remove(0, int(tremove/h.dt))
inh_recording.remove(0, int(tremove/h.dt))

plt.figure(figsize=(8, 6))
for i, vec in enumerate(recording_variables):
    plt.plot(t_vec, vec, label=f'soma {i}')
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.legend()
plt.show()


plt.figure()
#plt.plot(t_vec, dend_recording)
plt.plot(t_vec, inh_recording)
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.show()

