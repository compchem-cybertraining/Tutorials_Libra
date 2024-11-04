#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import matplotlib.pyplot as plt   # plots
import numpy as np
import scipy.sparse as sp
from scipy.optimize import curve_fit
import h5py
import warnings

from libra_py import units


# In[2]:


def exp_func(t, e0, tau):
    beta = 1.0
    return e0 * np.exp(-np.power(t / tau, beta))


# In[5]:


import numpy as np
import scipy.sparse as sp
import h5py
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.constants import physical_constants

# Constants for unit conversion
au2ev = physical_constants['hartree-electron volt relationship'][0]
au2fs = physical_constants['atomic unit of time'][0] * 1e15  

# Define the double exponential function
def double_exp_func(t, A1, tau1, A2, tau2, c):
    return A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2) + c

# Setup for plotting
plt.figure(figsize=(12, 18))  
energies = []

# Load energy data from files
for step in range(1000, 4994):
    energy = sp.load_npz(f'path_to_your_data/energy_data_{step}.npz').todense().real
    energies.append(np.diag(energy))

energies = np.array(energies) * au2ev  # Convert to eV

# List of methods to analyze
methods = ['Method1', 'Method2', 'Method3', 'Method4', 'Method5', 'Method6']

# Create subplots for each method
fig, axs = plt.subplots(4, 2, figsize=(12, 18))  
for c, method in enumerate(methods):
    row, col = divmod(c, 2)
    ax = axs[row, col]
    taus_double_exp = []
    averaged_times = []

    for icond in range(1, 3994, 200):
        # Load data for the current condition
        with h5py.File(f'{method}_data_icond_{icond}/data.hdf', 'r') as F:
            sh_pop = np.array(F['sh_pop_adi/data'])
            time = np.array(F['time/data'])[:3994] * au2fs 

        # Process the data
        tmp2 = np.roll(energies[0:3994, :], -icond, axis=0)
        tmp1 = np.multiply(sh_pop[0:3994, :], tmp2)
        tmp = np.sum(tmp1, axis=1)
        ax.plot(time, tmp, color='gray')  

        # Initial guess for fitting
        initial_energy = tmp[0]
        initial_guess = [initial_energy / 3, 100, initial_energy / 3, 1000, initial_energy / 3]

        # Define bounds for fitting
        bounds = ([0, 0, 0, 0, 0], [initial_energy, np.inf, initial_energy, np.inf, initial_energy])

        # Fit the data
        popt_double_exp, _ = curve_fit(double_exp_func, time, tmp, p0=initial_guess, bounds=bounds)
        A1, tau1, A2, tau2, c = popt_double_exp
        taus_double_exp.append((tau1, tau2))

        # Calculate average time
        if A1 + A2 > 0: 
            avg_tau = (A1 * tau1 + A2 * tau2) / (A1 + A2)
        else:
            avg_tau = np.nan 

        averaged_times.append(avg_tau)

    # Process fitting results
    taus_double_exp = np.array(taus_double_exp)
    ave_tau_double_exp = np.nanmean(taus_double_exp, axis=0)
    std_tau_double_exp = np.nanstd(taus_double_exp, axis=0)
    N_double_exp = len(taus_double_exp)
    Z = 1.96
    tau_error_double_exp = Z * std_tau_double_exp / np.sqrt(N_double_exp)

    # Fit line for plotting
    time_fit = np.linspace(time[0], time[-1], 1000)
    fit_line = double_exp_func(time_fit, *popt_double_exp)
    ax.plot(time_fit, fit_line, 'b--', label='Double Exp Fit', linewidth=4)

    # Display fitting results on plot
    tau_text = (
        f'Double Exp $\\tau_1$ = {int(ave_tau_double_exp[0])} $\\pm$ {int(tau_error_double_exp[0])} fs\n'
        f'$\\tau_2$ = {int(ave_tau_double_exp[1])} $\\pm$ {int(tau_error_double_exp[1])} fs\n'
        f'Avg $\\tau$ = {int(np.nanmean(averaged_times))} fs'
    )
    ax.text(0.03, 0.95, tau_text, transform=ax.transAxes, fontsize=16,
            verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

    ax.set_title(f'System Analysis: {method}', fontsize=20)
    ax.set_xlabel('Time (fs)', fontsize=16)
    ax.set_ylabel('Excess Energy (eV)', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xticks([0, 500, 1000, 1500, 2000]) 

# Final adjustments for the plot layout
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.tight_layout(rect=[0.05, 0, 1, 0.97])
plt.savefig('Methodes.png', dpi=600, bbox_inches='tight')
plt.show()


# In[23]:


import numpy as np
import scipy.sparse as sp
import h5py
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.constants import physical_constants
from libra_py import units
from libra_py.workflows.nbra import lz, step4
from libra_py import data_outs, data_conv

# Constants for unit conversion
au2ev = physical_constants['hartree-electron volt relationship'][0]
au2fs = physical_constants['atomic unit of time'][0] * 1e15  

# Double exponential function
def double_exp_func(t, A1, tau1, A2, tau2, c):
    return A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2) + c

# Single exponential function for fitting
def E_function(t, E0, Einf, tau):
    return (E0 - Einf) * np.exp(-t / tau) + Einf

# Parameters for BLLZ data retrieval
params = {
    "data_set_paths": ["path_to_your_data/"],
    "Hvib_re_prefix": "Hvib_ci_", "Hvib_re_suffix": "_re",
    "Hvib_im_prefix": "Hvib_ci_", "Hvib_im_suffix": "_im",
    "init_times": 1000, "nfiles": 3994,
    "nstates": 75, "active_space": list(range(75))
}

# Get Hvib data
Hvibs = step4.get_Hvib_scipy(params)

# Parameters for lz function
params_lz = {
    "dt": 0.5 * units.fs2au, "ntraj": 1, "nsteps": 3994, "istate": 54,
    "Boltz_opt_BL": 1, "Boltz_opt": 1, "T": 300.0,
    "do_output": True, "outfile": "output.txt", "do_return": True,
    "evolve_Markov": True, "evolve_TSH": False,
    "extend_md": False, "extend_md_time": 3994,
    "detect_SD_difference": False, "return_probabilities": False,
    "init_times": [0]
}

# Run the lz function
res, _ = lz.run(Hvibs, params_lz)
res0 = data_conv.MATRIX2nparray(res, _dtype=float)
t_data = res0[:, 0] * units.au2fs
E_SE_data = res0[:, 229] * units.au2ev

# Setup for plotting
plt.figure(figsize=(8.21, 6.41))
energies = []

# Load energy data from files
for step in range(1000, 4994):
    energy = sp.load_npz(f'path_to_your_data/energy_data_{step}.npz').todense().real
    energies.append(np.diag(energy))

energies = np.array(energies) * au2ev  # Convert to eV
e2 = energies

# List of methods to analyze
methods = ['Method1', 'Method2', 'Method3', 'Method4', 'Method5', 'Method6']

# Create subplots for each method
fig, axs = plt.subplots(2, 3, figsize=(15, 13))  # Adjusted figure size

for c, method in enumerate(methods):
    row, col = divmod(c, 3)
    ax = axs[row, col]
    taus_double_exp = []
    averaged_times = []
    
    for icond in range(1, 3994, 200):
        # Load data for the current condition
        with h5py.File(f'{method}_data_icond_{icond}/mem_data.hdf', 'r') as F:
            sh_pop = np.array(F['sh_pop_adi/data'])
            time = np.array(F['time/data'])[:3994] * au2fs  # Converted to femtoseconds

        # Process the data
        tmp2 = np.roll(e2[0:3994, :], -icond, axis=0)
        tmp1 = np.multiply(sh_pop[0:3994, :], tmp2)
        tmp = np.sum(tmp1, axis=1)
        ax.plot(time, tmp, color='gray')

        # Initial guess for fitting parameters
        initial_energy = tmp[0]
        initial_guess = [initial_energy / 3, 100, initial_energy / 3, 1000, initial_energy / 3]

        # Define bounds for fitting
        lower_bounds = [0, 0, 0, 0, 0]
        upper_bounds = [initial_energy, np.inf, initial_energy, np.inf, initial_energy]

        # Fit the data
        popt_double_exp, _ = curve_fit(double_exp_func, time, tmp, p0=initial_guess, bounds=(lower_bounds, upper_bounds))
        A1_double_exp, tau1_double_exp, A2_double_exp, tau2_double_exp, c_double_exp = popt_double_exp
        taus_double_exp.append((tau1_double_exp, tau2_double_exp))

        # Calculate the weighted average of tau
        if A1_double_exp + A2_double_exp > 0:
            weight_tau1 = A1_double_exp / (A1_double_exp + A2_double_exp)
            weight_tau2 = A2_double_exp / (A1_double_exp + A2_double_exp)
            avg_tau = weight_tau1 * tau1_double_exp + weight_tau2 * tau2_double_exp
        else:
            avg_tau = np.nan

        averaged_times.append(avg_tau)

    # Process fitting results
    taus_double_exp = np.array(taus_double_exp)
    ave_tau_double_exp = np.nanmean(taus_double_exp, axis=0)
    std_tau_double_exp = np.nanstd(taus_double_exp, axis=0)
    N_double_exp = len(taus_double_exp)
    Z = 1.96
    tau_error_double_exp = Z * std_tau_double_exp / np.sqrt(N_double_exp)

    # Plot average double exponential fit line
    time_fit = np.linspace(time[0], time[-1], 1000)
    fit_line = double_exp_func(time_fit, *popt_double_exp)
    ax.plot(time_fit, fit_line, 'b--', label='Double Exp Fit', linewidth=2.5)

    # Add fitting results to the plot
    tau_text = (
        f'Double Exp $\\tau_1$ = {ave_tau_double_exp[0]:.0f} $\\pm$ {tau_error_double_exp[0]:.0f} fs\n'
        f'$\\tau_2$ = {ave_tau_double_exp[1]:.0f} $\\pm$ {tau_error_double_exp[1]:.0f} fs\n'
        f'Weighted Avg $\\tau$ = {np.nanmean(averaged_times):.0f} fs\n'
        f'Weight $\\tau_1$ = {weight_tau1:.2f}\n'
        f'Weight $\\tau_2$ = {weight_tau2:.2f}'
    )
    ax.text(0.03, 0.95, tau_text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

    # Add BLLZ curve to the plot
    ax.plot(t_data, E_SE_data, color="red", label="BLLZ E_SE")
    ax.set_title(f'System Analysis: {method}', fontsize=20)
    ax.set_xlabel('Time (fs)', fontsize=16)
    ax.set_ylabel('Excess Energy (eV)', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)

# Final adjustments for the plot layout
plt.subplots_adjust(hspace=0.5, wspace=0.3)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('Energy+BLLZ.png', dpi=600, bbox_inches='tight')
plt.show()


# In[17]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import scipy.sparse as sp
import h5py
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.constants import physical_constants

# Constants for unit conversion
au2ev = physical_constants['hartree-electron volt relationship'][0]
au2fs = physical_constants['atomic unit of time'][0] * 1e15  

# Exponential function for fitting
def exp_func_2(t, A, tau, beta):
    return A * np.exp(-np.power(t / tau, beta))

# Initial amplitude value
A = 2.91

# Container for energies
energies = []

# Load energy data
for step in range(1000, 4994):
    energy = sp.load_npz(f'../path_to_data/energy_data_{step}.npz').todense().real
    energies.append(np.diag(energy))

energies = np.array(energies)
energies = au2ev * energies
e2 = energies

# Methods to analyze
methods = ['Method1', 'Method2', 'Method3', 'Method4', 'Method5', 'Method6']

# Create a plot
fig, ax = plt.subplots(figsize=(16, 12))

# Loop through each method
for method in methods:
    all_excess_energies = []
    taus = []

    # Analyze conditions
    for icond in range(1, 3994, 200):
        F = h5py.File(f'{method}_data_icond_{icond}/mem_data.hdf')
        sh_pop = np.array(F['sh_pop_adi/data'])
        time = np.array(F['time/data'])[0:3994] * au2fs 

        # Compute excess energy
        tmp2 = np.roll(e2[0:3994, :], -icond, axis=0)
        tmp1 = np.multiply(sh_pop[0:3994, :], tmp2)
        tmp = np.sum(tmp1, axis=1)
        all_excess_energies.append(tmp)

        # Fit the exponential function
        popt, _ = curve_fit(exp_func_2, time, tmp, bounds=([A - 0.000001, 0.0, 0.5], [A + 0.000001, np.inf, 4.0]))
        _, tau_fit, _ = popt
        taus.append(tau_fit)

    # Average excess energy
    avg_excess_energy = np.mean(all_excess_energies, axis=0)
    
    taus = np.array(taus)
    ave_tau = np.average(taus)
    std_tau = np.std(taus)
    N = len(taus)
    Z = 1.96
    tau_error = Z * std_tau / np.sqrt(N)

    # Plot results
    ax.plot(time, avg_excess_energy, label=method, linewidth=4)

# Finalize plot
ax.set_title('Excess Energy Analysis', fontsize=60)
ax.set_xlabel('Time (fs)', fontsize=54)
ax.set_ylabel('Excess Energy (eV)', fontsize=54)
ax.tick_params(axis='both', which='major', labelsize=40)
ax.legend(fontsize=24, loc='upper right', ncol=3, frameon=False)

plt.tight_layout()
plt.savefig('Energy.png', dpi=600, bbox_inches='tight')
plt.show()


# In[11]:


import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sp
import h5py
from scipy.optimize import curve_fit
from matplotlib import gridspec

# Constants
au2ev = physical_constants['hartree-electron volt relationship'][0]
au2fs = physical_constants['atomic unit of time'][0] * 1e15  

# Color palette
bright_colors = ['#3357ff', '#003f5c', '#FF5733', '#33A1FF', '#008080', '#FF33A6']

def load_adiabatic_energies(steps_range):
    energies = []
    time = None
    for step in steps_range:
        energy = sp.load_npz(f'../ustep3/res-mb-sd-DFT/Hvib_ci_{step}_re.npz').todense().real
        if time is None:
            time = np.arange(energy.shape[0]) * au2fs
        energies.append(np.diag(energy))
    return np.array(energies) * au2ev, time

def fit_excess_energy(method, time, e2):
    all_excess_energies = []
    taus = []
    for icond in range(1, 3994, 200):
        F = h5py.File(f'{method}_latestnewNBRA_icond_{icond}/mem_data.hdf')
        sh_pop = np.array(F['sh_pop_adi/data'])
        tmp2 = np.roll(e2[0:3994, :], -icond, axis=0)
        tmp1 = np.multiply(sh_pop[0:3994, :], tmp2)
        tmp = np.sum(tmp1, axis=1)
        all_excess_energies.append(tmp)

        try:
            popt, _ = curve_fit(exp_func_2, time, tmp, bounds=([2.91 - 0.000001, 0.0, 0.5], [2.91 + 0.000001, np.inf, 4.0]))
            taus.append(popt[1])
        except Exception as e:
            print(f"Error fitting data for method {method}: {e}")

    return np.mean(all_excess_energies, axis=0), taus

def plot_excess_energy(ax, time, avg_excess_energy, method, color):
    ax.plot(time, avg_excess_energy, label=method, color=color, linewidth=9)

def plot_bllz(ax, t_data, E_SE_data, popt):
    ax.plot(t_data, E_SE_data, color="red", label="BLLZ", linewidth=3)
    time_fit = np.linspace(t_data.min(), t_data.max(), 500)
    energy_fit = E_function(time_fit, *popt)
    ax.plot(time_fit, energy_fit, color="darkred", linestyle="--", label="BLLZ Fitted Curve", linewidth=2.5)

def main():
    # Load adiabatic energies
    adiabatic_energies, time = load_adiabatic_energies(range(1000, 4994))

    # Set up the plot
    plt.figure(figsize=(26, 22))
    gs = gridspec.GridSpec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4], wspace=0.05, hspace=0.05)
    ax0 = plt.subplot(gs[1, 0])
    ax1 = plt.subplot(gs[1, 1], sharey=ax0)

    # Process methods
    for method, color in zip(methods, bright_colors):
        avg_excess_energy, taus = fit_excess_energy(method, time, e2)
        if taus:
            taus = np.array(taus)
            ave_tau = np.average(taus)
            std_tau = np.std(taus)
            N = len(taus)
            tau_error = 1.96 * std_tau / np.sqrt(N)

            plot_excess_energy(ax0, time, avg_excess_energy, method, color)

    # BLLZ fitting
    params = {...}  # Define your parameters here
    res, _ = lz.run(Hvibs, params)
    res0 = data_conv.MATRIX2nparray(res, _dtype=float)
    t_data = res0[:, 0] * units.au2fs
    E_SE_data = res0[:, 229] * units.au2ev
    popt, _ = curve_fit(E_function, t_data, E_SE_data, p0=(E_SE_data[0], E_SE_data[-1], 100.0))

    plot_bllz(ax0, t_data, E_SE_data, popt)

    # Adiabatic energy levels
    for i in range(adiabatic_energies.shape[1]):
        ax0.plot(time, adiabatic_energies[:, i], linestyle='--', color='gray', alpha=0.5, linewidth=1.5)

    # Density of States
    energy_levels = res0[:, 3 * np.arange(75) + 1] * units.au2ev
    ax1.hist(energy_levels.flatten(), bins=50, density=True, orientation='horizontal', alpha=0.7, color='gray', edgecolor='black')
    ax1.set_xlabel('DOS', fontsize=54)
    ax1.tick_params(axis='x', labelsize=38)
    ax1.yaxis.set_visible(False)

    # Final plot settings
    ax0.set_title('C$_{60}$', fontsize=60)
    ax0.set_xlabel('Time (fs)', fontsize=54)
    ax0.set_ylabel('Energy (eV)', fontsize=54)
    ax0.tick_params(axis='both', which='major', labelsize=38)
    if ax0.get_legend_handles_labels()[1]:
        ax0.legend(fontsize=30, loc='upper center', bbox_to_anchor=(0.5, 0.23), ncol=3, frameon=False)

    plt.savefig('Energy+BLLZ+DOS.png', dpi=600)
    plt.show()


