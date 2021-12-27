# Computing the MO overlaps using the Linux environments on HPCs

If you have more resources on a cluster you can speed up the computation of the MO overlaps by splitting the trajectroy
into multiple jobs and run them independently. The `run_template.py` is the same as in the notebook file in previous folder. 
We use the `slurm` environment to submit our jobs on UB-CCR cluster. The `submit_template.slm` file is the one which will be submitted and runs the
`python run.py` where the `run.py` file is the copy of the `run_template.py` file but with the initial and final steps filled
based on the requested number of jobs and the initial and final step for the trajectory. We need to load all of the dependencies to run the
CP2K calculations. Here, we use the Intel compilers so we need to load them so that CP2K can run. For example, in the `submit_template.slm` file
we have:
```
module load intel/20.2
module load intel-mpi/2020.2
```
As in the Libra installation manual, one needs to add the full path to `liblibra_core.so` and Libra build folder in the `PYTHONPATH` and `LD_LIBRARY_PATH`
so that Libra can be loaded when using Python. Also, you will need to activate the `conda` environment as well if it is not set in the `.bashrc` file.
If you have added them to the `.bashrc` file, the slurm will set them but if not, you will need to set these paths
correctly in the slurm file. 

The `distribute_jobs.py` is the file that you need modify by specifying initial and final step of the trajectory and the number of jobs.
Libra will split the trajectory based on these values and will submit them by creating the specific folders for each job. The parameters in this file are as follows:

`run_slurm`: If set to `True`, it will use the slurm environment to submit the jobs using the `submit_template` file. If it is set to `False`, it will run the
calculations on the active session.

`istep`: The initial step of the trajectory,

`fstep`: The final step of the trajectory,

`njobs`: Number of jobs.

Then the function `CP2K_methods.distribute_cp2k_libint_jobs` will distribute and submit the jobs.

Now, the only thing left to do is to run `python distribute_jobs.py`.
