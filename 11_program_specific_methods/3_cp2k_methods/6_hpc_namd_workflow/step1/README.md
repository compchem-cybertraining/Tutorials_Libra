# Step 1: Run molecular dynamics using CP2K

## What is this

 - `TiO2_unit_cell.vasp` - geometry and unit cell information, usually obtained from VESTA

 - `convert.py` - auxiliary file for format conversion

 - `md.inp` - input file for CP2K

 - `submit.slm` - SLURM submit file

 - `reference` - example output of the calculations

## How to run

1. Obtain `TiO2_unit_Cell.vasp` from VESTA

2. Obtain `.xyz` file and unit cell information:

```bash
python convert.py
```

This will generate the Cartesian coordinates in `TiO2_unit_cell.xyz` and will print out the unit cell informaiton. Use it to prepare MD input file.

3. Edit `md.inp` file as needed

4. Edit `submit.slm` file as needed

5. Run the calculations on the HPC:

```bash
sbatch submit.slm
```

## Results

```bash
Rutile_TiO2_MD-1.ener     Rutile_TiO2_MD-1.restart.bak-1  Rutile_TiO2_MD-RESTART.wfn.bak-1  Rutile_TiO2_MD-pos-1.xyz  TiO2_unit_cell.xyz   slurm-24946008.out
Rutile_TiO2_MD-1.restart  Rutile_TiO2_MD-RESTART.wfn      Rutile_TiO2_MD-frc-1.xyz          Rutile_TiO2_MD-vel-1.xyz  out_md_tio2_dft.log
```

- `.ener` file contains energies

- `*-pos-1.xyz` file contains the trajectory - WE WILL NEED it in the following step

- `*-vel-1.xyz` velocities

- `*-frc-1.xyz` forces 

- `*.log` file - general output of CP2K

