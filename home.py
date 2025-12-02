import streamlit as st
import pandas as pd

# --- Load Data ---
tickets_df = pd.read_csv("DATA/it_tickets.csv")
cyber_df = pd.read_csv("DATA/cyber_incidents.csv") 
metadata_df = pd.read_csv("DATA/datasets_metadata.csv")  

# --- Page Config ---
st.set_page_config(page_title="Home", layout="wide", page_icon="😵‍💫")

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Sidebar Buttons ---
with st.sidebar:
    st.header("Navigation")
    if st.button("Home"):
        st.session_state.page = "Home"
    if st.button("IT"):
        st.session_state.page = "IT"
    if st.button("Cyber"):
        st.session_state.page = "Cyber"
    if st.button("Metadata"):
        st.session_state.page = "Metadata"

# --- Page Content ---
if st.session_state.page == "Home":
    st.title("Welcome to the Streamlit App!")
    st.write("Welcome to the homepage.")
elif st.session_state.page == "IT":
    st.title("IT Tickets")
    st.dataframe(tickets_df)
elif st.session_state.page == "Cyber":
    st.title("Cyber Incidents")
    st.dataframe(cyber_df)
elif st.session_state.page == "Metadata":
    st.title("Metadata")
    st.dataframe(metadata_df)
