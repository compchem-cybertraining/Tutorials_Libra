import os
import sys
import time
import numpy as np

from liblibra_core import *
from libra_py.workflows.nbra import mapping, mapping2, mapping3, step3
from libra_py import data_conv, data_outs, data_stat, units


# Remove the previous results and temporary working directory from the previous runs. Create a new directory
#os.system("rm -r traj0"); os.system("mkdir traj0")

# Create a path to the results directory from step2
res_dir = "res/"

############################################################################
#    VERY IMPORTANT - make sure to correctly set `num_aplpha_ks_orbs`  !!!!
############################################################################

# Set variables based on your data in step2. Indexing is from 1
num_alpha_ks_orbs = 569 # Number of alpha spin-orbtials in the alpha spin-block from the step2 data. 
                        # By extension, this is also the number of beta spin-orbitals

data_dim  = num_alpha_ks_orbs # Total number of rows or columns in the step2 data. 
act_sp    = range(data_dim)   # Consider every spin-orbital to be in our active space
start_time  = 0    # Start reading step2 data at this index   
finish_time = 47  # Stop  reading step2 data at this index   

# Make a parameters dictionary with the relevant information about the step2 data, and then fetch this data
params = { "data_set_paths" : [res_dir],
           "data_dim":data_dim, "active_space":act_sp,
           "isnap":start_time,  "fsnap":finish_time,
         }

# These files contain N x N matrices
params.update( { "read_S_data" : 1, 
                 "S_data_re_prefix": "S_",  "S_data_re_suffix": "_re",
                 "S_data_im_prefix": "S_",  "S_data_im_suffix": "_im",
                 "read_St_data" : 1,
                 "St_data_re_prefix": "St_",  "St_data_re_suffix": "_re",
                 "St_data_im_prefix": "St_",  "St_data_im_suffix": "_im",
                 "read_hvib_data" : 1,
                 "hvib_data_re_prefix": "hvib_",  "hvib_data_re_suffix": "_re",
                 "hvib_data_im_prefix": "hvib_",  "hvib_data_im_suffix": "_im" }
             )
S, St, Hvib_ks = step3.get_step2_data(params)

# S
#S[0][0].show_matrix()
#S[0][2].show_matrix()

# Hvibs
#Hvib_ks[0][0].show_matrix()
#Hvib_ks[0][2].show_matrix()

# Sts 
#St[0][0].show_matrix()
#St[0][2].show_matrix()


"""

The HOMO is 292
The TD-DFTB calculations yield this:

GS                                                                                       [6, -6, 7, -7]

      2.558        0.00000028       292   ->   293        1.000       2.558      S       [6, -6, 8, -7]  H   -> L
      2.797        0.00051493       291   ->   293        1.000       2.796      S       [8, -6, 7, -7]  H-1 -> L
      2.811        0.00005673       292   ->   294        1.000       2.810      S       [6, -6, 9, -7]  H   -> L+1
      2.853        0.00027415       292   ->   295        1.000       2.853      S       [6, -6,10, -7]  H   -> L+2
      2.909        0.00000676       292   ->   296        1.000       2.908      S       [6, -6,11, -7]  H   -> L+3
      2.939        0.00022816       292   ->   297        1.000       2.939      S       [6, -6,12, -7]  H   -> L+4
      2.961        0.00002725       292   ->   298        1.000       2.960      S       [6, -6,13, -7]  H   -> L+5
      2.979        0.00001034       292   ->   299        1.000       2.978      S       [6, -6,14, -7]  H   -> L+6
      3.029        0.00034158       292   ->   300        1.000       3.026      S       [6, -6,15, -7]  H   -> L+7
      3.029        0.00017169       289   ->   293        1.000       3.029      S       excluded

# The HOMO is 292, so out active space can be selected as:
# `mo_active_space":list(range(285, 305))`
# act sp indices:   285  286  287   288    289    290   291   292  293   294    295    296   297   298  299   ....  
# dftb MO indices:                                291   292   293  294   295    296    297   298   299  300   ....
# Orbitals:                                       H-1    H     L   L+1   L+2    L+3    L+4   L+5   L+6  L+7   ....
# User notation:                                   1     2     3    4     5      6      7     8     9    10   (old)
                     1    2    3     4      5      6     7     8    9    10     11     12    13    14    15

"""