# In[15]:


import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sp
import h5py
from scipy.optimize import curve_fit
from matplotlib import gridspec

# Constants
au2ev = physical_constants['hartree-electron volt relationship'][0]
au2fs = physical_constants['atomic unit of time'][0] * 1e15  

# Color palette for plotting
bright_colors = ['#3357ff', '#003f5c', '#FF5733', '#33A1FF', '#008080', '#FF33A6']

def load_adiabatic_energies(steps_range):
    energies = []
    time = None
    for step in steps_range:
        energy = sp.load_npz(f'../ustep3/res-mb-sd-DFT/Hvib_ci_{step}_re.npz').todense().real
        if time is None:
            time = np.arange(energy.shape[0]) * au2fs
        energies.append(np.diag(energy))
    return np.array(energies) * au2ev, time

def fit_excess_energy(method, time, e2):
    all_excess_energies = []
    taus = []
    for icond in range(1, 3994, 200):
        F = h5py.File(f'{method}_latestnewNBRA_icond_{icond}/mem_data.hdf')
        sh_pop = np.array(F['sh_pop_adi/data'])
        time = np.array(F['time/data'])[0:3994] * au2fs  

        tmp2 = np.roll(e2[0:3994, :], -icond, axis=0)
        tmp1 = np.multiply(sh_pop[0:3994, :], tmp2)
        tmp = np.sum(tmp1, axis=1)
        all_excess_energies.append(tmp)

        # Fit the data to get tau
        try:
            popt, _ = curve_fit(exp_func_2, time, tmp, bounds=([2.91 - 0.000001, 0.0, 0.5], [2.91 + 0.000001, np.inf, 4.0]))
            _, tau_fit, _ = popt
            taus.append(tau_fit)
        except Exception as e:
            print(f"Error fitting data for method {method}: {e}")

    return np.mean(all_excess_energies, axis=0), taus

