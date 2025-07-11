import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from tools import get_packages, create_package
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Travel Package Agent", page_icon="✈️", layout="wide")

# Use API key from secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

@st.cache_resource
def load_agent():
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",
        temperature=0,
    )
    return initialize_agent(
        tools=[get_packages, create_package],
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=False
    )

# UI
st.title("✈️ Travel Package Agent")
st.markdown("Ask about packages or create new ones")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("is_html", False):
            components.html(msg["content"], height=800, scrolling=True)
        else:
            st.markdown(f"<div style='color:white'>{msg['content']}</div>", unsafe_allow_html=True)

# Input
if prompt := st.chat_input("Ask about travel packages..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    agent = load_agent()
    with st.spinner("Thinking..."):
        try:
            result = agent.invoke({"input": prompt})
            reply = result.get("output", "⚠️ No response.")
        except Exception as e:
            reply = f"❌ Error: {e}"

    with st.chat_message("assistant"):
        # If it's package HTML, use components.html
        if "<div" in reply and "</div>" in reply:
            styled_reply = f"""
            <div style='color: white; background-color: #222; padding: 20px; border-radius: 10px; font-family: Arial, sans-serif;'>
                {reply}
            </div>
            """
            components.html(styled_reply, height=800, scrolling=True)
            st.session_state.messages.append({
                "role": "assistant",
                "content": styled_reply,
                "is_html": True
            })
        else:
            st.markdown(f"<div style='color:white'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply,
                "is_html": False
            })

# Sidebar: Create new package
with st.sidebar:
    st.header("📦 Create New Package")
    with st.form("package_form"):
        title = st.text_input("Title")
        destination = st.text_input("Destination")
        days = st.number_input("Duration (days)", min_value=1)
        price = st.number_input("Price ($)", min_value=0.0)
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create Package")
        if submitted:
            input_str = f"{title} | {destination} | {int(days)} | {float(price)} | {description}"
            agent = load_agent()
            with st.spinner("Creating package..."):
                result = agent.invoke({"input": f"Create a new package: {input_str}"})
                reply = result.get("output", "⚠️ No response.")
            st.success("Package created!")
            st.info(reply)
