[Go back to TOC](../../../README.md)

This tutorial demonstrates running NA-MD calculations driven by a machine-learning model:
a trained [hippynn](https://github.com/lanl/hippynn) neural network predicts the diabatic
electronic Hamiltonian of a 122-atom molecular dimer, and Libra propagates the dynamics on
it through the `libra_py.packages.hippynn` interface.

Topics covered:
 * using a trained hippynn model as a Libra model Hamiltonian
 * what a machine-learning model has to predict for nonadiabatic dynamics, and how labels
   select it (a diabatic Hamiltonian with couplings, or state energies alone)
 * obtaining nuclear gradients from the network by automatic differentiation
 * Ehrenfest dynamics in the diabatic representation, and the ensemble vibronic beating
 * adapting the interface to a hippynn model of your own

Required files:
 * `tutorial.ipynb` - the main tutorial file
 * `beating_ensemble.png` - precomputed 300-trajectory result shown in the tutorial

The trained model and its initial conditions are distributed with Libra as
`libra_py.models.NQDH_heterodimer`, so nothing has to be downloaded.

Requirements:
 * `hippynn` and `pytorch`, in addition to Libra. They are imported only when the network
   is evaluated, so the rest of `libra_py` is unaffected if they are not installed.
