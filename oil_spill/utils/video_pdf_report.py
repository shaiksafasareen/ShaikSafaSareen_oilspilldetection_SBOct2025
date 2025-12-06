"""
PDF report generation for video analysis with frame-by-frame comparison
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import List, Dict
import io
import numpy as np
from PIL import Image as PILImage
import cv2

def generate_video_pdf_report(stats: Dict, video_info: Dict = None, 
                             original_frames: List[np.ndarray] = None,
                             annotated_frames: List[np.ndarray] = None,
                             max_frames_to_show: int = 20) -> bytes:
    """
    Generate a comprehensive PDF report for video analysis
    
    Args:
        stats: Statistics dictionary with frame_details
        video_info: Video metadata dictionary
        original_frames: List of original frame arrays
        annotated_frames: List of annotated frame arrays
        max_frames_to_show: Maximum number of frames to include in PDF
        
    Returns:
        PDF file as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=8
    )
    
    # Title
    story.append(Paragraph("Video Oil Spill Detection Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Date
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                         styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Video information
    if video_info:
        story.append(Paragraph("Video Information", heading_style))
        info_data = [[key, str(value)] for key, value in video_info.items()]
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Overall statistics
    story.append(Paragraph("Overall Statistics", heading_style))
    stats_data = [
        ["Metric", "Value"],
        ["Total Frames", str(stats.get("total_frames", 0))],
        ["Processed Frames", str(stats.get("processed_frames", 0))],
        ["Frames with Detections", str(stats.get("frames_with_detections", 0))],
        ["Total Detections", str(stats.get("total_detections", 0))],
        ["Average Detections per Frame", f"{stats.get('avg_detections_per_frame', 0):.2f}"],
        ["Max Detections in Single Frame", str(stats.get("max_detections_in_frame", 0))],
        ["Detection Rate", f"{(stats.get('frames_with_detections', 0) / max(stats.get('total_frames', 1), 1) * 100):.2f}%"]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Frame-by-frame analysis
    if stats.get("frame_details") and original_frames and annotated_frames:
        story.append(PageBreak())
        story.append(Paragraph("Frame-by-Frame Analysis", heading_style))
        story.append(Paragraph(
            "Comparison between original frames and detected frames with oil spill annotations.",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.2*inch))
        
        # Select frames to show (prioritize frames with detections)
        frame_details = stats["frame_details"]
        frames_with_detections = [f for f in frame_details if f["has_detection"]]
        frames_without_detections = [f for f in frame_details if not f["has_detection"]]
        
        # Take frames with detections first, then fill with others
        frames_to_show = frames_with_detections[:max_frames_to_show]
        remaining = max_frames_to_show - len(frames_to_show)
        if remaining > 0:
            # Add some frames without detections for comparison
            step = max(1, len(frames_without_detections) // remaining)
            frames_to_show.extend(frames_without_detections[::step][:remaining])
        
        frames_to_show = sorted(frames_to_show, key=lambda x: x["frame_number"])[:max_frames_to_show]
        
        for idx, frame_detail in enumerate(frames_to_show):
            frame_num = frame_detail["frame_number"]
            
            # Frame header
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(
                f"Frame {frame_num + 1}",
                subheading_style
            ))
            
            # Frame info table
            frame_info_data = [
                ["Detections", str(frame_detail["detections_count"])],
                ["Average Confidence", f"{frame_detail['avg_confidence']:.2%}" if frame_detail["avg_confidence"] > 0 else "N/A"],
                ["Status", "⚠️ Oil Spill Detected" if frame_detail["has_detection"] else "✅ No Detection"]
            ]
            
            frame_info_table = Table(frame_info_data, colWidths=[2*inch, 4*inch])
            frame_info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(frame_info_table)
            
            # Add frame images side by side
            try:
                # Resize frames for PDF (smaller size)
                original_frame = original_frames[frame_num]
                annotated_frame = annotated_frames[frame_num]
                
                # Resize to fit in PDF
                max_size = (200, 150)
                orig_pil = PILImage.fromarray(original_frame)
                orig_pil.thumbnail(max_size, PILImage.Resampling.LANCZOS)
                
                annot_pil = PILImage.fromarray(annotated_frame)
                annot_pil.thumbnail(max_size, PILImage.Resampling.LANCZOS)
                
                # Convert to bytes
                orig_buffer = io.BytesIO()
                annot_buffer = io.BytesIO()
                orig_pil.save(orig_buffer, format='PNG')
                annot_pil.save(annot_buffer, format='PNG')
                
                orig_buffer.seek(0)
                annot_buffer.seek(0)
                
                # Create images
                orig_img = RLImage(orig_buffer, width=2*inch, height=1.5*inch)
                annot_img = RLImage(annot_buffer, width=2*inch, height=1.5*inch)
                
                # Create comparison table
                comparison_table = Table([
                    [Paragraph("Original Frame", styles['Normal']), Paragraph("Detected Frame", styles['Normal'])],
                    [orig_img, annot_img]
                ], colWidths=[3*inch, 3*inch])
                
                comparison_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(Spacer(1, 0.1*inch))
                story.append(comparison_table)
                
                # Detection details for this frame
                if frame_detail["detections"]:
                    story.append(Spacer(1, 0.1*inch))
                    story.append(Paragraph("Detection Details:", styles['Normal']))
                    
                    det_data = [["#", "Confidence", "Class"]]
                    for i, det in enumerate(frame_detail["detections"], 1):
                        det_data.append([
                            str(i),
                            f"{det['confidence']:.2%}",
                            f"Class {det['class']}"
                        ])
                    
                    det_table = Table(det_data, colWidths=[0.5*inch, 2*inch, 3.5*inch])
                    det_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(det_table)
            
            except Exception as e:
                story.append(Paragraph(f"Could not load frame images: {str(e)}", styles['Normal']))
            
            # Add page break every few frames
            if (idx + 1) % 3 == 0 and idx < len(frames_to_show) - 1:
                story.append(PageBreak())
    
    # Summary
    story.append(PageBreak())
    story.append(Paragraph("Summary", heading_style))
    story.append(Paragraph(
        f"This video analysis detected oil spills in {stats.get('frames_with_detections', 0)} out of "
        f"{stats.get('total_frames', 0)} frames, with a total of {stats.get('total_detections', 0)} "
        f"detections across the entire video.",
        styles['Normal']
    ))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

