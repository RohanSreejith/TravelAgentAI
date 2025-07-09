import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from tools import get_packages, create_package

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Travel Package Agent",
    page_icon="✈️",
    layout="wide"
)

# Initialize the agent (cached to avoid reloading)
@st.cache_resource
def load_agent():
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",  # Updated model name
            temperature=0,
            google_api_key=st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        )
        
        return initialize_agent(
            tools=[get_packages, create_package],
            llm=llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5  # Added to prevent infinite loops
        )
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return None

# Main UI
st.title("✈️ Travel Package Agent")
st.markdown("Ask about packages or create new ones")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you with travel packages today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about travel packages..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    agent = load_agent()
    if agent:
        with st.spinner("Thinking..."):
            try:
                response = agent.run(prompt)
            except Exception as e:
                response = f"Sorry, I encountered an error: {str(e)}"
    else:
        response = "Agent initialization failed. Please check the logs."
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar for package creation
with st.sidebar:
    st.header("📦 Create New Package")
    
    with st.form("package_form", clear_on_submit=True):
        title = st.text_input("Package Title*", placeholder="Bali Vacation")
        destination = st.text_input("Destination*", placeholder="Bali, Indonesia")
        days = st.number_input("Duration (days)*", min_value=1, value=7)
        price = st.number_input("Price ($)*", min_value=0, value=1500)
        description = st.text_area("Description", placeholder="A relaxing tropical getaway")
        
        submitted = st.form_submit_button("Create Package")
        if submitted:
            if not all([title, destination, days, price]):
                st.warning("Please fill all required fields (*)")
            else:
                input_str = f"{title}|{destination}|{days}|{price}|{description}"
                agent = load_agent()
                if agent:
                    with st.spinner("Creating package..."):
                        try:
                            result = agent.run(f"Create a new package: {input_str}")
                            st.success("Package created successfully!")
                            st.info(result)
                            # Auto-refresh chat to show new package
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to create package: {str(e)}")
                else:
                    st.error("Agent not available. Cannot create package.")

# Add footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Note:** All package data is managed through our secure API")
