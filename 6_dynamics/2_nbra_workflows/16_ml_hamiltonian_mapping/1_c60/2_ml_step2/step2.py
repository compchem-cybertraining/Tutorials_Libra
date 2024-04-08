import os
from libra_py.workflows.nbra.ml_map import train, load_models, compute_properties

params = {"prefix": "c60",
    "path_to_input_mats": os.getcwd() + "/../1_generate_data/guess",
    "path_to_output_mats": os.getcwd() + "/../1_generate_data/ref",
    "path_to_trajectory_xyz_file": os.getcwd() + "/../1_generate_data/C60-pos-1.xyz",
    "path_to_sample_files": os.getcwd() + "/../1_generate_data/sample_files",
    "input_property":  "kohn_sham",
    "output_property": "kohn_sham",
    "kernel":"linear",
    "degree": 1,
    "alpha": 1.0,
    "gamma": 1.0,
    "scaler": "standard_scaler", # "minmax_scaler"
    "save_models": True,
    "path_to_save_models": os.getcwd() + "/models",
    "partitioning_method": "equal", # "block", "atomwise", ""
    "npartition": 30,
    "memory_efficient": True,
    # Calculations
    "compute_overlap": True,
    "nprocs": 8,
    "write_wfn_file": True, 
    "path_to_save_wfn_files": os.getcwd() + "/wfn_files",
    "istep": 0,
    "is_periodic": False,
    "A_cell_vector": [10.0, 0.0, 0.0],
    "B_cell_vector": [0.0, 10.0, 0.0],
    "C_cell_vector": [0.0, 0.0, 10.0],
    "periodicity_type": "XYZ",
    "lowest_orbital": 100,
    "highest_orbital": 140,
    "res_dir": os.getcwd() + "/res",
    "train_parallel": False}

#models, models_error, input_scalers, output_scalers = train(params)
# You can also reload the saved models that are already trained with input and output data
models, models_error, input_scalers, output_scalers = load_models(os.getcwd()+'/models', params)
compute_properties(params, models, input_scalers, output_scalers)


