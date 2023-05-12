from liblibra_core import *

def load(dyn_general):

    # Uncomment one of the options in each of the categories below:
    #====== How to update Hamiltonian ===================
    #dyn_general.update({"ham_update_method":0}) # don't update any Hamiltonians
    dyn_general.update({"ham_update_method":1})  # recompute only diabatic Hamiltonian, common choice for model Hamiltonians 
    #dyn_general.update({"ham_update_method":2})  # recompute only adiabatic Hamiltonian; use with file-based or on-the-fly workflows


    #====== How to transform the Hamiltonians between representations ============
    #dyn_general.update( {"ham_transform_method":0 }) # don't do any transforms; usually for NBRA or on-the-fly workflows, 
                                                      # so you don't override the read values
    dyn_general.update( {"ham_transform_method":1 }) # diabatic->adiabatic according to internal diagonalization
    #dyn_general.update( {"ham_transform_method":2 }) # diabatic->adiabatic according to internally stored basis transformation matrix
    #dyn_general.update( {"ham_transform_method":3 }) # adiabatic->diabatic according to internally stored basis transformation matrix
    #dyn_general.update( {"ham_transform_method":4 }) # adiabatic->diabatic according to local diabatization method

    #====== How do get the time-overlaps in the dynamics ========
    #dyn_general.update( {"time_overlap_method":0 })  # don't update time-overlaps - maybe they are already pre-computed and read
    dyn_general.update( {"time_overlap_method":1 }) # explicitly compute it from the wavefunction info; common for model Hamiltonians

    #================== How to compute NACs ===============================
    dyn_general.update({"nac_update_method":1})  # explicit NAC calculations - let's just focus on this one for now
    #dyn_general.update({"nac_update_method":2, "nac_algo":0})  # HST algo
    #dyn_general.update({"nac_update_method":2, "nac_algo":1})  # NPI algo

    #============== How to compute vibronic Hamiltonian ==============
    #dyn_general.update( {"hvib_update_method":0 }) # don't update Hvib; maybe because we read it from files
    dyn_general.update( {"hvib_update_method":1 }) # recompute diabatic and adiabatic Hvib from the Ham and NACs in those reps

    #=========== Ehrenfest or state-resolved options ===========
    # This is what we use with any of the TSH-based methods - in all cases here, we would 
    # use "rep_force":1 so that we are guided by the forces derived from the adiabatic surfaces.
    # In Ehrenfest cases though, the forces can be computed using only diabatic properties though 
    #dyn_general.update( {"force_method":1, "rep_force":1} ) # state-resolved (e.g. TSH) with adiabatic forces
    #dyn_general.update( {"force_method":2, "rep_force":1} ) # for Ehrenfest in adiabatic rep
    dyn_general.update( {"force_method":2, "rep_force":0} ) # for Ehrenfest in diabatic rep


    #============ Types of surface hopping acceptance and momenta rescaling opntions =================
    #dyn_general.update({"hop_acceptance_algo":10, "momenta_rescaling_algo":100 })  # accept and rescale based on total energy, do not reverse on frustrated
    dyn_general.update({"hop_acceptance_algo":10, "momenta_rescaling_algo":101 })  # accept and rescale based on total energy, reverse on frustrated
    #dyn_general.update({"hop_acceptance_algo":20, "momenta_rescaling_algo":200 })  # accept and rescale based on NAC vectors, do not reverse on frustrated
    #dyn_general.update({"hop_acceptance_algo":20, "momenta_rescaling_algo":201 })  # accept and rescale based on NAC vectors, reverse on frustrated
    #dyn_general.update({"hop_acceptance_algo":21, "momenta_rescaling_algo":200 })  # accept and rescale based on force differences, do not reverse on frustrated
    #dyn_general.update({"hop_acceptance_algo":21, "momenta_rescaling_algo":201 })  # accept and rescale based on force differences, reverse on frustrated


    #============ Surface hopping opntions =================
    dyn_general.update({"tsh_method":-1 }) # adiabatic, no surface hopping
    #dyn_general.update({"tsh_method":0 }) # FSSH
    #dyn_general.update({"tsh_method":1 }) # GFSH
    #dyn_general.update({"tsh_method":2 }) # MSSH
    #dyn_general.update({"tsh_method":3, "rep_lz":0 })  # LZ options
    #dyn_general.update({"tsh_method":4, "rep_lz":0 }) # ZN
    #dyn_general.update({"tsh_method":5 }) # DISH

    #=========== Decoherence options =================
    dyn_general.update({ "decoherence_algo":-1}) # no (additional) decoherence
    #dyn_general.update({ "decoherence_algo":0}) # msdm  
    #dyn_general.update({ "decoherence_algo":1}) # IDA
    #dyn_general.update({ "decoherence_algo":2}) # A-FSSH, not yet ready
    #dyn_general.update({ "decoherence_algo":3}) # BCSH
    #dyn_general.update({ "decoherence_algo":4}) # mfsd

    #=========== Decoherence times (for decoherence options 0 or 4) ==================
    A = MATRIX(2,2); A.set(0, 0, 10.0); A.set(1,1, 10.0)
    dyn_general.update({"decoherence_times_type":-1 }) # No decoherence times, infinite decoherence times
    #dyn_general.update( { "decoherence_times_type":1, "decoherence_C_param": 1.0, "decoherence_eps_param":0.1 } )  # EDC + default params
    #dyn_general.update( { "decoherence_times_type":2, "schwartz_decoherence_inv_alpha":A } ) # Schwartz version 1
    #dyn_general.update( { "decoherence_times_type":3, "schwartz_decoherence_inv_alpha":A } ) # Schwartz version 2

    #======= Various decoherence-related parameters =====================
    dyn_general.update( {"dephasing_informed":0, "decoherence_rates":MATRIX(2,2), "ave_gaps":MATRIX(2,2) } )
                               
    #=========== Phase correction of SSY =================
    dyn_general.update({"do_ssy":0 }) # do no use it - that's the default

    #=========== What to integrate ==================
    # solve TD-SE in diabatic representation
    #dyn_general.update({"rep_tdse":0, "electronic_integrator":-1 })   # no propagation
    dyn_general.update({"rep_tdse":0, "electronic_integrator":0 })    # Lowdin exp_ with 2-point Hvib_dia
    #dyn_general.update({"rep_tdse":0, "electronic_integrator":1 })    # based on QTAG propagator
    #dyn_general.update({"rep_tdse":0, "electronic_integrator":2 })    # based on modified QTAG propagator (Z at two times)
    #dyn_general.update({"rep_tdse":0, "electronic_integrator":3 })    # non-Hermitian integrator with 2-point Hvib_dia

    # solve TD-SE in adiabatic representation
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":-1 })  # no propagation
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":0 })   # ld, with crude splitting,  with exp_
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":1 })   # ld, with symmetric splitting, with exp_
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":2 })   # ld, original, with exp_
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":3 })   # 1-point, Hvib integration, with exp_
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":4 })   # 2-points, Hvib integration, with exp_
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":5 })   # 2-points, Hvib, integration with the second-point correction of Hvib, with exp_
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":6 })   # same as 4, but without projection matrices (T_new = I)
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":10 })  # same as 0, but with rotations
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":11 })  # same as 1, but with rotations
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":12 })  # same as 2, but with rotations
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":13 })  # same as 3, but with rotations
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":14 })  # same as 4, but with rotations
    #dyn_general.update({"rep_tdse":1, "electronic_integrator":15 })  # same as 5, but with rotations

    # solve QCLE in diabatic representation
    #dyn_general.update({"rep_tdse":3, "electronic_integrator":0 })  # mid-point Hvib, using exp_
 
    # solve QCLE in adiabatic representation
    #dyn_general.update({"rep_tdse":3, "electronic_integrator":0 })  # mid-point Ham with the second-point correction of Hvib, using exp_
    #dyn_general.update({"rep_tdse":3, "electronic_integrator":1 })  # using Zhu Liouvillian THIS IS NOT JUST A DIFFERENT INTEGRATOR!!!!
    #dyn_general.update({"rep_tdse":3, "electronic_integrator":10 }) # same as 0 but with rotations
