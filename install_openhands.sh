#!/bin/bash

# Create a Python 3.9 virtual environment
python3.9 -m venv openhands_venv

# Activate the virtual environment
source openhands_venv/bin/activate

# Install specific version of pip
pip install pip==23.3.1

# Clone the OpenHands repository
git clone https://github.com/AI4Bharat/OpenHands.git
cd OpenHands

# Install dependencies
pip install -e .

# Run the CLI with magic
python -c "
import openhands.cli.main
openhands.cli.main.main()
"

# Keep the terminal open
exec $SHELL
