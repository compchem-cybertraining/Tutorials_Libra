# Machine-learned Kohn-Sham Hamiltonian mapping for computation of the molecular orbital overlaps and time-overlaps 

In this tutorial, we show how the machine-learning mapping approach can be used to compute the molecular orbitals in a higher level of theory, such as B3LYP, from a atomic guess density in a lower level such as PBE.


## Building and training the model 

Here are the set of parameters required to train a machine-learning model using `train` function in `ml_map` module in `1_train.py` file. 


`prefix`: The prefix used to save the files.

`path_to_input_mats`: The full path to input matrices files.

`path_to_output_mats`: The full path to output matrices files.

`path_to_trajectory_xyz_file`: The full path to trajectory `xyz` file. This is required for computation of the overlap
matrix and solving generalized Kohn-Sham equations. Also, it will be required for computation of the molecular orbitals 
overlap and time-overlap matrices.

`path_to_sample_files`: The full path to sample files obtained in the [generate data step](../1_generate_data).

`input_property`: The input property which appears in the middle of the name of the input files. It can take values of `kohn_sham`, `density`, `overlap`, and `hamiltonian` for xTB calculations.

`output_property`: The output property which appears in the middle of the name of the output files. It can take values of `kohn_sham`, `density`, `overlap`, and `hamiltonian` for xTB calculations.
    
We use a kernel ridge regression (KRR) method for mapping the Hamiltonian matrix from one calculations to another. The parameters for setting up the KRR are as follows:
    
`kernel`: The kernel name: `linear`, `poly` for polynomial kernels, and `rbf` for radial basis function kernel.

`degree`: The degree of the kernel function in case of a `poly` kernel.

`alpha`: This parameter represents the regularization strength in ridge regression. It controls the complexity of the model: a higher alpha value increases the amount of regularization, which in turn reduces the model's variance but might increase its bias. Specifically, it multiplies the identity matrix that is added to the kernel matrix in the ridge regression formula. This parameter helps to prevent overfitting by ensuring that the coefficients do not grow too large.


`gamma`: This parameter is specific to certain types of kernels such as the radial basis function, sigmoid, or polynomial kernels. Gamma defines how much influence a single training input has. The larger the gamma, the closer other inputs must be to be affected.

`scaler`: The scaler to scale the input and data. It can take `standard_scaler` and `minmax_scaler` values. The `standard_scaler` is recommended.

`partitioning_method`: The partitioning of the Hamiltonian matrix. It can take values of `equal` and `atomic`. In the 
`equal` partitioning, the upper triangular part of the Hamiltonian matrix is partitioned into `npartition` equal segments. A separate model maps each input partition to its corresponding partition in the output matrix.
The `atomic` partitioning method partitions the matrix based on the atomic angular momentum components of the matrix for each basis set.

`npartition`: The number of partition in the `equal` partitioning method.

`memory_efficient`: A boolean flag for memory efficiency of the calculations. This will remove the raw data and will remove them from the memory after they are processed.

`train_parallel`: A boolean flag for training models in parallel.

`save_models`: A boolean flag for saving the trained model 

`path_to_save_models`: The full path to save the model

`save_ml_ham`: A boolean flag for saving the predicted Hamiltonian matrices 

`save_ao_overlap`: A boolean flag for saving the atomic orbital overlap matrices

`save_ml_mos`: A boolean flag for saving the molecular orbitals eigenvalues and eigenvectors

`do_error_analysis`: Computing the overlap between reference molecular orbitals and difference in their energies, ML and reference Hamiltonians difference, and computation of the total energy with CP2K.

`save_ref_eigenvalues`: A boolean flag to save the reference eigenvalues.

`save_ref_eigenvectors`: A boolean flag to save the reference eigenvectors.

`path_to_save_ref_mos`: The full path to save the reference molecular orbitals

`compute_ml_total_energy`: A boolean flag to call CP2K to compute the total energy of the ML molecular orbitals using the outputed `wfn` files. Note that for this type of calculations, the `write_wfn_file` should also be set to `True`.

`write_wfn_file`: A boolean flag for writing `wfn` files readable by CP2K.

`path_to_save_wfn_files`: The full path to save the `wfn` files.

`cp2k_ml_input_template`: The full path to a sample CP2K input file for computing the total energy with the outputed `wfn` files.

`compute_overlap`: A boolean flag to compute the overlap and time-overlap between ML molecular orbital.

`nprocs`: The number of processors for computing the overlap matrices.

`is_periodic`: The flag for periodicity of he system for computing the overlaps.

`A_cell_vector`: A list containing the A cell vector.

`B_cell_vector`: A list containing the B cell vector.

