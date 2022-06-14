
import sys
import cmath
import math
import os
import multiprocessing as mp
import time
import numpy as np

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

#import libra_py.common_utils as comn
import util.libutil as comn

import libra_py.data_read as data_read
import libra_py.tsh as tsh
import libra_py.tsh_stat as tsh_stat
import libra_py.units as units
import libra_py.dynamics.tsh.compute as tsh_dynamics
import libra_py.dynamics.tsh.recipes as recipes
import libra_py.fit as fit
from libra_py import units, data_read

def energies_indices(indxs, nstates):

    res = []
    for indx in indxs:
        res.append( 2*(indx * nstates + indx) )

    return res


def plots(prefix, istate, name, batch):
    """
    This function produces nice plots of the ground state populations for all calculations
    """

    plt.rc('axes', titlesize=12)      # fontsize of the axes title
    plt.rc('axes', labelsize=12)      # fontsize of the x and y labels
    plt.rc('legend', fontsize=10)     # legend fontsize
    plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=8)    # fontsize of the tick labels
    plt.rc('figure.subplot', left=0.2)
    plt.rc('figure.subplot', right=0.95)
    plt.rc('figure.subplot', bottom=0.13)
    plt.rc('figure.subplot', top=0.88)
   

    t = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/time.txt", [0]) ) * units.au2fs
    q = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/q.txt", list(range(25)) ) )
    p = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/p.txt", [0]) )
    ekin = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/Ekin_ave.txt", [0]) )
    epot = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/Epot_ave.txt", [0]) )
    etot = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/Etot_ave.txt", [0]) )   
