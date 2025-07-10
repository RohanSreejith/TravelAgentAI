import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models import ChatGroq
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

# ✅ Use API key from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize the agent (cached)
@st.cache_resource
def load_agent():
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="mixtral-8x7b-32768",  # Or "llama3-70b-8192"
        temperature=0,
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

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about travel packages..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    agent = load_agent()
    with st.spinner("Thinking..."):
        result = agent.invoke({"input": prompt})
        reply = result.get("output", "⚠️ No response received.")

    with st.chat_message("assistant"):
        st.markdown(reply, unsafe_allow_html=False)

    st.session_state.messages.append({"role": "assistant", "content": reply})

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
            with st.spinner("Creating package..."):
                result = agent.invoke({"input": f"Create a new package: {input_str}"})
                reply = result.get("output", "⚠️ No response received.")
            st.success("Package created!")
            st.info(reply)
