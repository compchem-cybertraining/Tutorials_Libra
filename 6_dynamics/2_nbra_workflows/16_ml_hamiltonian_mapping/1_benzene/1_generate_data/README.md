# Generating data for Kohn-Sham Hamiltonian mapping approach with machine-learning

In this step, we need to generate guess Hamiltonian matrices for all the steps in the precomputed molecular dynamics trajectory and reference Hamiltonian matrices for only some random steps in the trajectory. The main file is `distribute_jobs.py` and one needs to run it using `python distribute_jobs.py`. 
The guess and reference Hamiltonian matrices, or any other atomic orbital matrices such as density or overlap matrix, can be generated in different levels of theory with different software. 
These matrices are then used in the next step to create a machine-learning model to map the Hamiltonians to each other. The calculations can be done from scratch and if more reference calculations are required, the user can come back and request more reference steps by `user_steps`. Here, we perform a set of single-point calculations and therefore one can simply distribute them over multiple nodes. The `distribute_jobs(params)` function does this task by taking a set of parameters ina dictionary which include the following key items:

`prefix`: The prefix used to names of the files when saved.

`trajectory_xyz_file`: The full path to the precomputed trajectory `xyz` file.

`user_steps`: The user defined steps. In this variable, you can specify for which steps the calculations must be performed. 

`njobs`: The number of jobs for distributing the calculations.

`nprocs`: The number of processors to be used for calculations in each job.

`remove_raw_outputs`: This falg removes large raw files which are read by Libra and saved.

`submit_template`: The full path to the submission file.

`software_load_instructions`: The loading instructions that are needed to load Python, guess and reference software, and any other thing required to run calculations.

`submit_exe`: The submission executable - for some HPC environments, it is `sbatch` and for some others, it is `qsub`. Currently, only slurm environment is tested.

`do_guess`: Generate only guess data.

`guess_dir`: The full path to save the guess calculations.

`guess_input_template`: The input template used for perfroming guess calculations.

`guess_software`: The software used to perform guess calculations. Current values are `cp2k` and `dftb+`

`guess_software_exe`: The executable or the full executable path to the software required to compute the guess calculations.

`guess_mpi_exe`: The `mpi` executable for running the `guess_software`.

`do_ref`: Generate only the reference data.

`reference_dir`: The full path to save the reference calculations.

`reference_input_template`: The input template required for performing reference calculations.

`reference_software`: The software to perform reference calculations. Current values are `cp2k` and `dftb+`.

`reference_software_exe`: The executable or the full executable path to the software required to compute the reference calculations.

`reference_mpi_exe`: The `mpi` executable for running the `reference_software`.


In this tutorial, we aligne the MD trajectory using the python script `align_trajectory.py` and remove the translational and rotational degrees of freedom.
