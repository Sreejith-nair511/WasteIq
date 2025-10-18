#!/bin/bash
# Build script for Render deployment

# Explicitly set Python version
export PYTHON_VERSION=3.9.15

# Install Python dependencies
pip install -r requirements.txt

echo "Build completed successfully!"