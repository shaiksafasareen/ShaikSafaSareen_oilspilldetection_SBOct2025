"""
Image Detection Page - Upload and detect oil spills in images
"""
import streamlit as st
from PIL import Image
import numpy as np
from utils.model_loader import load_model
from utils.image_processor import process_image, process_batch_images, calculate_spill_coverage, create_detection_dataframe
from utils.visualizations import create_confidence_distribution_plot, create_statistics_cards
from utils.report_generator import generate_text_report, generate_csv_report, generate_json_report
from utils.alert_system import AlertSystem
from utils.pdf_report import generate_pdf_report
from utils.activity_logger import ActivityLogger
import io

st.set_page_config(page_title="Image Detection", page_icon="📸", layout="wide")

st.title("📸 Image Detection")
st.markdown("Upload images to detect oil spills using our advanced YOLOv11 model")

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

# Initialize alert system
if 'alert_system' not in st.session_state:
    st.session_state.alert_system = AlertSystem()

# Initialize activity logger
if 'activity_logger' not in st.session_state:
    st.session_state.activity_logger = ActivityLogger()

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)
    show_heatmap = st.checkbox("Show Heatmap Overlay", value=False)
    show_stats = st.checkbox("Show Statistics", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Model Info")
    st.info(f"Device: {st.session_state.device}")
    st.info(f"Classes: {len(st.session_state.model.names)}")

# Main content
uploaded_files = st.file_uploader(
    "Upload Images",
    type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
    accept_multiple_files=True
)

if uploaded_files:
    # Process images
    tabs = st.tabs([f"Image {i+1}" for i in range(len(uploaded_files))])
    
    all_detections = []
    all_stats = []
    
    for idx, uploaded_file in enumerate(uploaded_files):
        with tabs[idx]:
            col1, col2 = st.columns(2)
            
            # Load image
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            
            with col1:
                st.subheader("Original Image")
                st.image(image, width='stretch')
                st.caption(f"Size: {image.size[0]} x {image.size[1]} pixels")
            
            # Process image
            with st.spinner("Processing image..."):
                annotated_img, detections, stats = process_image(
                    st.session_state.model, 
                    image, 
                    conf_threshold
                )
                
                # Calculate coverage
                coverage_stats = calculate_spill_coverage(detections, image.size)
                stats.update(coverage_stats)
                
                # Check for alerts
                alert = st.session_state.alert_system.check_detection(stats)
                
                # Log activity
                annotated_pil = Image.fromarray(annotated_img)
                img_buffer = io.BytesIO()
                annotated_pil.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                st.session_state.activity_logger.log_image_detection(
                    input_file=uploaded_file.getvalue(),
                    output_image=img_buffer.getvalue(),
                    detections=detections,
                    stats=stats,
                    filename=uploaded_file.name
                )
                
                all_detections.extend(detections)
                all_stats.append(stats)
            
            with col2:
                st.subheader("Detection Results")
                st.image(annotated_img, width='stretch')
                
                # Display alert
                if stats.get("total_detections", 0) > 0:
                    alert = st.session_state.alert_system.check_detection(stats)
                    if alert["severity"] == "critical":
                        st.error(alert["message"])
                    elif alert["severity"] == "high":
                        st.warning(alert["message"])
                    elif alert["severity"] == "medium":
                        st.info(alert["message"])
                    else:
                        st.success(alert["message"])
                
                # Display statistics
                if show_stats:
                    st.markdown("### 📊 Detection Statistics")
                    
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    with metric_col1:
                        st.metric("Total Detections", stats.get("total_detections", 0))
                    with metric_col2:
                        st.metric("Avg Confidence", f"{stats.get('avg_confidence', 0):.2%}")
                    with metric_col3:
                        st.metric("Coverage", f"{stats.get('coverage_percentage', 0):.2f}%")
                    with metric_col4:
                        st.metric("Spill Count", stats.get("spill_count", 0))
            
            # Detailed information
            if detections:
                st.markdown("---")
                st.subheader("🔍 Detection Details")
                
                # Detection table
                df = create_detection_dataframe(detections)
                st.dataframe(df, width='stretch')
                
                # Confidence distribution
                st.subheader("📈 Confidence Distribution")
                fig = create_confidence_distribution_plot(detections)
                st.plotly_chart(fig, width='stretch')
                
                # Export options
                st.markdown("---")
                st.subheader("📥 Export Results")
                
                export_col1, export_col2, export_col3 = st.columns(3)
                
                with export_col1:
                    # Text report
                    text_report = generate_text_report(detections, stats, 
                                                      {"Filename": uploaded_file.name,
                                                       "Size": f"{image.size[0]}x{image.size[1]}"})
                    st.download_button(
                        "Download Text Report",
                        text_report,
                        file_name=f"report_{uploaded_file.name}.txt",
                        mime="text/plain"
                    )
                
                with export_col2:
                    # CSV report
                    csv_report = generate_csv_report(detections)
                    st.download_button(
                        "Download CSV Report",
                        csv_report,
                        file_name=f"detections_{uploaded_file.name}.csv",
                        mime="text/csv"
                    )
                
                with export_col3:
                    # JSON report
                    json_report = generate_json_report(detections, stats)
                    st.download_button(
                        "Download JSON Report",
                        json_report,
                        file_name=f"report_{uploaded_file.name}.json",
                        mime="application/json"
                    )
                
                # PDF report
                export_col4, export_col5 = st.columns(2)
                with export_col4:
                    pdf_report = generate_pdf_report(
                        detections, 
                        stats,
                        {"Filename": uploaded_file.name, "Size": f"{image.size[0]}x{image.size[1]}"},
                        annotated_img
                    )
                    st.download_button(
                        "Download PDF Report",
                        pdf_report,
                        file_name=f"report_{uploaded_file.name}.pdf",
                        mime="application/pdf"
                    )
                
                # Download annotated image
                with export_col5:
                    annotated_pil = Image.fromarray(annotated_img)
                    img_buffer = io.BytesIO()
                    annotated_pil.save(img_buffer, format='PNG')
                    st.download_button(
                        "Download Annotated Image",
                        img_buffer.getvalue(),
                        file_name=f"annotated_{uploaded_file.name}",
                        mime="image/png"
                    )
            else:
                st.info("✅ No oil spills detected in this image.")
    
    # Summary across all images
    if len(uploaded_files) > 1:
        st.markdown("---")
        st.subheader("📊 Summary Across All Images")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        with summary_col1:
            st.metric("Total Images", len(uploaded_files))
        with summary_col2:
            st.metric("Total Detections", sum(s.get("total_detections", 0) for s in all_stats))
        with summary_col3:
            avg_conf = np.mean([s.get("avg_confidence", 0) for s in all_stats if s.get("total_detections", 0) > 0])
            st.metric("Avg Confidence", f"{avg_conf:.2%}" if avg_conf > 0 else "N/A")
        with summary_col4:
            images_with_detections = sum(1 for s in all_stats if s.get("total_detections", 0) > 0)
            st.metric("Images with Spills", images_with_detections)

else:
    st.info("👆 Please upload one or more images to get started with oil spill detection.")
    
    # Show example
    st.markdown("---")
    st.subheader("ℹ️ How to Use")
    st.markdown("""
    1. **Upload Images**: Click the upload area above and select one or more image files
    2. **Adjust Settings**: Use the sidebar to adjust confidence threshold
    3. **View Results**: See detections with bounding boxes and confidence scores
    4. **Export Data**: Download reports in various formats (TXT, CSV, JSON)
    5. **Analyze**: Review statistics and confidence distributions
    """)

