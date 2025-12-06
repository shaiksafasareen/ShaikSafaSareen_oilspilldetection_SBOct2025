"""
Real-time Camera Detection Page - Live oil spill detection from webcam
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils.model_loader import load_model
from utils.image_processor import process_image
from utils.activity_logger import ActivityLogger
import time

st.set_page_config(page_title="Real-time Camera", page_icon="📹", layout="wide")

st.title("📹 Real-time Camera Detection")
st.markdown("Detect oil spills in real-time using your webcam")

# Initialize session state
if 'model' not in st.session_state:
    with st.spinner("Loading model..."):
        model, device = load_model("best.pt")
        if model:
            st.session_state.model = model
            st.session_state.device = device
            st.success(f"Model loaded successfully on {device}!")
        else:
            st.error("Failed to load model. Please check if best.pt exists.")
            st.stop()

# Initialize activity logger
if 'activity_logger' not in st.session_state:
    st.session_state.activity_logger = ActivityLogger()

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)
    
    st.markdown("---")
    st.markdown("### 📊 Model Info")
    st.info(f"Device: {st.session_state.device}")
    
    st.markdown("---")
    st.markdown("### ⚠️ Note")
    st.warning("Make sure your camera is connected and accessible.")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Camera Feed")
    camera_placeholder = st.empty()
    
    start_button = st.button("▶️ Start Camera", type="primary")
    stop_button = st.button("⏹️ Stop Camera")

with col2:
    st.subheader("📊 Live Statistics")
    stats_placeholder = st.empty()
    
    detection_count_placeholder = st.empty()
    confidence_placeholder = st.empty()

# Camera control
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False

if start_button:
    st.session_state.camera_active = True

if stop_button:
    st.session_state.camera_active = False

# Camera processing
if st.session_state.camera_active:
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("❌ Could not open camera. Please check your camera connection.")
        st.session_state.camera_active = False
    else:
        frame_count = 0
        detection_history = []
        
        try:
            while st.session_state.camera_active:
                ret, frame = cap.read()
                
                if not ret:
                    st.warning("Failed to read frame from camera")
                    break
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                
                # Process frame
                annotated_img, detections, stats = process_image(
                    st.session_state.model,
                    frame_pil,
                    conf_threshold
                )
                
                # Update display
                camera_placeholder.image(annotated_img, width='stretch', channels="RGB")
                
                # Update statistics
                with stats_placeholder.container():
                    metric_col1, metric_col2 = st.columns(2)
                    with metric_col1:
                        st.metric("Detections", stats.get("total_detections", 0))
                    with metric_col2:
                        avg_conf = stats.get("avg_confidence", 0)
                        st.metric("Avg Confidence", f"{avg_conf:.2%}" if avg_conf > 0 else "N/A")
                
                # Detection alert
                if stats.get("total_detections", 0) > 0:
                    detection_count_placeholder.success(f"⚠️ {stats.get('total_detections', 0)} oil spill(s) detected!")
                else:
                    detection_count_placeholder.info("✅ No oil spills detected")
                
                frame_count += 1
                detection_history.append(stats.get("total_detections", 0))
                
                # Log detection if found (log every 10 frames or when detection found)
                if stats.get("total_detections", 0) > 0 and frame_count % 10 == 0:
                    st.session_state.activity_logger.log_camera_detection(
                        detections=[],
                        stats=stats,
                        frame_count=frame_count
                    )
                
                # Control frame rate
                time.sleep(0.1)  # ~10 FPS
        
        finally:
            cap.release()
            st.session_state.camera_active = False
            st.info("Camera stopped.")

else:
    camera_placeholder.info("👆 Click 'Start Camera' to begin real-time detection")
    stats_placeholder.info("Statistics will appear here when camera is active")

st.markdown("---")
st.subheader("ℹ️ How to Use")
st.markdown("""
1. **Start Camera**: Click the "Start Camera" button to begin live detection
2. **Adjust Settings**: Use the sidebar to adjust confidence threshold
3. **Monitor**: Watch real-time detections and statistics
4. **Stop**: Click "Stop Camera" when finished
5. **Note**: Make sure your camera permissions are enabled
""")

