import os
import sys
import time
import numpy as np

from liblibra_core import *
from libra_py.workflows.nbra import mapping, mapping2, step3
from libra_py import data_conv, data_outs, data_stat, units


# Remove the previous results and temporary working directory from the previous runs. Create a new directory
os.system("rm -r traj0"); os.system("mkdir traj0")

# Create a path to the results directory from step2
res_dir = "res/"

# Set variables based on your data in step2. Indexing is from 1
num_alpha_ks_orbs = 7 # Number of alpha spin-orbtials in the alpha spin-block from the step2 data. 
                      # By extension, this is also the number of beta spin-orbitals

data_dim          = num_alpha_ks_orbs # Total number of rows or columns in the step2 data. 
act_sp            = range(data_dim)   # Consider every spin-orbital to be in our active space
start_time  = 0    # Start reading step2 data at this index   
finish_time = 48   # Stop  reading step2 data at this index   

# Make a parameters dictionary with the relevant information about the step2 data, and then fetch this data
params = { "data_set_paths" : [res_dir],
           "data_dim":data_dim, "active_space":act_sp,
           "isnap":start_time,  "fsnap":finish_time,
         }

# These files contain N x N matrices
params.update( { "read_S_data" : 0, 
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

# Hvibs
Hvib_ks[0][0].show_matrix()
Hvib_ks[0][47].show_matrix()

# Sts 
St[0][0].show_matrix()
St[0][37].show_matrix()

"""

# We used `mo_active_space":list(range(290, 297))`
# HOMO is 292, so out active space consists of:
# act sp indices:      290   291   292  293   294    295    296  
# dftb MO indices:     291   292   293  294   295    296    297      
# Orbitals:            H-1    H     L   L+1   L+2    L+3    L+4
# User notation:        1     2     3    4     5      6      7   
#  

From the TD-DFT calculations, we got these states:
GS                                                                                       [1, -1, 2, -2]

      2.436        0.00059353       292   ->   293        1.000       2.431      S       [1, -1, 3, -2]   H->L
      2.489        0.00004560       292   ->   294        1.000       2.489      S       [1, -1, 4, -2]   H->L+1
      2.528        0.00194466       292   ->   295        1.000       2.513      S       [1, -1, 5, -2]   H->L+2
      2.556        0.00030835       292   ->   296        1.000       2.556      S       [1, -1, 6, -2]   H->L+3
      2.612        0.00018283       291   ->   293        1.000       2.609      S       [3, -1, 2, -2]   H-1->L
      2.624        0.00139939       292   ->   297        0.998       2.619      S       [1, -1, 7, -2]   H->L+4
      2.649        0.00405776       292   ->   298        0.999       2.641      S       [1, -1, 8, -2]   H->L+5      (can not be treated)
      2.670        0.00008806       291   ->   294        1.000       2.667      S       [4, -1, 2, -2]   H-1->L+1
      2.681        0.00038119       290   ->   293        0.999       2.671      S       [N/A]   H-2->L      (can not be treated)
      2.694        0.00106703       291   ->   295        1.000       2.692      S       [5, -1, 2, -2]   H-1->L+2

"""


# We exclude S6 and S7

GS = [1, -1, 2, -2]              
S1 = [1, -1, 3, -2]
S2 = [1, -1, 4, -2]
S3 = [1, -1, 5, -2] # the brightest state
S4 = [1, -1, 6, -2]
S5 = [3, -1, 2, -2]
S6 = [1, -1, 7, -2]


basis = [ GS, S1, S2, S3 ]

os.system("rm -r ham_sd"); os.system("mkdir ham_sd")
dt = 41.0
dE = [0.0, 0.0, 0.0, 0.0]

for i in range(0, 48):

    E = mapping.energy_mat_arb(basis, Hvib_ks[0][i] , dE)

    st = mapping2.ovlp_mat_arb(basis, basis, St[0][i], reduce_det=0)
    st.real().show_matrix(F"ham_sd/st_sd_{i}_re")
    st.imag().show_matrix(F"ham_sd/st_sd_{i}_im")

    nac = (st - st.H() )/(2.0 * dt)
    Hvib = E - 1j * nac
    Hvib.real().show_matrix(F"ham_sd/hvib_sd_{i}_re")
    Hvib.imag().show_matrix(F"ham_sd/hvib_sd_{i}_im")







