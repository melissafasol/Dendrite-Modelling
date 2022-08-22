import matplotlib as plt 
import seaborn as sns

# @title Make nicer plots -- Execute this cell
def mystyle():
  """
  Create custom plotting style.

  Returns
  -------
  my_style : dict
      Dictionary with matplotlib parameters.

  """
  # color pallette
  style = {
      # Use LaTeX to write all text
      "text.usetex": False,
      "font.family": "DejaVu Sans",
      "font.weight": "bold",
      # Use 16pt font in plots, to match 16pt font in document
      "axes.labelsize": 16,
      "axes.titlesize": 20,
      "font.size": 16,
      # Make the legend/label fonts a little smaller
      "legend.fontsize": 14,
      "xtick.labelsize": 14,
      "ytick.labelsize": 14,
      "axes.linewidth": 2.5,
      "lines.markersize": 10.0,
      "lines.linewidth": 2.5,
      "xtick.major.width": 2.2,
      "ytick.major.width": 2.2,
      "axes.labelweight": "bold",
      "axes.spines.right": False,
      "axes.spines.top": False
  }

  return style


plt.style.use("seaborn-colorblind")
plt.rcParams.update(mystyle())

# @markdown Plot the gating variables
def Exp(x):
  if x < -100:
    return 0
  else:
    return np.exp(x)

def vtrap(x, y):
  if np.abs(x/y) < 1e-6:
    v_ = y*(1 - x/y/2)
  else:
    v_ = x/(Exp(x/y) - 1)
  return v_


def inf_tau(a, b, qt=1):
  """
  Calculate the steady-state and the time constant.

  Args:
    a : list
      List with alpha values
    b : list
      List with beta values
    qt : float, optional
      Temperature correction. Default is 1.
  
  ----
  
  Returns:
    xinf : float
      The gate variable steady-state.
    xtau: float
      The gate variable time constant in ms.
  """

  a = np.array(a)
  b = np.array(b)

  xinf = a/(a+b)
  xtau = 1/(a+b)
  return xinf, xtau/qt
