#!/bin/bash
# Simple build script for Render deployment

# Upgrade pip first
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

echo "Build completed successfully!"