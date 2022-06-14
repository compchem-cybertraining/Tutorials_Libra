import os
import sys
import math
import time

import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt

from liblibra_core import *
import util.libutil as comn
from libra_py import units as units
from libra_py import data_conv, data_stat, data_outs, data_read
import libra_py.workflows.nbra.decoherence_times as decoherence_times
import libra_py.workflows.nbra.step4 as step4
import libra_py.models.Tully as Tully
import libra_py.models.Holstein as Holstein
import libra_py.models.Esch_Levine as EL
import libra_py.models.Zhu as Zhu
import libra_py.dynamics.tsh.compute as tsh
import recipes

def get_all(nstates, prefix):

    Hadi, Hvib, nac, St = [], [], [], []
    dummy = MATRIX(nstates, nstates)

 
    tmp = data_read.get_data_from_file2(F"{prefix}/hvib_adi.txt", list(range(2*nstates*nstates)) )
    tmp2 = data_read.get_data_from_file2(F"{prefix}/St.txt", list(range(2*nstates*nstates)) )
    nsteps = len(tmp[0])

    for step in range(nsteps):
        # Hvib
        hvib = CMATRIX(nstates, nstates)
        for i in range(nstates):
            for j in range(nstates):
                re = tmp[2*(i*nstates+j) + 0][step]
                im = tmp[2*(i*nstates+j) + 1][step]
                hvib.set(i, j, re+1j*im)
        Hvib.append(hvib)

        # Hadi
        Hadi.append( CMATRIX(hvib.real(), dummy) )

        # NAC
        nac.append( CMATRIX(-1.0*hvib.imag(), dummy) )

        # St
        st = CMATRIX(nstates, nstates)
        for i in range(nstates):
            for j in range(nstates):
                re = tmp2[2*(i*nstates+j) + 0][step]
                im = tmp2[2*(i*nstates+j) + 1][step]
                st.set(i, j, re+1j*im)
        St.append(st)

    return Hadi, Hvib, nac, St


class tmp:
    pass

def compute_model_nbra_files(q, params, full_id):
    """   
    Read in the vibronic Hamiltonians along the trajectories    

    Args: 
        q ( MATRIX(1,1) ): coordinates of the particle, ndof, but they do not really affect anything
        params ( dictionary ): model parameters

            * **params["timestep"]** ( int ):  [ index of the file to read ]
            * **params["prefix"]**   ( string ):  [ the directory where the hdf5 file is located ]
            * **params["filename"]** ( string ):  [ the name of the HDF5 file ]
        
    Returns:       
        PyObject: obj, with the members:

            * obj.hvib_adi ( CMATRIX(n,n) ): adiabatic vibronic Hamiltonian 
            
    """
                                    
    timestep = params["timestep"]
    
    #=========== Basis transform, if available =====
    basis_transform = CMATRIX(2, 2)            
    basis_transform.identity()        
                                                
    #========= Time-overlap matrices ===================
    #time_overlap_adi = CMATRIX(2, 2)            
    #time_overlap_adi.identity()    
        
    obj = tmp()
    obj.ham_adi = params["HADI"][timestep]
    obj.nac_adi = params["NAC"][timestep]
    obj.hvib_adi = params["HVIB"][timestep]
    obj.basis_transform = basis_transform
    obj.time_overlap_adi = params["ST"][timestep]
            
    return obj






def compute_model(q, params, full_id):


    #model_params = {"nstates":2, "filename":None, "istep":0, "E_n":[0.0,  -0.001], "x_n":[0.0, 4.0], 
    #                "k_n":[0.002, 0.004], "V": [ [0.0, 0.001],  [0.001, 0.0] ],
    #                "alpha": [ [0.00, 0.00], [0.00, 0.00] ],  "x_nm": [ [0.00, 0.00], [0.00, 0.00] ] ,
    #                "w0":0.25, "w1":0.25, "eps":0.0, "i_crit":0, "delta":0.0
    #               }

    #model_params = { } #"nstates":2, "filename":None, "istep":0 }

    #model_params.update({"model":1, "V":0.00})    # LZ type


    model = params["model"]
    res = None    

    if model==1:        
        res = Tully.Tully1(q, params, full_id)
        #res = EL.JCP_2020(q, params, full_id)
    elif model==2:
        res = Tully.Tully2(q, params, full_id)
        #res = Holstein.Holstein5(q, params, full_id)
    elif model==3:
        res = Tully.Tully3(q, params, full_id)
        #res = compute_model_nbra_files(q, params, full_id)

    elif model==4:
        res = Zhu.dual_RZD(q, params, full_id)

    return res




