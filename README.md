# 🌊 Oil Spill Detection System

An innovative, comprehensive web application for detecting oil spills in images and videos using advanced YOLOv11 deep learning model. Built with Streamlit for an intuitive, user-friendly interface.

## ✨ Features

### 🎯 Core Capabilities
- **📸 Image Detection**: Upload single or multiple images for batch processing
- **🎥 Video Detection**: Process video files frame-by-frame with progress tracking
- **📹 Real-time Camera**: Live detection from webcam with real-time statistics
- **📊 Analytics Dashboard**: Comprehensive statistics, visualizations, and insights
- **⚙️ Customizable Settings**: Adjust confidence thresholds and preferences

### 🚀 Advanced Features
- **Batch Processing**: Handle multiple images simultaneously
- **Interactive Visualizations**: Plotly charts for confidence distributions and timelines
- **Export Options**: Download results in multiple formats (TXT, CSV, JSON)
- **Heatmap Overlays**: Visualize detection density
- **Coverage Analysis**: Calculate spill coverage percentages
- **Detection History**: Track and analyze detection patterns over time
- **Real-time Statistics**: Live metrics during processing
- **GPU Support**: Automatic GPU acceleration when available

## 📋 Requirements

- Python 3.10 or higher
- CUDA-capable GPU (optional, for faster processing)
- Webcam (optional, for real-time detection)

## 🛠️ Installation

### Option 1: Using Conda (Recommended)

1. **Create the conda environment:**
   ```bash
   conda env create -f environment.yml
   ```

2. **Activate the environment:**
   ```bash
   conda activate oil_spill
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Option 2: Using pip

1. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv oil_spill_env
   source oil_spill_env/bin/activate  # On Windows: oil_spill_env\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
oil_spill/
├── app.py                      # Main Streamlit application
├── best.pt                     # YOLOv11 trained model
├── pages/                      # Multi-page application pages
│   ├── 1_📸_Image_Detection.py
│   ├── 2_🎥_Video_Detection.py
│   ├── 3_📹_Real-time_Camera.py
│   ├── 4_📊_Analytics_Dashboard.py
│   └── 5_⚙️_Settings.py
├── utils/                      # Utility modules
│   ├── model_loader.py         # Model loading and caching
│   ├── image_processor.py      # Image processing functions
│   ├── video_processor.py      # Video processing functions
│   ├── visualizations.py       # Visualization utilities
│   └── report_generator.py     # Report generation
├── requirements.txt            # Python dependencies
├── environment.yml             # Conda environment file
└── README.md                   # This file
```

## 🎮 Usage

### Image Detection
1. Navigate to **📸 Image Detection** page
2. Upload one or more images (PNG, JPG, JPEG, BMP, TIFF)
3. Adjust confidence threshold in the sidebar
4. View detection results with bounding boxes
5. Export results in various formats

### Video Detection
1. Navigate to **🎥 Video Detection** page
2. Upload a video file (MP4, AVI, MOV, MKV, etc.)
3. Preview sample frames
4. Process the video (progress bar shows status)
5. Download annotated video and analysis reports

### Real-time Camera
1. Navigate to **📹 Real-time Camera** page
2. Click "Start Camera" button
3. View live detections with real-time statistics
4. Click "Stop Camera" when finished

### Analytics Dashboard
1. Navigate to **📊 Analytics Dashboard** page
2. View comprehensive statistics and visualizations
3. Analyze detection patterns over time
4. Export analytics data

## ⚙️ Configuration

### Model Settings
- **Confidence Threshold**: Adjust detection sensitivity (0.0 - 1.0)
- **Device**: Automatically uses GPU if available, falls back to CPU

### Application Settings
- Customize display preferences
- Configure export formats
- Adjust processing parameters

## 📊 Supported Formats

### Input
- **Images**: PNG, JPG, JPEG, BMP, TIFF
- **Videos**: MP4, AVI, MOV, MKV, FLV, WMV

### Output
- **Annotated Images/Videos**: With bounding boxes and labels
- **Text Reports**: Detailed detection information
- **CSV Files**: Structured data for analysis
- **JSON Files**: Machine-readable results

## 🔧 Technical Details

- **Model**: YOLOv11 (Ultralytics)
- **Framework**: PyTorch
- **Web Framework**: Streamlit
- **Visualization**: Plotly, Matplotlib
- **Image Processing**: OpenCV, PIL
- **Data Handling**: Pandas, NumPy

## 🎨 UI Features

- **Modern Design**: Clean, intuitive interface
- **Responsive Layout**: Works on different screen sizes
- **Custom Styling**: Enhanced visual appearance
- **Progress Indicators**: Real-time processing feedback
- **Interactive Charts**: Plotly visualizations
- **Color-coded Alerts**: Visual feedback for detections

## 🚀 Performance Tips

1. **Use GPU**: Ensure CUDA is available for faster processing
2. **Batch Processing**: Process multiple images together for efficiency
3. **Adjust Thresholds**: Lower confidence threshold for more detections (may include false positives)
4. **Video Resolution**: Lower resolution videos process faster

## 📝 Notes

- The model file (`best.pt`) must be in the project root directory
- First run may take longer as the model loads
- GPU acceleration significantly improves processing speed
- Large videos may take time to process - be patient!

## 🐛 Troubleshooting

### Model not loading
- Ensure `best.pt` exists in the project directory
- Check file permissions

### Camera not working
- Verify camera permissions
- Check if camera is being used by another application

### Slow processing
- Use GPU if available
- Reduce image/video resolution
- Process fewer images at once

### Import errors
- Ensure all dependencies are installed
- Activate the correct conda/virtual environment

## 📄 License

This project is provided as-is for demonstration and research purposes.

## 🙏 Acknowledgments

- YOLOv11 by Ultralytics
- Streamlit for the web framework
- All open-source contributors

## 📧 Support

For issues, questions, or contributions, please refer to the project documentation or create an issue in the repository.

---

**Built with ❤️ for environmental protection and oil spill detection**

