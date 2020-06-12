[Go back to TOC](../../../README.md)

This tutorial demonstrates running adiabatic molecular dynamics of HFCO molecule on ground and excited states via
the use of Libra/DFTB+ interface. The excited states dynamics is computed at the TD-DFTB level. 

Topics covered: 
 * adiabatic MD on ground or excited states
 * reading in coordinates stored in the output HDF5 files produced by Libra and visualizing them
 * setting up the dynamical simulations and using pre-defined recipes

Required files:
 * `tutorial.ipynb` - the main tutorial file
 * `dftb_input_template.hsd` - a template file for DFTB+ 
 * Slater-Koster files are required, but are not supplied with this tutorial. Download them from the
   official website. See the `tutorial.ipynb` file for the links.
