"""
Activity Logger - Tracks all app usage and saves files with comprehensive logging
"""
import os
import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import Dict, List, Optional
import json
import numpy as np

class ActivityLogger:
    """Comprehensive activity logger for oil spill detection app"""
    
    def __init__(self, base_dir: str = "information_record"):
        """
        Initialize activity logger
        
        Args:
            base_dir: Base directory for storing all records
        """
        self.base_dir = Path(base_dir)
        self.input_dir = self.base_dir / "inputs"
        self.output_dir = self.base_dir / "outputs"
        self.excel_file = self.base_dir / "activity_log.xlsx"
        
        # Create directories
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.input_dir / "images").mkdir(exist_ok=True)
        (self.input_dir / "videos").mkdir(exist_ok=True)
        (self.output_dir / "images").mkdir(exist_ok=True)
        (self.output_dir / "videos").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
    
    def _get_timestamp(self) -> Dict[str, str]:
        """Get current timestamp information"""
        now = datetime.now()
        return {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": now.timestamp()
        }
    
    def _json_safe_dumps(self, obj) -> str:
        """
        Safely convert object to JSON string, handling numpy arrays and other non-serializable types
        
        Args:
            obj: Object to serialize
            
        Returns:
            JSON string
        """
        def convert_to_serializable(o):
            """Recursively convert numpy types to Python native types"""
            if isinstance(o, np.ndarray):
                return o.tolist()
            elif isinstance(o, (np.integer, np.floating)):
                return o.item()
            elif isinstance(o, np.bool_):
                return bool(o)
            elif isinstance(o, dict):
                return {key: convert_to_serializable(value) for key, value in o.items()}
            elif isinstance(o, list):
                return [convert_to_serializable(item) for item in o]
            elif isinstance(o, (str, int, float, bool, type(None))):
                return o
            else:
                # Try to convert to string for unknown types
                return str(o)
        
        try:
            cleaned_obj = convert_to_serializable(obj)
            return json.dumps(cleaned_obj, indent=2)
        except Exception as e:
            # Fallback to string representation if JSON conversion fails
            return json.dumps({"error": f"Could not serialize: {str(e)}"})
    
    def _save_file(self, file_data, original_filename: str, file_type: str, 
                   is_input: bool = True) -> str:
        """
        Save file with timestamp
        
        Args:
            file_data: File bytes or file path
            original_filename: Original filename
            file_type: 'image' or 'video'
            is_input: Whether it's input or output
            
        Returns:
            Saved file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(original_filename)
        new_filename = f"{timestamp}_{name}{ext}"
        
        if is_input:
            save_dir = self.input_dir / (file_type + "s")
        else:
            save_dir = self.output_dir / (file_type + "s")
        
        save_path = save_dir / new_filename
        
        # Save file
        if isinstance(file_data, (str, Path)):
            # It's a file path
            shutil.copy2(file_data, save_path)
        else:
            # It's file bytes
            with open(save_path, 'wb') as f:
                f.write(file_data)
        
        return str(save_path)
    
    def _load_excel_log(self) -> pd.DataFrame:
        """Load existing Excel log or create new one"""
        if self.excel_file.exists():
            try:
                return pd.read_excel(self.excel_file)
            except:
                # If corrupted, create new
                return pd.DataFrame()
        else:
            return pd.DataFrame()
    
    def _save_excel_log(self, df: pd.DataFrame):
        """Save Excel log"""
        df.to_excel(self.excel_file, index=False, engine='openpyxl')
    
    def log_image_detection(self, input_file, output_image: Optional[bytes] = None,
                           detections: List[Dict] = None, stats: Dict = None,
                           filename: str = None) -> Dict:
        """
        Log image detection activity
        
        Args:
            input_file: Input image file (bytes or path)
            output_image: Output annotated image (bytes)
            detections: List of detections
            stats: Statistics dictionary
            filename: Original filename
            
        Returns:
            Log entry dictionary
        """
        timestamp_info = self._get_timestamp()
        
        # Save input image
        if isinstance(input_file, bytes):
            input_path = self._save_file(input_file, filename or "image.jpg", "image", True)
        else:
            input_path = self._save_file(input_file, filename or os.path.basename(input_file), "image", True)
        
        # Save output image
        output_path = None
        if output_image is not None:
            output_filename = f"annotated_{filename or 'image.jpg'}"
            output_path = self._save_file(output_image, output_filename, "image", False)
        
        # Create log entry
        log_entry = {
            "Date": timestamp_info["date"],
            "Time": timestamp_info["time"],
            "Day": timestamp_info["day"],
            "Action_Type": "Image Detection",
            "Input_File": input_path,
            "Output_File": output_path,
            "Original_Filename": filename or "unknown",
            "Total_Detections": stats.get("total_detections", 0) if stats else 0,
            "Avg_Confidence": f"{stats.get('avg_confidence', 0):.4f}" if stats else "0.0000",
            "Coverage_Percentage": f"{stats.get('coverage_percentage', 0):.2f}%" if stats and 'coverage_percentage' in stats else "0.00%",
            "Detection_Details": self._json_safe_dumps(detections) if detections else "[]",
            "Statistics": self._json_safe_dumps(stats) if stats else "{}",
            "Timestamp": timestamp_info["datetime"]
        }
        
        # Update Excel
        df = self._load_excel_log()
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        self._save_excel_log(df)
        
        return log_entry
    
    def log_video_detection(self, input_file, output_video_path: Optional[str] = None,
                           stats: Dict = None, filename: str = None) -> Dict:
        """
        Log video detection activity
        
        Args:
            input_file: Input video file (bytes or path)
            output_video_path: Path to output video
            stats: Statistics dictionary
            filename: Original filename
            
        Returns:
            Log entry dictionary
        """
        timestamp_info = self._get_timestamp()
        
        # Save input video
        if isinstance(input_file, bytes):
            input_path = self._save_file(input_file, filename or "video.mp4", "video", True)
        else:
            input_path = self._save_file(input_file, filename or os.path.basename(input_file), "video", True)
        
        # Save output video
        output_path = None
        if output_video_path and os.path.exists(output_video_path):
            output_filename = f"annotated_{filename or 'video.mp4'}"
            output_path = self._save_file(output_video_path, output_filename, "video", False)
        
        # Create log entry
        log_entry = {
            "Date": timestamp_info["date"],
            "Time": timestamp_info["time"],
            "Day": timestamp_info["day"],
            "Action_Type": "Video Detection",
            "Input_File": input_path,
            "Output_File": output_path,
            "Original_Filename": filename or "unknown",
            "Total_Frames": stats.get("total_frames", 0) if stats else 0,
            "Frames_with_Detections": stats.get("frames_with_detections", 0) if stats else 0,
            "Total_Detections": stats.get("total_detections", 0) if stats else 0,
            "Avg_Detections_per_Frame": f"{stats.get('avg_detections_per_frame', 0):.2f}" if stats else "0.00",
            "Statistics": self._json_safe_dumps(stats) if stats else "{}",
            "Timestamp": timestamp_info["datetime"]
        }
        
        # Update Excel
        df = self._load_excel_log()
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        self._save_excel_log(df)
        
        return log_entry
    
    def log_camera_detection(self, detections: List[Dict] = None, 
                           stats: Dict = None, frame_count: int = 0) -> Dict:
        """
        Log real-time camera detection activity
        
        Args:
            detections: List of detections
            stats: Statistics dictionary
            frame_count: Number of frames processed
            
        Returns:
            Log entry dictionary
        """
        timestamp_info = self._get_timestamp()
        
        log_entry = {
            "Date": timestamp_info["date"],
            "Time": timestamp_info["time"],
            "Day": timestamp_info["day"],
            "Action_Type": "Real-time Camera Detection",
            "Input_File": "Camera Feed",
            "Output_File": "N/A",
            "Original_Filename": "camera_feed",
            "Frames_Processed": frame_count,
            "Total_Detections": stats.get("total_detections", 0) if stats else 0,
            "Avg_Confidence": f"{stats.get('avg_confidence', 0):.4f}" if stats else "0.0000",
            "Detection_Details": self._json_safe_dumps(detections) if detections else "[]",
            "Statistics": self._json_safe_dumps(stats) if stats else "{}",
            "Timestamp": timestamp_info["datetime"]
        }
        
        # Update Excel
        df = self._load_excel_log()
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        self._save_excel_log(df)
        
        return log_entry
    
    def log_comparison(self, comparison_type: str, files: List[str], 
                     results: Dict = None) -> Dict:
        """
        Log comparison mode activity
        
        Args:
            comparison_type: Type of comparison (Before/After, Multiple, Threshold)
            files: List of file paths used
            results: Comparison results
            
        Returns:
            Log entry dictionary
        """
        timestamp_info = self._get_timestamp()
        
        log_entry = {
            "Date": timestamp_info["date"],
            "Time": timestamp_info["time"],
            "Day": timestamp_info["day"],
            "Action_Type": f"Comparison Mode - {comparison_type}",
            "Input_File": "; ".join(files) if files else "N/A",
            "Output_File": "N/A",
            "Original_Filename": "; ".join([os.path.basename(f) for f in files]) if files else "N/A",
            "Comparison_Results": self._json_safe_dumps(results) if results else "{}",
            "Timestamp": timestamp_info["datetime"]
        }
        
        # Update Excel
        df = self._load_excel_log()
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        self._save_excel_log(df)
        
        return log_entry
    
    def log_report_generation(self, report_type: str, report_data: bytes,
                            original_filename: str = None, 
                            associated_action: str = None) -> Dict:
        """
        Log report generation
        
        Args:
            report_type: Type of report (PDF, CSV, JSON, TXT)
            report_data: Report file bytes
            original_filename: Original file that generated the report
            associated_action: Associated action type
            
        Returns:
            Log entry dictionary
        """
        timestamp_info = self._get_timestamp()
        
        # Save report
        report_filename = f"report_{timestamp_info['date']}_{timestamp_info['time'].replace(':', '')}.{report_type.lower()}"
        report_path = self._save_file(report_data, report_filename, "report", False)
        
        log_entry = {
            "Date": timestamp_info["date"],
            "Time": timestamp_info["time"],
            "Day": timestamp_info["day"],
            "Action_Type": f"Report Generation - {report_type}",
            "Input_File": original_filename or "N/A",
            "Output_File": report_path,
            "Original_Filename": original_filename or "N/A",
            "Associated_Action": associated_action or "N/A",
            "Timestamp": timestamp_info["datetime"]
        }
        
        # Update Excel
        df = self._load_excel_log()
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        self._save_excel_log(df)
        
        return log_entry

