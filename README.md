# Microstructure engineering of Ti-6Al-4V in laser powder bed fusion

## Description
This repository accompanies the publication on 
"Microstructure engineering of Ti-6Al-4V in laser powder bed fusion via 1D thermal modeling and supporting experiments"
by Carina van der Linde, et al. (see [arXiv:2604.24669](https://doi.org/10.48550/arXiv.2604.24669))

It provides the complete computational framework, simulation scripts, and supporting data used to link LPBF process parameters to thermal history and 
resulting microstructure evolution.

The work addresses the challenge of controlling phase composition in LPBF, where cyclic thermal conditions govern the formation of α_s, α_m and β phases. 
To enable efficient exploration of the large and multidimensional process parameter space, the framework couples a fast one-dimensional 
finite-difference thermal model with a phase transformation model. 
This approach allows prediction of microstructure evolution across a broad range of processing conditions while remaining computationally efficient 
and suitable for large parametric studies.

The framework is validated against experimental measurements and demonstrates sufficient accuracy while being several orders of magnitude faster than 
high-fidelity simulations. A design of experiments spanning approximately 2,000 parameter combinations—including volumetric energy density, 
layer thickness, interlayer time, and build-plate temperature—illustrates how individual process parameters influence phase evolution and provides 
practical guidelines for LPBF process design.

If you benefit from this work, please include a reference to above study. Likewise, any feedback is welcome. Please do reach out or open an issue 
if you have any questions or suggestions for improvement.

## Branch: reproducibility
For the sake of reproducibility, this branch contains Abaqus result data and input files from the 3D FEM thermal models with scan-resolved 
and layer-wise heat source, which were used to validate the 1D thermal model. 
Furthermore, the branch contains scripts focused around Abaqus model set up and workflows that are not cleaned up for public use, 
but rather serve as a record of the workflow used to set up and run the simulations and might give some hints on what to try. 
Do expect bugs and inconsistencies. 

