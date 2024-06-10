import os
import numpy as np
from libra_py.workflows.nbra.generate_data import distribute_jobs

params = {}
# =========================== Part 1: General variables
# Setting the prefix with which the data will be saved
params["prefix"] = "benzene"
# The full path to trajectory xyz file
params["trajectory_xyz_file"] = os.getcwd()+"/water_dimer-pos-aligned.xyz"
# ======== Geometry selection
# Since this is an interpolation we recommend to have the 
# first and final step of the trajectory in the "user_steps"
# === Equispaced geometries
params["user_steps"] =  list(range(2000,12000,20)) 
# You can also select random geometries using below line
# === Random geometries
# Make sure to turn this into a list type so that json can save the parameters
# params["user_steps"] = np.random.randint(0, 10000, size=100).tolist() 
# How many jobs for distributing them?
params["njobs"] = 40
# Number of processors
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
# =========================== Part 2: Guess 
params["do_guess"] = True
params["guess_dir"] = os.getcwd()+"/guess"
params["guess_input_template"] = os.getcwd()+"/cp2k_guess.inp"
params["guess_software"] = "cp2k"
params["guess_software_exe"] = "cp2k.psmp"
params["guess_mpi_exe"] = "mpirun"
# =========================== Part 3: Reference
params["do_ref"] = True
params["reference_dir"] = os.getcwd()+"/ref"
params["reference_input_template"] = os.getcwd()+"/cp2k_ref.inp"
params["reference_software"] = "cp2k"
params["reference_software_exe"] = "cp2k.psmp"
params["reference_mpi_exe"] = "mpirun"
# =========================== Part 4: Distribute the single-point calculations jobs
distribute_jobs(params)

