#! /usr/pin/env python

import numpy as np

def visible(Acoord, Bcoord, R=6450e3):
  """Computes the (boolean) visibility of two satellites which 
have the (cartesian) coordinates Acoord and Bccoord aroud a
spherical planet on radius R (in meters). The coord should be 
length 3 iterable 

Acoord and Bcoord ar either length 3 iterable, or arrays of
(same) shape (3,:). The center of the planet is at coordinate (0,0,0)

The default value correspond to the earth with a slightly too 
thick atmosphere
"""
  def v2(npv): return (npv**2).sum(0)
  Acoord=np.array(Acoord)
  Bcoord=np.array(Bcoord)
  R2=R*R
  
  return (np.sqrt(v2(Acoord-Bcoord)) <
    np.sqrt(v2(Acoord)-R2) + np.sqrt(v2(Acoord) -R2))

