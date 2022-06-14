
def set_recipe(recipe):

    # Format for the `recipe` (int list)

    name = ""
    params = { "rep_ham":0 }                              # Hamiltonian is definied in the diabatic basis initially
    params.update( {"force_method":1, "rep_force":1} )    # state-specific forces, compute them in the adiabatic rep
    params.update( {"nac_update_method":1} )              # update NACs based on derivative couplings and momenta
    params.update( {"time_overlap_method":0} )            # state-tracking based on the on-the-fly time-overlaps                         


    # ======= Hop proposal algo ======
    if recipe[0] == 0:
        name = F"{name}_FSSH"
        params.update( {"tsh_method": 0} )                    # FSSH prop algo 


    # ======= Hop acceptance =========
    if recipe[1] == 0:
        name = F"{name}_E"
        params.update( {"hop_acceptance_algo":10} )           # acceptance on the adiabatic energy conservation
    elif recipe[1] == 1:
        name = F"{name}_D"
        params.update( {"hop_acceptance_algo":20} )           # acceptance on the ability to rescale along NAC
    elif recipe[1] == 2:
        name = F"{name}_F"
        params.update( {"hop_acceptance_algo":21} )           # acceptance on the ability to rescale along dF
    elif recipe[1] == 3:
        name = F"{name}_B"
        params.update( {"hop_acceptance_algo":31} )           # acceptance with Boltzmann probability


    # ======= Velocity rescaling =========
    if recipe[2] == 0:
        name = F"{name}_V+"
        params.update( {"momenta_rescaling_algo":100} )          # rescale along V, no reversal on frustr. hops
    elif recipe[2] == 1:
        name = F"{name}_V-"
        params.update( {"momenta_rescaling_algo":101} )          # rescale along V, reversal on frustr. hops
    elif recipe[2] == 2:
        name = F"{name}_D+"
        params.update( {"momenta_rescaling_algo":200} )          # rescale along D, no reversal on frustr. hops
    elif recipe[2] == 3:
        name = F"{name}_D-"
        params.update( {"momenta_rescaling_algo":201} )          # rescale along D, reversal on frustr. hops
    elif recipe[2] == 4:
        name = F"{name}_F+"
        params.update( {"momenta_rescaling_algo":210} )          # rescale along dF, no reversal on frustr. hops
    elif recipe[2] == 5:
        name = F"{name}_F-"
        params.update( {"momenta_rescaling_algo":211} )          # rescale along dF, reversal on frustr. hops


    # ======= Decoherence options =========
    if recipe[3] == 0:
        name = F"{name}_no_decoh"
        params.update( {"decoherence_algo":-1 } )             # no decoherence
        params.update( {"decoherence_times_type":-1 } )       # no need for dephasing times
        params.update( {"dephasing_informed":0 } )            # no deph-informed

    elif recipe[3] == 1:
        name = F"{name}_IDA"
        params.update( {"decoherence_algo":1 } )              # IDA
        params.update( {"decoherence_times_type":-1 } )       # no need for dephasing times
        params.update( {"dephasing_informed":0 } )            # no deph-informed - doesn't matter

    elif recipe[3] == 2:
        name = F"{name}_mSDM_user_tau"
        params.update( {"decoherence_algo":0 } )              # mSDM
        params.update( {"decoherence_times_type":0 } )        # provided by user
        params.update( {"dephasing_informed":0 } )            # no deph-informed

    elif recipe[3] == 3:
        name = F"{name}_mSDM_user_tau_deph-inf"
        params.update( {"decoherence_algo":0 } )              # mSDM
        params.update( {"decoherence_times_type":0 } )        # provided by user
        params.update( {"dephasing_informed":1 } )            # deph-informed

    elif recipe[3] == 4:
        name = F"{name}_mSDM_EDC"
        params.update( {"decoherence_algo":0 } )              # mSDM
        params.update( {"decoherence_times_type":0 } )        # EDC
        params.update( {"dephasing_informed":0 } )            # no deph-informed

    elif recipe[3] == 5:
        name = F"{name}_mSDM_EDC_deph-inf"
        params.update( {"decoherence_algo":0 } )              # mSDM
        params.update( {"decoherence_times_type":0 } )        # EDC
        params.update( {"dephasing_informed":1 } )            # deph-informed
     
    elif recipe[3] == 6:
        name = F"{name}_mSDM_Schwartz"
        params.update( {"decoherence_algo":0 } )              # mSDM
        params.update( {"decoherence_times_type":3 } )        # Schwartz
        params.update( {"dephasing_informed":0 } )            # no deph-informed

    elif recipe[3] == 7:
        name = F"{name}_mSDM_Schwartz_deph-inf"
        params.update( {"decoherence_algo":0 } )              # mSDM
        params.update( {"decoherence_times_type":3 } )        # Schwartz
        params.update( {"dephasing_informed":1 } )            # deph-informed

    elif recipe[3] == 8:
        name = F"{name}_BC"
        params.update( {"decoherence_algo":3 } )              # Branching-corrected FSSH
        params.update( {"decoherence_times_type":-1 } )       # no need for dephasing times
        params.update( {"dephasing_informed":0 } )            # no deph-informed, doesn't matter

    elif recipe[3] == 9:
        name = F"{name}_AFSSH"
        params.update( {"decoherence_algo":2 } )              # Aumented FSSH
        params.update( {"decoherence_times_type":-1 } )       # no need for dephasing times
        params.update( {"dephasing_informed":0 } )            # no deph-informed, doesn't matter



    return name, params

def recipe_mapping(recipe):
    # mapping: [a, b, c, d] -> a * 240 + b * 60 + c * 10 + d
    # Normal FSSH: a = 0, b = 1, c = 3, d = 0   => indx = 0*240 + 1*60 + 3*10+ 0 = 90

    a, b, c, d = recipe[0], recipe[1], recipe[2], recipe[3]

    indx = 240*a + 60*b + 10*c + d

    return indx



def recipe_inv_mapping(indx):
    # mapping: [a, b, c, d] -> a * 240 + b * 60 + c * 10 + d

    r1 = indx % 240  # 60*b + 10*c + d
    r2 = r1 % 60     # 10*c + d
    d = r2 % 10
    c = (r2 - d)/10
    b = (r1 - r2)/60
    a = (indx - r1)/240
    
    return [a,b,c,d]
     

def make_all_sets():

    # ============== So far, 240 methods ============
    # mapping: [a, b, c, d] -> a * 240 + b * 60 + c * 10 + d
    # Normal FSSH: a = 0, b = 1, c = 3, d = 0   => indx = 0*240 + 1*60 + 3*10+ 0 = 90

    all_sets = []
    for a in [0]:
        for b in [0, 1, 2, 3]:
            for c in [0, 1, 2, 3, 4, 5]:
                for d in range(0, 10):
                    all_sets.append([a, b, c, d]) 

    return all_sets

