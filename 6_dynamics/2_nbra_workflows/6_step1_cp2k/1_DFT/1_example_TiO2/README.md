# Run molecular dynamics using CP2K

[Go back to TOC](../../../../../README.md)

This is an example of modeling TiO2 system

## What is this

  We run calculations with cp2k v8.2  

  We run MD calculations of TiO2 system using regular PBE functional

      &XC_FUNCTIONAL
         &PBE
         &END PBE
      &END XC_FUNCTIONAL


  In addition, a dispersion correction is added via vdW potential

      &VDW_POTENTIAL
         POTENTIAL_TYPE PAIR_POTENTIAL 
         &PAIR_POTENTIAL
            PARAMETER_FILE_NAME dftd3.dat
            TYPE DFTD3
            REFERENCE_FUNCTIONAL PBE
            R_CUTOFF [angstrom] 16
         &END
      &END VDW_POTENTIAL



## How to run

    sbatch submit.slm

## Results 

  The results are located in the archive `data.tar.bz2`
