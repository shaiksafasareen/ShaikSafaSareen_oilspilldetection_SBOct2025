"""
Report generation utilities for oil spill detection results
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict
import json
import numpy as np

def generate_text_report(detections: List[Dict], stats: Dict, 
                        image_info: Dict = None) -> str:
    """
    Generate a text report of detection results
    
    Args:
        detections: List of detection dictionaries
        stats: Statistics dictionary
        image_info: Image metadata dictionary
        
    Returns:
        Formatted text report
    """
    report = []
    report.append("=" * 60)
    report.append("OIL SPILL DETECTION REPORT")
    report.append("=" * 60)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    if image_info:
        report.append("IMAGE INFORMATION:")
        report.append("-" * 60)
        for key, value in image_info.items():
            report.append(f"  {key}: {value}")
        report.append("")
    
    report.append("DETECTION STATISTICS:")
    report.append("-" * 60)
    report.append(f"  Total Detections: {stats.get('total_detections', 0)}")
    report.append(f"  Average Confidence: {stats.get('avg_confidence', 0):.4f}")
    report.append(f"  Max Confidence: {stats.get('max_confidence', 0):.4f}")
    report.append(f"  Min Confidence: {stats.get('min_confidence', 0):.4f}")
    
    if 'coverage_percentage' in stats:
        report.append(f"  Coverage Percentage: {stats['coverage_percentage']:.2f}%")
        report.append(f"  Total Spill Area: {stats.get('total_spill_area', 0):.2f} pixels")
    
    report.append("")
    report.append("DETECTION DETAILS:")
    report.append("-" * 60)
    
    if detections:
        for i, det in enumerate(detections, 1):
            report.append(f"  Detection {i}:")
            report.append(f"    Class: {det.get('class_name', 'Unknown')}")
            report.append(f"    Confidence: {det.get('confidence', 0):.4f}")
            report.append(f"    Bounding Box: {det.get('bbox', [])}")
            report.append(f"    Area: {det.get('area', 0):.2f} pixels")
            report.append("")
    else:
        report.append("  No detections found.")
    
    report.append("=" * 60)
    
    return "\n".join(report)

def generate_csv_report(detections: List[Dict], filename: str = None) -> str:
    """
    Generate a CSV report of detections
    
    Args:
        detections: List of detection dictionaries
        filename: Optional filename to save CSV
        
    Returns:
        CSV string
    """
    if not detections:
        return ""
    
    data = []
    for det in detections:
        bbox = det.get('bbox', [0, 0, 0, 0])
        data.append({
            "Class": det.get('class_name', 'Unknown'),
            "Confidence": f"{det.get('confidence', 0):.4f}",
            "X1": f"{bbox[0]:.2f}",
            "Y1": f"{bbox[1]:.2f}",
            "X2": f"{bbox[2]:.2f}",
            "Y2": f"{bbox[3]:.2f}",
            "Area": f"{det.get('area', 0):.2f}"
        })
    
    df = pd.DataFrame(data)
    csv_string = df.to_csv(index=False)
    
    if filename:
        df.to_csv(filename, index=False)
    
    return csv_string

def generate_json_report(detections: List[Dict], stats: Dict, 
                        filename: str = None) -> str:
    """
    Generate a JSON report of detection results
    
    Args:
        detections: List of detection dictionaries
        stats: Statistics dictionary
        filename: Optional filename to save JSON
        
    Returns:
        JSON string
    """
    # Create a clean copy of stats without numpy arrays for JSON serialization
    clean_stats = {}
    for key, value in stats.items():
        # Skip numpy arrays and frame data (not JSON serializable)
        if key in ['original_frames', 'annotated_frames']:
            continue
        elif isinstance(value, (np.ndarray, np.generic)):
            # Convert numpy types to Python native types
            clean_stats[key] = value.tolist() if hasattr(value, 'tolist') else float(value)
        elif isinstance(value, list):
            # Check if list contains numpy arrays
            if value and isinstance(value[0], np.ndarray):
                continue  # Skip lists of numpy arrays
            clean_stats[key] = value
        else:
            clean_stats[key] = value
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "statistics": clean_stats,
        "detections": detections
    }
    
    # Custom JSON encoder for numpy types
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, (np.integer, np.floating)):
                return obj.item()
            elif isinstance(obj, np.bool_):
                return bool(obj)
            return super().default(obj)
    
    json_string = json.dumps(report, indent=2, cls=NumpyEncoder)
    
    if filename:
        with open(filename, 'w') as f:
            f.write(json_string)
    
    return json_string

