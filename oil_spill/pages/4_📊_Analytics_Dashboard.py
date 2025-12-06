"""
Analytics Dashboard Page - Comprehensive analytics and insights
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

st.title("📊 Analytics Dashboard")
st.markdown("Comprehensive analytics and insights for oil spill detection")

# Initialize session state for analytics
if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []

# Sidebar
with st.sidebar:
    st.header("📈 Analytics Options")
    show_demo = st.checkbox("Show Demo Data", value=True)
    clear_history = st.button("Clear History", type="secondary")
    
    if clear_history:
        st.session_state.detection_history = []
        st.success("History cleared!")

# Demo data
if show_demo and len(st.session_state.detection_history) == 0:
    demo_data = [
        {"timestamp": "2024-01-15 10:00", "detections": 3, "avg_confidence": 0.85, "type": "Image"},
        {"timestamp": "2024-01-15 11:30", "detections": 5, "avg_confidence": 0.92, "type": "Image"},
        {"timestamp": "2024-01-15 14:20", "detections": 2, "avg_confidence": 0.78, "type": "Video"},
        {"timestamp": "2024-01-15 16:45", "detections": 0, "avg_confidence": 0.0, "type": "Image"},
        {"timestamp": "2024-01-16 09:15", "detections": 7, "avg_confidence": 0.88, "type": "Video"},
        {"timestamp": "2024-01-16 12:30", "detections": 4, "avg_confidence": 0.91, "type": "Image"},
    ]
    st.session_state.detection_history = demo_data

if st.session_state.detection_history:
    df = pd.DataFrame(st.session_state.detection_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Overview metrics
    st.subheader("📊 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Scans", len(df))
    with col2:
        st.metric("Total Detections", df['detections'].sum())
    with col3:
        avg_conf = df[df['detections'] > 0]['avg_confidence'].mean()
        st.metric("Avg Confidence", f"{avg_conf:.2%}" if not pd.isna(avg_conf) else "N/A")
    with col4:
        detection_rate = (df['detections'] > 0).sum() / len(df) * 100
        st.metric("Detection Rate", f"{detection_rate:.1f}%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Detection Timeline")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['detections'],
            mode='lines+markers',
            name='Detections',
            line=dict(color='#ff7f0e', width=2),
            marker=dict(size=8)
        ))
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Number of Detections",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("📊 Detection Distribution")
        fig = px.histogram(
            df,
            x='detections',
            nbins=20,
            title="Distribution of Detection Counts",
            labels={'detections': 'Number of Detections', 'count': 'Frequency'}
        )
        fig.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig, width='stretch')
    
    # Confidence analysis
    st.subheader("🎯 Confidence Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        confidence_df = df[df['detections'] > 0]
        if len(confidence_df) > 0:
            fig = px.box(
                confidence_df,
                y='avg_confidence',
                title="Confidence Score Distribution",
                labels={'avg_confidence': 'Average Confidence'}
            )
            fig.update_layout(template="plotly_white", height=300)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No detections to analyze")
    
    with col2:
        if 'type' in df.columns:
            type_counts = df['type'].value_counts()
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title="Detection by Source Type"
            )
            fig.update_layout(template="plotly_white", height=300)
            st.plotly_chart(fig, width='stretch')
    
    # Data table
    st.markdown("---")
    st.subheader("📋 Detection History")
    st.dataframe(df, width='stretch')
    
    # Export options
    st.markdown("---")
    st.subheader("📥 Export Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        json_data = df.to_json(orient='records', date_format='iso')
        st.download_button(
            "Download JSON",
            json_data,
            file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

else:
    st.info("📊 No analytics data available. Start detecting oil spills to see analytics here!")
    
    st.markdown("---")
    st.subheader("ℹ️ About Analytics")
    st.markdown("""
    The Analytics Dashboard provides:
    - **Overview Metrics**: Key statistics at a glance
    - **Timeline Analysis**: Detection trends over time
    - **Distribution Charts**: Understanding detection patterns
    - **Confidence Analysis**: Quality metrics for detections
    - **Export Options**: Download data for further analysis
    """)

