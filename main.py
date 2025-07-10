import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models import ChatGroq
from langchain.agents import initialize_agent, AgentType
from tools import get_packages, create_package

# Load env vars and secrets
load_dotenv()

# Use GROQ API key from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize the Groq LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="mixtral-8x7b-32768",  # or "llama3-70b-8192", etc.
    temperature=0
)

# Initialize agent with tools
agent = initialize_agent(
    tools=[get_packages, create_package],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
