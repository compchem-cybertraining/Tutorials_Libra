import os
import time
import json
from libra_py.workflows.nbra.ml_map import distribute_jobs
#load_models, compute_properties

# ==================== User inputs
# Load the parameters used to train the model
with open("train_params.json", "r") as f:
    params = json.load(f) 
# Number of jobs to distribute the energy calculations
params["njobs"] = 20
# Setup the steps to compute the properties for
params["steps"] = list(range(1000,3000))
# Submit template file
params["submit_template"] = "submit_template.slm"
# ==================== End of user inputs

# ==================== Distributing the jobs over multiple nodes
distribute_jobs(params)

