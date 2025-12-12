import streamlit as st
from google import genai
import re
import time
import random
from streamlit.components.v1 import html

# Custom CSS for animations
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    .typing-animation {
        overflow: hidden;
        white-space: nowrap;
        animation: typing 2s steps(40, end), blink .75s step-end infinite;
    }
    
    .ai-thinking {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }
    
    .thinking-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: white;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .thinking-dot:nth-child(1) { animation-delay: -0.32s; }
    .thinking-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    .message-container {
        margin: 15px 0;
        padding: 15px;
        border-radius: 15px;
        background: #f0f2f6;
        transition: all 0.3s ease;
    }
    
    .message-container:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    
    .ai-message {
        background: white;
        margin-right: 20%;
        border-left: 4px solid #764ba2;
    }
    
    .send-button {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Mini AI Helper")

# Load API key from secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Store chat messages in session state
if "mini_chat" not in st.session_state:
    st.session_state.mini_chat = []

# Store typing animation state
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

# Sidebar for chat history
st.sidebar.title("📜 Chat History")

# Display previous messages in sidebar
for role, msg in st.session_state.mini_chat:
    st.sidebar.markdown(f"""
    <div class="fade-in">
        <div class="message-container {'user-message' if role == 'You' else 'ai-message'}">
            <strong>{role}:</strong><br>
            {msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Clear chat button in sidebar
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.mini_chat = []
    st.rerun()

# Main content area
st.markdown("---")

# Create a centered layout
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Display the last AI response with animation
    if st.session_state.mini_chat and st.session_state.mini_chat[-1][0] == "AI":
        latest_ai_response = st.session_state.mini_chat[-1][1]
        st.markdown(f"""
        <div class="fade-in">
            <div class="message-container ai-message">
                <strong>🤖 AI:</strong><br>
                {latest_ai_response}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI Thinking animation placeholder
    thinking_placeholder = st.empty()
    
    # Animated typing input
    st.markdown("### ✍️ Type your message below:")
    
    user_msg = st.text_area(
        "Your message",
        height=120,
        label_visibility="collapsed",
        placeholder="Type your message here... ✨ (Maximum 4 sentences)",
        key="user_input"
    )
    
    # Sentence limit checker
    def sentence_count(text):
        return len(re.split(r'[.!?]+', text)) - 1
    
    # Buttons with animations
    col_left, col_mid, col_right = st.columns([1, 2, 1])
    
    with col_mid:
        if st.button("🚀 Send Message", type="primary", use_container_width=True, key="send_btn"):
            if not user_msg.strip():
                st.warning("⚠️ Please type something.")
            elif sentence_count(user_msg) > 4:
                st.error("❌ Please keep your message under 4 sentences.")
            else:
                # Add user message with animation
                st.session_state.mini_chat.append(("You", user_msg))
                
                # Show thinking animation
                with thinking_placeholder.container():
                    st.markdown("""
                    <div class="ai-thinking">
                        <strong>AI is thinking...</strong>
                        <div class="thinking-dot"></div>
                        <div class="thinking-dot"></div>
                        <div class="thinking-dot"></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Simulate thinking time with random delay
                time.sleep(random.uniform(0.5, 1.5))
                
                # Query Google AI model
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=user_msg
                )
                
                ai_reply = response.text or "Sorry, I couldn't generate a response."
                
                # Simulate typing effect
                st.session_state.is_typing = True
                
                # Clear thinking animation
                thinking_placeholder.empty()
                
                # Show typing animation
                typing_placeholder = st.empty()
                typed_text = ""
                
                for char in ai_reply:
                    typed_text += char
                    typing_placeholder.markdown(f"""
                    <div class="ai-thinking">
                        <div class="typing-animation">
                            {typed_text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.01)  # Adjust typing speed here
                
                # Add final AI message
                st.session_state.mini_chat.append(("AI", ai_reply))
                st.session_state.is_typing = False
                
                # JavaScript to scroll to bottom and trigger rerun
                html_string = """
                <script>
                window.scrollTo(0, document.body.scrollHeight);
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
                </script>
                """
                html(html_string)
        
        if st.button("🔄 Refresh View", use_container_width=True, key="refresh_btn"):
            st.rerun()

# Add a footer with animated emoji
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h3 style="animation: pulse 2s infinite;">✨ AI Assistant Ready! ✨</h3>
    </div>
    """, unsafe_allow_html=True)

# Display a fun fact in sidebar with animation
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="fade-in">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 15px; 
                border-radius: 10px;
                text-align: center;">
        <h4>💡 Did you know?</h4>
        <p>Each AI response is generated uniquely in real-time! ✨</p>
    </div>
</div>
""", unsafe_allow_html=True)