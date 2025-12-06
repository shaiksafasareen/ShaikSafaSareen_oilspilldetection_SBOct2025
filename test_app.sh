#!/bin/bash
cd /home/surendra208/Downloads/oil_spill

echo "🔍 Checking conda environment..."
if conda env list 2>/dev/null | grep -q "oil_spill"; then
    echo "✅ Environment exists"
    echo "📝 To activate: conda activate oil_spill"
else
    echo "📦 Environment not found. Creating..."
    echo "📝 Run: conda env create -f environment.yml"
fi

echo ""
echo "🔍 Checking model file..."
if [ -f "best.pt" ]; then
    echo "✅ Model file found: $(ls -lh best.pt | awk '{print $5}')"
else
    echo "❌ Model file (best.pt) not found!"
fi

echo ""
echo "🔍 Checking demo images..."
if [ -d "demo_images" ]; then
    echo "✅ Demo images found: $(ls demo_images/*.jpg 2>/dev/null | wc -l) images"
else
    echo "❌ Demo images folder not found!"
fi

echo ""
echo "🚀 To run the app:"
echo "   1. conda activate oil_spill"
echo "   2. streamlit run app.py"
