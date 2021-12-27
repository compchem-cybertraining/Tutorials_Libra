# Computing the molecular orbital overlaps and time-overlaps

Here, we compute the molecular orbital (MO) overlaps and time-overlaps using the Libra/Libint interface. The electronic
structure calculations are for DFT and xTB calculations. The computed MO overlap matrices 
are stored as sparse matrices in `npz` files and will be used in Step 3 to compute the nonadiabatic couplings (NACs) between pairs of
Kohn-Sham and excited states. Detailed information are brought in the jupyter notebook files and python files.
