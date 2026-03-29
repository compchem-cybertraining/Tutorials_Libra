import os
import sys
import math

from liblibra_core import *


from libra_py import units
from libra_py.packages.dftbplus import methods as DFTB_methods
import libra_py.workflows.nbra.step2_dftb as step2    

i = 25
DFTB_methods.xyz_traj2gen_sp("Ti17-md-aligned.xyz", "x1.gen", i, "C")


os.system("cp dftb_tddftb.hsd dftb_in.hsd")
EXE="/home/alexvakimov/SOFTWARE/dftbplus/_install/bin/dftb+"
os.system(F"{EXE} > o")
