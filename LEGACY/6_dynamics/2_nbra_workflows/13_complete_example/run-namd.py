import matplotlib.pyplot as plt   # plots
import numpy as np
import warnings

from liblibra_core import *
import util.libutil as comn
from libra_py import units
from libra_py import data_conv
from libra_py import dynamics_plotting
import libra_py.dynamics.tsh.compute as tsh_dynamics
import libra_py.dynamics.tsh.plot as tsh_dynamics_plot
import libra_py.data_savers as data_savers

#from matplotlib.mlab import griddata
#%matplotlib inline 
warnings.filterwarnings('ignore')

colors = {}
colors.update({"11": "#8b1a0e"})  # red       
colors.update({"12": "#FF4500"})  # orangered 
colors.update({"13": "#B22222"})  # firebrick 
colors.update({"14": "#DC143C"})  # crimson   
colors.update({"21": "#5e9c36"})  # green
colors.update({"22": "#006400"})  # darkgreen  
colors.update({"23": "#228B22"})  # forestgreen
colors.update({"24": "#808000"})  # olive      
colors.update({"31": "#8A2BE2"})  # blueviolet
colors.update({"32": "#00008B"})  # darkblue  
colors.update({"41": "#2F4F4F"})  # darkslategray

clrs_index = ["11", "21", "31", "41", "12", "22", "32", "13","23", "14", "24"]

istep = 0    # the first timestep to read
fstep = 40   # the last timestep to read
dt = 0.5*41.0   # integration time-step [a.u. of time]

nsteps = fstep - istep
NSTEPS = nsteps
print(F"Number of steps = {nsteps}")

x = np.loadtxt(F'ham_sd/hvib_sd_0_im')
nstates = x.shape[0]
NSTATES = nstates                                                            
print(F"Number of states = {nstates}")


#================== Read energies =====================
Hvib, NAC, HAM = [], [], []
for step in range(istep,fstep):  
    re = MATRIX(NSTATES,NSTATES)
    im = MATRIX(NSTATES,NSTATES)  
    ze = MATRIX(NSTATES,NSTATES)
    re.Load_Matrix_From_File(F'ham_sd/st_sd_{step}_re')
    im.Load_Matrix_From_File(F'ham_sd/st_sd_{step}_im')
                                
    ham = CMATRIX(re, ze)
    nac = CMATRIX(im, ze)
    hvib = CMATRIX(re, im)

    HAM.append(ham)
    NAC.append(nac)
    Hvib.append(hvib)

#================== Read time-overlap =====================
St = []
for step in range(istep,fstep):
    re = MATRIX(NSTATES,NSTATES)
    im = MATRIX(NSTATES,NSTATES)  
    re.Load_Matrix_From_File(F'ham_sd/hvib_sd_{step}_re')
    im.Load_Matrix_From_File(F'ham_sd/hvib_sd_{step}_im')
                                                       
    st = CMATRIX(re, im)
    St.append(st)


class tmp:
    pass

def compute_model(q, params, full_id):
    timestep = params["timestep"]
    nst = params["nstates"]
    obj = tmp()

    obj.ham_adi = HAM[timestep]
    obj.nac_adi = NAC[timestep]
    obj.hvib_adi = Hvib[timestep]
    obj.basis_transform = CMATRIX(nst,nst); obj.basis_transform.identity()  #basis_transform
    obj.time_overlap_adi = St[timestep]
            
    return obj




#================== Model parameters ====================
model_params = { "timestep":0, "icond":0,  "model0":0, "nstates":NSTATES }


#=============== Some automatic variables, related to the settings above ===================

dyn_general = { "nsteps":NSTEPS, "ntraj":250, "nstates":NSTATES, "dt":dt,                                                 
                "decoherence_rates":MATRIX(NSTATES,NSTATES), "ave_gaps":MATRIX(NSTATES,NSTATES),                
                "progress_frequency":0.1, "which_adi_states":range(NSTATES), "which_dia_states":range(NSTATES),
                "mem_output_level":2,
                "properties_to_save":[ "timestep", "time","se_pop_adi", "sh_pop_adi" ],
                "prefix":F"NBRA", "prefix2":F"NBRA", "isNBRA":0
              }

