"""
Image processing utilities for oil spill detection
"""
import cv2
import numpy as np
from PIL import Image
import streamlit as st
from typing import List, Dict, Tuple
import pandas as pd

def process_image(model, image: Image.Image, conf_threshold: float = 0.25) -> Tuple[np.ndarray, List[Dict], Dict]:
    """
    Process a single image through the model
    
    Args:
        model: YOLO model instance
        image: PIL Image object
        conf_threshold: Confidence threshold for detections
        
    Returns:
        Tuple of (annotated_image, detections_list, statistics_dict)
    """
    # Convert PIL to numpy array
    img_array = np.array(image)
    
    # Run inference
    results = model(img_array, conf=conf_threshold, verbose=False)
    
    # Get first result (single image)
    result = results[0]
    
    # Extract detections
    detections = []
    stats = {
        "total_detections": 0,
        "avg_confidence": 0.0,
        "max_confidence": 0.0,
        "min_confidence": 1.0,
        "bounding_boxes": []
    }
    
    if result.boxes is not None and len(result.boxes) > 0:
        boxes = result.boxes
        confidences = boxes.conf.cpu().numpy()
        classes = boxes.cls.cpu().numpy()
        xyxy = boxes.xyxy.cpu().numpy()
        
        stats["total_detections"] = len(boxes)
        stats["avg_confidence"] = float(np.mean(confidences))
        stats["max_confidence"] = float(np.max(confidences))
        stats["min_confidence"] = float(np.min(confidences))
        
        for i in range(len(boxes)):
            detection = {
                "class": int(classes[i]),
                "class_name": model.names[int(classes[i])],
                "confidence": float(confidences[i]),
                "bbox": xyxy[i].tolist(),
                "area": float((xyxy[i][2] - xyxy[i][0]) * (xyxy[i][3] - xyxy[i][1]))
            }
            detections.append(detection)
            stats["bounding_boxes"].append(xyxy[i].tolist())
    
    # Get annotated image
    annotated_img = result.plot()
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    
    return annotated_img, detections, stats

def process_batch_images(model, images: List[Image.Image], conf_threshold: float = 0.25) -> List[Tuple]:
    """
    Process multiple images in batch
    
    Args:
        model: YOLO model instance
        images: List of PIL Image objects
        conf_threshold: Confidence threshold
        
    Returns:
        List of tuples (annotated_image, detections, stats) for each image
    """
    results = []
    for img in images:
        result = process_image(model, img, conf_threshold)
        results.append(result)
    return results

def calculate_spill_coverage(detections: List[Dict], image_size: Tuple[int, int]) -> Dict:
    """
    Calculate oil spill coverage statistics
    
    Args:
        detections: List of detection dictionaries
        image_size: (width, height) of the image
        
    Returns:
        Dictionary with coverage statistics
    """
    width, height = image_size
    total_area = width * height
    
    coverage_stats = {
        "total_spill_area": 0,
        "coverage_percentage": 0.0,
        "spill_count": len(detections),
        "avg_spill_size": 0.0,
        "largest_spill_area": 0.0
    }
    
    if len(detections) > 0:
        areas = [det["area"] for det in detections]
        coverage_stats["total_spill_area"] = sum(areas)
        coverage_stats["coverage_percentage"] = (coverage_stats["total_spill_area"] / total_area) * 100
        coverage_stats["avg_spill_size"] = np.mean(areas)
        coverage_stats["largest_spill_area"] = max(areas)
    
    return coverage_stats

def create_detection_dataframe(detections: List[Dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from detections
    
    Args:
        detections: List of detection dictionaries
        
    Returns:
        pandas DataFrame
    """
    if not detections:
        return pd.DataFrame(columns=["Class", "Class Name", "Confidence", "Area", "X1", "Y1", "X2", "Y2"])
    
    data = []
    for det in detections:
        data.append({
            "Class": det["class"],
            "Class Name": det["class_name"],
            "Confidence": f"{det['confidence']:.4f}",
            "Area": f"{det['area']:.2f}",
            "X1": f"{det['bbox'][0]:.2f}",
            "Y1": f"{det['bbox'][1]:.2f}",
            "X2": f"{det['bbox'][2]:.2f}",
            "Y2": f"{det['bbox'][3]:.2f}"
        })
    
    return pd.DataFrame(data)

