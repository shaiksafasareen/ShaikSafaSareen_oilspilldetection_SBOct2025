"""
Video processing utilities for oil spill detection
"""
import cv2
import numpy as np
from PIL import Image
import streamlit as st
from typing import List, Dict, Tuple
import tempfile
import os

def process_video(model, video_path: str, conf_threshold: float = 0.25, 
                 output_path: str = None, progress_callback=None, 
                 store_frames: bool = False) -> Tuple[str, Dict]:
    """
    Process video frame by frame for oil spill detection
    
    Args:
        model: YOLO model instance
        video_path: Path to input video file
        conf_threshold: Confidence threshold
        output_path: Path to save annotated video (optional)
        progress_callback: Callback function for progress updates
        store_frames: Whether to store original and annotated frames for comparison
        
    Returns:
        Tuple of (output_video_path, statistics_dict)
    """
    # Open video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create output video writer
    if output_path is None:
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
    
    # Try multiple codecs in order of preference (most compatible first)
    codecs_to_try = [
        ('mp4v', 'mp4v'),  # Most universally available
        ('XVID', 'XVID'),  # Xvid codec
        ('MJPG', 'MJPG'),  # Motion JPEG
        ('X264', 'X264'),  # x264 encoder if available
    ]
    
    out = None
    used_codec = None
    
    for codec_name, fourcc_str in codecs_to_try:
        try:
            fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            if out.isOpened():
                used_codec = codec_name
                break
            else:
                out.release()
                out = None
        except Exception as e:
            if out:
                out.release()
                out = None
            continue
    
    # If all codecs failed, use mp4v as last resort
    if out is None or not out.isOpened():
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        used_codec = 'mp4v'
        if not out.isOpened():
            raise RuntimeError("Failed to initialize video writer with any available codec")
    
    # Statistics
    stats = {
        "total_frames": total_frames,
        "processed_frames": 0,
        "frames_with_detections": 0,
        "total_detections": 0,
        "avg_detections_per_frame": 0.0,
        "max_detections_in_frame": 0,
        "detection_history": [],
        "frame_details": [] if store_frames else None
    }
    
    frame_count = 0
    original_frames = [] if store_frames else None
    annotated_frames = [] if store_frames else None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            
            # Run inference
            results = model(frame_rgb, conf=conf_threshold, verbose=False)
            result = results[0]
            
            # Process detections
            detections_count = 0
            detections_info = []
            avg_confidence = 0.0
            
            if result.boxes is not None and len(result.boxes) > 0:
                detections_count = len(result.boxes)
                stats["frames_with_detections"] += 1
                stats["total_detections"] += detections_count
                stats["max_detections_in_frame"] = max(
                    stats["max_detections_in_frame"], 
                    detections_count
                )
                
                # Get detailed detection info
                confidences = result.boxes.conf.cpu().numpy()
                avg_confidence = float(np.mean(confidences))
                
                for i in range(len(result.boxes)):
                    detections_info.append({
                        "confidence": float(confidences[i]),
                        "class": int(result.boxes.cls[i].cpu().numpy()),
                        "bbox": result.boxes.xyxy[i].cpu().numpy().tolist()
                    })
            
            stats["detection_history"].append({
                "frame": frame_count,
                "detections": detections_count
            })
            
            # Get annotated frame (must be done before storing)
            annotated_frame = result.plot()
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
            
            # Store frame details if requested
            if store_frames:
                frame_detail = {
                    "frame_number": frame_count,
                    "detections_count": detections_count,
                    "avg_confidence": avg_confidence,
                    "detections": detections_info,
                    "has_detection": detections_count > 0
                }
                stats["frame_details"].append(frame_detail)
                
                # Store frames for comparison
                original_frames.append(frame_rgb.copy())
                annotated_frames.append(annotated_frame.copy())
            
            # Write frame
            out.write(annotated_frame_bgr)
            
            frame_count += 1
            stats["processed_frames"] = frame_count
            
            # Update progress
            if progress_callback:
                progress = frame_count / total_frames
                progress_callback(progress)
    
    finally:
        cap.release()
        out.release()
    
    # Calculate averages
    if stats["processed_frames"] > 0:
        stats["avg_detections_per_frame"] = stats["total_detections"] / stats["processed_frames"]
    
    # Add frame data if stored
    if store_frames:
        stats["original_frames"] = original_frames
        stats["annotated_frames"] = annotated_frames
    
    return output_path, stats

def extract_frames_from_video(video_path: str, num_frames: int = 10) -> List[np.ndarray]:
    """
    Extract sample frames from video for preview
    
    Args:
        video_path: Path to video file
        num_frames: Number of frames to extract
        
    Returns:
        List of frame arrays
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frames = []
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
    
    cap.release()
    return frames

