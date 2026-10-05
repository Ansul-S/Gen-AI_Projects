from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver



# LLM


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    streaming=True
)


# TOOL - Google Search


search = GoogleSerperAPIWrapper()

search_tool = Tool(
    name="google_search",
    description="Search the web for current or factual information.",
    func=search.run
)

tools = [search_tool]



# MEMORY


if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

if "history" not in st.session_state:
    st.session_state.history = []



# AGENT


agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt=(
        "You are a capable AI agent that can reason, use tools, "
        "and search the web to provide accurate answers."
    )
)



# WEB INTERFACE


st.subheader("⚡️ LightBot — Answer Before You Think ⚡️")


# ------------------------------------------------------------
# Display previous conversation
# ------------------------------------------------------------

for message in st.session_state.history:

    role = message["role"]
    content = message["content"]

    with st.chat_message(role):
        st.markdown(content)


# ------------------------------------------------------------
# User input
# ------------------------------------------------------------

query = st.chat_input("Ask Anything")


if query:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.markdown(query)


    # --------------------------------------------------------
    # Save user message
    # --------------------------------------------------------

    st.session_state.history.append({
        "role": "user",
        "content": query
    })


    # --------------------------------------------------------
    # Stream agent response
    # --------------------------------------------------------

    response = agent.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        },
        {
            "configurable": {
                "thread_id": "1"
            }
        },
        stream_mode="messages"
    )


    # --------------------------------------------------------
    # Display streaming response
    # --------------------------------------------------------

    message = ""

    with st.chat_message("assistant"):

        space = st.empty()

        for chunk, metadata in response:

            if chunk.content:

                message += chunk.content

                space.markdown(message)


    # --------------------------------------------------------
    # Save complete AI response
    # --------------------------------------------------------

    st.session_state.history.append({
        "role": "assistant",
        "content": message
    })