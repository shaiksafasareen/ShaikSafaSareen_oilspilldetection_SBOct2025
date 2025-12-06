"""
Main Streamlit Application for Oil Spill Detection
"""
import streamlit as st
from utils.model_loader import load_model

# Page configuration
st.set_page_config(
    page_title="Oil Spill Detection System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    h1 {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
        animation: fadeIn 1s;
    }
    
    h2 {
        color: #2c3e50;
        margin-top: 2rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 3rem;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Success message */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        padding: 1rem;
        animation: fadeIn 0.5s;
    }
    
    /* Info message */
    .stInfo {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 5px;
        padding: 1rem;
        animation: fadeIn 0.5s;
    }
    
    /* Warning message */
    .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 5px;
        padding: 1rem;
        animation: fadeIn 0.5s;
    }
    
    /* Error message */
    .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 5px;
        padding: 1rem;
        animation: fadeIn 0.5s;
    }
    
    /* Custom container */
    .feature-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%);
    }
    
    /* File uploader */
    .uploadedFile {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Sidebar enhancements */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Metric enhancements */
    [data-testid="metric-container"] {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Main title and description
st.title("🌊 Oil Spill Detection System")
st.markdown("""
<div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%); 
            border-radius: 10px; color: white; margin-bottom: 2rem;'>
    <h2 style='color: white; margin: 0;'>Advanced AI-Powered Oil Spill Detection</h2>
    <p style='margin: 0.5rem 0 0 0;'>Using YOLOv11 Deep Learning Model</p>
</div>
""", unsafe_allow_html=True)

# Initialize model in session state
if 'model' not in st.session_state:
    with st.spinner("🔄 Loading AI model..."):
        model, device = load_model("best.pt")
        if model:
            st.session_state.model = model
            st.session_state.device = device
        else:
            st.error("❌ Failed to load model. Please ensure 'best.pt' exists in the project directory.")
            st.stop()

# Sidebar navigation and info
with st.sidebar:
    st.image("https://via.placeholder.com/200x100/1f77b4/ffffff?text=Oil+Spill+AI", width='stretch')
    
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    st.markdown("""
    Use the pages in the sidebar to:
    - **📸 Image Detection**: Upload and analyze images
    - **🎥 Video Detection**: Process video files
    - **📹 Real-time Camera**: Live detection from webcam
    - **🔄 Comparison Mode**: Compare before/after or multiple images
    - **📊 Analytics**: View comprehensive statistics
    - **📋 Activity Log**: View all activities and records
    - **⚙️ Settings**: Configure application
    """)
    
    st.markdown("---")
    st.markdown("### 📊 System Status")
    if 'model' in st.session_state:
        st.success(f"✅ Model Loaded")
        st.info(f"🖥️ Device: {st.session_state.device.upper()}")
        st.info(f"🤖 Model: YOLOv11")
    else:
        st.error("❌ Model Not Loaded")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.info("""
    - Adjust confidence threshold for better results
    - Use batch processing for multiple images
    - Export results in various formats
    - Check analytics for insights
    """)

# Main content area
st.markdown("## 🚀 Welcome to Oil Spill Detection System")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='feature-box'>
        <h3>📸 Image Detection</h3>
        <p>Upload single or multiple images to detect oil spills with bounding boxes and confidence scores.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-box'>
        <h3>🎥 Video Processing</h3>
        <p>Process video files frame-by-frame with comprehensive analysis and annotated output.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-box'>
        <h3>📹 Real-time Detection</h3>
        <p>Live detection from webcam with real-time statistics and alerts.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class='feature-box'>
        <h3>🔄 Comparison Mode</h3>
        <p>Compare before/after images or analyze multiple images side-by-side.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class='feature-box'>
        <h3>🚨 Alert System</h3>
        <p>Intelligent alerts based on detection severity and coverage.</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class='feature-box'>
        <h3>📄 PDF Reports</h3>
        <p>Generate professional PDF reports with detailed analysis.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Key features
st.markdown("## ✨ Key Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    - ✅ **Advanced AI Model**: YOLOv11 deep learning architecture
    - ✅ **Multi-format Support**: Images (PNG, JPG, etc.) and Videos (MP4, AVI, etc.)
    - ✅ **Real-time Processing**: Live webcam detection
    - ✅ **Batch Processing**: Handle multiple images simultaneously
    - ✅ **Confidence Scoring**: Detailed confidence metrics for each detection
    """)

with feature_col2:
    st.markdown("""
    - ✅ **Analytics Dashboard**: Comprehensive statistics and visualizations
    - ✅ **Export Options**: Download results in TXT, CSV, JSON, PDF formats
    - ✅ **Interactive Visualizations**: Plotly charts and graphs
    - ✅ **Comparison Mode**: Before/after and multi-image analysis
    - ✅ **Alert System**: Intelligent severity-based notifications
    - ✅ **PDF Reports**: Professional report generation
    - ✅ **User-friendly Interface**: Clean and intuitive design
    """)

st.markdown("---")

# Getting started
st.markdown("## 🎯 Getting Started")

st.markdown("""
1. **Navigate to a Detection Page**: Use the sidebar to select Image Detection, Video Detection, or Real-time Camera
2. **Upload Your Media**: Select images or videos from your device
3. **Adjust Settings**: Use the sidebar to fine-tune confidence thresholds
4. **View Results**: See detections with bounding boxes and statistics
5. **Export Data**: Download annotated media and analysis reports
6. **Analyze**: Check the Analytics Dashboard for insights
""")

st.markdown("---")

# Technical information
with st.expander("🔧 Technical Information"):
    st.markdown("""
    **Model Architecture**: YOLOv11 (You Only Look Once version 11)
    
    **Framework**: Ultralytics YOLO
    
    **Inference Engine**: PyTorch
    
    **Supported Devices**: CPU and GPU (CUDA)
    
    **Input Formats**: 
    - Images: PNG, JPG, JPEG, BMP, TIFF
    - Videos: MP4, AVI, MOV, MKV, FLV, WMV
    
    **Output Formats**: 
    - Annotated images/videos
    - Text reports (TXT)
    - Data exports (CSV, JSON)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; color: #6c757d;'>
    <p>🌊 Oil Spill Detection System | Powered by YOLOv11 AI</p>
    <p>Version 1.0.0 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

