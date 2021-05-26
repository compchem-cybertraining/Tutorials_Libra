
The phonon calculations are involved and one needs to do the following steps:

1. Optimize the geometry very well (using pw.x)

   We assume we already start with such a geometry


2. Do the SCF calculations


   Additionally, nscf calculation is needed, if we are interested in phonons other than at the gamma-point


  pw.x < scf.in > scf.out


3. Compute the dynamical matrix


  ph.x < ph.in > ph.out  


  This will generate a bunch of silicon.dyn\* files for different q-point phonons


  At this step we already have the output to visualize


4.  Compute the force constant matrix

  q2r.x < q2r.in > q2r.out

   Generates the file `silicon.fc` with the force constants


5.  Compute the frequencies and normal modes by diagonalizing the dynamical matrix


  matdyn.x < matdyn.in > matdyn.out



6. Plot the .freq files with plotband.x
 

  plotband.x < plotband.in > plotband.out


7. Compute the density of phonon states

  matdyn.x < phdos.in > phdos.out



