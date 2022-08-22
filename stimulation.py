from cell_properties import PyramidalCell
import neuron
from neuron import h


cell_0 = PyramidalCell(0)
cell_1 = PyramidalCell(1)
cell_2 = PyramidalCell(2)
cell_3 = PyramidalCell(3)
cell_4 = PyramidalCell(4)

#create a new synapse on cell 2 that will connect cell 1 and t 
#put synapse of cell 0 on apical dendrites 
syn_0 = h.ExpSyn(cell_0.apic1(0.5))
syn_1 = h.ExpSyn(cell_1.trunk3(0.5))
syn_2 = h.ExpSyn(cell_2.trunk3(0.5))
syn_3 = h.ExpSyn(cell_3.trunk3(0.5))
syn_4 = h.ExpSyn(cell_4.trunk3(0.5))

# netcon object to connect cell 0 and 1 
ncon_0 = h.NetCon(cell_1.soma(0.5)._ref_v, syn_1, sec= cell_1.soma)
ncon_1 = h.Netcon(cell_2.soma(0.5)._ref_v, syn_2, sec = cell_2.soma)
ncon_2 = h.NetCon(cell_3.soma(0.5)._ref_v, syn_3, sec= cell_3.soma)
ncon_3 = h.Netcon(cell_4.soma(0.5)._ref_v, syn_2, sec = cell_4.soma)

#spike threshold to decide whether spike will be transmitted to the next cell 
ncon_0.threshold = -10
ncon_1.threshold = -10
ncon_2.threshold = -10
ncon_3.threshold = -10

#delay of spike to next cell 
ncon_0.delay = 0
ncon_0.weight[0] = 0.01
ncon_1.delay = 0
ncon_1.weight[0] = 0.01
ncon_2.delay = 0
ncon_2.weight[0] = 0.01
ncon_3.delay = 0
ncon_3.weight[0] = 0.01

# Create a current Clamp starting at 200 ms and with duration 5ms. Amplitude is an argument.     
ic = h.IClamp(cell_0.soma(0.5))
ic.delay = 200  # ms
ic.dur = 5  # ms
ic.amp = 0.2  # nA

# Include an EPSP
syn = h.Exp2Syn(cell_0.tuft0(0.5))
syn.tau1 = 0.1  # rise time
syn.tau2 = 20  # decay time
syn.e = 0  # reversal potential of the synapse

#========== ...create an artificial spike (an "event" to be delivered to the synapse)...
ns = h.NetStim(0.5)
ns.start = 200  # stimulus onset
ns.number = 1  # number of events

#... and connect the event to the synapse.
nc = h.NetCon(ns, syn)
nc.delay = 0  # synaptic delay (ms)
nc.weight[0] = 0.002  # synaptic weight (strength) - importance of synapse in overall potential 


vsoma_vec = h.Vector().record(new_cell.soma(0.5)._ref_v)  # Membrane potential vector
vtrunk4_vec = h.Vector().record(new_cell.trunk4(0.5)._ref_v)  # Membrane potential vector
t_vec = h.Vector().record(h._ref_t)  # Time stamp vector


vsoma_vec_2 = h.Vector().record(new_cell2.soma(0.5)._ref_v)
vtrunk4_vec_2 = h.Vector().record(new_cell2.trunk3(0.5)._ref_v)
#t_vec_2 = h.Vector().record(h._ref_t)

# Run the simulation
h.finitialize(vinit)
h.continuerun(tstop)

# Remove the first 20ms to avoid artifacts
tremove = 20
vsoma_vec.remove(0, int(tremove/h.dt))
vsoma_vec_2.remove(0, int(tremove/h.dt))
vtrunk4_vec.remove(0, int(tremove/h.dt))
vtrunk4_vec_2.remove(0, int(tremove/h.dt))
t_vec.remove(0, int(tremove/h.dt))

plt.figure(figsize=(8, 6))
plt.plot(t_vec, vsoma_vec, label='soma')
plt.plot(t_vec, vtrunk4_vec, label='trunk4')
#plt.plot(t_vec, vsoma_vec_2, label='soma 2')
#plt.plot(t_vec, vtrunk4_vec_2, label='trunk3')
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.legend()
plt.show()