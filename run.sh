#!/bin/bash
ENV_NAME="nhlEnv"
PYTHON_VERSION="3.8"

if ! command -v conda &> /dev/null; then
    echo "Conda is not installed."
    echo "To install Linux 64bit Miniconda, run the following commands:"
    echo "  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    echo "  bash Miniconda3-latest-Linux-x86_64.sh"
    echo "If you dont use Linux maybe you should consider doing so"
    exit 1  
fi

# Create nhlEnv if it doesn't exist
if conda env list | grep -q "$ENV_NAME"; then
    echo "nhlEnv already exists."
else
    echo "Creating Conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
    conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -y
fi

# Activate the environment.
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

echo "Installing required packages..."
conda install -y numpy pandas matplotlib scipy
pip install ngsolve

# Check if the "data" directory exists; if not, create it.
if [ ! -d "data" ]; then
    mkdir data
    echo "Created directory: data"
fi

# Check if the "plots" directory exists; if not, create it.
if [ ! -d "plots" ]; then
    mkdir plots
    echo "Created directory: plots"
fi

# Running files, here please comment and uncommend the ones you are not interested in after the first run :-)
echo "Running data generation for 2D 1-forms"
python3 oneForms2DdataGeneration.py

echo "Running data generation for 3D 1-forms"
python3 oneForms3DdataGeneration.py

echo "Running data generation for 2D 2-forms"
python3 twoForms3DdataGeneration.py

echo "Creating all plots"
python3 createPlots.py

echo "All done."