# pages/dashboard.py - WITH VISUALIZATIONS (Method 1)

import streamlit as st
import pandas as pd

# Check authentication
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Please login first!")
    st.stop()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Dashboard", layout="wide")

# --- Load datasets ---
@st.cache_data
def load_data():
    tickets_df = pd.read_csv("DATA/it_tickets.csv")
    cyber_df = pd.read_csv("DATA/cyber_incidents.csv")
    metadata_df = pd.read_csv("DATA/datasets_metadata.csv")
    return tickets_df, cyber_df, metadata_df

tickets_df, cyber_df, metadata_df = load_data()

# --- Sidebar Navigation ---
with st.sidebar:
    st.header("📊 Data Dashboard")
    st.write(f"👤 **{st.session_state.username}**")
    
    page = st.radio(
        "Navigate to:",
        ["Dashboard Overview", "IT Tickets", "Cyber Incidents", "Metadata", "Analytics"]
    )
    
    if st.button("🏠 Home"):
        st.switch_page("home.py")
    
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

# --- Main Content ---
if page == "Dashboard Overview":
    st.title("📈 Dashboard Overview")
    
    # Metrics cards WITHOUT percentage trends
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("IT Tickets", len(tickets_df))  # Removed: , "+5%"
    with col2:
        st.metric("Cyber Incidents", len(cyber_df))  # Removed: , "-2%"
    with col3:
        st.metric("Datasets", len(metadata_df))
    
    st.divider()
    
    # Quick previews with charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 IT Tickets Status")
        if 'status' in tickets_df.columns:
            status_counts = tickets_df['status'].value_counts()
            st.bar_chart(status_counts)
        st.dataframe(tickets_df.head(3), use_container_width=True)
    
    with col2:
        st.subheader("🛡️ Cyber Severity")
        if 'severity' in cyber_df.columns:
            severity_counts = cyber_df['severity'].value_counts()
            st.line_chart(severity_counts)
        st.dataframe(cyber_df.head(3), use_container_width=True)

elif page == "IT Tickets":
    st.title("📋 IT Tickets Analysis")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        if 'status' in tickets_df.columns:
            selected_status = st.multiselect(
                "Filter by Status",
                options=tickets_df['status'].unique(),
                default=tickets_df['status'].unique()
            )
    
    with col2:
        if 'priority' in tickets_df.columns:
            selected_priority = st.multiselect(
                "Filter by Priority",
                options=tickets_df['priority'].unique(),
                default=tickets_df['priority'].unique()
            )
    
    # Apply filters
    filtered_df = tickets_df.copy()
    if 'status' in tickets_df.columns and selected_status:
        filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]
    if 'priority' in tickets_df.columns and selected_priority:
        filtered_df = filtered_df[filtered_df['priority'].isin(selected_priority)]
    
    # Show filtered data
    st.dataframe(filtered_df, use_container_width=True)
    
    # Visualizations
    st.subheader("📊 Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'status' in filtered_df.columns:
            st.write("**Status Distribution**")
            status_data = filtered_df['status'].value_counts()
            st.bar_chart(status_data)
    
    with col2:
        if 'priority' in filtered_df.columns:
            st.write("**Priority Distribution**")
            priority_data = filtered_df['priority'].value_counts()
            st.area_chart(priority_data)
    
    # Time-based chart if date column exists
    if 'created_at' in filtered_df.columns:
        try:
            st.write("**Tickets Over Time**")
            # Convert to datetime and group by date
            filtered_df['date'] = pd.to_datetime(filtered_df['created_at']).dt.date
            daily_counts = filtered_df.groupby('date').size()
            st.line_chart(daily_counts)
        except:
            pass

elif page == "Cyber Incidents":
    st.title("🛡️ Cyber Incidents Analysis")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Data", "Charts", "Statistics"])
    
    with tab1:
        st.dataframe(cyber_df, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'severity' in cyber_df.columns:
                st.write("**Severity Levels**")
                severity_counts = cyber_df['severity'].value_counts()
                st.bar_chart(severity_counts)
        
        with col2:
            if 'category' in cyber_df.columns:
                st.write("**Incident Categories**")
                category_counts = cyber_df['category'].value_counts()
                st.line_chart(category_counts)
        
        # Pie chart simulation (Streamlit doesn't have native pie, so we use bar)
        if 'status' in cyber_df.columns:
            st.write("**Incident Status**")
            status_counts = cyber_df['status'].value_counts()
            st.bar_chart(status_counts)
    
    with tab3:
        st.subheader("Dataset Statistics")
        st.write(f"**Total Incidents:** {len(cyber_df)}")
        if not cyber_df.empty:
            st.write(f"**Date Range:** {cyber_df['timestamp'].min()} to {cyber_df['timestamp'].max()}")
        
        # Show numeric statistics
        st.write("**Numeric Columns Summary:**")
        numeric_cols = cyber_df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            st.dataframe(cyber_df[numeric_cols].describe())

elif page == "Metadata":
    st.title("📁 Datasets Metadata")
    
    st.dataframe(metadata_df, use_container_width=True)
    
    # Show each dataset info in expanders
    for idx, row in metadata_df.iterrows():
        with st.expander(f"📄 Dataset: {row.get('name', f'Dataset {idx+1}')}"):
            for col in metadata_df.columns:
                st.write(f"**{col}:** {row[col]}")

elif page == "Analytics":
    st.title("📈 Advanced Analytics")
    
    # Comparison between datasets
    st.subheader("Dataset Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**IT Tickets Summary**")
        if not tickets_df.empty:
            st.metric("Total Tickets", len(tickets_df))
            if 'status' in tickets_df.columns:
                open_tickets = (tickets_df['status'] == 'Open').sum() if 'Open' in tickets_df['status'].values else 0
                st.metric("Open Tickets", open_tickets)
    
    with col2:
        st.write("**Cyber Incidents Summary**")
        if not cyber_df.empty:
            st.metric("Total Incidents", len(cyber_df))
            if 'severity' in cyber_df.columns:
                high_severity = (cyber_df['severity'] == 'High').sum() if 'High' in cyber_df['severity'].values else 0
                st.metric("High Severity", high_severity)
    
    st.divider()
    
    # Data quality metrics
    st.subheader("Data Quality Check")
    
    quality_col1, quality_col2, quality_col3 = st.columns(3)
    
    with quality_col1:
        st.metric("IT Tickets Completeness", 
                 f"{tickets_df.notnull().mean().mean()*100:.1f}%")
    
    with quality_col2:
        st.metric("Cyber Data Completeness", 
                 f"{cyber_df.notnull().mean().mean()*100:.1f}%")
    
    with quality_col3:
        st.metric("Total Records", 
                 f"{len(tickets_df) + len(cyber_df)}")

# Footer
st.divider()
st.caption(f"User: {st.session_state.username} | Data loaded: {len(tickets_df) + len(cyber_df)} records")