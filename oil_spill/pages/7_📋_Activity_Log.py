"""
Activity Log Page - View comprehensive activity tracking and records
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from utils.activity_logger import ActivityLogger
from io import BytesIO
import os

st.set_page_config(page_title="Activity Log", page_icon="📋", layout="wide")

st.title("📋 Activity Log & Records")
st.markdown("View comprehensive tracking of all app activities, inputs, outputs, and results")

# Initialize activity logger
if 'activity_logger' not in st.session_state:
    st.session_state.activity_logger = ActivityLogger()

logger = st.session_state.activity_logger

# Sidebar
with st.sidebar:
    st.header("📊 Log Options")
    show_stats = st.checkbox("Show Statistics", value=True)
    filter_action = st.selectbox(
        "Filter by Action Type",
        ["All", "Image Detection", "Video Detection", "Real-time Camera Detection", 
         "Comparison Mode", "Report Generation"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📁 Storage Info")
    if os.path.exists(logger.base_dir):
        total_size = sum(f.stat().st_size for f in logger.base_dir.rglob('*') if f.is_file())
        st.info(f"Total Size: {total_size / (1024*1024):.2f} MB")
        st.info(f"Location: {logger.base_dir.absolute()}")

# Main content
if os.path.exists(logger.excel_file):
    # Load log data
    try:
        df = pd.read_excel(logger.excel_file, engine='openpyxl')
        
        if len(df) > 0:
            # Filter by action type if selected
            if filter_action != "All":
                df = df[df['Action_Type'].str.contains(filter_action, na=False)]
            
            # Statistics
            if show_stats:
                st.subheader("📊 Activity Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Activities", len(df))
                with col2:
                    image_count = len(df[df['Action_Type'].str.contains('Image', na=False)])
                    st.metric("Image Detections", image_count)
                with col3:
                    video_count = len(df[df['Action_Type'].str.contains('Video', na=False)])
                    st.metric("Video Detections", video_count)
                with col4:
                    camera_count = len(df[df['Action_Type'].str.contains('Camera', na=False)])
                    st.metric("Camera Sessions", camera_count)
                
                st.markdown("---")
            
            # Activity timeline
            st.subheader("📈 Activity Timeline")
            
            # Group by date
            df['Date'] = pd.to_datetime(df['Date'])
            daily_activity = df.groupby(df['Date'].dt.date).size().reset_index(name='Count')
            
            import plotly.express as px
            fig = px.bar(
                daily_activity,
                x='Date',
                y='Count',
                title="Daily Activity Count",
                labels={'Date': 'Date', 'Count': 'Number of Activities'}
            )
            st.plotly_chart(fig, width='stretch')
            
            st.markdown("---")
            
            # Activity log table
            st.subheader("📋 Activity Log")
            
            # Sort by timestamp (newest first)
            df_sorted = df.sort_values('Timestamp', ascending=False)
            
            # Display table
            st.dataframe(
                df_sorted,
                use_container_width=True,
                height=400
            )
            
            # Action type distribution
            st.markdown("---")
            st.subheader("📊 Action Type Distribution")
            
            action_counts = df['Action_Type'].value_counts()
            fig2 = px.pie(
                values=action_counts.values,
                names=action_counts.index,
                title="Distribution of Activity Types"
            )
            st.plotly_chart(fig2, width='stretch')
            
            # Download options
            st.markdown("---")
            st.subheader("📥 Export Log")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download as Excel
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)
                st.download_button(
                    "📊 Download Excel Log",
                    excel_buffer.getvalue(),
                    file_name=f"activity_log_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                # Download as CSV
                csv_data = df.to_csv(index=False)
                st.download_button(
                    "📄 Download CSV Log",
                    csv_data,
                    file_name=f"activity_log_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # File browser
            st.markdown("---")
            st.subheader("📁 Stored Files")
            
            tab1, tab2, tab3 = st.tabs(["Input Files", "Output Files", "Reports"])
            
            with tab1:
                input_images = list((logger.input_dir / "images").glob("*"))
                input_videos = list((logger.input_dir / "videos").glob("*"))
                
                st.markdown("#### 📸 Input Images")
                if input_images:
                    for img_path in sorted(input_images, reverse=True)[:10]:
                        st.text(f"📷 {img_path.name} ({img_path.stat().st_size / 1024:.1f} KB)")
                else:
                    st.info("No input images stored yet.")
                
                st.markdown("#### 🎥 Input Videos")
                if input_videos:
                    for vid_path in sorted(input_videos, reverse=True)[:10]:
                        st.text(f"🎬 {vid_path.name} ({vid_path.stat().st_size / (1024*1024):.1f} MB)")
                else:
                    st.info("No input videos stored yet.")
            
            with tab2:
                output_images = list((logger.output_dir / "images").glob("*"))
                output_videos = list((logger.output_dir / "videos").glob("*"))
                
                st.markdown("#### 📸 Output Images")
                if output_images:
                    for img_path in sorted(output_images, reverse=True)[:10]:
                        st.text(f"📷 {img_path.name} ({img_path.stat().st_size / 1024:.1f} KB)")
                else:
                    st.info("No output images stored yet.")
                
                st.markdown("#### 🎥 Output Videos")
                if output_videos:
                    for vid_path in sorted(output_videos, reverse=True)[:10]:
                        st.text(f"🎬 {vid_path.name} ({vid_path.stat().st_size / (1024*1024):.1f} MB)")
                else:
                    st.info("No output videos stored yet.")
            
            with tab3:
                reports = list((logger.output_dir / "reports").glob("*"))
                if reports:
                    for report_path in sorted(reports, reverse=True)[:10]:
                        st.text(f"📄 {report_path.name} ({report_path.stat().st_size / 1024:.1f} KB)")
                else:
                    st.info("No reports stored yet.")
        
        else:
            st.info("📋 No activities logged yet. Start using the app to see activity records here!")
    
    except Exception as e:
        st.error(f"Error loading activity log: {str(e)}")
        st.info("The log file may be corrupted or in use. Please try again.")

else:
    st.info("📋 Activity log file not found. Start using the app to create activity records!")
    
    st.markdown("---")
    st.subheader("ℹ️ About Activity Logging")
    st.markdown("""
    The activity logger automatically tracks:
    - **All image detections** with input/output files
    - **All video detections** with processing results
    - **Camera sessions** with detection statistics
    - **Comparison operations** with results
    - **Report generations** with file locations
    
    All files are saved in the `information_record` folder with timestamps.
    """)

