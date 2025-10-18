#!/bin/bash
# Build script for Render deployment

# Install system dependencies if needed
if command -v apt-get &> /dev/null; then
    echo "Installing system dependencies..."
    apt-get update && apt-get install -y build-essential python3-dev
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"