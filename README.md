# nitscheDirichletHodgeLaplace
Repository with all the code for the Hodge Laplacian with Nitsche type enforced Dirichlet boundary conditions in NGSolve.
```
NitscheDirichletHodgeLaplace/
├── src/
│   ├── __init__.py                 # Exports all submodules as the "nhl" package
│   ├── autoDiffFunctions.py        # File with autoDiff functions for manufactured solutions
│   ├── hodgeLaplaceOneForms2D.py   # File containing the NHL functions (2D1F)
│   ├── hodgeLaplaceOneForms3D.py   # File containing the NHL functions (3D1F)
│   ├── hodgeLaplaceTwoForms2D.py   # File containing the NHL functions (2D2F)
│   └── util.py
├── data/                           # After running "bash run.sh", the data are stored here
├── plots/                          # After running "bash run.sh", the plots are stored here
├── oneForms2DdataGeneration.py     # Script for data generation (2D1F)
├── oneForms3DdataGeneration.py     # Script for data generation (3D1F)
├── twoForms3DdataGeneration.py     # Script for data generation (3D2F)
├── run.sh                          # Bash script for environment setup and generating data and plots
└── README.md
```
## Setup Instructions

### Using the Provided Bash Script

A bash script (`run.sh`) is provided to help you set up a Conda environment and run the main Python scripts.

1. **Check for Conda Installation**

The script checks if Conda is installed. If it is not, you will be prompted with instructions on how to install Miniconda. If you don't have Conda installed, follow these commands manually:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

2. **Make the bashscript executable and run it**
    
```bash
    chmod +x run.sh
    ./run.sh```
```
3. **If you prefer to run the files manually**
```bash
    conda create -n nitscheEnv python=3.8 -y
    conda activate nitscheEnv
    conda install numpy pandas matplotlib scipy -y
    pip install ngsolve

    python3 oneForms2DdataGeneration.py
    python3 oneForms3DdataGeneration.py
    python3 twoForms3DdataGeneration.py
    python3 createPlots.py
```

4. **Use of the repository**

in the files oneForms2DdataGeneration.py, oneForms3DdataGeneration.py, twoForms3DdataGeneration.py
after the library imports, you can change the tested orders, meshsizes, Cw values and manufactured solutions. After you adapted the inputs, just rerun ./run.sh. Note that your plots and data from before will be overwritten. If you intend to keep them, rename them.