# Step 3: Compute time-overlaps and Hvib files at the TD-DFT level

## What is this

 - `Rutile_TiO2_MD-pos-1.xyz` - MD trajectory file (from step1)

 - `all_logfiles` - log files from CP2K with TD-DFT amplitudes (from step2)

 - `res` - .npz files for KS orbitals (from step2)
 
 - `run.py` - the main file to run

## How to run

1. Copy all the necessary files (see above) to the directory

2. Run the `run.py` script:

```bash
python run.py
```

## Results

The following folders will be created:

 - `coord-*.xyz` - these files are generated along the trajectory, can be deleted

 - `ci_tio2` - this the is the main output folder, which now contains files 
 
   - `ham_adi_*.txt` - diagonal matrices with state energies (a.u.)

   - `hvib_adi_*.txt` - vibronic Hamiltonians

   - `s_adi_*.txt` - overlaps of the CI (TD-DFT) pseudowavefunctions

   - `st_adi_*.txt` - time-overlaps of the CI (TD-DFT) pseudowavefunctions

