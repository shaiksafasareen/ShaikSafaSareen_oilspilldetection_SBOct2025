#!/bin/bash

# Oil Spill Detection System - Setup Script

echo "🌊 Oil Spill Detection System - Setup"
echo "======================================"
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Anaconda or Miniconda first."
    exit 1
fi

echo "📦 Creating conda environment 'oil_spill'..."
conda env create -f environment.yml

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Environment created successfully!"
    echo ""
    echo "🚀 To activate the environment, run:"
    echo "   conda activate oil_spill"
    echo ""
    echo "🚀 To run the application, run:"
    echo "   streamlit run app.py"
    echo ""
else
    echo "❌ Failed to create environment. Please check the error messages above."
    exit 1
fi

