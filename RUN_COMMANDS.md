# 🚀 How to Run and Test the Application

## Step-by-Step Commands

### Step 1: Navigate to Project Directory
```bash
cd /home/surendra208/Downloads/oil_spill
```

### Step 2: Check if Conda Environment Exists
```bash
conda env list | grep oil_spill
```

**If environment doesn't exist**, proceed to Step 3.  
**If environment exists**, skip to Step 4.

### Step 3: Create Conda Environment

**Option A: Using environment.yml (Recommended)**
```bash
conda env create -f environment.yml
```

**Option B: Using setup script**
```bash
chmod +x setup.sh
./setup.sh
```

**Option C: Using pip (if conda has issues)**
```bash
python -m venv oil_spill_env
source oil_spill_env/bin/activate
pip install -r requirements.txt
```

### Step 4: Activate Environment

**If using conda:**
```bash
conda activate oil_spill
```

**If using venv:**
```bash
source oil_spill_env/bin/activate
```

### Step 5: Verify Installation
```bash
python -c "import streamlit; import ultralytics; print('✅ All packages installed!')"
```

### Step 6: Run the Application
```bash
streamlit run app.py
```

The app will:
- Start the Streamlit server
- Automatically open in your browser at `http://localhost:8501`
- If it doesn't open automatically, manually visit: `http://localhost:8501`

### Step 7: Test the Application

#### Test 1: Image Detection
1. Click on **"📸 Image Detection"** in the sidebar
2. Click "Upload Images"
3. Navigate to `demo_images/` folder
4. Upload `oil_spill_medium.jpg`
5. Wait for processing
6. Check detection results, statistics, and charts

#### Test 2: Comparison Mode
1. Click on **"🔄 Comparison Mode"** in the sidebar
2. Select "Before/After" mode
3. Upload `clean_water_1.jpg` as "Before"
4. Upload `oil_spill_medium.jpg` as "After"
5. View comparison metrics and charts

#### Test 3: Multiple Images
1. Go to **"📸 Image Detection"**
2. Upload multiple images at once:
   - `clean_water_1.jpg`
   - `oil_spill_small.jpg`
   - `oil_spill_large.jpg`
3. View batch processing results

#### Test 4: Export Features
1. Process an image with detections
2. Scroll down to "Export Results"
3. Test downloading:
   - Text Report (.txt)
   - CSV Report (.csv)
   - JSON Report (.json)
   - PDF Report (.pdf)
   - Annotated Image (.png)

#### Test 5: Analytics Dashboard
1. Click on **"📊 Analytics Dashboard"**
2. Enable "Show Demo Data" checkbox
3. View statistics, charts, and visualizations
4. Test export options

## Quick Test Script

Save this as `test_app.sh`:

```bash
#!/bin/bash
cd /home/surendra208/Downloads/oil_spill

echo "🔍 Checking conda environment..."
if conda env list | grep -q "oil_spill"; then
    echo "✅ Environment exists"
    conda activate oil_spill
else
    echo "📦 Creating environment..."
    conda env create -f environment.yml
    conda activate oil_spill
fi

echo "🔍 Verifying installation..."
python -c "import streamlit; import ultralytics; print('✅ Packages OK')" || {
    echo "❌ Missing packages, installing..."
    pip install -r requirements.txt
}

echo "🚀 Starting application..."
streamlit run app.py
```

Make it executable and run:
```bash
chmod +x test_app.sh
./test_app.sh
```

## Troubleshooting

### Issue: "conda: command not found"
**Solution**: Install Anaconda/Miniconda first, or use pip method:
```bash
python -m venv oil_spill_env
source oil_spill_env/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Issue: "Model not found"
**Solution**: Ensure `best.pt` is in the project root:
```bash
ls -lh best.pt
```

### Issue: "Module not found"
**Solution**: Install missing packages:
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
**Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Browser doesn't open automatically
**Solution**: Manually visit:
- `http://localhost:8501`
- Or `http://127.0.0.1:8501`

## Expected Output

When you run `streamlit run app.py`, you should see:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

## Testing Checklist

- [ ] Application starts without errors
- [ ] Model loads successfully (check sidebar)
- [ ] Can upload images
- [ ] Detections appear with bounding boxes
- [ ] Statistics display correctly
- [ ] Charts render properly
- [ ] Export buttons work
- [ ] Comparison mode functions
- [ ] Analytics dashboard shows data
- [ ] All pages load correctly

## Demo Images Location

All demo images are in:
```
/home/surendra208/Downloads/oil_spill/demo_images/
```

Available test images:
- `clean_water_1.jpg` - No spills
- `clean_water_2.jpg` - No spills
- `oil_spill_small.jpg` - 1 spill
- `oil_spill_medium.jpg` - 3 spills (good for demo)
- `oil_spill_large.jpg` - 5 spills
- `oil_spill_multiple.jpg` - 8 spills

## Quick Commands Summary

```bash
# Navigate
cd /home/surendra208/Downloads/oil_spill

# Create environment (if needed)
conda env create -f environment.yml

# Activate
conda activate oil_spill

# Run app
streamlit run app.py

# Or if using pip
python -m venv oil_spill_env
source oil_spill_env/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

**That's it! Your app should be running now! 🎉**

