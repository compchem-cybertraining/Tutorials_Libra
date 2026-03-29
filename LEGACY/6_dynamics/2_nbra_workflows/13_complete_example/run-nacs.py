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


odin_params = {"ODIN_EXE":"/home/alexvakimov/SOFTWARE/odin/odin",
               "filename":"x1.gen", 
               "slakos_prefix":"skfiles/",
               "max_ang_mom":{"C":2, "O":2, "H":1, "Ti":3}}

#list(range(285, 305)),
# HOMO = 292 -> 291
params = { "EXE":"/home/alexvakimov/SOFTWARE/dftbplus/_install/bin/dftb+", 
           "mo_active_space":list(range(285, 305)),
           "md_file":"Ti17-md-aligned.xyz",
           "sp_gen_file": "x1.gen",
           "ovlp_gen_file": "x2.gen",
           "syst_spec" : "C", 
           "scf_in_file" : "dftb_in_ham1.hsd", 
           "hs_in_file" : "dftb_in_ham2.hsd",
           "do_tddftb": False,
           "dt":0.5*41.0, "isnap":0, "fsnap":50, "out_dir":"res",
           "tol":0.5,
           "ODIN_PARAMS": odin_params
         }

# Try options for eigensolver until you get small errors
#params["eigensolver"] = "libra"
params["eigensolver"] = "eigh"
#params["eigensolver"] = "eig"
#params["eigensolver"] = "cholesky" - may be problematic

# This is to include all the orbitals
params["mo_active_space"] = list(range(0, 569))

step2.run_step2(params)

