# Generating data for Kohn-Sham Hamiltonian mapping approach with machine-learning

In this step, we need to generate guess Hamiltonian matrices for all the steps in the precomputed molecular dynamics trajectory and reference Hamiltonian matrices for only some random steps in the trajectory. The main file is `distribute_jobs.py` and one needs to run it using `python distribute_jobs.py`. 
The guess and reference Hamiltonian matrices can be generated in different levels of theory with different software. 
These matrices are then used in the next step to create a machine-learning model to map the Hamiltonians to each other. The calculations can be done from scratch and if more reference calculations are required, the user can come back and request more reference steps. Here, we perform a set of single-point calculations and therefore one can simply distribute them over multiple nodes. The `distribute_jobs(params)` function does this task by taking a set of parameters ina dictionary which include the following key items:

`prefix`: The prefix used to names of the files when saved.

`trajectory_xyz_file`: The full path to the precomputed trajectory `xyz` file.

`scratch`: This flag is used to compute all the data, including both guess and reference data, from scratch.


`do_more`: This flag is used to perform additional reference calculations. This may be needed when more data are required to train the ML model. This and `scratch` flags cannot have the same logical values at the same time.

`do_more_steps`: The number of additional reference steps while the `do_more` flag is set to `True`.

`guess_dir`: The full path to save the guess calculations.

`reference_dir`: The full path to save the reference calculations.

`guess_input_template`: The input template used for perfroming guess calculations.

`reference_input_template`: The input template required for performing reference calculations.

`guess_software`: The software used to perform guess calculations. Current values are `cp2k` and `dftb+`

`guess_software_exe`: The executable or the full executable path to the software required to compute the guess calculations.

`reference_software`: The software to perform reference calculations. Current values are `cp2k` and `dftb+`.

`reference_software_exe`: The executable or the full executable path to the software required to compute the reference calculations.

`reference_steps`: The number of reference steps.

`njobs`: The number of jobs for distributing the calculations.

`istep`: The initial step in the precomputed molecular dynamics trajectory.

`fstep`: The final step in the precomputed molecular dynamics trajectory.

`nprocs`: The number of processors to be used for calculations in each job.

`remove_raw_outputs`: This falg removes large raw files which are read by Libra and saved.

`submit_template`: The full path to the submission file.

`submit_exe`: The submission executable - for some HPC environments, it is `sbatch` and for some others, it is `qsub`. Currently, only slurm environment is tested.

`software_load_instructions`: The loading instructions that are needed to load Python, guess and reference software, and any other thing required to run calculations.