#    ham = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/hvib_adi.txt", energies_indices([8,7,6], 9) ) )
#    ham = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/hvib_adi.txt", [0, 6, 3] ) )
    pop = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/SH_pop.txt", [0, 1] ) )
    pop_raw = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/SH_pop_raw.txt", [0, 1] ) )
    cadi = np.array( data_read.get_data_from_file2(F"{prefix}/start_s{istate}_{name}_batch{batch}/Cadi.txt", [0, 1, 2, 3] ) )


    #========================= q, p vs. t =======================
    nsteps = 2998    

    figure = plt.figure(num=1, figsize=(3.21, 2.41), dpi=300, edgecolor='black', frameon=True)    
    #plt.plot(t[0], q[0], color="black", label="Q", linewidth=1)
    #plt.plot(t[0], p[0], color="red", label="P", linewidth=1)
    for i in range(25):
        plt.plot(t[0], q[i], color="black", label="", linewidth=1)
    

    plt.title("Coordinate/Momentum",fontsize=9.5)
    plt.legend(fontsize=6.75, ncol=1, loc='upper left')
    plt.xlabel('Time, fs',fontsize=10)
    plt.ylabel('Coordinate/Momentum, a.u.',fontsize=10)
    plt.tight_layout()
    plt.savefig(F"t-q-p-start_s{istate}_{name}.png", dpi=300)
    #plt.show()                                                                                                            


    #========================= q vs p =======================
    
    figure = plt.figure(num=2, figsize=(3.21, 2.41), dpi=300, edgecolor='black', frameon=True)    
    plt.plot(q[0], p[0], color="black", label="Phase portrait", linewidth=1)

    plt.title("Coordinate/Momentum",fontsize=9.5)
    plt.legend(fontsize=6.75, ncol=1, loc='upper left')
    plt.xlabel('Coordinate, a.u.',fontsize=10)
    plt.ylabel('Momentum, a.u.',fontsize=10)
    plt.tight_layout()
    plt.savefig(F"q-p-start_s{istate}_{name}.png", dpi=300)
    #plt.show()                                                                                                            



    #========================= Pop vs. t =======================
    
    figure = plt.figure(num=3, figsize=(3.21, 2.41), dpi=300, edgecolor='black', frameon=True)    
    plt.plot(t[0], pop[0], color="black", label="S0", linewidth=1)
    plt.plot(t[0], pop[1], color="blue", label="S1", linewidth=1)

    plt.title("Population",fontsize=9.5)
    plt.legend(fontsize=6.75, ncol=1, loc='upper left')
    plt.xlabel('Time, fs',fontsize=10)
    plt.ylabel('Population',fontsize=10)
    plt.tight_layout()
    plt.savefig(F"t-pop-start_s{istate}_{name}.png", dpi=300)
    #plt.show()                                                                                                            


    #========================= Pop_raw vs. t =======================
    
    figure = plt.figure(num=4, figsize=(3.21, 2.41), dpi=300, edgecolor='black', frameon=True)    
    plt.plot(t[0], pop_raw[0], color="black", label="S0", linewidth=1)
    plt.plot(t[0], pop_raw[1], color="blue", label="S1", linewidth=1)

    plt.title("Population",fontsize=9.5)
    plt.legend(fontsize=6.75, ncol=1, loc='upper left')
    plt.xlabel('Time, fs',fontsize=10)
    plt.ylabel('Population',fontsize=10)
    plt.tight_layout()
    plt.savefig(F"t-pop_raw-start_s{istate}_{name}.png", dpi=300)
    #plt.show()                                                                                                            


    #========================= E vs. t =======================
    
    figure = plt.figure(num=5, figsize=(3.21, 2.41), dpi=300, edgecolor='black', frameon=True)    
    plt.plot(t[0], ekin[0], color="black", label="Ekin", linewidth=1)
    plt.plot(t[0], epot[0], color="red", label="Epot", linewidth=1)
    plt.plot(t[0], etot[0], color="blue", label="Etot", linewidth=1)

    plt.title("Energy",fontsize=9.5)
    plt.legend(fontsize=6.75, ncol=1, loc='upper left')
    plt.xlabel('Time, fs',fontsize=10)
    plt.ylabel('Energy, a.u.',fontsize=10)
    plt.tight_layout()
    plt.savefig(F"t-energy-start_s{istate}_{name}.png", dpi=300)
    #plt.show()                                                                                                            


    #========================= Ham vs. t =======================
    """
    nsteps = 1997
    figure = plt.figure(num=6, figsize=(3.21, 2.41), dpi=300, edgecolor='black', frameon=True)    
    plt.plot(t[0][:nsteps], ham[0][:nsteps], color="black", label="E0", linewidth=1)
    plt.plot(t[0][:nsteps], ham[1][:nsteps], color="red", label="E1", linewidth=1)
    plt.plot(t[0][:nsteps], ham[2][:nsteps], color="blue", label="NAC", linewidth=1)

    plt.title("Hamiltonian",fontsize=9.5)
    plt.legend(fontsize=6.75, ncol=1, loc='upper left')
    plt.xlabel('Time, fs',fontsize=10)
    plt.ylabel('Energy, a.u.',fontsize=10)
    plt.tight_layout()
    plt.savefig(F"t-ham-start_s{istate}_{name}.png", dpi=300)
    plt.show()                                                                                                            
    """

    #========================= Cadi vs. t =======================
    #nsteps = 1997
    figure = plt.figure(num=7, figsize=(3.21, 2.41), dpi=300, edgecolor='black', frameon=True)    
    #plt.plot(t[0][:nsteps], cadi[0][:nsteps], color="black", label="C0(re)", linewidth=1)
    #plt.plot(t[0][:nsteps], cadi[1][:nsteps], color="black", label="C0(im)", linewidth=1)
    ist = 0
    plt.plot(t[0][:nsteps], cadi[ist*2+0][:nsteps]**2 + cadi[ist*2+1][:nsteps]**2, color="black", label=F"P{ist}", linewidth=3)

    #plt.plot(t[0][:nsteps], cadi[2][:nsteps], color="blue", label="C1(re)", linewidth=1)
    #plt.plot(t[0][:nsteps], cadi[3][:nsteps], color="blue", label="C1(im)", linewidth=1)
    ist = 1
    plt.plot(t[0][:nsteps], cadi[ist*2+0][:nsteps]**2 + cadi[ist*2+1][:nsteps]**2, color="blue", label=F"P{ist}", linewidth=3)

    plt.title("SE amplitudes and pops",fontsize=9.5)
    plt.legend(fontsize=6.75, ncol=1, loc='upper left')
    plt.xlabel('Time, fs',fontsize=10)
    plt.ylabel('Amplitude/Population',fontsize=10)
    plt.tight_layout()
    plt.savefig(F"t-cadi-start_s{istate}_{name}.png", dpi=300)
    #plt.show()                                                                                                            




#def plots(prefix, istate, name, batch):
#plots("AFSSH", 1, "AFSSH", 0)
#plots("AFSSH", 1, "FSSH", 0)
#plots("BC_FSSH", 1, "BC_FSSH", 0)

plots("MDL_4_P0_18.0_RECIPE_90", 0, "_FSSH_D_D-_no_decoh", 0)
