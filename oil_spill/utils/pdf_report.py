"""
PDF report generation utilities
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import List, Dict
import io
from PIL import Image as PILImage
import numpy as np

def generate_pdf_report(detections: List[Dict], stats: Dict, 
                       image_info: Dict = None, 
                       annotated_image: np.ndarray = None) -> bytes:
    """
    Generate a PDF report of detection results
    
    Args:
        detections: List of detection dictionaries
        stats: Statistics dictionary
        image_info: Image metadata dictionary
        annotated_image: Annotated image array (optional)
        
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
    
    # Title
    story.append(Paragraph("Oil Spill Detection Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Date
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                         styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Image information
    if image_info:
        story.append(Paragraph("Image Information", heading_style))
        info_data = [[key, str(value)] for key, value in image_info.items()]
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
    
    # Statistics
    story.append(Paragraph("Detection Statistics", heading_style))
    stats_data = [
        ["Metric", "Value"],
        ["Total Detections", str(stats.get("total_detections", 0))],
        ["Average Confidence", f"{stats.get('avg_confidence', 0):.2%}"],
        ["Max Confidence", f"{stats.get('max_confidence', 0):.2%}"],
        ["Min Confidence", f"{stats.get('min_confidence', 0):.2%}"]
    ]
    
    if 'coverage_percentage' in stats:
        stats_data.append(["Coverage Percentage", f"{stats['coverage_percentage']:.2f}%"])
        stats_data.append(["Total Spill Area", f"{stats.get('total_spill_area', 0):.2f} pixels"])
    
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
    
    # Detections
    if detections:
        story.append(Paragraph("Detection Details", heading_style))
        det_data = [["#", "Class", "Confidence", "Area", "Bounding Box"]]
        for i, det in enumerate(detections, 1):
            bbox = det.get('bbox', [0, 0, 0, 0])
            det_data.append([
                str(i),
                det.get('class_name', 'Unknown'),
                f"{det.get('confidence', 0):.2%}",
                f"{det.get('area', 0):.2f}",
                f"[{bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f}]"
            ])
        
        det_table = Table(det_data, colWidths=[0.5*inch, 1.5*inch, 1*inch, 1*inch, 2*inch])
        det_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(det_table)
    else:
        story.append(Paragraph("No detections found.", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

