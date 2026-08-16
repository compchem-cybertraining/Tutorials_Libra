import os
import sys
import re
import numpy as np
from liblibra_core import MATRIX, CMATRIX, CMATRIXList, Py2Cpp_int, Cpp2Py, Random
import libra_py.packages.dftbplus.methods as dftb
from libra_py import units
from libra_py.units import kB
import libra_py.dynamics.tsh.compute as tsh_dynamics
import libra_py.dynamics.tsh.plot as tsh_dynamics_plot
from recipes import fssh2
from wigner import prepare_wigner_from_modes

traj_idx = int(sys.argv[1])

output_file = f"FSSH2_traj_{traj_idx:03d}/mem_data.hdf"
if os.path.exists(output_file):
    print(f">>> Trajectory {traj_idx} already completed. Skipping.")
    sys.exit(0)

labels = ['N', 'N', 'C', 'C', 'C', 'C', 'H', 'H', 'H', 'H']
nat = len(labels)
ndof = 3 * nat
nexcitations = 5
nstates     = nexcitations + 1
ISTATE      = 3
temperature = 300.0
DT          = 0.5

mass_map = {"N": 14.0, "C": 12.0, "H": 1.0}
mass = []
for elt in labels:
    m = mass_map[elt] * units.amu
    mass.extend([m, m, m])

coords_eq_ang = [
     1.397389772,  -0.0008423226,  -0.0000282719,
    -1.397375322,   0.0008217057,  -0.0000247962,
     0.7002955864, -1.1432855270,  -0.0000115720,
    -0.7016386487, -1.1424470400,  -0.0000347895,
     0.7016531643,  1.1424276620,  -0.0000302877,
    -0.7002809311,  1.1432631340,  -0.0000160692,
     1.2652815770, -2.0944791720,  -0.0000042173,
    -1.2677524290, -2.0929674790,  -0.0000728923,
     1.2677740730,  2.0929461430,  -0.0000726997,
    -1.2652605130,  2.0944600380,  -0.0000044041
]
q_eq = np.array([x * units.Angst for x in coords_eq_ang], dtype=float)

os.chdir("/user/someshch/somesh1/dftb+/pyrazine/freq/wigner")

wigner_data = prepare_wigner_from_modes(
    labels=labels,
    q_eq=q_eq,
    mode_start=10,
    mode_end=30,
    mode_file_pattern="mode_{}.xyz",
    mass_map=mass_map,
    temperature=temperature,
    ntraj=1,
    seed=42 + traj_idx
)

ic = wigner_data["ics"][0]

nucl_params = {
    "ndof": ndof,
    "q": ic["q"].tolist(),
    "p": ic["p"].tolist(),
    "mass": mass,
    "force_constant": [0.0] * ndof,
    "q_width": [0.0] * ndof,
    "p_width": [0.0] * ndof,
    "init_type": 4
}

# ── Electronic params ──
istates = [0.0] * nstates
istates[ISTATE] = 1.0
elec_params = {
    "verbosity"    : 2,
    "init_dm_type" : 0,
    "ndia"         : nstates,
    "nadi"         : nstates,
    "rep"          : 1,
    "init_type"    : 1,
    "istates"      : istates,
    "istate"       : ISTATE
}

# ── DFTB+ params ──
dftb_params = {
    "gen_file"           : "x1.gen",
    "sk_prefix"          : "/user/someshch/somesh1/dftb+/cyclopropanone/mio/FinalSK/",
    "Driver"             : "{}",
    "SCCTolerance"       : 1.0e-6,
    "MaxSCCIterations"   : 100,
    "MaxAngularMomentum" : """{ N = "p"
                                C = "p"
                                H = "s"
                             }""",
    "Symmetry"           : "Singlet",
    "NrOfExcitations"    : nexcitations,
    "StateOfInterest"    : 1,
    "WriteSPTransitions" : "Yes",
    "WriteXplusY"        : "Yes",
    "WriteXplusYAscii"   : "Yes",
    "StateCouplings"     : "{0 5}",
    "WriteAutotestTag"   : "Yes",
    "WriteHS"            : "No",
    "WriteEigenvectors"  : "Yes",
    "EigenvectorsAsText" : "Yes",
    "PrintForces"        : "Yes",
    "Filling"            : """Fermi { Temperature [K] = 0.01 }"""
}

# ── Model params ──
model_params = {
    "atom_labels"              : labels,
    "timestep"                 : 0,
    "dftb_exe"                 : "/user/someshch/cyberwksp21/SOFTWARE/dftbplus/_install/bin/dftb+",
    "dftb_run_params"          : dftb_params,
    "working_directory_prefix" : f"non_nbra_wd_traj_{traj_idx:03d}",
    "odin_exe"                 : "/user/someshch/software/odin/odin",
    "odin_max_ang_mom"         : {"N": 2, "C": 2, "H": 1},
    "orbital_space"            : None,
    "dt"                       : DT * units.fs2au,
    "nelec_act_space"          : None,
    "ci_threshold"             : 0.002,
    "act_state"                : {0: ISTATE},
    "is_first_time"            : {0: True},
    "read_forces"              : True,
    "read_nacvs"               : False,
    "nstates"                  : nstates,
    "model"                    : 0,
    "model0"                   : 0
}

# ── Dynamics params ──
dyn_general = {
    "nsteps"                  : 40,
    "ntraj"                   : 1,
    "nstates"                 : nstates,
    "dt"                      : DT * units.fs2au,
    "num_electronic_substeps" : 25,
    "isNBRA"                  : 0,
    "is_nbra"                 : 0,
    "progress_frequency"      : 0.5,
    "which_adi_states"        : list(range(nstates)),
    "which_dia_states"        : list(range(nstates)),
    "mem_output_level"        : 3,
    "properties_to_save"      : [
        "timestep", "time", "q", "p", "f",
        "Cadi", "Cdia",
        "Epot_ave", "Ekin_ave", "Etot_ave",
        "states",
        "se_pop_adi", "se_pop_dia",
        "sh_pop_adi", "sh_pop_dia"
    ],
    "prefix"  : f"FSSH2_traj_{traj_idx:03d}",
    "prefix2" : f"FSSH2_traj_{traj_idx:03d}"
}

fssh2.load(dyn_general)


# RUN THIS SINGLE TRAJECTORY

print(f">>> Running trajectory {traj_idx}")
sys.stdout.flush()

res = tsh_dynamics.generic_recipe(
    dyn_general,
    dftb.dftb_compute_adi,
    model_params,
    elec_params,
    nucl_params,
    Random()
)

print(f">>> Trajectory {traj_idx} completed successfully")
sys.stdout.flush()
sys.exit(0)
