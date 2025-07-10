import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from tools import get_packages, create_package
import streamlit as st

GOOGLE_API_KEY = st.secrets["general"]["GOOGLE_API_KEY"]


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0,
    google_api_key = st.secrets["GOOGLE_API_KEY"]

)

agent = initialize_agent(
    tools=[get_packages, create_package],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

#print(agent.run("Show me my travel packages"))