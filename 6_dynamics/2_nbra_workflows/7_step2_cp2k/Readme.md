# Computing the molecular orbital overlaps and time-overlaps

Here, we compute the molecular orbital (MO) overlaps and time-overlaps using the Libra/Libint interface. The electronic
structure calculations are for DFT and xTB calculations. The computed MO overlap matrices 
are stored as sparse matrices in `npz` files and will be used in the step3 to compute the nonadiabatic couplings (NACs) between pairs of
Kohn-Sham and excited states. Here, we will present how one can use the current workflow both on a local desktop computer 
and on an HPC. The latter can be used to distribute jobs and increase the speed of calculations by splitting the trajectory. 
The files that contain the main parameters are in the `run_template.py` and the `tutorial.ipynb`. The detailed information about 
the needed parameters to run the main calculations in these files are as follows:


`path`: This will be the path to the job folder in which the calculations will be done. It is set to `os.getcwd()`. Please do not change this.

`params['nprocs']`: The number of processors to use for the calculations. This will be both the number of processors used
by CP2K and the number of processors that will be used to compute the AO overlap matrices.

`params['istep']`: The initial time step for this job. Libra will choose the `istep` from the trajectory `.xyz` file.

`params['fstep']`: The final time step for this job. Again, it will be chosen from the trajectory `.xyz` file.

_*Note:*_ If you want to run it by submitting multiple jobs, do not fill them. Libra will automatically fill them based on the
number of jobs and the number of steps.

`params['lowest_orbital']`: The lowest number of orbital to be considered in the calculations. This value starts from 1.

`params['highest_orbital']`: The highest number of orbital to be considered in the calculations. This value starts from 1.

`params['isXTB']`: A boolean flag for xTB calculations. If it is set to `False` the DFT calculations will be considered. The difference between 
xTB and DFT calculations is that for diagonalization in xTB we need a converged OT wavefunction as an initial guess. Therefore,
we will need an extra input for OT calculations (the `param['cp2k_ot_input_template']`).

`params['isUKS']`: A boolean flag for the unrestricted spin Kohn-Sham calculations. If it is set to `True`, the unrestricted spin calclations is considered.
Make sure consistent keywords are used in the CP2K input template for spin-polarized calculations(the `UKS` or `LSD` keywords).

`params['is_periodic']`: A boolean flag for periodic calculations. If it is set to `True` a periodic AO overlap matrix will be computed.

`params['A_cell_vector']`: The Cartesian A cell vector as in the CP2K input file used to compute the electronic structure calculations.

`params['B_cell_vector']`: The Cartesian B cell vector as in the CP2K input file used to compute the electronic structure calculations.

`params['C_cell_vector']`: The Cartesian C cell vector as in the CP2K input file used to compute the electronic structure calculations.


`params['periodicity_type']`: This parameter is used to generate the translational vectors and shows the periodicity in each of the 
Cartesian X, Y, and Z axes. For example, if the system is a bulk structure, you can set it to `'XYZ'` and if it is a monolayer and you have vacuum in
the Z axis, you can set it to `'XY'`. 


`params['translational_vectors']`: For periodic calculations, CP2K uses a periodic Kohn-Sham Hamiltonian and AO overlap matrix. In order to
accurately compute the MO overlaps, we therefore need to compute the periodic AO overlap matrix. This will be done by computing the overlap between
the central cell and the periodic images of the central cell obtained from the translational vectors. These translational vectors are 
generated using `CP2K_methods.generate_translational_vectors`. The translational vectors are obtained with respect to the `origin`, which 
in here is `[0,0,0]`. The second argument of this function, is a list of 3 elements showing the number of periodic images in each of the 
X, Y, and Z axis respectively. Note that this includes the periodic images in the opposite directions of the axis as well. For example, `[1,1,1]` with 
`params['periodicity_type']='XY'`, computes the AO overlap between the central cell and 8 other cells and itself then sums them to get the periodic 
AO overlap. Since the periodicity is set to `'XY'`, Libra will ignore the 3rd element in this list and will generate the translational vectors 
only for X and Y directions. The following image shows the periodic cells for this configuration:
```

-----------------------------
|         |        |        |      
|(-1,1,0) |(0,1,0) |(1,1,0) |
|         |        |        |
-----------------------------
|         |Central |        |
|(-1,0,0) | Cell   |(1,0,0) |
|         |(0,0,0) |        |
-----------------------------
|         |        |        |
|(-1,-1,0)|(0,-1,0)|(1,-1,0)|
|         |        |        |
-----------------------------

```

`params['is_spherical']`: A boolean flag for computing the AO overlaps in Cartesian or spherical coordinates.

`params['remove_molden']`: A boolean flag to remove or keep the `molden` files after the computations are done.

`params['res_dir']`: The full path to where the MO overlap files will be stored. 

`params['all_pdosfiles']`: The full path to where the `.pdos` files for each step will be stored.

`params['all_logfiles']`: The full path to where the `.log` files for each step will be stored.

`params['cp2k_exe']`: The full path to where the CP2K executable is. If you load CP2K using `module load`, you just need to set the executable name,
 such as `'cp2k.popt'` or `'cp2k.psmp'`.

`params['cp2k_ot_input_template']`: The full path to the CP2K OT input template for xTB calculations. As was mentioned before, we need a good guess 
for the diagonalization algorithm of the xTB calculations. A good guess can be obtained using the OT method. Libra will ignore this if the 
`params['isXTB'] = False`. In this case you can set an empty string.

`params['cp2k_diag_input_template']`: The full path to the CP2K diagonalization input template, either for DFT or xTB.

`params['trajectory_xyz_filename']`: The full path to the trajectory `.xyz` file. 

The calculations are then run using the function `step2.run_cp2k_libint_step2(params)`.


_*Note:*_ If you set the `path` to `os.getcwd()` and you want to compute the overlaps by splitting the trajectory into multiple jobs, you will
need to add one more `../` to the above paths. It is already added in the current files except for the ones run within a notebook. The reason is that the 
`os.getcwd()` is obtained in a new subdirectory in `job` folders.


# Computing the MO overlaps by submitting multiple jobs on HPCs


If you have more resources on a cluster you can speed up the computation of the MO overlaps by splitting the trajectroy
into multiple jobs and run them independently.
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
so that Libra can be loaded when using Python. Also, you will need to activate the `conda` environment as well if it is not set in the `.bashrc` or 
`.bash_profile` file.
If you have added them to the `.bashrc`, the slurm will set them automatically but if not, you will need to set these paths
correctly in the slurm file.

The `distribute_jobs.py` is the file that you need modify by specifying initial and final step of the trajectory and the number of jobs.
Libra will split the trajectory based on these values and will submit them by creating the specific folders for each job. 
The parameters in this file are as follows:

`run_slurm`: If set to `True`, it will use the slurm environment to submit the jobs using the `submit_template` file. If it is set to `False`, it will run the
calculations on the active session.

`istep`: The initial step of the trajectory,

`fstep`: The final step of the trajectory,

`njobs`: Number of jobs.

Then the function `CP2K_methods.distribute_cp2k_libint_jobs` will distribute and submit the jobs.

Now, the only thing left to do is to run `python distribute_jobs.py`.