def plot_excess_energy(ax, time, avg_excess_energy, method, color):
    ax.plot(time, avg_excess_energy, label=method, color=color, linewidth=9)

def plot_bllz(ax, t_data, E_SE_data, popt):
    ax.plot(t_data, E_SE_data, color="red", label="BLLZ", linewidth=6)
    time_fit = np.linspace(t_data.min(), t_data.max(), 500)
    energy_fit = E_function(time_fit, *popt)
    ax.plot(time_fit, energy_fit, color="darkred", linestyle="--", label="BLLZ Fitted Curve", linewidth=2.5)

def load_uv_vis_data(file_path):
    x, y = [], []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip(): 
                parts = line.split()
                x.append(float(parts[0]))
                y.append(float(parts[1]))
    return np.array(x), np.array(y)

def normalize_uv_vis(y, max_hist_value):
    max_y = max(y)
    return (y / max_y) * max_hist_value

def main():
    # Load adiabatic energies
    adiabatic_energies, time = load_adiabatic_energies(range(1000, 4994))

    # Set up the plot
    plt.figure(figsize=(30, 22))
    gs = gridspec.GridSpec(2, 3, width_ratios=[4, 1, 2], height_ratios=[1, 4], wspace=0.05, hspace=0.05)
    ax0 = plt.subplot(gs[1, 0])
    ax1 = plt.subplot(gs[1, 1], sharey=ax0)

    # Process methods and plot excess energies
    for method, color in zip(methods, bright_colors):
        avg_excess_energy, taus = fit_excess_energy(method, time, e2)
        if taus:  
            plot_excess_energy(ax0, time, avg_excess_energy, method, color)

    # Energy data processing
    params = {
        "data_set_paths": ["/projects/academic/alexeyak/kosar/cp2k/fullerenes/c60-MOs60/ustep3/res-mb-sd-DFT/"], 
        "Hvib_re_prefix": "Hvib_ci_", "Hvib_re_suffix": "_re", 
        "Hvib_im_prefix": "Hvib_ci_", "Hvib_im_suffix": "_im",
        "init_times": 1000, "nfiles": 3994, 
        "nstates": 75, "active_space": list(range(75))
    }

    Hvibs = step4.get_Hvib_scipy(params)
    params = {
        "dt": 0.5 * units.fs2au, "ntraj": 1, "nsteps": 3994, "istate": 54,
        "Boltz_opt_BL": 1, "Boltz_opt": 1, "T": 300.0,  
        "do_output": True, "outfile": "BL.txt", "do_return": True, 
        "evolve_Markov": True, "evolve_TSH": False, 
        "extend_md": False, "extend_md_time": 3994,
        "detect_SD_difference": False, "return_probabilities": False,
        "init_times": [0]
    }
    params["gap_min_exception"] = 0
    params["target_space"] = 0

    res, _ = lz.run(Hvibs, params)
    res0 = data_conv.MATRIX2nparray(res, _dtype=float)

    t_data = res0[:, 0] * units.au2fs
    E_SE_data = res0[:, 229] * units.au2ev

    # Fit BLLZ
    p0 = (E_SE_data[0], E_SE_data[-1], 100.0)
    popt, _ = curve_fit(E_function, t_data, E_SE_data, p0=p0)

    plot_bllz(ax0, t_data, E_SE_data, popt)

    # Adiabatic Energy Levels
    for i in range(adiabatic_energies.shape[1]):
        ax0.plot(time, adiabatic_energies[:, i], linestyle='--', color='gray', alpha=0.5, label=f'Adiabatic Level {i+1}' if i == 0 else "", linewidth=1.5)

    # Density of States
    energy_levels = []
    for i in range(75):
        energy_levels.extend(res0[:, 3 * i + 1] * units.au2ev)
    energy_levels = np.array(energy_levels)

    hist_values, bin_edges = np.histogram(energy_levels, bins=50, density=True)
    ax1.hist(energy_levels, bins=50, density=True, orientation='horizontal', alpha=0.7, color='gray', edgecolor='black', label='DOS')
    ax1.set_xlabel('DOS', fontsize=54)
    ax1.tick_params(axis='x', labelsize=38)
    ax1.yaxis.set_visible(False)

    # Load and normalize UV-VIS data
    uv_vis_data_path = 'C60-spectrum_curve.txt'
    x_uv, y_uv = load_uv_vis_data(uv_vis_data_path)
    y_normalized = normalize_uv_vis(y_uv, hist_values.max())

    ax1.plot(y_normalized, x_uv, linestyle='-', color='b', label='UV-VIS', linewidth=9)
    ax1.set_xlabel('UV-VIS', fontsize=54)
    ax1.tick_params(axis='x', which='major', labelsize=38) 
    ax1.yaxis.set_visible(False) 

    # Final plot settings
    ax0.set_title('C$_{60}$', fontsize=60)
    ax0.set_xlabel('Time (fs)', fontsize=54)
    ax0.set_ylabel('Energy (eV)', fontsize=54)
    ax0.tick_params(axis='both', which='major', labelsize=38)

    if ax0.get_legend_handles_labels()[1]:
        ax0.legend(fontsize=28, loc='upper center',
                   bbox_to_anchor=(0.5, 0.23), 
                   ncol=3,
                   frameon=False)

    plt.savefig('Energy+BLLZ+DOS+UV.png', dpi=600)
    plt.show()


