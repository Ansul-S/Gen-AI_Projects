
import os
import shutil
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()

# -------------------- Configuration --------------------

DOC_DIR = Path("./doc_files")
THREAD_ID = "pdf-chat"

# -------------------- Session State --------------------

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- Document Processing --------------------

def process_document(path: Path):
    """Load PDFs, split them into chunks, embed them, and create an agent."""

    # Load PDFs
    loader = PyPDFDirectoryLoader(str(path))
    documents = loader.load()

    if not documents:
        raise ValueError(
            "No readable PDF content found. Please upload valid PDFs."
        )

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No text chunks could be extracted from the PDFs.")

    # Embeddings and vector store
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    vector_store = InMemoryVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    # LLM
    llm = ChatGroq(model="openai/gpt-oss-20b")

    # Retrieval tool
    @tool
    def retrieve_context(query: str) -> str:
        """Retrieve relevant passages from the uploaded PDF knowledge base."""

        relevant_docs = vector_store.similarity_search(
            query=query,
            k=3,
        )

        if not relevant_docs:
            return "No relevant information was found in the documents."

        # FIX: Accumulate all retrieved passages instead of overwriting them.
        context = "\n\n---\n\n".join(
            doc.page_content for doc in relevant_docs
        )

        return context

    system_prompt = """
    You are a helpful PDF question-answering assistant.

    Use the retrieve_context tool for questions that require information
    from the uploaded documents.

    Base document-specific answers on the retrieved passages.
    Do not invent facts or claim that information appears in the documents
    when it does not.

    If the retrieved context does not contain the answer, say so clearly.
    You may use conversation history to understand follow-up questions.
    """

    # Agent with conversational checkpointing
    memory = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=[retrieve_context],
        system_prompt=system_prompt,
        checkpointer=memory,
    )

    # Save successfully initialized components
    st.session_state.vector_store = vector_store
    st.session_state.agent = agent
    st.session_state.document_uploaded = True


# -------------------- Streamlit UI --------------------

st.title("📚 PDF Chatbot")
st.caption("Upload your PDFs and ask questions about their contents.")

if not st.session_state.document_uploaded:
    uploaded_files = st.file_uploader(
        "Select PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files and st.button("Process PDFs", type="primary"):
        try:
            with st.spinner("Processing PDFs and creating embeddings..."):

                # Create directory and remove stale PDFs from prior uploads.
                DOC_DIR.mkdir(parents=True, exist_ok=True)

                for old_file in DOC_DIR.iterdir():
                    if old_file.is_file():
                        old_file.unlink()
                    elif old_file.is_dir():
                        shutil.rmtree(old_file)

                # Save the newly uploaded PDFs.
                for uploaded_file in uploaded_files:
                    filename = Path(uploaded_file.name).name

                    if not filename.lower().endswith(".pdf"):
                        continue

                    file_path = DOC_DIR / filename
                    file_path.write_bytes(uploaded_file.getvalue())

                if not any(DOC_DIR.glob("*.pdf")):
                    raise ValueError("Please upload at least one PDF file.")

                process_document(DOC_DIR)

            st.success("PDFs processed successfully!")
            st.rerun()

        except Exception as exc:
            st.error(f"Could not process the PDFs: {exc}")

# -------------------- Chat UI --------------------

if st.session_state.document_uploaded and st.session_state.agent:

    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Ask a question about your PDFs...")

    if query:
        st.session_state.messages.append(
            {"role": "user", "content": query}
        )

        with st.chat_message("user"):
            st.markdown(query)

        try:
            with st.chat_message("assistant"):
                with st.spinner("Searching your documents..."):

                    response = st.session_state.agent.invoke(
                        {
                            "messages": [
                                {"role": "user", "content": query}
                            ]
                        },
                        {
                            "configurable": {
                                "thread_id": THREAD_ID
                            }
                        },
                    )

                    answer = response["messages"][-1].content

                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as exc:
            st.error(f"An error occurred while answering: {exc}")
