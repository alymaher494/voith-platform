#!/bin/bash
set -e

echo "Installing CUDA 12 + cuDNN 9 runtime dependencies for WhisperX..."

sudo apt update

# Install cuDNN for CUDA 12
sudo apt install -y libcudnn9-cuda-12 libcudnn9-dev-cuda-12

# Ensure correct library paths
if ! grep -q "LD_LIBRARY_PATH" ~/.bashrc; then
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH' >> ~/.bashrc
fi

echo "Done. Please restart your terminal."