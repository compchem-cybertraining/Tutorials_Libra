# Running nonadiabatic dynamics 

[Go back to TOC](../../../README.md)

Here, we will perform nonadiabatic molecular dynamics (NA-MD) using the computed nonadiabatic couplings (NACs) in different bases. First, we need to 
choose the initial exicted states by computing the average excitation energy of the excited states over the MD trajectory. Then, we set the 
`ini_states` and the `tsh_methods` and start the NA-MD for different times simultaneously by running them in multiple batches. This is done by
spreading the runs over multiple CPU cores. The `nthreads` will run each NA-MD run on one processor. Also, `nthreads` is used for multithreading 
of the computations using OpenMP library. 

After the dynamics is done, one needs to fit the results of the NA-MD to some fitting functions. There are different types of functions for this
including stretched-compressed exponential or Gaussian-exponential functions. We will show our case using the stretched-compressed function
but if one wants to fit with another function the procedure is almost the same. For fitting, we use the `scipy.optimize` library.

After fitting, we compute the average and the error bars for the computed dynamics and plot them. The fitting are applied to either hot state
decay or recovery of other states such as the recovery dynamics of the band edge states.


The list of the paramters used here are as follwos:

`nthread`: The number of processors used for simultaneous running of the NA-MD simulations.

`methods`: The NA-MD methods which is a dictionary with these methods `{0:"FSSH", 1:"IDA", 2:"mSDM", 3:"DISH", 21:"mSDM2", 31:"DISH2" }`.

`init_states`: The initial states to start the dynamics from.

`tsh_methods`: The methods chosen `methods`. You just need to put the numbers in `methods` in this variable.

`batches`: This is a list of integers for the batches you want to run. You can use `range(nbatches)` or specify them manually.

The above variables are needed to be set in the `run_dynamics` for NA-MD to be run and before defining other general parameters.
Other general parameters that do the NA-MD are as follows. Note that we first need to read all the data from `step3`. This is done by the function
`data_read.get_all_data`. For that we need the following parameters to be set. 

`params['path_to_res_files']`: The full path to the folder where the NAcs were computed.

`params['is_sparse']`: This flag shows whether the files are in `scipy.sparse` format or they are obtained using the previous workflow that used `cube` files
and the data are stored in readable text files. 

`params['istep']`: The initial step that the files start.

`params['Hvib_re_prefix']`: The prefix of the real part of the vibronic Hamiltonian.

`params['Hvib_re_suffix']`: The suffix of the real part of the vibronic Hamiltonian.

`params['Hvib_im_prefix']`: The prefix of the imaginary part of the vibronic Hamiltonian.

`params['Hvib_im_suffix']`: The suffix of the imaginary part of the vibronic Hamiltonian.

`params['St_re_prefix']`: The prefix of the time-overlap files.

`params['St_re_suffix']`: The suffix of the time-overlap files.

After reading the files, the parameters to run the dynamics are as follows:

`params['nsteps']`: The number of steps.

`params['dt']`: The time-step in atomic unit. You can use `libra_py.units.fs2au` for conversion of `fs` to atomic unit.

`params['ntraj']`: The number of surface hopping trajectories.

`params['nstates']`: The number of states. Libra will fill this based on the files it reads.

`params['istate']`: The initial state that the dynamics start from.

`params['which_adi_states']`: This parameter is for some plotting that chooses which adiabatic states to plot. We do not use it in this tutorial.

`params['which_dia_states']`: This parameter is for some plotting that chooses which diabatic states to plot. We do not use it in this tutorial.

`params['is_parallel']`: The multiprocessing flag that takes boolean values.

`params['rep_ham']`: This is the representation in which the computed properties are assumed to be.
For instance, we may have set it to 1, to read the adiabatic energies and couplings,
to bypass the diabatic-to-adiabatic transformation, which may be useful in some atomistic
calculations, or with the NBRA. The values it takes are :

- 0: diabatic
- 1: adiabatic


`params['tsh_method']`: Formula for computing SH probabilities:

- -1: adiabatic - no hops (default)
- 0: FSSH
- 1: GFSH 
- 2: MSSH
- 3: DISH


`params['force_method']`: How to compute forces in the dynamics: 

- 0: don't compute forces at all - e.g. we do not really need them

- 1: state-specific  as in the TSH or adiabatic (including adiabatic excited states) [ default ]

- 2: Ehrenfest


`params['nac_update_method']`: How to update NACs and vibronic Hamiltonian before electronic TD-SE propagation:

- 0: don't update them (e.g. for simplest NAC)

- 1: update according to changed momentum and existing derivative couplings [ default ]


`params['hop_acceptance_algo']`: Options to control the acceptance of the proposed hops:

