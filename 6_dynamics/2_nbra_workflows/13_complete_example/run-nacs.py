import os
import sys

# Fisrt, we add the location of the library to test to the PYTHON path
if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
from libra_py.packages.dftbplus import methods as DFTB_methods
import libra_py.workflows.nbra.step2_dftb as step2
from libra_py import units


params = { "EXE":"/home/alexvakimov/SOFTWARE/dftbplus/dftbplus_22.2/_install/bin/dftb+", 
           "mo_active_space":list(range(290, 297)), 
           "md_file":"Ti17-md.xyz",
           "sp_gen_file": "x1.gen",
           "ovlp_gen_file": "x2.gen",
           "syst_spec" : "C", 
           "scf_in_file" : "dftb_in_ham1.hsd", 
           "hs_in_file" : "dftb_in_ham2.hsd",
           "ovlp_in_file" : "dftb_in_overlaps.hsd",
           "do_tddftb": False,
           "dt":41.0, "isnap":0, "fsnap":50, "out_dir":"res"
         }

step2.run_step2(params)

