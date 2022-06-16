# Run molecular dynamics using CP2K

[Go back to TOC](../../../../../README.md)

This is an example of modelling adamantane system with BEEF functional

This is run on the UB CCR as of June 15, 2022

## What is this

  We run the calculations with the cp2k v9.1

  This example shows the calculation of the MD trajectory using BEEF functional, which is set up by
  the following block


      &XC_FUNCTIONAL
        &BEEF .TRUE.
        &END
      &END




## How to run

    sbatch submit.slm


## Results 

 The reference results are shown in the archive `step1.tar.gz`

