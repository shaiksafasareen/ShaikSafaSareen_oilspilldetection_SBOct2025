# 🚀 Quick Start Guide

Get up and running with the Oil Spill Detection System in minutes!

## ⚡ Fast Setup (5 minutes)

### Step 1: Create Conda Environment
```bash
conda env create -f environment.yml
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Activate Environment
```bash
conda activate oil_spill
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎯 First Steps

1. **Verify Model**: Check that `best.pt` is in the project directory
2. **Test Image Detection**: 
   - Go to "📸 Image Detection" page
   - Upload a test image
   - Adjust confidence threshold if needed
3. **Explore Features**: Try video detection and real-time camera
4. **Check Analytics**: Visit the Analytics Dashboard

## 📸 Testing with Sample Images

You can test the system with any image containing water/ocean scenes. The model will detect oil spills if present.

## 🎥 Testing Video Detection

Upload a video file (MP4 recommended) and watch the progress bar as it processes frame by frame.

## 📹 Testing Real-time Camera

1. Ensure your webcam is connected
2. Go to "📹 Real-time Camera" page
3. Click "Start Camera"
4. Point camera at test images or scenes

## ⚙️ Recommended Settings

- **Confidence Threshold**: Start with 0.25, adjust based on results
- **Batch Processing**: Use for multiple images
- **GPU**: Enable if available for faster processing

## 🐛 Common Issues

**Model not loading?**
- Check if `best.pt` exists in the root directory
- Verify file permissions

**Camera not working?**
- Check camera permissions
- Ensure no other app is using the camera

**Slow processing?**
- Use GPU if available
- Reduce image/video resolution
- Process fewer images at once

## 💡 Pro Tips

1. **Batch Processing**: Upload multiple images at once for efficiency
2. **Export Results**: Download reports for documentation
3. **Analytics**: Use the dashboard to track detection patterns
4. **Settings**: Customize thresholds for your specific use case

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all features in the application
- Customize settings for your needs
- Export and analyze results

---

**Happy Detecting! 🌊**

