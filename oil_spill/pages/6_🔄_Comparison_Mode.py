"""
Comparison Mode Page - Compare before/after images or multiple detections
"""
import streamlit as st
from PIL import Image
import numpy as np
from utils.model_loader import load_model
from utils.image_processor import process_image, calculate_spill_coverage
from utils.activity_logger import ActivityLogger
import plotly.graph_objects as go

st.set_page_config(page_title="Comparison Mode", page_icon="🔄", layout="wide")

st.title("🔄 Comparison Mode")
st.markdown("Compare images side-by-side to analyze oil spill detection differences")

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
    comparison_mode = st.radio(
        "Comparison Type",
        ["Before/After", "Multiple Images", "Same Image Different Thresholds"],
        index=0
    )

# Main content
if comparison_mode == "Before/After":
    st.subheader("📸 Before/After Comparison")
    st.markdown("Upload two images to compare detection results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Before Image")
        before_file = st.file_uploader("Upload Before Image", type=['png', 'jpg', 'jpeg'], key="before")
    
    with col2:
        st.markdown("### After Image")
        after_file = st.file_uploader("Upload After Image", type=['png', 'jpg', 'jpeg'], key="after")
    
    if before_file and after_file:
        before_img = Image.open(before_file)
        after_img = Image.open(after_file)
        
        # Process both images
        with st.spinner("Processing images..."):
            before_annotated, before_detections, before_stats = process_image(
                st.session_state.model, before_img, conf_threshold
            )
            after_annotated, after_detections, after_stats = process_image(
                st.session_state.model, after_img, conf_threshold
            )
        
        # Display side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(before_annotated, width='stretch', caption="Before")
            st.metric("Detections", before_stats.get("total_detections", 0))
            st.metric("Avg Confidence", f"{before_stats.get('avg_confidence', 0):.2%}")
        
        with col2:
            st.image(after_annotated, width='stretch', caption="After")
            st.metric("Detections", after_stats.get("total_detections", 0))
            st.metric("Avg Confidence", f"{after_stats.get('avg_confidence', 0):.2%}")
        
        # Log comparison activity
        comparison_results = {
            "before_detections": before_stats.get("total_detections", 0),
            "after_detections": after_stats.get("total_detections", 0),
            "before_confidence": before_stats.get("avg_confidence", 0),
            "after_confidence": after_stats.get("avg_confidence", 0)
        }
        st.session_state.activity_logger.log_comparison(
            comparison_type="Before/After",
            files=[before_file.name, after_file.name],
            results=comparison_results
        )
        
        # Comparison metrics
        st.markdown("---")
        st.subheader("📊 Comparison Metrics")
        
        diff_detections = after_stats.get("total_detections", 0) - before_stats.get("total_detections", 0)
        diff_confidence = after_stats.get("avg_confidence", 0) - before_stats.get("avg_confidence", 0)
        
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        with comp_col1:
            st.metric("Detection Difference", diff_detections, delta=f"{diff_detections}")
        with comp_col2:
            st.metric("Confidence Difference", f"{diff_confidence:.2%}", delta=f"{diff_confidence:.2%}")
        with comp_col3:
            change_pct = ((after_stats.get("total_detections", 0) - before_stats.get("total_detections", 0)) / 
                         max(before_stats.get("total_detections", 1), 1)) * 100
            st.metric("Change Percentage", f"{change_pct:.1f}%")
        
        # Comparison chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Before',
            x=['Detections', 'Avg Confidence'],
            y=[before_stats.get("total_detections", 0), before_stats.get("avg_confidence", 0) * 100],
            marker_color='#1f77b4'
        ))
        fig.add_trace(go.Bar(
            name='After',
            x=['Detections', 'Avg Confidence'],
            y=[after_stats.get("total_detections", 0), after_stats.get("avg_confidence", 0) * 100],
            marker_color='#ff7f0e'
        ))
        fig.update_layout(
            title="Before vs After Comparison",
            barmode='group',
            yaxis_title="Value",
            template="plotly_white"
        )
        st.plotly_chart(fig, width='stretch')

