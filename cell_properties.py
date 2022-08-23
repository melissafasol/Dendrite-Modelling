
import sys
sys.path
import neuron
import numpy as np
import matplotlib.pyplot as plt
from neuron import h
from neuron.units import mV, um, ms
h.load_file("stdrun.hoc")


class PyramidalCell:
  def __init__(self, gid):
        self._gid = gid
        self._setup_morphology()
        self._setup_topology()
        self._create_lists()
        self._setup_geometry()
        self._setup_passive()
        self._setup_segments()
        self._setup_biophysics()

        self._spike_detector = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.spike_times = h.Vector()
        self._spike_detector.record(self.spike_times)
        self._ncs = []

        self.soma_v = h.Vector().record(self.soma(0.5)._ref_v)
        self.dend_v = h.Vector().record(self.apic2(0.5)._ref_v)


  def _geom_nseg(self, section, f=100):
        return int((section.L/(0.1*h.lambda_f(f)) + 0.9)/2)*2 + 1

  def _setup_morphology(self):
        self.soma = h.Section(name='soma', cell=self)
        self.apic1 = h.Section(name='apic1', cell=self)
        self.apic2 = h.Section(name='apic2', cell=self)
        self.tuft1 = h.Section(name='tuft1', cell=self)
        self.tuft2 = h.Section(name='tuft2', cell=self)

  def _create_lists(self):
        self.all = self.soma.wholetree()
        self.apic = [sec for sec in self.all if sec.name().__contains__('apic')]
        self.tuft = [sec for sec in self.all if sec.name().__contains__('tuft')]

  def _setup_topology(self):
        # Connect sections
        self.apic1.connect(self.soma(1))
        self.apic2.connect(self.apic1(1))
        self.tuft1.connect(self.apic2(1))
        self.tuft2.connect(self.apic2(1))
        self._create_lists()

  def _setup_geometry(self):
        self.soma.L = self.soma.diam = 10 * um
        self.apic1.L, self.apic1.diam = 80 * um, 2.5 * um
        self.apic2.L, self.apic2.diam = 70 * um, 2.0 * um
        self.tuft1.L, self.tuft1.diam = 50 * um, 1.0 * um
        self.tuft2.L, self.tuft2.diam = 50 * um, 1.0 * um

  def _setup_passive(self):
        self.soma.cm, self.soma.Ra = 1.0, 200
        self.apic1.cm, self.apic1.Ra = 1.0, 200
        self.apic2.cm, self.apic2.Ra = 1.0, 200 #resistance is ebtween 100-250
        self.tuft1.cm, self.tuft1.Ra = 1.5, 200
        self.tuft2.cm, self.tuft2.Ra = 1.5, 200

  def _setup_biophysics(self):

        # Somatic compartment
        self.soma.insert('hh')

        for sec in self.apic:
            sec.insert('hh')
            for seg in sec:
                seg.hh.gnabar = 0.01
                seg.hh.gkbar = 0.001
        for sec in self.tuft:
            sec.insert('pas')
            for seg in sec:
                seg.pas.g = 1/20000

        # NEW: the synapse
        self.syn1 = h.Exp2Syn(self.tuft1(0.5))
        self.syn1.tau1 = 0.5
        self.syn1.tau2 = 10

        self.syn2 = h.Exp2Syn(self.tuft2(0.5))
        self.syn2.tau1 = 0.5
        self.syn2.tau2 = 10

  def _setup_segments(self):
        # Create segments based on `lambda_f`
        for sec in self.all:
            sec.nseg = self._geom_nseg(section=sec)

  def __repr__(self):
        return 'MyCell[{}]'.format(self._gid)