def main_tully_mdls(model_indx, p0, recipe_indx, recipes_pool ):
    """
    Tully models

    """
    
    nthreads = 2
    batches = list(range(2))

    recipe_name, recipe = recipes.set_recipe( recipes_pool[recipe_indx] )

    methods_map = { -1 : recipe_name }  # recipe name
    init_states = [0]
    methods = [-1]

    #================== SET UP THE DYNAMICS AND DISTRIBUTED COMPUTING SCHEME  ===============                      

    rnd = Random()   
    SCH_alp = MATRIX(1, 1);  SCH_alp.set(0,0, 1.0)
    decoherence_rates = MATRIX(2,2)
    tau = 1.0/100.0  # a.u.^-1
    decoherence_rates.set(0, 1, tau)
    decoherence_rates.set(1, 0, tau)

    ave_gaps = MATRIX(2,2)
    ave_gaps.set(1,1)
   
    # Common prms
    dyn_params = { "nsteps":2000, "dt":(1.0/p0)*units.fs2au, 
                   "ntraj":25, "x0":[-15.0], "p0":[p0], "masses":[2000.0], "k":[(0.000025/2000.0) * p0**4], 
                   "nstates":2, "istate":[1, 0],
                   "which_adi_states":range(2), "which_dia_states":range(2),
                   "time_overlap_method":1, "mem_output_level":-1,  "txt_output_level":3,
                   "properties_to_save": ['timestep', 'time', 'q', 'states', 'Ekin_ave', 'Epot_ave', 
                                          'Etot_ave', 'SH_pop', 'SH_pop_raw', 'p', 'Cadi' ],
                   "state_tracking_algo":2, "convergence":0,  "max_number_attempts":1000, "min_probability_reordering":0.01,
                   "do_phase_correction":1, "Temperature": 300.0,   
                   "schwartz_decoherence_inv_alpha":SCH_alp,
                   "decoherence_rates":decoherence_rates,
                   "ave_gaps":ave_gaps,
                   "num_electronic_substeps":1,
                   "sdm_norm_tolerance":0.001,
                   "is_nbra":0
                 }
 
    # Method-defining params
    dyn_params.update( recipe )   # recipe parameters
    print(dyn_params)

    model_params = {"model":model_indx}
    # `ham_rep` sets:  rep_ham   
    # `is_nbra` sets:  force_method, rep_force, 
    #                  nac_update_method, time_overlap_method, 
    #                  hop_acceptance_algo, and momenta_rescaling_algo
    # `method` (from methods) sets: tsh_method, decoherence_algo, dephasing_informed 
    # 
    #  `-1` is a free setup for `is_nbra` and `method` parameters
    #
    ham_rep, is_nbra = 0, -1  # free-format
    #ham_rep, is_nbra = 0, 0  # non-NBRA
    #ham_rep, is_nbra = 1, 1 # file-based NBRA
    #ham_rep, is_nbra = 0, 2 # on-the-fly NBRA


    os.system(F"mkdir MDL_{model_indx}_P0_{p0}_RECIPE_{recipe_indx}")
    dyn_params.update({ "dir_prefix":F"MDL_{model_indx}_P0_{p0}_RECIPE_{recipe_indx}" })
    step4.namd_workflow(dyn_params, compute_model, model_params, rnd, nthreads, 
                        methods_map, init_states, methods, batches, "fork", True, ham_rep, is_nbra)



all_sets = recipes.make_all_sets()

fssh = recipes.recipe_mapping([0, 1, 3, 0])  
fssh_plus = recipes.recipe_mapping([0, 1, 2, 0])  

#for mdl in [1, 2, 3]:
for mdl in [4]:
    for p0 in np.arange(10.0, 40.0, 2.0):
        #for recipe_indx in all_sets:
        #for recipe_indx in [90]:
         for recipe_indx in [ fssh_plus ]:
             main_tully_mdls(mdl, p0, recipe_indx, all_sets)


