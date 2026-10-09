from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)


# Streamlit UI
st.title("Answers Of Your Questions 😀")
st.markdown("My QnA Bot with LangChain and Google Gemini!")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]

    st.chat_message(role).markdown(content)


# User input
query = st.chat_input("Ask Anything?")


if query:

    # Display user message
    st.chat_message("user").markdown(query)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Get Gemini response
    res = llm.invoke(query)

    # Extract only the actual text (works whether content is a string or a list of blocks)
    answer = res.text

    # Display AI response
    st.chat_message("ai").markdown(answer)

    # Save AI response
    st.session_state.messages.append({
        "role": "ai",
        "content": answer
    })