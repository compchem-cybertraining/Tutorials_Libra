1. Run regular MD using DFTB+

 A. Edit the `dftb_in_md.hsd` and `run-md.py` files as needed

 B. Run

        python run-md.py


2. Convert the DFTB+-produced MD trajectory to a more common format

 A. Edit the `run-md-2.hsd` file as needed

 B. Run

        python run-md-2.py


3. Run TD-DFTB calculations to determine desired active space and states

 A. Edit the `dftb_tddftb.hsd` and `run_tddftb.py` files as needed

 B. Run

        python run-tddftb.py


4. Compute single-particle time-overlaps and energies

 A. Edit the `dftb_in_ham1.hsd`, `dftb_in_ham2.hsd`, `dftb_in_overlaps.hsd`, and `run-nacs.py` file as needed

 B. Run

        python run-nacs.py


5. Based on the Step 3 calculations, define the Slater Determinants to be used and run the mapping

 A. Edit the `run-mapping.py` file as needed

 B. Run

        python run-mapping.py


6. Finally, run the NA-MD calculations

 A. Edit the `run-namd.py` file as needed

 B. Run

        python run-namd.py




