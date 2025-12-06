"""
Video Detection Page - Upload and detect oil spills in videos
"""
import streamlit as st
from utils.model_loader import load_model
from utils.video_processor import process_video, extract_frames_from_video
from utils.visualizations import create_detection_timeline_plot
from utils.report_generator import generate_text_report, generate_json_report
from utils.video_pdf_report import generate_video_pdf_report
from utils.activity_logger import ActivityLogger
import tempfile
import os
import cv2
import numpy as np

st.set_page_config(page_title="Video Detection", page_icon="🎥", layout="wide")

st.title("🎥 Video Detection")
st.markdown("Upload videos to detect oil spills frame by frame using our advanced YOLOv11 model")

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
    show_preview = st.checkbox("Show Frame Preview", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Model Info")
    st.info(f"Device: {st.session_state.device}")

# Main content
uploaded_file = st.file_uploader(
    "Upload Video",
    type=['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']
)

if uploaded_file:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_video_path = tmp_file.name
    
    try:
        # Video info
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📹 Original Video")
            st.video(uploaded_file)
        with col2:
            st.subheader("📹 Video Information")
            st.info(f"Filename: {uploaded_file.name}")
            st.info(f"Size: {uploaded_file.size / (1024*1024):.2f} MB")
        
        # Process video
        st.markdown("---")
        st.subheader("🔍 Processing Video")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(progress):
            progress_bar.progress(progress)
            status_text.text(f"Processing: {progress:.1%} complete")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as output_file:
            output_path = output_file.name
        
        try:
            with st.spinner("Processing video frames..."):
                annotated_video_path, stats = process_video(
                    st.session_state.model,
                    tmp_video_path,
                    conf_threshold=conf_threshold,
                    output_path=output_path,
                    progress_callback=update_progress,
                    store_frames=True  # Store frames for comparison
                )
            
            progress_bar.progress(1.0)
            status_text.text("✅ Processing complete!")
            
            # Store in session state for later use
            st.session_state.processed_video_path = annotated_video_path
            st.session_state.video_stats = stats
            
            # Ensure stats has frame data
            if not stats.get("frame_details"):
                st.warning("⚠️ Frame details not available in stats. This might affect frame display.")
            
            # Display side-by-side video comparison
            st.markdown("---")
            st.subheader("🎬 Video Comparison: Original vs Detected")
            
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.markdown("### 📹 Original Video")
                st.video(uploaded_file)
            
            with comp_col2:
                st.markdown("### 🔍 Detected Video (with Annotations)")
                # Display annotated video
                try:
                    # Read video file and display
                    with open(annotated_video_path, 'rb') as video_file:
                        video_bytes = video_file.read()
                        # Try to display video
                        st.video(video_bytes)
                except Exception as e:
                    st.warning(f"⚠️ Video preview unavailable: {str(e)}")
                    st.info("💡 You can download the annotated video using the download button below to view it.")
                    # Show file info as fallback
                    file_size = os.path.getsize(annotated_video_path) / (1024*1024)
                    st.info(f"📁 Annotated video file size: {file_size:.2f} MB")
            
            # Display detected frames at the bottom
            st.markdown("---")
            st.subheader("🖼️ Detected Frames (Frames with Oil Spill Detections)")
            
            if stats.get("frame_details") and stats.get("annotated_frames"):
                # Get frames with detections
                frames_with_detections = [
                    (idx, detail) for idx, detail in enumerate(stats["frame_details"])
                    if detail["has_detection"]
                ]
                
                if frames_with_detections:
                    # Show up to 12 detected frames
                    num_frames_to_show = min(12, len(frames_with_detections))
                    selected_frames = frames_with_detections[:num_frames_to_show]
                    
                    # Display in grid (3 columns)
                    num_cols = 3
                    for i in range(0, len(selected_frames), num_cols):
                        cols = st.columns(num_cols)
                        for j, col in enumerate(cols):
                            if i + j < len(selected_frames):
                                frame_idx, frame_detail = selected_frames[i + j]
                                with col:
                                    annotated_frame = stats["annotated_frames"][frame_idx]
                                    st.image(annotated_frame, width='stretch', 
                                           caption=f"Frame {frame_detail['frame_number'] + 1} - "
                                                  f"{frame_detail['detections_count']} detection(s), "
                                                  f"Confidence: {frame_detail['avg_confidence']:.2%}" 
                                                  if frame_detail['avg_confidence'] > 0 
                                                  else f"Frame {frame_detail['frame_number'] + 1} - "
                                                       f"{frame_detail['detections_count']} detection(s)")
                else:
                    st.info("✅ No frames with detections found in this video.")
            else:
                st.info("Frame data not available. Please reprocess the video.")
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Detection Statistics")
            
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            with metric_col1:
                st.metric("Total Frames", stats.get("total_frames", 0))
            with metric_col2:
                st.metric("Frames with Detections", stats.get("frames_with_detections", 0))
            with metric_col3:
                st.metric("Total Detections", stats.get("total_detections", 0))
            with metric_col4:
                st.metric("Avg Detections/Frame", f"{stats.get('avg_detections_per_frame', 0):.2f}")
            
            # Detection timeline
            if stats.get("detection_history"):
                st.subheader("📈 Detection Timeline")
                fig = create_detection_timeline_plot(stats["detection_history"])
                st.plotly_chart(fig, width='stretch')
            
            # Download section
            st.markdown("---")
            st.subheader("📥 Download Results")
            
            # Video downloads
            download_col1, download_col2 = st.columns(2)
            
            with download_col1:
                st.markdown("#### 📹 Videos")
                with open(annotated_video_path, 'rb') as video_file:
                    st.download_button(
                        "📥 Download Annotated Video",
                        video_file.read(),
                        file_name=f"annotated_{uploaded_file.name}",
                        mime="video/mp4",
                        key="download_video"
                    )
            
            with download_col2:
                st.markdown("#### 📄 Reports")
                # Text report
                report = generate_text_report([], stats, {
                    "Filename": uploaded_file.name,
                    "Total Frames": stats.get("total_frames", 0),
                    "Size": f"{uploaded_file.size / (1024*1024):.2f} MB"
                })
                st.download_button(
                    "📄 Download Text Report",
                    report,
                    file_name=f"video_report_{uploaded_file.name}.txt",
                    mime="text/plain",
                    key="download_txt"
                )
            
            # PDF Report with frame-by-frame analysis
            st.markdown("#### 📊 Comprehensive PDF Report")
            st.info("📋 The PDF report includes frame-by-frame comparison between original and detected frames, "
                   "with detailed analysis of each frame showing detections, confidence scores, and visual comparisons.")
            
            if stats.get("frame_details") and stats.get("original_frames") and stats.get("annotated_frames"):
                with st.spinner("Generating comprehensive PDF report..."):
                    pdf_report = generate_video_pdf_report(
                        stats,
                        {
                            "Filename": uploaded_file.name,
                            "Total Frames": stats.get("total_frames", 0),
                            "Size": f"{uploaded_file.size / (1024*1024):.2f} MB",
                            "Frames with Detections": stats.get("frames_with_detections", 0),
                            "Total Detections": stats.get("total_detections", 0)
                        },
                        stats.get("original_frames"),
                        stats.get("annotated_frames"),
                        max_frames_to_show=20
                    )
                    
                    st.download_button(
                        "📑 Download PDF Report (Frame-by-Frame Analysis)",
                        pdf_report,
                        file_name=f"video_analysis_{uploaded_file.name}.pdf",
                        mime="application/pdf",
                        key="download_pdf"
                    )
            else:
                st.warning("Frame data not available for PDF generation. Please reprocess the video.")
            
            # JSON report
            st.markdown("---")
            json_report = generate_json_report([], stats)
            st.download_button(
                "📊 Download JSON Report",
                json_report,
                file_name=f"video_report_{uploaded_file.name}.json",
                mime="application/json",
                key="download_json"
            )
            
            # Log activity after displaying results (to avoid interrupting display)
            # Use file path instead of bytes to avoid memory issues with large videos
            try:
                # Create a copy of stats without frame data for logging (to avoid memory issues)
                stats_for_logging = {k: v for k, v in stats.items() 
                                    if k not in ['original_frames', 'annotated_frames']}
                # Use file path instead of reading entire file into memory
                st.session_state.activity_logger.log_video_detection(
                    input_file=tmp_video_path,  # Use file path instead of bytes
                    output_video_path=annotated_video_path,
                    stats=stats_for_logging,
                    filename=uploaded_file.name
                )
            except Exception as e:
                # Don't show error to user, just log silently
                pass
        
        finally:
            # Cleanup
            if os.path.exists(output_path):
                pass  # Keep for download, will be cleaned up later
    
    finally:
        # Cleanup uploaded file
        if os.path.exists(tmp_video_path):
            os.unlink(tmp_video_path)

else:
    st.info("👆 Please upload a video file to get started with oil spill detection.")
    
    st.markdown("---")
    st.subheader("ℹ️ How to Use")
    st.markdown("""
    1. **Upload Video**: Click the upload area above and select a video file
    2. **Preview**: View sample frames from your video
    3. **Process**: The video will be processed frame by frame
    4. **Analyze**: Review detection statistics and timeline
    5. **Download**: Get the annotated video and analysis reports
    """)

