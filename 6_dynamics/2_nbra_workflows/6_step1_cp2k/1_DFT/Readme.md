# Run molecular dynamics using CP2K

In this folder, we perform the molecular dynamics (MD) for a rutile TiO2 unit cell. The notebook file contains some information
on how one can obtain the coordinates and run the MD calculations on UB-CCR. More instructions about the input files and the outputs
can be found in [this link](https://github.com/compchem-cybertraining/Tutorials_CP2K/tree/master/7_molecular_dynamics). Before running the calculations 
we need to load all the needed libraries used to compile CP2K so that we can run the calculations. This is dependent on the cluster or system you use. You can 
find more information on loading and installation of different libraries 
and CP2K in [this link](https://github.com/compchem-cybertraining/Tutorials_CP2K/blob/master/INSTALLATION.md)
The MD trajectory of this structure will be used to compute the MO overlaps and time-overlaps and NACs. 
