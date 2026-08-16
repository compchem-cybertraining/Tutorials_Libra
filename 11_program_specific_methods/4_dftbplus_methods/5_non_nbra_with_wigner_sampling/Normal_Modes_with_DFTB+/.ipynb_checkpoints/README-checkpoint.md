# Steps to perform normal modes calculations using DFTB+
## Step 1
Geometry optimization using GeometryOptimization Driver

Driver = GeometryOptimization {
Optimizer = Rational {}
MovedAtoms = 1:-1
MaxSteps = 100
OutputPrefix = "geom.out"
Convergence {GradElem = 1E-4} }

## Step 2

Perform Hessian calculation using SecondDerivative Driver with WriteDetailedXml = Yes,

Driver = SecondDerivatives { Delta = 0.01
}
Options = { WriteDetailedXml = Yes
WriteResultsTag = Yes }

## Step 3
Prepare modes_in.hsd file

""" 
#Needs the equilibrium geometry, at which the Hessian had been calculated
Geometry = GenFormat {
<<< x1.gen
}

DisplayModes = {
PlotModes = -24:-1 # Take the top 24 modes out of 30 modes (exclude 6 starting modes)
Animate = Yes # make xyz files showing the atoms moving
}
#You need to specify the SK-files, as the mass of the elements is needed
SlaterKosterFiles = Type2FileNames { Prefix = "/user/someshch/somesh1/dftb+/cyclopropanone/mio/FinalSK/"
Separator = "-"
Suffix = ".skf"
}
#/ Include the Hessian, which was calculated by DFTB+
Hessian = { <<< "hessian.out" }
#/ Output file settings
OutputPrefix = "modes.out"
#/ Keeps the standard structural translations/rotations out of your vibrations
AnalyseModes = Yes
#/ This file uses the 3rd input format of the modes code
InputVersion = 3
"""
#/user/someshch/cyberwksp21/SOFTWARE/dftbplus/_install/bin/modes # to run the mode analysis calculations
