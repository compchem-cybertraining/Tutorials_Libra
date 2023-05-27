import os
import sys
import math

from liblibra_core import *


from libra_py import units
from libra_py.packages.dftbplus import methods as DFTB_methods    

DFTB_methods.dftb_traj2xyz_traj("geo_end.xyz", "Ti17-md.xyz")

