from cell_properties import PyramidalCell
import neuron


cell_0 = PyramidalCell(0)
cell_1 = PyramidalCell(1)
cell_2 = PyramidalCell(2)
cell_3 = PyramidalCell(3)
cell_4 = PyramidalCell(4)

#create a new synapse on cell 2 that will connect cell 1 and t 
syn_xxx = h.ExpSyn(new_cell2.trunk3(0.5))

#create a netcon object through which cell 1 and 2 will be connected - through syn_xxx
ncon_xxx = h.NetCon(new_cell.soma(0.5)._ref_v, syn_xxx, sec=new_cell.soma)

#spike threshold to decide whether spike will be transmitted to the next cell 
ncon_xxx.threshold = -10
#delay of spike to next cell 
ncon_xxx.delay = 0
ncon_xxx.weight[0] = 0.01

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