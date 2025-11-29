import streamlit as st
import pandas as pd
import time
from pathlib import Path

file_path = 'DATA\\it_tickets.csv'
tickets_df = pd.read_csv(file_path)
cyber_incidents_df = pd.read_csv(file_path)


st.set_page_config(
    page_title= "home page",
    layout = "wide",
    page_icon = "😵‍💫"
)

st.title("Welcome to the Streamlit App!!!!")
st.write("welcome to home page")


with st.sidebar:
    st.header("Controls")
    option = st.selectbox(
    "Choose",
    ["IT", "CYBER", "METADATA"]
)
    
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tickets")
    st.dataframe(tickets_df)

#make seperate pages and link from side bar 
with col2:
    st.subheader("cyber")
    st.dataframe(cyber_incidents_df)





