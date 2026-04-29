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

## Getting Started

### Dependencies and installing
To install the dependencies you can run:

```
pip install -r requirements.txt
```

### Structure of the program files and folders

```
abaqus_scripts/                     # Abaqus scripts to set up and run 3D FEM simulations with layer-wise heat source
abaqus_scripts/pre_processing/      # Pre-processing scripts for Abaqus simulations
abaqus_scripts/processing/          # Executing Abaqus simulations
abaqus_scripts/post_processing/     # Post-processing scripts for Abaqus simulations
data/                               # Data files containing results of 3D FEM simulation from two considered Abaqus thermal models
src/                                # Source code for the 1D FD thermal model and microstructure evolution
src/thermal_model/                  # 1D FD thermal model implementation
src/microstructure_model/           # Microstructure evolution model implementation
src/utils/                          # Utility functions
misc/                               # Miscellaneous scripts for plotting and analysis
execs/                              # Data files containing prediction results (created by investigate_microstructure_forward.py) 
```

### Executing program

#### Set up 3D FEM thermal model in Abaqus with layer-wise heat source
The Abaqus script to set up the 3D FEM thermal model with a layer-wise heat source are found in `abaqus_scripts/pre_processing/` 
for the three considered geometries: thin wall, cuboid and inverted pyramid amongst other scripts. 
Generating variations of these model in terms of volumetric energy density, inter layer time and material parameters can be done with the scripts in
`abaqus_scripts/processing/`.
Reading temperature histories from abaqus odb files and visualizing results can be done with the scripts in `abaqus_scripts/post_processing/`.

#### Set up 3D FEM thermal model in Abaqus with scan-resolved heat source
The Abaqus 3F FEM thermal model with scan-resolved heat source included in the publication accompaying this repository were set up based on 
the git repository [HighTempIntegrity/Ghanbari_Multiscale2023](https://github.com/HighTempIntegrity/Ghanbari_Multiscale2023) and 
the publication by [Scheel et al., 2023](https://doi.org/10.1016/j.ijmecsci.2023.108583). 

#### Validate 1D thermal model against Abaqus FEM 3D model with layer-wise and scan-resolved heat source
The 1D FD thermal model can be compared to the 3D FEM thermal models with both layer-wise and scan-resolved heat source via the script:
`validate_fd_1d_thermal_model_Abaqus.py`

#### Investigate microstructure evolution during LPBF of Ti6Al4V with 1D FD thermal model
The microstructure evolution during LPBF of Ti6Al4V as well as their final microstructures can be investigated with the script:
`investigate_microstructure_forward.py`

#### Visualize results of microstructure evolution during LPBF of Ti6Al4V
The results of the studies regarding the accuracy of the 1D FD thermal model 
as well as trends in microstructure evolution during LPBF of Ti6Al4V as well as their final microstructures can be visualized with the scripts:
```
misc/plot_evolution.py
misc/plot_nitzler_model.py
misc/plot_trends.py
misc/plot_forward_study.py (*)
(*) (These plots are exploratory and intended primarily for data screening and early-stage analysis. They are less polished, the code is less refined, 
and they are not included in the accompanying publication.)
```

## Authors
- [Carina van der Linde](https://github.com/C-vdL) - Main developer
- [Iason Sideris](https://github.com/iss1995) - Contributor to analytical 1D FD thermal model 

## License
This project is licensed under the MIT License.