- 0: accept all proposed hops (default)

- 10: based on adiabatic energy - accept only those hops that can obey the energy conservation with adiabatic potential energies

- 11: based on diabatic energy - same as 10, but we use diabatic potential energies

- 20: based on derivative coupling vectors - accept only those hops that can obey the energy conservation by rescaling nuclear velocities along the directions of derivative couplings for the quantum nuclear DOFs                   

- 21: based on difference of state-specific forces - same as 20, but the rescaling is done along the vector parallel to the difference of adiabatic forces on initial and target states

- 31: accept hops with the probability taken from the quantum Boltzmann distribution
- 32: accept hops with the probability taken from the classical Maxwell-Boltzmann distribution
- 33: accept hops with the probability taken from the updated quantum Boltzmann distribution (experimental)


`params['momenta_rescaling_algo']`: Options to control nuclear momenta changes upon successful or frustrated hops.

- 0: don't rescale [ default ]

- 100: based on adiabatic energy, don't reverse on frustrated hops
- 101: based on adiabatic energy, reverse on frustrated hops
- 110: based on diabatic energy, don't reverse on frustrated hops
- 111: based on diabatic energy, reverse on frustrated hops

- 200: along derivative coupling vectors, don't reverse on frustrated hops
- 201: along derivative coupling vectors, reverse on frustrated hops
- 210: along difference of state-specific forces, don't reverse on frustrated hops
- 211: along difference of state-specific forces, reverse on frustrated hops


`params['time_overlap_method']`: The flag to select how the time-overlaps are computed:

- 0: on-the-fly, based on the wavefunction (`'basis_transform'`) (default)
- 1: read externally (via `'time_overlap_adi'`), use this option with the NBRA, but don't forget to set up its update in the Hamiltonian update functions (aka `'compute_model'`)


`params['mem_output_level']`: Controls what info to save into HDF5 files (all at the end). Same meaning and output as with `hdf5_output_level`, except all 
the variables are first stored in memory (while the calcs are running) and then they are written into the HDF5 file at the end of the calculations. This is 
a much faster version of HDF5 saver.


`params['txt_output_level']`: Controls what info to save into `.txt` files Same meaning and output as with `hdf5_output_level`, except all the variables are written as text files. (default: -1)



`params['properties_to_save']`: Describes what properties to save to the HDF5 files. Note that if some properties are not listed in this variable, then they are not saved, even if `mem_output_level` suggests they may be saved. You need to *BOTH* set the appropriate `mem_output_level` AND `properties_to_save`.

```
default:  [ 'timestep', 'time', 'Ekin_ave', 'Epot_ave', 'Etot_ave', 
           'dEkin_ave', 'dEpot_ave', 'dEtot_ave', 'states', 'SH_pop', 'SH_pop_raw',
           'D_adi', 'D_adi_raw', 'D_dia', 'D_dia_raw', 'q', 'p', 'Cadi', 'Cdia', 
           'hvib_adi', 'hvib_dia', 'St', 'basis_transform', 'projector'
] 
```


`params['state_tracking_algo']`: The algorithm to keep track of the states' identities:

- 0: no state tracking
- 1: Sato
- 2: using the mincost, Munkres-Kuhn [ default ]
- 3: experimental stochastic algorithm, the original version with elimination (known problems)
- 32: experimental stochastic algorithms with all permutations (too expensive)
- 33: the improved stochastic algorithm with good scaling and performance, on par with the mincost


`params['convergence']`: A swtich for stochastic reordering algorithm 3 (and variants) to choose what happens when an acceptable permutation isn't generated in the set number of attempts:

- 0: returns the identity permutation (does not require convergence) [ default ]
- 1: exits and prints an error (requires convergence)


`params['max_number_attempts']`: The maximum number of hops that an be attempted before either choosing the identity or exiting in stochastic reordering algorithm 3 (and variants). The default value is 100.


`params['do_phase_correction']`: The algorithm to correct phases on adiabatic states.

- 0: no phase correction
- 1: according to our phase correction algorithm [ default ]


`params['min_probability_reordering']`: The probability threshold for stochastic state reordering algorithm. If a probability for a multi-state stransition is below this value, it will be disregarded and set to 0. The rest of the probabilities will be renormalized. The default value is 0.


`params['decoherence_algo']`: Selector of the method to incorporate decoherence:

- -1: no decoherence (defaul)
- 0: SDM and alike
- 1: instantaneous decoherence options (ID-S, ID-A, ID-C)



`params['Temperature']`: Temperature of the system. This parameter could be used even in the NVE simulations e.g. as a parameters to compute hop 
acceptance probabilities based on Boltzmann factors. The default value is 300 K.


More details on how to use them are given in the Jupyter notebook files.


