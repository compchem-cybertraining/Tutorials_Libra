import os
import sys
import subprocess
import time

# CONFIGURATION

NTRAJ          = 10
PYTHON_EXE     = sys.executable
SINGLE_SCRIPT  = "run_single_traj.py"
MAX_PARALLEL   = 4          
LOG_DIR        = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

# TRACK STATUS

completed = []
failed    = []
skipped   = []

print(f">>> Starting {NTRAJ} trajectories")
print(f">>> Max parallel jobs: {MAX_PARALLEL}")
print("="*60)

running_procs = {}
traj_queue = list(range(NTRAJ))

while traj_queue or running_procs:

    # ── Fill up to MAX_PARALLEL slots ──
    while len(running_procs) < MAX_PARALLEL and traj_queue:
        traj_idx = traj_queue.pop(0)

        # Skip if already completed
        output_file = f"FSSH2_traj_{traj_idx:03d}/mem_data.hdf"
        if os.path.exists(output_file):
            print(f"    Traj {traj_idx:03d} already done — skipping")
            skipped.append(traj_idx)
            continue

        log_path = os.path.join(LOG_DIR, f"traj_{traj_idx:03d}.log")
        log_file = open(log_path, "w")

        proc = subprocess.Popen(
            [PYTHON_EXE, SINGLE_SCRIPT, str(traj_idx)],
            stdout=log_file,
            stderr=log_file
        )
        running_procs[traj_idx] = (proc, log_file)
        print(f"     Launched traj {traj_idx:03d}  (PID {proc.pid})")

    # ── Check finished processes ──
    finished_now = []
    for traj_idx, (proc, log_file) in running_procs.items():
        retcode = proc.poll()
        if retcode is not None:
            log_file.close()
            if retcode == 0:
                print(f"    ✅ Traj {traj_idx:03d} completed")
                completed.append(traj_idx)
            else:
                print(f"    Traj {traj_idx:03d} FAILED (exit code {retcode})")
                failed.append(traj_idx)
            finished_now.append(traj_idx)

    for t in finished_now:
        del running_procs[t]

    # ── Wait before checking again ──
    if running_procs:
        time.sleep(5)


# FINAL SUMMARY

print("\n" + "="*60)
print(">>> FINAL SUMMARY")
print(f"    Requested  : {NTRAJ}")
print(f"    Completed  : {len(completed)}")
print(f"    Skipped    : {len(skipped)}")
print(f"    Failed     : {len(failed)}")
if failed:
    print(f"    Failed idx : {failed}")
print("="*60)
