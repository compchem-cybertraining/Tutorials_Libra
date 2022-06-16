import os
import sys
from libra_py import CP2K_methods
from libra_py.workflows.nbra import step2


path = os.getcwd()
params = {}
# number of processors
params['nprocs'] = 16
# The mpi executable
params['mpi_executable'] = 'srun'
# The istep and fstep
params['istep'] = 
params['fstep'] = 
# Lowest and highest orbital, Here HOMO is 28
params['lowest_orbital'] = 28-20
params['highest_orbital'] = 28+20
# extended tight-binding calculation type
params['isxTB'] = False
# DFT calculation type
params['isUKS'] = False
# Periodic calculations flag
params['is_periodic'] = False
# Set the cell parameters for periodic calculations
if params['is_periodic']:
    params['A_cell_vector'] = [50.0,0.0,0.0]
    params['B_cell_vector'] = [0.0,50.0,0.0]
    params['C_cell_vector'] = [0.0,0.0,50.0]
    params['periodicity_type'] = 'XYZ'
    # Set the origin
    origin = [0,0,0]
    tr_vecs = params['translational_vectors'] = CP2K_methods.generate_translational_vectors(origin, [1,1,1],
                                                                                            params['periodicity_type'])
    
    print('The translational vectors for the current periodic system are:\n')
    print(tr_vecs)
    print(F'Will compute the S^AO between R(0,0,0) and {tr_vecs.shape[0]+1} translational vectors')

# The AO overlaps in spherical or Cartesian coordinates
params['is_spherical'] =  True
# Remove the molden files, which are large files for some systems, 
# after the computaion is done for tha system
params['remove_molden'] = True
# Cube visualization using VMD
params['cube_visualization'] = False
if params['cube_visualization']:
    # The only parts that we will change in this template are loading the cubes and rendering the images.
    params['vmd_input_template'] = '../vmd_cube_template.tcl'
    params['states_to_plot'] = [2223,2224,2225,2226]
    params['plot_phase_corrected'] = True
    params['vmd_exe'] = 'vmd'
    params['tachyon_exe'] = '/util/academic/vmd/1.9.2/lib/vmd/tachyon_LINUXAMD64'
    params['x_pixels'] = 1024
    params['y_pixels'] = 1024
    params['remove_cube'] = True
# The results are stored in this folder
params['res_dir'] = path + '/../res'
params['all_pdosfiles'] = path + '/../all_pdosfiles'
params['all_logfiles'] = path + '/../all_logfiles'
# CP2K executable 
#params['cp2k_exe'] = '/projects/academic/cyberwksp21/Software/cp2k-intel/cp2k-8.2/exe/Linux-x86-64-intelx/cp2k.psmp'
#params['cp2k_exe'] = '/projects/academic/cyberwksp21/Software/cp2k-intel/sse/cp2k/exe/Linux-x86-64-intelx/cp2k.psmp'
params['cp2k_exe'] = '/projects/academic/cyberwksp21/Software/cp2k-intel/cp2k-9.1/exe/Linux-x86-64-intelx/cp2k.psmp'
# If the xTB calculations are needed, we need an OT procedure 
#params['cp2k_ot_input_template'] = path + '/../es_ot_temp.inp'
params['cp2k_diag_input_template'] = path + '/../es_diag_temp.inp'
# The trajectory xyz file path
params['trajectory_xyz_filename'] = path + '/../adamantane-pos-1.xyz'

step2.run_cp2k_libint_step2(params)

