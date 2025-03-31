#!/bin/bash

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