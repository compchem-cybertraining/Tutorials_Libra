import os
import numpy as np
from libra_py.workflows.nbra.generate_data import distribute_jobs

params = {}
params["prefix"] = "c60"
params["scratch"] = True
params["do_more"] = False
if params["do_more"]:
    params["do_more_steps"] = 10

params["trajectory_xyz_file"] = os.getcwd()+"/C60-pos-1.xyz"
params["guess_dir"] = os.getcwd()+"/guess"
params["reference_dir"] = os.getcwd()+"/ref"
params["guess_input_template"] = os.getcwd()+"/cp2k_guess.inp"
params["reference_input_template"] = os.getcwd()+"/cp2k_ref.inp"
params["software"] = "cp2k"
params["reference_steps"] = 50
params["njobs"] = 10
params["istep"] = 1000
params["fstep"] = 1500
params["nprocs"] = 9
params["software_exe"] = "cp2k.psmp"
params["remove_raw_outputs"] = True
params["submit_template"] = "submit_template.slm"
# Here put whatever needed for loading the software
params["software_load_instructions"] = """
module use /projects/academic/cyberwksp21/MODULES
module load cp2k/v24/avx512
export OMP_NUM_THREADS=1
eval "$(/projects/academic/alexeyak/mohammad/software/mc/bin/conda shell.bash hook)" 
conda activate libra
export PYTHONPATH=/projects/academic/alexeyak/mohammad/software/libra-code-1/_build/src:$PYTHONPATH
export LD_LIBRARY_PATH=/projects/academic/alexeyak/mohammad/software/libra-code-1/_build/src:$LD_LIBRARY_PATH
"""
# The submission executable, for some HPC environement it is qsub
params["submit_exe"] = "sbatch"

distribute_jobs(params)

