import numpy as np
import h5py
from functools import reduce
from scipy.special import erf
import matplotlib.pyplot as plt

"""
    Calculate the electronic states using DVR for Shin-Metiu-cavity.
    Storing the potential energy surface information.

    See (52)-(57) in J. Chem. Phys. 157, 104118 (2022)
"""

# ----------- PARAMETERS -----------
N = 300                   # number of grid points for electronic DVR
r_min, r_max = -22, 22    # range for electronic r
r_grid = np.linspace(r_min, r_max, N)
dr = r_grid[1] - r_grid[0]
L_sm1 = 18.897
Rc_sm1 = 2.8345
a_sm2 = {-1: 4.0, 1: 3.1}
L_sm2 = 19
af_sm2 = 5.0

# ----------- KINETIC ENERGY -----------
def kinetic_energy_matrix(N, dr):
    T = np.zeros((N, N))
    prefactor = 0.5
    for i in range(N):
        for j in range(N):
            if i == j:
                T[i, j] = prefactor * (np.pi ** 2) / (3 * dr ** 2) * (1 + 2 / N ** 2)
            else:
                delta = j - i
                sin_term = np.sin(np.pi * delta / N)
                T[i, j] = prefactor * 2 * (-1) ** delta * (np.pi ** 2) / ((dr * N * sin_term) ** 2)
    return T

# ----------- POTENTIAL ENERGY -----------
def V_en_matrix_sm1(r_list, R):
    """
    sm1 model
    Compute the matrix elements of the electron-nucleus potential operator
    in real space: V_ij = V_en(r_j, R) * delta_ij
    """
    r_list = np.asarray(r_list)
    V = np.zeros_like(r_list)

    for sigma in [+1, -1]:
        R_shift = R + sigma * L_sm1 / 2.0
        r_shift = r_list + sigma * L_sm1 / 2.0
        term1 = 1.0 / np.abs(R_shift)
        term2 = erf(np.abs(r_shift) / Rc_sm1) / np.abs(r_shift)
        V += term1 - term2

    V -= erf(np.abs(R - r_list) / Rc_sm1) / np.abs(R - r_list)

    V_matrix = np.diag(V)
    return V_matrix

def V_en_matrix_sm2(r_list, R):
    """
    sm2 model
    Compute the matrix elements of the electron-nucleus potential operator
    in real space: V_ij = V_en(r_j, R) * delta_ij
    """
    r_list = np.asarray(r_list)
    V = np.zeros_like(r_list)

    for sigma in [+1, -1]:
        R_shift = R + sigma * L_sm2 / 2.0
        r_shift = r_list + sigma * L_sm2 / 2.0
        term1 = 1.0 / np.abs(R_shift)
        term2 = erf(np.abs(r_shift) / a_sm2[sigma]) / np.abs(r_shift)
        V += term1 - term2

    V -= erf(np.abs(R - r_list) / af_sm2) / np.abs(R - r_list)

    V_matrix = np.diag(V)
    return V_matrix

# ----------- POTENTIAL ENERGY GRADIENT -----------
def V_en_deri_matrix_sm1(r_list, R):
    """
    Compute the matrix elements of the electron-nucleus potential gradient operator
    """
    r_list = np.asarray(r_list)
    dV = np.zeros_like(r_list)

    for sigma in [+1, -1]:
        R_shift = R + sigma * L_sm1 / 2.0
        dV += -1.0 / np.abs(R_shift)**2 * np.sign(R_shift)

    R_shift = R - r_list
    dV -= 2.0 / np.sqrt(np.pi) / Rc_sm1 * np.exp(-(R_shift/Rc_sm1)**2) / np.abs(R_shift) * np.sign(R_shift)
    dV += erf(abs(R_shift)/Rc_sm1) / np.abs(R_shift)**2 * np.sign(R_shift)
    
    dV_matrix = np.diag(dV)
    return dV_matrix


