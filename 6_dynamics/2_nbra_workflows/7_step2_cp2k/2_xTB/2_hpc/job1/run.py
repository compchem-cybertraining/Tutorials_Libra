import os
import sys
from libra_py import CP2K_methods
from libra_py.workflows.nbra import step2


path = os.getcwd()
params = {}
# number of processors
params['nprocs'] = 12
# The mpi executable
params['mpi_executable'] = 'srun'
params['istep'] = 1
params['istep'] = 1
params['fstep'] = 51
# Lowest and highest orbital, Here HOMO is 128
params['lowest_orbital'] = 128-20
params['highest_orbital'] = 128+21
# extended tight-binding calculation type
params['isxTB'] = True
# DFT calculation type
params['isUKS'] = False
# Periodic calculations flag
params['is_periodic'] = True
# Set the cell parameters for periodic calculations
if params['is_periodic']:
    params['A_cell_vector'] = [14.2415132523,0.0000000000,0.0000000000]
    params['B_cell_vector'] = [0.0002151559,12.3343009930,0.0000000000]
    # The vacuum 
    params['C_cell_vector'] = [0.0018975023,0.0028002808,14.9999996186]
    params['periodicity_type'] = 'XY'
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
# The results are stored in this folder
params['res_dir'] = path + '/../res'
params['all_pdosfiles'] = path + '/../all_pdosfiles'
params['all_logfiles'] = path + '/../all_logfiles'
# CP2K executable 
params['cp2k_exe'] = '/projects/academic/cyberwksp21/Software/cp2k-intel/cp2k-8.2/exe/Linux-x86-64-intelx/cp2k.psmp'
# If the xTB calculations are needed, we need an OT procedure 
params['cp2k_ot_input_template'] = path + '/../es_ot_temp.inp'
params['cp2k_diag_input_template'] = path + '/../es_diag_temp.inp'
# The trajectory xyz file path
params['trajectory_xyz_filename'] = path + '/../../../../6_step1_cp2k/2_xTB/c3n4_1x1_MD_xTB-pos-1.xyz'

step2.run_cp2k_libint_step2(params)

