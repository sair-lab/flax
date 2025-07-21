#!/bin/bash

VAL_REPO_URL="https://github.com/KCL-Planning/VAL.git"
VAL_REPO_DIR="VAL"

# Clone the VAL repository if it doesn't already exist
if [ ! -d "$VAL_REPO_DIR" ]; then
    git clone "$VAL_REPO_URL"
else
    echo "VAL repo already cloned."
fi

cd VAL

# Run the build script
bash ./scripts/linux/build_linux64.sh all Release

# Check if Validate runs successfully
build/linux64/Release/bin/Validate && echo "VAL installed successfully!" || echo "Installation failed."