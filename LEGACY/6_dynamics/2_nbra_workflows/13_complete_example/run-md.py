import os
import sys
import math

from liblibra_core import *


from libra_py import units
from libra_py.packages.dftbplus import methods as DFTB_methods
import libra_py.workflows.nbra.step2_dftb as step2
    

DFTB_methods.xyz_traj2gen_sp("Ti17.xyz", "x1.gen", 0, "C")

os.system("cp dftb_in_md.hsd dftb_in.hsd")
EXE="/home/alexvakimov/SOFTWARE/dftbplus/_install/bin/dftb+"
os.system(F"{EXE} > o")
