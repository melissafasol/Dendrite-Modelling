import numpy as np
import matplotlib.pyplot as plt


def poisson_spikes(t1, t2, N, rate=10, dt=0.1):
  """
  Poisson spike generator.
  Parameters
  ----------
  t1 : float
      Simulation time start in miliseconds (ms).
  t2 : float
      Simulation time end in miliseconds (ms).
  N : int, optional
      Number of presynaptic spikes.
  rate : float, optional
      Mean firing rate in Hz. The default is 10.
  dt : float, optional
      Time step in ms. The default is 0.1.
  Returns
  -------
  spks : TYPE
      DESCRIPTION.
  """
  spks = []
  tarray = np.arange(t1, t2+dt, dt)
  for n in range(N):
    spkt = tarray[np.random.rand(len(tarray)) < rate*dt/1000.]  # Determine list of times of spikes
    idx = [n]*len(spkt)  # Create vector for neuron ID number the same length as time
    spkn = np.concatenate([[idx], [spkt]], axis=0).T  # Combine tw lists
    if len(spkn) > 0:
      spks.append(spkn)
  spks = np.concatenate(spks, axis=0)
  return spks

pre_cells = 10000
spks = poisson_spikes(t1=0, t2=1000, N=pre_cells, rate=25)

#plt.figure(figsize=(12, 8))
for i, r in enumerate(np.random.choice(pre_cells, 100, replace=False)):
  spks_i = spks[spks[:, 0] == r][:,1]
  #plt.scatter(spks_i, i*np.ones((len(spks_i), )), color='k')
#plt.ylabel('neuron id')
#plt.xlabel('time (ms)')
#plt.show()

freqs = []
for i in range(pre_cells):
  spks_i = spks[spks[:, 0] == i][:, 1]
  freqs.append(len(spks_i))

# plt.figure(figsize=(12, 8))
# plt.hist(freqs, bins=20)
# plt.ylabel('neuron id')
# plt.xlabel('time (ms)')
# plt.show()
