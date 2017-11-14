
import numpy as np
import sys
import math
import time

#https://www.sfu.ca/~ssurjano/branin.html

def braninhoo(x):
  x[0] = x[0]*15
  x[1] = (x[1]*15)-5

  y = np.square(x[1] - (5.1/(4*np.square(math.pi)))*np.square(x[0]) + (5/math.pi)*x[0] - 6) + 10*(1-(1./(8*math.pi)))*np.cos(x[0]) + 10;

  return y

