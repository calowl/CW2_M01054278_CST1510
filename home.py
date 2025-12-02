# Importing authentication function

import sqlite3
import streamlit as st
import pandas as pd
from main import login_user, hash_password 

# --- Registration function ---
def register_user_direct(username: str, password: str) -> bool:
    """Register a new user directly in the database."""
    import sqlite3
    from main import hash_password, DB_PATH
    
    if not username or not password:
        return False
    
    hashed = hash_password(password)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        st.error(f"Database error: {e}")
        return False
    finally:
        conn.close()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Home", layout="wide", page_icon="😵‍💫")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = "user"

# --- AUTHENTICATION CHECK (before loading data) ---
if not st.session_state.authenticated:
    st.title("🔐 Login Required")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            if login_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with col2:
        st.subheader("Register")
        reg_username = st.text_input("New Username", key="reg_user")
        reg_password = st.text_input("New Password", type="password", key="reg_pass")
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register"):
            if not reg_username or not reg_password:
                st.error("Username and password are required")
            elif reg_password != reg_confirm:
                st.error("Passwords do not match")
            elif len(reg_password) < 4:
                st.error("Password must be at least 4 characters")
            else:
                # Register the user directly
                success = register_user_direct(reg_username, reg_password)
                if success:
                    st.success("✅ Registration successful! You can now login.")
                    st.rerun()
                else:
                    st.error("❌ Username already exists or registration failed")
    
    st.stop()  # Stop execution here - don't load dashboard

# --- Dashboard content for authenticated users ---
# --- Load datasets ---
tickets_df = pd.read_csv("DATA/it_tickets.csv")
cyber_df = pd.read_csv("DATA/cyber_incidents.csv")
metadata_df = pd.read_csv("DATA/datasets_metadata.csv")

# --- Modify sidebar to show user info ---
with st.sidebar:
    st.header("Navigation")
    st.write(f"👤 **{st.session_state.username}**")
    
    if st.button("Home"):
        st.session_state.page = "Home"
    if st.button("IT"):
        st.session_state.page = "IT"
    if st.button("Cyber"):
        st.session_state.page = "Cyber"
    if st.button("Metadata"):
        st.session_state.page = "Metadata"
    
    # the Logout button
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

# --- Page Content ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

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

