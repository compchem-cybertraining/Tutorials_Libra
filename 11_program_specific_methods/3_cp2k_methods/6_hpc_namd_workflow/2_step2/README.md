# Step 2: Computing overlaps and time-overlaps in the KS basis + TD-DFT amplitudes and energies.

## What is this

 - `smaller_active_space` - results for smaller number of KS orbitals included in calculations

 - `clean.sh` - helper script to clean up the directory after unsuccessful run
  
 - `input` - this directory contains pre-computed MD trajectory
 
 - `reference` - this directory contains files and folders that would be generated during this step

 - `distribute_jobs.py` - main script for submitting the jobs: it creates several folders, copies necessary content into each one, adjusts the actual inputs for each job and submits the SLURM jobs

 - `submit_template.slm` - this is the template SLURM for each job; the main difference among them is in the start and finish indices of the corresponding sub-trajectories

 - `run_template.py` - this is the script that is run for each job (started by the `submit_template.slm`) and calls actual external calculations. Among other calculations, this script will call CP2K calculations. Note: this template becomes just `run.py` script in each job directory. 
 
 - `es_diag_temp.inp` - template for CP2K input file; the CP2K calculations are executed by the `run.py` script in each job.

 So the control sequence is this:

 `distribute_jobs.py (Libra) -> submit_template.slm (SLURM) -> run_template.py (Libra) -> es_diag_temp.inp (CP2K)`


## How to run

1. Obtain the MD trajectory file from Step 1 or use the pre-computed trajectory:

```bash
cp input/Rutile_TiO2_MD-pos-1.xyz .
```

2. Trajectory alignment (less critical for periodic systems)

Edit `align.py` as needed, then run:

```bash
python align.py
```

3. Edit files as necessary:

- `distribute_jobs.py` - e.g. define how many time-teps to handle and how many jobs to start

- `submit_template.slm` - mainly resource management and accounts

- `run_template.py` - system-specific setups such as: periodicity, orbitals to handle, whether to visualize the orbitals, etc. Keep in mind that the initial and final steps will be updated automatically - for each job separately.

- `es_diag_temp.inp` - adjust as needed for your kind of calculations (control DFT and TD-DFT options)

4. Submit calculations

```bash
conda activate libra
python distribute_jobs.py
```


## Results

The following folders will be created:

- `all_logfiles` - collects all the .log files with the TD-DFT amplitudes (will be needed in the next step)

- `all_pdosfiles` - collects all pDOS files

- `job1,  job2,  job3,  job4, ...`  - working directories - you can explore them on your own, or restate such jobs (e.g. if the calculations aren't completed and you want to rerun them after some adjustments). These folders are not needed later, so once your calculations are finished successfully, you can remove the `job*` folders to save space. 

- `res` - contains the energy, overlap and time-overlap files for KS orbitals in the `.npz` format (will be needed in the next step).




