import libra_py
import libra_py.packages.cp2k.input as cp2k_input

#cp2k_input.generate({"input_filename":"default1.inp", "solver":"OT"})
#cp2k.input_gen.generate({"input_filename":"default2.inp", "solver":"DIAG"})
#cp2k.input_gen.generate({"input_filename":"default3.inp", "solver":"OT", "smearing":True, "added_mos":50 })
#cp2k.input_gen.generate({"input_filename":"default4.inp", "solver":"DIAG", "smearing":True, "added_mos":50 })                                                                             
#cp2k.input_gen.generate({"input_filename":"default5.inp", "solver":"DIAG", "smearing":True, "added_mos":50, "istate":1 })
#cp2k.input.generate({"input_filename":"default6.inp", "solver":"DIAG", "method":"CAM-B3LYP" })
#cp2k_input.generate({"input_filename":"default7.inp", "solver":"DIAG", "method":"HSE06" })





#============================= xTB runs =================================
# OT xTB, single point, single particle
#cp2k_input.generate({"input_filename":"md.inp", "method":"xTB", "solver":"OT", "run_type":"ENERGY"})

# DIAG + added MO xTB, single point, single particle
#cp2k_input.generate({"input_filename":"md.inp", "method":"xTB", "solver":"DIAG", "run_type":"ENERGY" })

# DIAG + added MO + Fermi smearing xTB, single point, single particle
#cp2k_input.generate({"input_filename":"md.inp", "method":"xTB", "solver":"DIAG", "run_type":"ENERGY",
#                     "smearing":True, "smearing.method":"FERMI_DIRAC", "smearing.electronic_temperature":300.0  })

# DIAG + added MO xTB, single point, sTDA approach for excitations
cp2k_input.generate({"input_filename":"md.inp", "method":"xTB", "solver":"DIAG", "istate":1 })

# In this case, we do all the same, but for root 0 (ground state), so we don't actually do the excited states calcs
#cp2k_input.generate({"input_filename":"md.inp", "method":"xTB", "solver":"DIAG", "istate":0 })



#============================== DFT runs =================================
h = {"element": "H", "basis_set":"ORB DZVP-GTH", "potential":"GTH-PBE-q1", "fit_basis_set":"cFIT3" }
c = {"element": "C", "basis_set":"ORB DZVP-GTH", "potential":"GTH-PBE-q4", "fit_basis_set":"cFIT3" }
o = {"element": "O", "basis_set":"ORB DZVP-GTH", "potential":"GTH-PBE-q6", "fit_basis_set":"cFIT3" }
ti = {"element": "Ti", "basis_set":"ORB DZVP-MOLOPT-SR-GTH", "potential":"GTH-PBE-q12", "fit_basis_set":"cFIT10" }
ti_u = {"element": "Ti", "basis_set":"ORB DZVP-MOLOPT-SR-GTH", "potential":"GTH-PBE-q12", "fit_basis_set":"cFIT10", 
        "dft_plus_u":[2, 0.1] }


# PBE with OT, single point, single particle
#cp2k_input.generate({"input_filename":"md.inp", "method":"PBE", "solver":"OT", "run_type":"ENERGY", "kinds":[c,h,o,ti]})

# PBE with DIAG, single point, single particle
#cp2k_input.generate({"input_filename":"md.inp", "method":"PBE", "solver":"DIAG", "run_type":"ENERGY", "kinds":[c,h,o,ti]})

# PBE with DIAG, single point, TDDFT (full kernel)
#cp2k_input.generate({"input_filename":"md.inp", "method":"PBE", "solver":"DIAG", "run_type":"ENERGY", "kinds":[c,h,o,ti], "istate":1 } )

# B3LYP with OT, single point, single particle
#cp2k_input.generate({"input_filename":"md.inp", "method":"B3LYP", "solver":"OT", "run_type":"ENERGY", "kinds":[c,h,o,ti]})

# HSE06 with OT, single point, single particle
#cp2k_input.generate({"input_filename":"md.inp", "method":"HSE06", "solver":"OT", "run_type":"ENERGY", "kinds":[c,h,o,ti]})



