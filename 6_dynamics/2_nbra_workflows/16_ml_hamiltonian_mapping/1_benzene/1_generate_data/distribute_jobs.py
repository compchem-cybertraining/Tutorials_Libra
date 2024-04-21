import os
import numpy as np
from libra_py.workflows.nbra.generate_data import distribute_jobs

params = {}
# Setting the prefix with which the data will be saved
params["prefix"] = "benzene"
# Either to do the calculations from scratch or perform 
# additional reference calculations
params["scratch"] = True
params["do_more"] = False
if params["do_more"]:
    # When doing more steps please also check 
    # if njobs<=nsteps/2
    params["do_more_steps"] = 10
# The full path to trajectory xyz file
params["trajectory_xyz_file"] = os.getcwd()+"/benzene-pos-1.xyz"
# The path to save the data
params["guess_dir"] = os.getcwd()+"/guess"
params["reference_dir"] = os.getcwd()+"/ref"
params["do_guess"] = True
params["do_ref"] = True
# The input templates and their corresponding software
# for both guess and reference calculations
params["guess_input_template"] = os.getcwd()+"/cp2k_guess.inp"
params["reference_input_template"] = os.getcwd()+"/cp2k_ref.inp"
params["guess_software"] = "cp2k"
params["guess_software_exe"] = "cp2k.psmp"
params["guess_mpi_exe"] = "mpirun"
params["reference_software"] = "cp2k"
params["reference_software_exe"] = "cp2k.psmp"
params["reference_mpi_exe"] = "mpirun"
# From which step to which step? How many reference steps?
# How many jobs for distributing them?
params["reference_steps"] = 100
params["njobs"] = 10
params["istep"] = 1000
params["fstep"] = 3000
params["nprocs"] = 9
# For debugging purpose and if you need any output set to False
params["remove_raw_outputs"] = True
# Submission file template - Only slurm is tested!
params["submit_template"] = "submit_template.slm"
# Here put whatever needed for loading the software
# This includes Python, guess, and reference software
params["software_load_instructions"] = """
module use /projects/academic/cyberwksp21/MODULES
module load cp2k/v24/avx512
export OMP_NUM_THREADS=1
eval "$(/projects/academic/alexeyak/mohammad/software/mc/bin/conda shell.bash hook)" 
conda activate libra
export PYTHONPATH=/projects/academic/alexeyak/mohammad/software/libra-code-1/_build/src:$PYTHONPATH
export LD_LIBRARY_PATH=/projects/academic/alexeyak/mohammad/software/libra-code-1/_build/src:$LD_LIBRARY_PATH
"""
# The submission executable, for some HPC environement 
# is 'qsub' but not tested
params["submit_exe"] = "sbatch"
# Distribute the single-point calculations jobs
distribute_jobs(params)

