import neuron 
from neuron import h
import numpy as np 
from cell_properties import PyramidalCell
import random 

class Network:
    """A network of *N* ball-and-stick cells where cell n makes an
    excitatory synapse onto cell n + 1 and the last, Nth cell in the
    network projects to the first cell.
    """

    def __init__(self, N=5, stim_w=0.04, stim_t=9, stim_delay=1, syn_w=0.01,
                 syn_delay=5, conn='ring', p_conn=None):
        """
        :param N: Number of cells.
        :param stim_w: Weight of the stimulus
        :param stim_t: time of the stimulus (in ms)
        :param stim_delay: delay of the stimulus (in ms)
        :param syn_w: Synaptic weight
        :param syn_delay: Delay of the synapse
        :param r: radius of the network
        """
        self.conn = conn
        self.p_conn = p_conn
        self._syn_w = syn_w
        self._syn_delay = syn_delay
        self._create_cells(N)
        self._connect_cells()
        # add stimulus
        self._netstim = h.NetStim()
        self._netstim.number = 100
        self._netstim.noise = 0.5
        self._netstim.start = stim_t
        self._nc1 = h.NetCon(self._netstim, self.cells[0].syn1)
        self._nc2 = h.NetCon(self._netstim, self.cells[0].syn2)
        self._nc1.delay = stim_delay
        self._nc1.weight[0] = stim_w
        self._nc2.delay = stim_delay
        self._nc2.weight[0] = stim_w

    def _create_cells(self, N):
        self.cells = []
        for i in range(N):
            self.cells.append(PyramidalCell(i))

    def _connect_cells(self):
        if self.conn == 'ring':
            for source, target in zip(self.cells, self.cells[1:] + [self.cells[0]]):
                if random.random() < 0.5:
                    nc = h.NetCon(source.soma(0.5)._ref_v, target.syn1, sec=source.soma)
                else:
                    nc = h.NetCon(source.soma(0.5)._ref_v, target.syn2, sec=source.soma)
                nc.weight[0] = self._syn_w
                nc.delay = self._syn_delay
                source._ncs.append(nc)
        elif self.conn == 'random':
            for source in self.cells:
                for target in self.cells:
                    if source != target and random.random() < self.p_conn:
                        print(source, target)
                        if random.random() < 0.5:
                            nc = h.NetCon(source.soma(0.5)._ref_v, target.syn1, sec=source.soma)
                        else:
                            nc = h.NetCon(source.soma(0.5)._ref_v, target.syn2, sec=source.soma)
                        nc.weight[0] = self._syn_w
                        nc.delay = self._syn_delay
                        source._ncs.append(nc)