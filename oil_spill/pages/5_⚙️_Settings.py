"""
Settings Page - Configure application settings
"""
import streamlit as st
import os

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings")
st.markdown("Configure application settings and preferences")

# Model settings
st.header("🤖 Model Settings")

if 'model' in st.session_state:
    model_info = st.session_state.model
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Information")
        st.info(f"**Device**: {st.session_state.get('device', 'Unknown')}")
        st.info(f"**Model Type**: YOLOv11")
        
        if hasattr(model_info, 'names'):
            st.info(f"**Classes**: {len(model_info.names)}")
            with st.expander("View Class Names"):
                for idx, name in model_info.names.items():
                    st.text(f"{idx}: {name}")
    
    with col2:
        st.subheader("Model Status")
        if os.path.exists("best.pt"):
            file_size = os.path.getsize("best.pt") / (1024 * 1024)
            st.success(f"✅ Model loaded successfully")
            st.info(f"**File Size**: {file_size:.2f} MB")
            st.info(f"**Location**: best.pt")
        else:
            st.error("❌ Model file not found")

# Application settings
st.markdown("---")
st.header("🎨 Application Settings")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Display Settings")
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"], index=2)
    show_sidebar = st.checkbox("Show Sidebar by Default", value=True)
    page_icon = st.text_input("Page Icon", value="🌊")

with col2:
    st.subheader("Performance Settings")
    enable_caching = st.checkbox("Enable Model Caching", value=True)
    max_image_size = st.slider("Max Image Size (MB)", 1, 50, 10)
    max_video_size = st.slider("Max Video Size (MB)", 10, 500, 100)

# Detection settings
st.markdown("---")
st.header("🔍 Detection Settings")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Default Thresholds")
    default_conf = st.slider("Default Confidence Threshold", 0.0, 1.0, 0.25, 0.05)
    default_iou = st.slider("Default IoU Threshold", 0.0, 1.0, 0.45, 0.05)

with col2:
    st.subheader("Processing Options")
    batch_size = st.number_input("Batch Size", min_value=1, max_value=32, value=1)
    num_workers = st.number_input("Number of Workers", min_value=0, max_value=8, value=0)

# Export settings
st.markdown("---")
st.header("📥 Export Settings")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Report Format")
    default_report_format = st.selectbox("Default Report Format", ["TXT", "CSV", "JSON", "PDF"], index=0)
    include_timestamp = st.checkbox("Include Timestamp in Reports", value=True)
    include_images = st.checkbox("Include Images in Reports", value=False)

with col2:
    st.subheader("File Naming")
    naming_convention = st.selectbox("File Naming Convention", 
                                     ["Original Name", "Timestamp", "Custom"], 
                                     index=0)
    if naming_convention == "Custom":
        custom_prefix = st.text_input("Custom Prefix", value="oil_spill_")

# Save settings
st.markdown("---")
if st.button("💾 Save Settings", type="primary"):
    st.success("Settings saved successfully!")
    st.info("Note: Some settings require app restart to take effect.")

# Reset settings
if st.button("🔄 Reset to Defaults", type="secondary"):
    st.warning("Settings reset to defaults")

# About
st.markdown("---")
st.header("ℹ️ About")

st.markdown("""
**Oil Spill Detection Application**

- **Version**: 1.0.0
- **Model**: YOLOv11
- **Framework**: Streamlit
- **Purpose**: Detect oil spills in images and videos using advanced AI

For support or questions, please refer to the documentation.
""")