`C_cell_vector`: A list containing the C cell vector.

`periodicity_type`: The periodicity type for each direction of the periodic cell.

`translational_vectors`: The set of translational vectors for overlap calculations. This should be a list as we need to save it with `json` library.

`lowest_orbital`: The lowest orbital index to be saved.

`highest_orbital`: The highest orbital index to be saved.

`res_dir`: The full path to save the overlap, time-overlap, and energies similar as in [step 2](../../../7_step2_cp2k).

To run this you can call the `python 1_train.py` with different arguments:

```
--partition: 'equal' or 'atomic', default is 'equal'
--npartition: the number of partitions for 'equal' partitioning , default is 10
--kernel: the name of the kernel which can take 'linear', 'poly', and 'rbf', default is 'linear'
--polydegree: the degree of polynomial only if a 'poly' kernel was selected, default is 10
--alpha: the alpha parameter, default is 0.1
--gamma: the gamma parameter, default is 0.1
```

For example:

```
python 1_train.py --partition equal --npartition 20 --kernel poly --polydegree 2 --alpha 0.05 --gamma 0.05
```

This will generate and save the models which can then be used to generate the properties. Also, a `train_params.json` file is created which contains the necessary parameters for training and are used later on to compute the properties.

## Using the model 

In order to use the model and generate the data, you need to specify three other simple parameters in the `2_distribute_jobs.py` file:

`steps`: The geometries you want to compute the properties for in the precomputed molecular dynamics trajectory you specified its path in `1_train.py` file.

`njobs`: The number of jobs to distribute the calculations similar as in [step 2](../../../7_step2_cp2k) calculations.

`submit_template`: The full path to the submit template file which you want to run the calculations of each job with. This file will be filled with the software loading instructions as you specified in the [data generation step](../1_generate_data).


For each geometry we do the following in this step:

1- Load the models where they are saved

2- Call CP2K to compute the guess property for each geometry

3- Use the models to predict the Hamiltonian matrix

4- Diagonalize the Hamiltonian matrix to generate the molecular orbitals

5- Compute the molecular orbital overlap and time-overlap matrices and save them in the `res_dir` folder as `npz` format.

6- Write the `wfn` file and compute the total energy of the system if specified

7- Remove the guess and large output data or keep them as specified by the user

Then, we can use these data in the `res_dir` for [step 3](../../../8_step3) calculations and then perform the NA-MD simulations as we did in [step 4](../../../9_step4). 

One can visualize the evolution of the ML energy levels as we did in step 3 calculations using the following piece of code which is brought in the `3_plot_energies.ipynb` jupyter file.

```
import json
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from libra_py import units

# Read the parameters
with open('train_params.json', 'r') as f:
    params = json.load(f)
# Reading and plotting the energy data
fs = 24
time_step = 0.5 # fs
plt.rcParams.update({'font.size': fs})
plt.figure(figsize=(3.21*3, 2.41*3))

energies = []
for step in range(5000,7000):
    tmp = np.diag(sp.load_npz(f"{params['res_dir']}/E_ks_{step}.npz").real.todense())
    tmp = tmp[0:int(tmp.shape[0]/2)] # Only the energies of alpha orbitals
    energies.append(tmp)
energies = np.array(energies)*units.au2ev

md_time = np.arange(len(energies))*time_step
for i in range(energies.shape[1]):
    if i<8:
        plt.plot(md_time, energies[:,i], lw=2.0, color='blue')
    else:
        plt.plot(md_time, energies[:,i], lw=2.0, color='red')
# The HOMO level index is 14
ave_gap = np.average(energies[:,8]-energies[:,7])
plt.text(200, -4.0, f'{ave_gap:.2f} eV')
plt.title('Water dimer MO Energies, B3LYP')
plt.ylabel('Energy, eV')
plt.xlabel('Time, fs')
plt.tight_layout()
plt.savefig('ml_energy_levels.jpg', dpi=600)
```

## Trials and errors with partitioning methods 

Here are some trials and errors that is done with different partitioning methods.

* For `equal` partitioning:

`npartition`: 1 

```
Average MAE for all models: 0.0006977372607982587
Average MSE for all models: 3.962586874434997e-06
Average R^2 for all models: 0.9974170865111319
```

`npartition1: 10

```
Average MAE for all models: 0.007447090949634428
Average MSE for all models: 0.0003964626579931684
Average R^2 for all models: 0.8794368493556999
```

* For `atomic` partitioning:

```
Average MAE for all models: 0.02520863231050299
Average MSE for all models: 0.002891714835368408
Average R^2 for all models: 0.6484891268088989
```

