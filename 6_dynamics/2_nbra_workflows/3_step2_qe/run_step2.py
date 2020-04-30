import os
import sys
import time
import math

# Fisrt, we add the location of the library to test to the PYTHON path
if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import *

# Remove the previous results and temporary working directory from the previous runs
os.system("rm -r res")
os.system("rm -r wd")
os.system("mkdir res")

tot_nsteps     = 100
nsteps_per_job = 10
# tot_nsteps = total simulation time (from 0!)
# tot_nsteps / nsteps_per_job = total number of jobs submitted

# For non-SOC
QE_methods.out2inp("x0.md.out","x0.scf.in","wd","x0.scf",0,tot_nsteps,1)
os.system("cp submit_templ.slm wd"); os.system("cp x0.exp.in wd"); os.chdir("wd")
hpc_utils.distribute(0,tot_nsteps,nsteps_per_job,"submit_templ.slm",["x0.exp.in"],["x0.scf"],2)

#For SOC
#QE_methods.out2inp("x0.md.out","x1.scf.in","wd","x1.scf",0,tot_nsteps,1)
#os.system("cp submit_templ.slm wd"); os.system("cp x1.exp.in wd"); os.chdir("wd")
#hpc_utils.distribute(0,tot_nsteps,nsteps_per_job,"submit_templ.slm",["x1.exp.in"],["x1.scf"],2)