#=========== Some NBRA-specific parameters - these are the key settings for running file-based NBRA calculations ===========

dyn_general.update({"ham_update_method":2})  # read adiabatic properties from mthe files
dyn_general.update({"ham_transform_method":0})  # don't attempt to compute adiabatic properties from the diabatic ones, not to override the read ones     
dyn_general.update({"time_overlap_method":0})  # don't attempt to compute those, not to override the read ones
dyn_general.update({"nac_update_method":0})    # don't attempt to recompute NACs, so that we don't override the read values
dyn_general.update({"hvib_update_method":0})   # don't attempt to recompute Hvib, so that we don't override the read values
dyn_general.update( {"force_method":0, "rep_force":1} ) # NBRA = don't compute forces, so rep_force actually doesn't matter
dyn_general.update({"hop_acceptance_algo":31, "momenta_rescaling_algo":0 })  # accept based on Boltzmann, no velocity rescaling
dyn_general.update( {"rep_tdse":1}) # the TDSE integration is conducted in adiabatic rep
dyn_general.update( {"electronic_integrator":2} )  # using the local diabatization approach to integrate TD-SE

#============ Surface hopping opntions =================
dyn_general.update({"tsh_method":0 }) # FSSH

#=========== Decoherence options =================
dyn_general.update({ "decoherence_algo":-1}) # no (additional) decoherence
#dyn_general.update({ "decoherence_algo":0}) # msdm  
#dyn_general.update({ "decoherence_algo":1}) # IDA
#dyn_general.update({ "decoherence_algo":2}) # A-FSSH, not yet ready
#dyn_general.update({ "decoherence_algo":3}) # BCSH
#dyn_general.update({ "decoherence_algo":4}) # mfsd


dyn_general.update({"decoherence_times_type":-1 }) # No decoherence times, infinite decoherence times
dyn_general.update({"do_ssy":0 }) # do no use Shenvi-Subotnik-Yang phase correction
dyn_general.update( {"dephasing_informed":0} ) # no dephasing-informed correction


#=================== Dynamics =======================
# Nuclear DOF - these parameters don't matter much in the NBRA calculations
nucl_params = {"ndof":1, "init_type":3, "q":[-10.0], "p":[0.0], "mass":[2000.0], "force_constant":[0.01], "verbosity":-1 }

# Amplitudes are sampled
elec_params = {"ndia":NSTATES, "nadi":NSTATES, "verbosity":-1, "init_dm_type":0}
elec_params.update( {"init_type":1,  "rep":1,  "istate":3, "istates":[0.0, 0.0, 0.0, 1.0] } )  # how to initialize: random phase, adiabatic representation


rnd = Random()
res = tsh_dynamics.generic_recipe(dyn_general, compute_model, model_params, elec_params, nucl_params, rnd)



pref = "NBRA"

nst = model_params["nstates"]
ntraj = dyn_general["ntraj"]

plot_params = { "prefix":pref, "filename":"mem_data.hdf", "output_level":2,
                "which_trajectories":list(range(ntraj)), "which_dofs":[0], "which_adi_states":list(range(nst)), 
                "which_dia_states":list(range(nst)), 
                "frameon":True, "linewidth":3, "dpi":300,
                "axes_label_fontsize":(8,8), "legend_fontsize":8, "axes_fontsize":(8,8), "title_fontsize":8,
                "what_to_plot":["se_pop_adi", "sh_pop_adi" ], 
                "which_energies":["potential", "kinetic", "total"],
                "save_figures":1, "do_show":0
              }

tsh_dynamics_plot.plot_dynamics(plot_params)