# We exclude S10

GS = [6, -6, 7, -7]
              
S1 = [6, -6, 8, -7]
S2 = [8, -6, 7, -7]
S3 = [6, -6, 9, -7]
S4 = [6, -6,10, -7]
S5 = [6, -6,11, -7]
S6 = [6, -6,12, -7]
S7 = [6, -6,13, -7]
S8 = [6, -6,14, -7]
S9 = [6, -6,15, -7]

basis = [ GS, S1, S2, S3 ]


GS_2 = [5, -5, 6, -6, 7, -7]
S1_2 = [5, -5, 6, -6, 8, -7]
S2_2 = [5, -5, 8, -6, 7, -7]
S3_2 = [5, -5, 6, -6, 9, -7]

basis2 = [GS_2, S1_2, S2_2, S3_2]

os.system("rm -r ham_sd"); os.system("mkdir ham_sd")
#os.system("rm -r ham_sd2"); os.system("mkdir ham_sd2")

dt = 0.5*41.0
dE = [0.0, 0.0, 0.0, 0.0]




which_approach = 2 # 0 - old, 1 - new, 2 - even newer

for i in range(0, 47):

    E = mapping.energy_mat_arb(basis2, Hvib_ks[0][i] , dE)

    s, st = None, None 

    if which_approach == 0:
        # ============= Old approach ========================
        st = data_conv.MATRIX2nparray(St[0][i].real(), np.float64)
        st = mapping.ovlp_mat_arb(basis2, basis2, st, use_minimal=False, use_mo_approach=False, user_notation=0)

        s = data_conv.MATRIX2nparray(S[0][i].real(), np.float64)
        s = mapping.ovlp_mat_arb(basis2, basis2, s, use_minimal=False, use_mo_approach=False, user_notation=0)

        s = data_conv.nparray2CMATRIX( np.array(s, dtype=np.complex128))
        st = data_conv.nparray2CMATRIX( np.array(st, dtype=np.complex128) )

    elif which_approach == 1:
        # ============== New approach =============================
        st = mapping2.ovlp_mat_arb(basis2, basis2, St[0][i]) # reduce_det=True)
        s = mapping2.ovlp_mat_arb(basis2, basis2, S[0][i]) # reduce_det=True)

    elif which_approach == 2:
        # ============== New approach =============================
        st = data_conv.MATRIX2nparray(St[0][i].real(), np.float64)
        st = mapping3.ovlp_mat_arb(basis2, basis2, st) 

        s = data_conv.MATRIX2nparray(S[0][i].real(), np.float64)
        s = mapping3.ovlp_mat_arb(basis2, basis2, s) 

        s = data_conv.nparray2CMATRIX( np.array(s, dtype=np.complex128))
        st = data_conv.nparray2CMATRIX( np.array(st, dtype=np.complex128) )


    # =============== Printing to files =========================
    st.real().show_matrix(F"ham_sd/st_sd_{i}_re")
    st.imag().show_matrix(F"ham_sd/st_sd_{i}_im")
    s.real().show_matrix(F"ham_sd/s_sd_{i}_re")
    s.imag().show_matrix(F"ham_sd/s_sd_{i}_im")

    nac = (st - st.H() )/(2.0 * dt)
    Hvib = E - 1j * nac
    Hvib.real().show_matrix(F"ham_sd/hvib_sd_{i}_re")
    Hvib.imag().show_matrix(F"ham_sd/hvib_sd_{i}_im")





