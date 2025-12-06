# 📋 Activity Logging & Tracking Feature

## Overview
A comprehensive activity logging system that tracks all app usage, saves all input/output files, and maintains detailed Excel records.

## Features

### 1. **Automatic File Storage**
- **Input Files**: All uploaded images and videos are saved with timestamps
- **Output Files**: All processed images, videos, and reports are saved
- **Organized Structure**: Files organized in `information_record/` folder:
  ```
  information_record/
  ├── inputs/
  │   ├── images/
  │   └── videos/
  ├── outputs/
  │   ├── images/
  │   ├── videos/
  │   └── reports/
  └── activity_log.xlsx
  ```

### 2. **Excel Activity Log**
Comprehensive Excel file (`activity_log.xlsx`) tracks:
- **Date, Time, Day**: When each action occurred
- **Action Type**: What type of action (Image Detection, Video Detection, etc.)
- **Input File**: Path to original input file
- **Output File**: Path to generated output file
- **Original Filename**: Original file name
- **Detection Results**: Number of detections, confidence scores
- **Statistics**: Complete statistics in JSON format
- **Detection Details**: Full detection information
- **Timestamp**: Complete datetime stamp

### 3. **Tracked Activities**

#### Image Detection
- Input image saved
- Output annotated image saved
- Detection count, confidence, coverage logged
- All detection details recorded

#### Video Detection
- Input video saved
- Output annotated video saved
- Frame-by-frame statistics logged
- Total detections and frame counts recorded

#### Real-time Camera
- Camera sessions logged
- Detection statistics recorded
- Frame counts tracked

#### Comparison Mode
- Comparison type logged
- Files used recorded
- Comparison results saved

#### Report Generation
- Report type tracked
- Report files saved
- Associated actions linked

### 4. **Activity Log Viewer Page**
New page (`📋 Activity Log`) provides:
- **Statistics Dashboard**: Overview of all activities
- **Activity Timeline**: Visual chart of daily activity
- **Filtered View**: Filter by action type
- **File Browser**: View all stored files
- **Export Options**: Download log as Excel or CSV
- **Action Distribution**: Pie chart of activity types

## Usage

### Automatic Logging
All activities are automatically logged - no user action required!

### Viewing Logs
1. Navigate to **📋 Activity Log** page
2. View statistics and timeline
3. Browse activity log table
4. Filter by action type
5. Export logs for analysis

### File Access
All files are saved in `information_record/` folder:
- Input files: `information_record/inputs/`
- Output files: `information_record/outputs/`
- Excel log: `information_record/activity_log.xlsx`

## Excel Log Columns

| Column | Description |
|--------|-------------|
| Date | Date of activity (YYYY-MM-DD) |
| Time | Time of activity (HH:MM:SS) |
| Day | Day of week |
| Action_Type | Type of action performed |
| Input_File | Path to input file |
| Output_File | Path to output file |
| Original_Filename | Original filename |
| Total_Detections | Number of detections |
| Avg_Confidence | Average confidence score |
| Coverage_Percentage | Spill coverage percentage |
| Detection_Details | JSON string of detection details |
| Statistics | JSON string of all statistics |
| Timestamp | Complete datetime |

## Benefits

1. **Complete Audit Trail**: Every action is recorded
2. **File Management**: All files organized and timestamped
3. **Analytics**: Track usage patterns and model performance
4. **Compliance**: Maintain records for documentation
5. **Debugging**: Review past activities for troubleshooting
6. **Research**: Analyze detection patterns over time

## Technical Details

### Dependencies
- `pandas`: For Excel file handling
- `openpyxl`: For Excel file creation/reading
- `pathlib`: For file path management

### File Naming
Files are saved with timestamps:
- Format: `YYYYMMDD_HHMMSS_originalname.ext`
- Example: `20241130_143025_image.jpg`

### Excel Updates
- Excel file is updated in real-time
- New entries appended to existing log
- No data loss on app restart

## Privacy & Security

- All files stored locally in `information_record/` folder
- No external data transmission
- User has full control over stored data
- Can delete folder to clear all records

---

**This feature provides complete transparency and tracking of all app activities! 📋✨**