def V_en_deri_matrix_sm2(r_list, R):
    """
    Compute the matrix elements of the electron-nucleus potential gradient operator
    """
    r_list = np.asarray(r_list)
    dV = np.zeros_like(r_list)

    for sigma in [+1, -1]:
        R_shift = R + sigma * L_sm2 / 2.0
        dV += -1.0 / np.abs(R_shift)**2 * np.sign(R_shift)

    R_shift = R - r_list
    dV -= 2.0 / np.sqrt(np.pi) / af_sm2 * np.exp(-(R_shift/af_sm2)**2) / np.abs(R_shift) * np.sign(R_shift)
    dV += erf(abs(R_shift)/af_sm2) / np.abs(R_shift)**2 * np.sign(R_shift)
    
    dV_matrix = np.diag(dV)
    return dV_matrix

# ----------- PHOTONIC ENERGY -----------
def H_p_matrix(size, hwc=0.1):
    """
    Construct the photonic Hamiltonian matrix H_p.

    """
    diagonal = [hwc * (m + 0.5) for m in range(size)]
    return np.diag(diagonal)

# ----------- DIPOLE SELF POLARIZED ENERGY -----------
def dipole_matrix(r_list, R):
    """
    Compute the dipole matrix elements: D_ij = r_j * delta_ij
    """
    r_list = np.asarray(r_list)
    mu = R - r_list
    mu_matrix = np.diag(mu)
    return mu_matrix

def DVR_single_point(V_func, dV_func, R, vecs_last = None):
    # in principle, T can be computed outside the loop
    T = kinetic_energy_matrix(N, dr)
    V = V_func(r_grid, R)
    H = T + V
    eigvals, eigvecs = np.linalg.eigh(H) #electronic basis without cavity 

    # phase correction why we do this phase correction?
    if vecs_last is not None:
        # Check the phase factor
        for i in range(len(vecs_last)):
            if np.dot(eigvecs[:, i].conj(), vecs_last[i]) < 0:
                eigvecs[:, i] = -eigvecs[:, i]

    # ----------- COMPUTE PROPERTIES -----------
    # Gradients, non-adiabatic couplings, and dipole moments
    dV = dV_func(r_grid, R)
    mu = dipole_matrix(r_grid, R)
    dmu = np.eye(len(r_grid))  # Dipole gradient is identity matrix in this case
    # Transform dV to the eigenbasis 
    V = reduce(np.dot, (eigvecs.conj().T, V, eigvecs))
    dV = reduce(np.dot, (eigvecs.conj().T, dV, eigvecs))
    nac = np.zeros_like(dV)
    for p in range(len(eigvals)):
        for q in range(len(eigvals)):
            if p != q:
                nac[p,q] = dV[p,q] / (eigvals[q] - eigvals[p])
    mu = reduce(np.dot, (eigvecs.conj().T, mu, eigvecs))
    dmu = reduce(np.dot, (eigvecs.conj().T, dmu, eigvecs))
    mu_deri_analytical = dmu + np.dot(mu, nac) - np.dot(nac, mu)

    return eigvals, eigvecs, dV, nac, mu, dmu, mu_deri_analytical

def DVR_run(V_func, dV_func, R_grid, dump_dvr = False, nelec_dim_dump = 2, file_dump = "dvr.h5"):

