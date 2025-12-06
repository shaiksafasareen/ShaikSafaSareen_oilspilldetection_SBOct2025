"""
Visualization utilities for oil spill detection results
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import List, Dict

def create_confidence_distribution_plot(detections: List[Dict]) -> go.Figure:
    """
    Create a histogram of confidence scores
    
    Args:
        detections: List of detection dictionaries
        
    Returns:
        Plotly figure
    """
    if not detections:
        fig = go.Figure()
        fig.add_annotation(text="No detections to display", 
                          xref="paper", yref="paper", x=0.5, y=0.5)
        return fig
    
    confidences = [det["confidence"] for det in detections]
    
    fig = go.Figure(data=[go.Histogram(
        x=confidences,
        nbinsx=20,
        marker_color='#1f77b4',
        marker_line_color='white',
        marker_line_width=1
    )])
    
    fig.update_layout(
        title="Confidence Score Distribution",
        xaxis_title="Confidence Score",
        yaxis_title="Frequency",
        template="plotly_white",
        height=300
    )
    
    return fig

def create_detection_timeline_plot(detection_history: List[Dict]) -> go.Figure:
    """
    Create a timeline plot of detections over frames
    
    Args:
        detection_history: List of {frame, detections} dictionaries
        
    Returns:
        Plotly figure
    """
    if not detection_history:
        fig = go.Figure()
        fig.add_annotation(text="No detection history", 
                          xref="paper", yref="paper", x=0.5, y=0.5)
        return fig
    
    df = pd.DataFrame(detection_history)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['frame'],
        y=df['detections'],
        mode='lines+markers',
        name='Detections per Frame',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title="Detection Timeline",
        xaxis_title="Frame Number",
        yaxis_title="Number of Detections",
        template="plotly_white",
        height=300
    )
    
    return fig

def create_statistics_cards(stats: Dict) -> List[Dict]:
    """
    Create statistics card data for display
    
    Args:
        stats: Statistics dictionary
        
    Returns:
        List of card dictionaries
    """
    cards = []
    
    if "total_detections" in stats:
        cards.append({
            "title": "Total Detections",
            "value": stats["total_detections"],
            "icon": "🔍"
        })
    
    if "avg_confidence" in stats:
        cards.append({
            "title": "Avg Confidence",
            "value": f"{stats['avg_confidence']:.2%}",
            "icon": "📊"
        })
    
    if "coverage_percentage" in stats:
        cards.append({
            "title": "Coverage",
            "value": f"{stats['coverage_percentage']:.2f}%",
            "icon": "🌊"
        })
    
    if "spill_count" in stats:
        cards.append({
            "title": "Spill Count",
            "value": stats["spill_count"],
            "icon": "💧"
        })
    
    return cards

def create_heatmap_overlay(image: np.ndarray, detections: List[Dict], alpha: float = 0.5) -> np.ndarray:
    """
    Create a heatmap overlay on the image showing detection density
    
    Args:
        image: Input image array
        detections: List of detection dictionaries
        alpha: Transparency of overlay
        
    Returns:
        Image array with heatmap overlay
    """
    if not detections:
        return image
    
    # Create heatmap
    heatmap = np.zeros(image.shape[:2], dtype=np.float32)
    
    for det in detections:
        bbox = det["bbox"]
        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        confidence = det["confidence"]
        
        # Add confidence-weighted heat
        heatmap[y1:y2, x1:x2] += confidence
    
    # Normalize heatmap
    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()
    
    # Apply colormap
    try:
        colormap = cm.get_cmap('hot')
    except AttributeError:
        # For newer matplotlib versions
        colormap = plt.cm.get_cmap('hot')
    heatmap_colored = colormap(heatmap)[:, :, :3]
    heatmap_colored = (heatmap_colored * 255).astype(np.uint8)
    
    # Blend with original image
    overlay = cv2.addWeighted(image, 1 - alpha, heatmap_colored, alpha, 0)
    
    return overlay

