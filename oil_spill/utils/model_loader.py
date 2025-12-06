"""
Model loader utility for YOLOv11 oil spill detection model
"""
import os
from pathlib import Path
import streamlit as st
from ultralytics import YOLO
import torch

@st.cache_resource
def load_model(model_path="best.pt"):
    """
    Load YOLOv11 model with caching for better performance
    
    Args:
        model_path: Path to the model file
        
    Returns:
        Loaded YOLO model
    """
    try:
        # Check if model file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        # Load model
        model = YOLO(model_path)
        
        # Move to GPU if available
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model.to(device)
        
        return model, device
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

def get_model_info(model):
    """
    Get information about the loaded model
    
    Args:
        model: YOLO model instance
        
    Returns:
        Dictionary with model information
    """
    if model is None:
        return {}
    
    info = {
        "Model Type": "YOLOv11",
        "Task": "Object Detection",
        "Classes": model.names if hasattr(model, 'names') else {},
        "Device": next(model.model.parameters()).device.type if hasattr(model, 'model') else "Unknown"
    }
    
    return info