elif comparison_mode == "Multiple Images":
    st.subheader("📸 Multiple Image Comparison")
    st.markdown("Upload multiple images to compare detection results")
    
    uploaded_files = st.file_uploader(
        "Upload Images for Comparison",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True
    )
    
    if uploaded_files and len(uploaded_files) >= 2:
        # Process all images
        results = []
        with st.spinner("Processing images..."):
            for file in uploaded_files:
                img = Image.open(file)
                annotated, detections, stats = process_image(
                    st.session_state.model, img, conf_threshold
                )
                results.append({
                    "filename": file.name,
                    "image": annotated,
                    "detections": detections,
                    "stats": stats
                })
        
        # Display grid
        cols_per_row = 3
        for i in range(0, len(results), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(results):
                    with col:
                        result = results[i + j]
                        st.image(result["image"], width='stretch', caption=result["filename"])
                        st.metric("Detections", result["stats"].get("total_detections", 0))
        
        # Comparison table
        st.markdown("---")
        st.subheader("📊 Comparison Table")
        
        import pandas as pd
        comparison_data = []
        for result in results:
            comparison_data.append({
                "Image": result["filename"],
                "Detections": result["stats"].get("total_detections", 0),
                "Avg Confidence": f"{result['stats'].get('avg_confidence', 0):.2%}",
                "Max Confidence": f"{result['stats'].get('max_confidence', 0):.2%}"
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, width='stretch')
        
        # Summary chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[r["filename"] for r in results],
            y=[r["stats"].get("total_detections", 0) for r in results],
            marker_color='#1f77b4'
        ))
        fig.update_layout(
            title="Detection Count Comparison",
            xaxis_title="Image",
            yaxis_title="Number of Detections",
            template="plotly_white"
        )
        st.plotly_chart(fig, width='stretch')
        
        # Log comparison activity for multiple images
        comparison_results = {
            "image_count": len(results),
            "detections": [r["stats"].get("total_detections", 0) for r in results],
            "confidences": [r["stats"].get("avg_confidence", 0) for r in results]
        }
        st.session_state.activity_logger.log_comparison(
            comparison_type="Multiple Images",
            files=[f.name for f in uploaded_files],
            results=comparison_results
        )

elif comparison_mode == "Same Image Different Thresholds":
    st.subheader("🔍 Threshold Comparison")
    st.markdown("Upload one image and compare results at different confidence thresholds")
    
    uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        
        # Get multiple thresholds
        thresholds = st.multiselect(
            "Select Thresholds to Compare",
            [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            default=[0.2, 0.25, 0.3, 0.4]
        )
        
        if thresholds:
            results = []
            with st.spinner("Processing at different thresholds..."):
                for threshold in sorted(thresholds):
                    annotated, detections, stats = process_image(
                        st.session_state.model, img, threshold
                    )
                    results.append({
                        "threshold": threshold,
                        "image": annotated,
                        "detections": detections,
                        "stats": stats
                    })
            
            # Display results
            cols_per_row = 2
            for i in range(0, len(results), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(results):
                        with col:
                            result = results[i + j]
                            st.image(result["image"], width='stretch', 
                                   caption=f"Threshold: {result['threshold']}")
                            st.metric("Detections", result["stats"].get("total_detections", 0))
                            st.metric("Avg Confidence", f"{result['stats'].get('avg_confidence', 0):.2%}")
            
            # Threshold comparison chart
            st.markdown("---")
            st.subheader("📊 Threshold Analysis")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[r["threshold"] for r in results],
                y=[r["stats"].get("total_detections", 0) for r in results],
                mode='lines+markers',
                name='Detections',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=10)
            ))
            fig.update_layout(
                title="Detection Count vs Confidence Threshold",
                xaxis_title="Confidence Threshold",
                yaxis_title="Number of Detections",
                template="plotly_white"
            )
            st.plotly_chart(fig, width='stretch')
            
            # Log comparison activity for threshold comparison
            comparison_results = {
                "thresholds": thresholds,
                "detections": [r["stats"].get("total_detections", 0) for r in results],
                "confidences": [r["stats"].get("avg_confidence", 0) for r in results]
            }
            st.session_state.activity_logger.log_comparison(
                comparison_type="Threshold Comparison",
                files=[uploaded_file.name],
                results=comparison_results
            )

