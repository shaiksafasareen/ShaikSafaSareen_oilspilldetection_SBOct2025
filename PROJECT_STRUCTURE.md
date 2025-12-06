# 📁 Project Structure

This document describes the complete structure of the Oil Spill Detection System.

## 🗂️ Directory Tree

```
oil_spill/
├── app.py                          # Main Streamlit application entry point
├── best.pt                         # YOLOv11 trained model (your model file)
├── pages/                          # Multi-page application pages
│   ├── 1_📸_Image_Detection.py    # Image upload and detection page
│   ├── 2_🎥_Video_Detection.py    # Video processing page
│   ├── 3_📹_Real-time_Camera.py   # Real-time webcam detection page
│   ├── 4_📊_Analytics_Dashboard.py # Analytics and statistics dashboard
│   └── 5_⚙️_Settings.py           # Application settings page
├── utils/                          # Utility modules
│   ├── __init__.py                # Package initialization
│   ├── model_loader.py            # Model loading and caching
│   ├── image_processor.py         # Image processing functions
│   ├── video_processor.py         # Video processing functions
│   ├── visualizations.py          # Visualization utilities
│   └── report_generator.py        # Report generation functions
├── assets/                         # Static assets (images, icons, etc.)
├── environment.yml                 # Conda environment configuration
├── requirements.txt                # Python package dependencies
├── setup.sh                       # Setup script for conda environment
├── README.md                      # Comprehensive documentation
├── QUICKSTART.md                  # Quick start guide
├── PROJECT_STRUCTURE.md           # This file
└── .gitignore                     # Git ignore file

```

## 📄 File Descriptions

### Main Application
- **app.py**: Main entry point with navigation, custom styling, and welcome page

### Pages
- **1_📸_Image_Detection.py**: 
  - Single and batch image processing
  - Interactive visualization
  - Export options (TXT, CSV, JSON)
  - Confidence distribution charts
  
- **2_🎥_Video_Detection.py**:
  - Video upload and processing
  - Frame-by-frame analysis
  - Progress tracking
  - Annotated video download
  
- **3_📹_Real-time_Camera.py**:
  - Live webcam detection
  - Real-time statistics
  - Detection alerts
  
- **4_📊_Analytics_Dashboard.py**:
  - Comprehensive statistics
  - Timeline visualizations
  - Detection patterns
  - Data export
  
- **5_⚙️_Settings.py**:
  - Model configuration
  - Application preferences
  - Export settings

### Utilities
- **model_loader.py**: Handles YOLOv11 model loading with caching
- **image_processor.py**: Image processing, detection, and statistics
- **video_processor.py**: Video frame processing and analysis
- **visualizations.py**: Plotly charts and visualizations
- **report_generator.py**: Text, CSV, and JSON report generation

### Configuration
- **environment.yml**: Conda environment with all dependencies
- **requirements.txt**: pip requirements for virtual environments
- **setup.sh**: Automated setup script

### Documentation
- **README.md**: Complete project documentation
- **QUICKSTART.md**: Quick start guide for new users
- **PROJECT_STRUCTURE.md**: This file

## 🔄 Data Flow

1. **User Input** → Upload image/video or start camera
2. **Model Loading** → YOLOv11 model loaded (cached)
3. **Processing** → Image/video processed through model
4. **Detection** → Bounding boxes and confidence scores extracted
5. **Visualization** → Results displayed with annotations
6. **Statistics** → Metrics calculated and displayed
7. **Export** → Results available for download

## 🎨 UI Components

- **Custom CSS**: Enhanced styling in app.py
- **Streamlit Components**: Native Streamlit widgets
- **Plotly Charts**: Interactive visualizations
- **Multi-column Layouts**: Responsive design
- **Progress Indicators**: Real-time feedback

## 🚀 Key Features by Module

### Image Processing
- Batch processing
- Coverage analysis
- Confidence scoring
- Heatmap overlays

### Video Processing
- Frame extraction
- Progress tracking
- Timeline analysis
- Annotated output

### Real-time Detection
- Live webcam feed
- Real-time statistics
- Detection alerts
- Performance optimization

### Analytics
- Historical tracking
- Pattern analysis
- Statistical summaries
- Data export

## 📊 Model Integration

The YOLOv11 model (`best.pt`) is:
- Loaded once at startup (cached)
- Used across all pages
- Supports GPU acceleration
- Handles batch processing

## 🔧 Extensibility

The modular structure allows easy:
- Adding new detection pages
- Extending utility functions
- Customizing visualizations
- Adding export formats
- Integrating new models

---

**This structure provides a clean, maintainable, and scalable foundation for the Oil Spill Detection System.**

