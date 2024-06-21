import os
import time
import numpy as np
from libra_py.workflows.nbra.ml_map import train
import libra_py.packages.cp2k.methods as CP2K_methods
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--partition', type=str, default='equal')
parser.add_argument('--npartition', type=int, default=10)
parser.add_argument('--kernel', type=str, default='linear')
parser.add_argument('--polydegree', type=int, default=1)
parser.add_argument('--gamma', type=float, default=0.1)
parser.add_argument('--alpha', type=float, default=0.1)
args = parser.parse_args()

params = { # ====== Part 1: General parameters
    "prefix": "benzene",
    "path_to_input_mats": os.path.abspath( os.getcwd() + "/../1_generate_data/guess" ),
    "path_to_output_mats": os.path.abspath( os.getcwd() + "/../1_generate_data/ref" ),
    "path_to_trajectory_xyz_file": os.path.abspath( os.getcwd() + "/../1_generate_data/water_dimer-pos-aligned.xyz" ),
    "path_to_sample_files": os.path.abspath( os.getcwd() + "/../1_generate_data/sample_files"),
    "input_property":  "kohn_sham",
    "output_property": "kohn_sham",
    # Only in case you want to train the model with your own 
    # selections from the reference data that you generated in the previous step
    # "user_train_indices": [],This should be a list
    # ====== Part 2: Setting up the models properties
    "kernel": args.kernel,
    "degree": args.polydegree,
    "alpha": args.alpha,
    "gamma": args.gamma,
    "scaler": "standard_scaler", # Another option is the "minmax_scaler"
    "partitioning_method": args.partition, # Optios: "equal" and "atomic"
    "npartition": args.npartition, # Only for the case of equal partitioning
    "memory_efficient": True, # Removing the raw loaded input and output data after processing them
    "train_parallel": False, # Currently not available
    # ====== Saving ML models parameters and outputs
    # Save the model so that you can use it in the next step
    "save_models": True, 
    # Where to save the models
    "path_to_save_models": os.path.abspath( os.getcwd() + "/models" ),
    # These savings are only for development purposes so it's recommended to turn them off
    # since they will occupy a huge amount of disk space
    # Saving the ML Hamiltonian matrices
    "save_ml_ham": False,
    # Saving the atomic orbital overlap matrices
    "save_ao_overlap": False,
    # Saving the ML molecular orbitals
    "save_ml_mos": False,
    # ====== Part 3: Error analysis
    # If true, it will compute the epsilon parameter and the energy difference with the 
    # reference molecular orbitals computed in the previous step
    "do_error_analysis": False, 
    # Save the MOs from the reference Hamiltonian
    "save_ref_eigenvalues": False,
    "save_ref_eigenvectors": False, 
    "path_to_save_ref_mos": os.path.abspath( os.getcwd() + "/ref_mos" ),
    # Compute the total energy of the ML wavefunction with CP2K
    "compute_ml_total_energy": False,
    "write_wfn_file": False,
    "path_to_save_wfn_files": os.path.abspath( os.getcwd() + "/wfn_files" ),
    "cp2k_ml_input_template": os.path.abspath( os.getcwd()+"/cp2k_ml_temp.inp" ),
    # ====== Part 4: Computing the step2 calculations for molecular orbitals overlap and time-overlap 
    "compute_overlap": True,
    "nprocs": 9,
    "is_periodic": True,
    "A_cell_vector": [15.0, 0.0, 0.0],
    "B_cell_vector": [0.0, 15.0, 0.0],
    "C_cell_vector": [0.0, 0.0, 15.0],
    "periodicity_type": "XYZ",
    # Similar as in step2
    "translational_vectors": CP2K_methods.generate_translational_vectors([0,0,0], [2,2,2], "XYZ").tolist(), 
    "lowest_orbital": 1,
    "highest_orbital": 30,
    "res_dir": os.path.abspath( os.getcwd() + "/res" )}


t1 = time.time()
models, models_error, input_scalers, output_scalers = train(params)
print(F"Elapsed time for training the model: {time.time()-t1} seconds")