"""
The section  computes eigenvalues, eigenvectors, gradients, non-adiabatic couplings, 
dipole moments, and their derivatives, storing them if dump_dvr is enabled. 
Additionally, it extracts key quantities such as ground and excited state 
energies, state gradients, couplings, and dipole matrix elements for use in 
plotting and dynamics simulations.
"""
    E_adia0 = np.zeros_like(R_grid)
    E_adia1 = np.zeros_like(R_grid)
    grad_g = np.zeros_like(R_grid)
    grad_e = np.zeros_like(R_grid)
    nac_ge = np.zeros_like(R_grid)
    mu_g = np.zeros_like(R_grid)
    mu_e = np.zeros_like(R_grid)
    mu_ge = np.zeros_like(R_grid)

    mu_g_deri = np.zeros_like(R_grid)
    mu_e_deri = np.zeros_like(R_grid)
    mu_ge_deri = np.zeros_like(R_grid)

    vec0_last = np.zeros(N)
    vec1_last = np.zeros(N)

    if dump_dvr:
        N_grids_R = len(R_grid)
        eigvals_info = np.zeros((N_grids_R, nelec_dim_dump))
        d_V_info = np.zeros((N_grids_R, nelec_dim_dump, nelec_dim_dump))
        nac_info = np.zeros((N_grids_R, nelec_dim_dump, nelec_dim_dump))
        mu_info = np.zeros((N_grids_R, nelec_dim_dump, nelec_dim_dump))
        d_mu_info = np.zeros((N_grids_R, nelec_dim_dump, nelec_dim_dump))
        mu_deri_info = np.zeros((N_grids_R, nelec_dim_dump, nelec_dim_dump))

    for i, R in enumerate(R_grid):
        # for phase correction
        eigvals, eigvecs, dV, nac, mu, dmu, mu_deri_analytical = \
            DVR_single_point(V_func, dV_func, R, vecs_last=[vec0_last, vec1_last])
        if dump_dvr:
            eigvals_info[i,:] = eigvals[:nelec_dim_dump]
            d_V_info[i,:,:] = dV[:nelec_dim_dump,:nelec_dim_dump]
            nac_info[i,:,:] = nac[:nelec_dim_dump,:nelec_dim_dump]
            mu_info[i,:,:] = mu[:nelec_dim_dump,:nelec_dim_dump]
            d_mu_info[i,:,:] = dmu[:nelec_dim_dump,:nelec_dim_dump]
            mu_deri_info[i,:,:] = mu_deri_analytical[:nelec_dim_dump,:nelec_dim_dump]

        E_adia0[i] = eigvals[0]  # Ground state energy
        E_adia1[i] = eigvals[1]  # First excited state energy
        vec0_last = eigvecs[:, 0]
        vec1_last = eigvecs[:, 1]

        # Select some for plotting and dynamics
        grad_g[i] = dV[0,0]  # Gradient of ground state
        grad_e[i] = dV[1,1]  # Gradient of excited state
        nac_ge[i] = nac[0,1]  # Non-adiabatic coupling
        mu_g[i] =  mu[0,0]  # Dipole moment for ground state
        mu_e[i] =  mu[1,1]  # Dipole moment for excited state
        mu_ge[i] = mu[0,1]  # Dipole moment between states
        mu_g_deri[i] = mu_deri_analytical[0,0]  # Dipole moment gradient for ground state
        mu_e_deri[i] = mu_deri_analytical[1,1]  # Dipole moment gradient for excited state
        mu_ge_deri[i] = mu_deri_analytical[0,1]  # Dipole moment gradient between states

        # One can confirm that the dipole gradient is similar to the finite difference approximation
        # for i in range(1,len(R_grid)-1):
        #     print(mu_ge_deri[i], (mu_ge[i+1] - mu_ge[i-1]) / (R_grid[i+1] - R_grid[i-1]))
    
    if dump_dvr:
        with h5py.File(file_dump, 'w') as f:
            f.create_dataset('R_grid', data=R_grid)
            f.create_dataset('eigvals', data=eigvals_info)
            f.create_dataset('d_V', data=d_V_info)
            f.create_dataset('nac', data=nac_info)
            f.create_dataset('mu', data=mu_info)
            f.create_dataset('d_mu', data=d_mu_info)
            f.create_dataset('mu_deri', data=mu_deri_info)

    return E_adia0, E_adia1, grad_g, grad_e, nac_ge, mu_g, mu_e, mu_ge, mu_g_deri, mu_e_deri, mu_ge_deri

