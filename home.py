# home.py - Login and home page once logged in a user can see the page , if not logged in they see nothing
import streamlit as st
from main import login_user, hash_password
from main import hash_password, DB_PATH
import sqlite3

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Home", layout="wide", page_icon="😵‍💫")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = "user"

# --- AUTHENTICATION CHECK ---
if not st.session_state.authenticated:
    st.title("🔐 Login Required")
    
    col1, col2 = st.columns([1, 2])
    
    # Login Section
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
    
    # Registration Section
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
                # Registration function
                
                
                if not reg_username or not reg_password:
                    st.error("Username and password are required")
                else:
                    hashed = hash_password(reg_password)
                    
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                            (reg_username, hashed)
                        )
                        conn.commit()
                        st.success("✅ Registration successful! You can now login.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("❌ Username already exists")
                    except Exception as e:
                        st.error(f"Database error: {e}")
                    finally:
                        conn.close()
    
    st.stop()

# --- Welcome Page for Authenticated Users ---
st.title(f"Welcome, {st.session_state.username}! 👋")
st.write("This is the home page.")

# Button to go to dashboard
if st.button("Go to Dashboard"):
    st.switch_page("pages/dashboard.py")

# Logout button in sidebar
with st.sidebar:
    st.write(f"👤 **{st.session_state.username}**")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()