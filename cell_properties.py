
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

  def geom_nseg(self, section, f=100):
    return int((section.L/(0.1*h.lambda_f(f)) + 0.9)/2)*2 + 1

  def _setup_morphology(self):
    self.soma = h.Section(name='soma', cell=self)
    self.trunk0 = h.Section(name='trunk0', cell=self)
    self.trunk1 = h.Section(name='trunk1', cell=self)
    self.trunk2 = h.Section(name='trunk2', cell=self)
    self.trunk3 = h.Section(name='trunk3', cell=self)
    self.trunk4 = h.Section(name='trunk4', cell=self)
    self.tuft0 = h.Section(name='tuft0', cell=self)
    self.tuft1 = h.Section(name='tuft1', cell=self)

  def _create_lists(self):
    self.all = self.soma.wholetree()
    self.trunk = [sec for sec in self.all if sec.name().__contains__('trunk')]
    self.tuft = [sec for sec in self.all if sec.name().__contains__('tuft')]

  def _setup_topology(self):
    # Connect sections
    self.trunk0.connect(self.soma(0.5))
    self.trunk1.connect(self.trunk0(1))
    self.trunk2.connect(self.trunk1(1))
    self.trunk3.connect(self.trunk2(1))
    self.trunk4.connect(self.trunk3(1))
    self.tuft0.connect(self.trunk4(1))
    self.tuft1.connect(self.trunk4(1))

  def _setup_geometry(self):
    self.soma.L = self.soma.diam = 20 * um

    diams = [3, 2.5, 2, 1.5, 1.2]  # reducing diameters as we are distal from the soma
    for i, sec in enumerate(self.trunk):
      sec.diam = diams[i]  # diameter (um)
      sec.L = 120 if i < 4 else 20  # length (um)

    for i, sec in enumerate(self.tuft):
      sec.L = 100 * um
      sec.diam = 1.0 * um

  def _setup_passive(self):
    for sec in self.all:
      sec.cm = 1  # specific membrane capacitance (uF/cm2)
      sec.Ra = 100  # Axial resistance (Ohm * cm)

  def _setup_biophysics(self):

    # Somatic compartment
    self.soma.insert('hh')
    for seg in self.soma: 
      seg.hh.gnabar = 0.12  # Sodium conductance (S/cm2)
      seg.hh.gkbar = 0.025  # Potassium conductance (S/cm2)
      seg.hh.gl = 0.00025  # Leak conductance (S/cm2)
      seg.hh.el = -65  # Reversal potential (mV)

    # Trunk compartments
    for sec in self.trunk:
      sec.insert('pas')
      for seg in sec:
        seg.pas.e = -65  # leak reversal potential (mV)
        seg.pas.g = 0.00025  # leak maximal conductance (S/cm2)
    
    # Add calcium mechanisms in `trunk4` section
    self.trunk4.insert('cad')
    self.trunk4.insert('sca')
    for seg in self.trunk4:
      seg.sca.gcabar = 0.35  # Ca2+ maximal conductance (S/cm2)
    
    # tuft compartments
    for sec in self.tuft:
      sec.insert('pas')
      for seg in sec:
        seg.pas.e = -65  # leak reversal potential (mV)
        seg.pas.g = 0.00025  # leak maximal conductance (S/cm2)

  def _setup_segments(self):
    # Create segments based on `lambda_f`
    for sec in self.all:
      sec.nseg = self.geom_nseg(sec)

  def __repr__(self):
    return 'PyramidalCell[{}]'.format(self._gid)


class InhibitoryCell():
    
    def __init__(self, gid):
        self._gid = gid 
        self._setup_morphology()
        self._setup_topology()
        self._create_lists()
        self._setup_geometry()
        self._setup_passive()
        self._setup_segments()
        self._setup_biophysics()
        
        def geom_nseg(self, section, f=100):
            return int((section.L/(0.1*h.lambda_f(f)) + 0.9)/2)*2 + 1
        
        def _setup_morphology(self):
            self.soma = h.Section(name='soma', cell=self)
            self.dendrite1 = h.Section(name='dendrite1', cell=self)
            self.dendrite2 = h.Section(name='dendrite2', cell=self)
            self.dendrite3 = h.Section(name='dendrite3', cell=self)
            self.dendrite4 = h.Section(name='dendrite4', cell=self)
            self.dendrite5 = h.Section(name='dendrite5', cell=self)
            self.dendrite6 = h.Section(name='dendrite6', cell=self)

        def _create_lists(self):
            self.all = self.soma.wholetree()
            self.dendrite = [sec for sec in self.all if sec.name().__contains__('dendrite')]
            
        def _setup_topology(self):
        # Connect sections
            self.dendrite1.connect(self.soma(0.5))
            self.dendrite2.connect(self.soma(0.5))
            self.dendrite3.connect(self.soma(0.5))
            self.dendrite4.connect(self.soma(0.5))
            self.dendrite5.connect(self.soma(0.5))
            self.dendrite6.connect(self.soma(0.5))
            

        def _setup_geometry(self):
            self.soma.L = self.soma.diam = 20 * um

        diams = [3, 2.5, 2, 1.5, 1.2]  # reducing diameters as we are distal from the soma
        for i, sec in enumerate(self.dendrite):
            sec.diam = diams[i]  # diameter (um)
            sec.L = 120 if i < 4 else 20  # length (um)

        def _setup_passive(self):
            for sec in self.all:
                sec.cm = 1  # specific membrane capacitance (uF/cm2)
                sec.Ra = 100  # Axial resistance (Ohm * cm)

        def _setup_biophysics(self):
             # Somatic compartment
            self.soma.insert('hh')
            for seg in self.soma: 
                seg.hh.gnabar = 0.12  # Sodium conductance (S/cm2)
                seg.hh.gkbar = 0.025  # Potassium conductance (S/cm2)
                seg.hh.gl = 0.00025  # Leak conductance (S/cm2)
                seg.hh.el = -65  # Reversal potential (mV)

        # Somatic compartment
            self.soma.insert('hh')
            for seg in self.soma: 
                seg.hh.gnabar = 0.12  # Sodium conductance (S/cm2)
                seg.hh.gkbar = 0.025  # Potassium conductance (S/cm2)
                seg.hh.gl = 0.00025  # Leak conductance (S/cm2)
                seg.hh.el = -65  # Reversal potential (mV)

            # Dendrite compartments
            for sec in self.dendrite:
                sec.insert('pas')
            for seg in sec:
                seg.pas.e = -65  # leak reversal potential (mV)
                seg.pas.g = 0.00025  # leak maximal conductance (S/cm2)
    
            
            def _setup_segments(self):
            # Create segments based on `lambda_f`
                for sec in self.all:
                    sec.nseg = self.geom_nseg(sec)

            def __repr__(self):
                return 'InhibitoryCell[{}]'.format(self._gid)