if __name__ == "__main__":
    """
        Reproduce Figura 1 in the reference paper
    """
    R_min, R_max = -8.0, 8.0  # Range for R
    N_grids_R = 2000
    R_grid = np.linspace(R_min, R_max, N_grids_R)
    E_adia0_sm1, E_adia1_sm1, grad_g_sm1, grad_e_sm1, nac_ge_sm1, mu_g_sm1, mu_e_sm1, mu_ge_sm1,\
    mu_g_deri_sm1, mu_e_deri_sm1, mu_ge_deri_sm1 \
        = DVR_run(R_grid=R_grid,V_func=V_en_matrix_sm1, dV_func=V_en_deri_matrix_sm1, dump_dvr=True, file_dump="dvr_sm1.h5")
    E_adia0_sm2, E_adia1_sm2, grad_g_sm2, grad_e_sm2, nac_ge_sm2, mu_g_sm2, mu_e_sm2, mu_ge_sm2,\
    mu_g_deri_sm2, mu_e_deri_sm2, mu_ge_deri_sm2 \
        = DVR_run(R_grid=R_grid,V_func=V_en_matrix_sm2, dV_func=V_en_deri_matrix_sm2, dump_dvr=True, file_dump="dvr_sm2.h5")
    # ----------- PLOT RESULTS -----------
    f, ax = plt.subplots(3, 2, sharex=True, figsize=(12, 12))
    ax[0,0].plot(R_grid, E_adia0_sm1, label='E_g', color='red')
    ax[0,0].plot(R_grid, E_adia1_sm1, label='E_e', color='blue')
    ax[0,0].set_ylabel('Energy (a.u.)')
    ax[0,0].set_xlim(R_min, R_max)
    ax[0,0].set_ylim(-0.4,0.2)
    ax[0,0].legend()
    ax[1,0].plot(R_grid, abs(nac_ge_sm1), label='|nac_ge|', color='green')
    ax[1,0].set_ylabel('NAC (a.u.)')
    ax[1,0].set_ylim(0.0, 0.4)
    ax[1,0].legend()
    ax[2,0].plot(R_grid, mu_g_sm1, label='mu_g', color='red')
    ax[2,0].plot(R_grid, mu_e_sm1, label='mu_e', color='blue')
    ax[2,0].plot(R_grid, abs(mu_ge_sm1), label='|mu_ge|', color='green')
    ax[2,0].set_ylabel('Dipole moment (a.u.)')
    ax[2,0].set_xlabel('R (a.u.)')
    ax[2,0].set_ylim(-5, 5)
    ax[2,0].legend()

    ax[0,1].plot(R_grid, E_adia0_sm2, label='E_g', color='red')
    ax[0,1].plot(R_grid, E_adia1_sm2, label='E_e', color='blue')
    ax[0,1].set_ylabel('Energy (a.u.)')
    ax[0,1].set_xlim(R_min, R_max)
    ax[0,1].set_ylim(-0.4,0.4)
    ax[0,1].legend()
    ax[1,1].plot(R_grid, abs(nac_ge_sm2), label='|nac_ge|', color='green')
    ax[1,1].set_ylabel('NAC (a.u.)')
    ax[1,1].set_ylim(-1.0, 3.0)
    ax[1,1].legend()
    ax[2,1].plot(R_grid, mu_g_sm2, label='mu_g', color='red')
    ax[2,1].plot(R_grid, mu_e_sm2, label='mu_e', color='blue')
    ax[2,1].plot(R_grid, abs(mu_ge_sm2), label='|mu_ge|', color='green')
    ax[2,1].set_ylabel('Dipole moment (a.u.)')
    ax[2,1].set_xlabel('R (a.u.)')
    ax[2,1].set_ylim(-10, 20)
    ax[2,1].legend()

    plt.tight_layout()
    plt.show()
