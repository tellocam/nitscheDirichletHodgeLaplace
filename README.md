# nitscheDirichletHodgeLaplace
Repository with all the code for the Hodge Laplacian with Nitsche type enforced Dirichlet boundary conditions in NGSolve. The content of this repository has been created in the context of a masters thesis in Computational Science and Engineering at ETHZ, by Camilo Tello Fachin.
```
NitscheDirichletHodgeLaplace/
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
├── run.sh                          # Bash script for environment setup and generating data and plots
├── Dockerfile                      
└── README.md
```
## Setup Instructions
First you have to clone the repository
```bash
git clone https://github.com/tellocam/nitscheDirichletHodgeLaplace.git
```
You can run the experiments Either Docker or with bash run.sh (conda required for the latter).

### Running the experiments with Docker
If you have Docker on your system you can start with building the image
```bash
docker build -t nhl-experiments .
```
After you have successfully built the image, you run the following code
```bash
    sudo docker run -it --rm \
    -v "$(pwd)/data:/app/data" \
    -v "$(pwd)/plots:/app/plots" \
    nhl-experiments
```
After execution you will have 2 new folders in the root directory of the repository,
data & plots. Since they were created with root privilege in the container, you can remove them after your done by running the following command in the root directory of the repository
```bash
sudo rm -rf data/ plots/
```

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
This repository is mainly for the purpose of recreating the numerical experiments conducted in the aforementioned thesis.
If you wish to explore other parameter and function configurations you can do so in the files oneForms2DdataGeneration.py, oneForms3DdataGeneration.py, twoForms3DdataGeneration.py. After the library imports, you can change the tested orders, meshsizes, Cw values and manufactured solutions. After you adapted the inputs, just rerun ./run.sh. Note that your plots and data from before will be overwritten. If you intend to keep them, rename them. You can also rename the folder. The script will create a new folder with the new result.