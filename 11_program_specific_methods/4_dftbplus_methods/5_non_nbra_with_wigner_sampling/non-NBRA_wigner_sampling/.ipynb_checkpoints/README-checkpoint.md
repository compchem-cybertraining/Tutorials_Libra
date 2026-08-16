# This tutorial is the same as the 4_non_nbra_workflow, but uses Wigner sampling. 
# 1. 
The run_single_traj.py script performs the non-NBRA calculations using Wigner sampling, which generates the initial conditions for each trajectory.

wigner_data = prepare_wigner_from_modes(
    labels=labels,
    q_eq=q_eq,
    mode_start=10, # choose after discarding the translation, rotation and few low frequency torsional modes to prevent the unnecessary bond breaking.
    mode_end=30,
    mode_file_pattern="mode_{}.xyz",
    mass_map=mass_map,
    temperature=temperature,
    ntraj=1,
    seed=42 + traj_idx
)
ic = wigner_data["ics"][0]

# 2.
run_batch.py script is a parallel task manager designed to run multiple trajectory simulations efficiently.

In short, it does the following:

Queue Management: It sets up a queue to run a total of 10 (NTRAJ) independent trajectory simulations using a separate Python script (run_single_traj.py).

Parallel Execution: It launches these simulations in parallel, ensuring that exactly 4 (MAX_PARALLEL) are running at the same time to avoid overloading the computer's CPU.

Restart Capability (Skipping): Before starting a trajectory, it checks if the final output file (mem_data.hdf) already exists. If it does, it skips that trajectory, saving time if the script had to be restarted.

Logging: It routes the output and errors of each trajectory into its own separate log file inside a logs directory.

Monitoring and Reporting: It continuously checks which processes have finished, launches new ones to replace them, and prints a final summary of how many trajectories succeeded, failed, or were skipped.