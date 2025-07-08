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
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    return initialize_agent(
        tools=[get_packages, create_package],
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

# Main UI
st.title("✈️ Travel Package Agent")
st.markdown("Ask about packages or create new ones")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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
    with st.spinner("Thinking..."):
        response = agent.run(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar for package creation
with st.sidebar:
    st.header("📦 Create New Package")
    
    with st.form("package_form"):
        title = st.text_input("Package Title")
        destination = st.text_input("Destination")
        days = st.number_input("Duration (days)", min_value=1)
        price = st.number_input("Price ($)", min_value=0)
        description = st.text_area("Description")
        
        submitted = st.form_submit_button("Create Package")
        if submitted:
            input_str = f"{title}|{destination}|{days}|{price}|{description}"
            agent = load_agent()
            result = agent.run(f"Create a new package: {input_str}")
            st.success("Package created!")
            st.info(result)