import streamlit as st
from config import TITLE, DESCRIPTION, PAGE_ICON, TREE_PATH  # Import first

# ✅ Move set_page_config as the first Streamlit command
st.set_page_config(page_title=TITLE, page_icon=PAGE_ICON)

import os
from dotenv import load_dotenv
from chatbot import ChatbotBackend
from styles import load_css
from ui_components import display_message, display_chat_history

# ✅ Access secrets AFTER set_page_config
# Hide API key from being displayed
os.environ["GOOGLE_API_KEY"] = st.secrets["google"]["GOOGLE_API_KEY"]

def initialize_session_state():
    """Initialize session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotBackend(TREE_PATH)
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_node_id' not in st.session_state:
        st.session_state.current_node_id = None
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'interview_completed' not in st.session_state:
        st.session_state.interview_completed = False

def start_conversation():
    """Start a new conversation"""
    st.session_state.history = []
    st.session_state.conversation_started = True
    st.session_state.interview_completed = False
    
    # Get the root node
    root_node = st.session_state.chatbot.find_root_node()
    if not root_node:
        st.error("No root node found in the tree")
        return
    
    st.session_state.current_node_id = root_node["nodeId"]
    
    # Generate the initial response
    ai_prompt = st.session_state.chatbot.generate_response(root_node["prompt"], st.session_state.history)
    
    # Update history
    display_message("AI", ai_prompt)
    
    st.rerun()

def process_input(user_input):
    """Process user input and generate response"""
    if not user_input or not st.session_state.conversation_started:
        return
    
    # Get current node
    current_node_id = st.session_state.current_node_id
    current_node = st.session_state.chatbot.get_node_by_id(current_node_id)
    
    # Add user message to history
    display_message("User", user_input)
    
    # Show a spinner while processing
    with st.spinner("Monika is thinking..."):
        # Determine the next node
        next_node_id = None
        for edge in current_node.get("edges", []):
            if st.session_state.chatbot.evaluate_condition(current_node["prompt"], user_input, edge["condition"]):
                next_node_id = edge["targetNodeId"]
                break
        
        # If no condition matched
        if not next_node_id:
            clarification_message = "I'm sorry, I didn't understand. Could you please clarify?"
            display_message("AI", clarification_message)
            st.rerun()
            return
        
        # Get the next node
        next_node = st.session_state.chatbot.get_node_by_id(next_node_id)
        st.session_state.current_node_id = next_node_id
        
        # Generate AI response
        ai_message = st.session_state.chatbot.generate_response(next_node["prompt"], st.session_state.history)
        display_message("AI", ai_message)
        
        # Check if this is a terminal node
        if next_node_id in ["node6", "node7", "node8"]:
            st.session_state.interview_completed = True
            display_message("AI", "Thank you for completing the interview. The session has ended.")
    
    # Clear the input box and rerun
    if "user_input" in st.session_state:
        del st.session_state.user_input
    st.rerun()

def reset_conversation():
    """Reset the conversation"""
    st.session_state.history = []
    st.session_state.current_node_id = None
    st.session_state.conversation_started = False
    st.session_state.interview_completed = False
    st.rerun()

def main():
    """Main application function"""
    # Load and apply CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title(TITLE)
    st.markdown(DESCRIPTION)
    
    # Display chat messages
    for message in st.session_state.history:
        if "User" in message:
            with st.container():
                st.markdown(f"""
                <div class="chat-message user">
                    <div>
                        <b>You:</b>
                        <span class="chat-message-content">{message["User"]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown(f"""
                <div class="chat-message bot">
                    <div>
                        <b>Monika:</b>
                        <span class="chat-message-content">{message["AI"]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Input and buttons
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Your response:", 
            disabled=not st.session_state.conversation_started or st.session_state.interview_completed, 
            key="user_input"
        )
    
    with col2:
        if not st.session_state.conversation_started:
            if st.button("Start Interview", type="primary"):
                start_conversation()
        else:
            if not st.session_state.interview_completed:
                if st.button("Send", type="primary"):
                    process_input(user_input)
    
    # Reset button at the bottom
    if st.session_state.conversation_started:
        if st.button("Reset Interview"):
            reset_conversation()

if __name__ == "__main__":
    main()
