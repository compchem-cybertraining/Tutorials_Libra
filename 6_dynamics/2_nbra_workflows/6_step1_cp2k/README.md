# Run molecular dynamics using CP2K

[Go back to TOC](../../../README.md)

Here, we perform the molecular dynamics (MD) for a rutile TiO2 unit cell using DFT and a C3N4 unit cell using xTB. The notebook files contain some information
on how one can obtain the coordinates and run the MD calculations on UB-CCR but can be used for other 
systems too. The chosen systems here are periodic. For non-periodic calculations
we only need to turn off the periodic calculations in the CP2K input in the `&CELL` and `&POISSON` sections. More instructions about the input files and the outputs
can be found in [this link](https://github.com/compchem-cybertraining/Tutorials_CP2K/tree/master/7_molecular_dynamics). Before running the calculations 
we need to load all the needed libraries used to compile CP2K so that we can run the calculations. This is dependent on the cluster or system you use. You can 
find more information on loading and installation of different libraries 
and CP2K in [this link](https://github.com/compchem-cybertraining/Tutorials_CP2K/blob/master/INSTALLATION.md)
The MD trajectory of these two structures will be used to compute the MO overlaps and time-overlaps and NACs in other steps of this tutorial. 
