# nitscheDirichletHodgeLaplace
Repository containing the code for the Hodge Laplacian with Nitsche-type enforced Dirichlet boundary conditions in NGSolve. The content of this repository was created for a master's thesis in Computational Science and Engineering at ETH Zürich by Camilo Tello Fachin.
```
nitscheDirichletHodgeLaplace/
├── src/
│   ├── __init__.py                 # Exports all submodules as the "nhl" package
│   ├── autoDiffFunctions.py        # File with autoDiff functions for manufactured solutions
│   ├── hodgeLaplaceOneForms2D.py   # File containing the NHL functions (2D1F)
│   ├── hodgeLaplaceOneForms3D.py   # File containing the NHL functions (3D1F)
│   ├── hodgeLaplaceTwoForms2D.py   # File containing the NHL functions (2D2F)
│   └── util.py
├── oneForms2DdataGeneration.py     # Script for data generation (2D1F)
├── oneForms3DdataGeneration.py     # Script for data generation (3D1F)
├── twoForms3DdataGeneration.py     # Script for data generation (3D2F)
├── run.sh                          # Bash script for environment setup and generating data/plots
├── Dockerfile
└── README.md
```
## Setup Instructions
First, clone the repository:
```bash
git clone https://github.com/tellocam/nitscheDirichletHodgeLaplace.git
cd nitscheDirichletHodgeLaplace
```
You can run the experiments either via Docker or with the ```run.sh``` script (the latter requires Conda).

### Running the experiments with Docker
Pull the Docker image:
```bash
docker pull ghcr.io/tellocam/nhl:latest
```
Run the container (using ```sudo``` if necessary):
```bash
    docker run --rm -it \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/plots:/app/plots \
    ghcr.io/tellocam/nhl:latest
```
After execution, two new folders (```data``` and ```plots```) will appear in the root directory of the repository. These folders were created by the container (often with root privileges), so if you want to remove them later, run:
```bash
sudo rm -rf data/ plots/
```

### Using the Provided Bash Script
A Bash script (```run.sh```) is provided to help you set up a Conda environment and run the main Python scripts.

1. **Check for Conda Installation**
The script checks if Conda is installed. If it is not, you will be prompted with instructions to install Miniconda. If you don’t have Conda installed, follow these commands manually:
```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
```

2. **Make the bashscript executable and run it**
```bash
    chmod +x run.sh
    ./run.sh
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

This repository is primarily for recreating the numerical experiments conducted in the aforementioned thesis. If you wish to explore different parameters or manufactured solutions, you can modify the following files:

```oneForms2DdataGeneration.py```

```oneForms3DdataGeneration.py```

```twoForms3DdataGeneration.py```

After changing orders, mesh sizes, Cw values etc., simply re-run:
```bash
    ./run.sh
```
Note: Your previous data and plots will be overwritten after a rerun. 
If you intend to keep them, rename or move them before re-running. 
You could also rename the folder in the scripts; a new folder with the updated results will be created.

That’s it! Feel free to reach out if you have any questions or run into any issues.
