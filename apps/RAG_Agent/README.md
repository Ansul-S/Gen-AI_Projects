# 📚 PDF Chatbot — Chat With Your Documents Using Agentic RAG

PDF Chatbot is an AI-powered application that lets users **upload PDF files and ask questions about them in natural language**.

For example, instead of opening a 60-page PDF and searching with `Ctrl + F` for:

```text
"leave", "holiday", "vacation", "time off" ...
```

the user can simply ask:

> "How many days of annual leave do employees get?"

The AI agent searches the uploaded documents for the most relevant passages, reads them, and answers the question **based on what the documents actually say**.

This technique is called **RAG — Retrieval-Augmented Generation**.

The application is built using:

- 🐍 Python
- 🤖 LangChain
- 🧠 Groq LLM (`openai/gpt-oss-20b`)
- 🧬 Google Gemini Embeddings
- 📄 PyPDF
- ✂️ LangChain Text Splitters
- 🧮 LangChain `InMemoryVectorStore`
- 🕸️ Streamlit
- 🧩 LangGraph's `InMemorySaver`

---

# 📌 Table of Contents

1. [What Is PDF Chatbot?](#-what-is-pdf-chatbot)
2. [Why This Project?](#-why-this-project)
3. [What You Can Learn](#-what-you-can-learn)
4. [Features](#-features)
5. [What Is RAG?](#-what-is-rag)
6. [How the Application Works](#-how-the-application-works)
7. [Architecture](#-architecture)
8. [Project Flow](#-project-flow)
9. [Technologies Used](#-technologies-used)
10. [Project Structure](#-project-structure)
11. [Installation](#-installation)
12. [Environment Variables](#-environment-variables)
13. [Keeping Secrets and PDFs Out of Git](#-keeping-secrets-and-pdfs-out-of-git)
14. [Understanding the Code](#-understanding-the-code)
15. [Understanding PDF Loading](#-understanding-pdf-loading)
16. [Understanding Chunking](#-understanding-chunking)
17. [Understanding Embeddings](#-understanding-embeddings)
18. [Understanding the Vector Store](#-understanding-the-vector-store)
19. [Understanding the LLM](#-understanding-the-llm)
20. [Understanding the Retrieval Tool](#-understanding-the-retrieval-tool)
21. [Understanding the System Prompt](#-understanding-the-system-prompt)
22. [Understanding the Agent](#-understanding-the-agent)
23. [Understanding Memory](#-understanding-memory)
24. [Understanding Streamlit](#-understanding-streamlit)
25. [Complete Request Lifecycle](#-complete-request-lifecycle)
26. [Example Conversations](#-example-conversations)
27. [Running the Application](#-running-the-application)
28. [Testing the Application](#-testing-the-application)
29. [Troubleshooting](#-troubleshooting)
30. [Important Concepts](#-important-concepts)
31. [Limitations](#-limitations)
32. [Possible Improvements](#-possible-improvements)
33. [Learning Path](#-learning-path)
34. [Conclusion](#-conclusion)

---

# 🤖 What Is PDF Chatbot?

PDF Chatbot is a **document question-answering application**.

The user uploads one or more PDFs. The application:

1. Extracts the text from every page.
2. Splits the text into small overlapping chunks.
3. Converts every chunk into a vector (a list of numbers) using an embedding model.
4. Stores the vectors in a vector store.
5. Creates an AI agent that has a **retrieval tool** for searching that vector store.

After that, the user can chat with the documents:

```text
User:
What is the refund policy?

AI:
According to the document, customers can request a full refund
within 30 days of purchase, provided the product is unused...
```

The user doesn't need to know where the answer is in the document.

Behind the scenes, the agent calls something similar to:

```python
retrieve_context("refund policy")
```

reads the three most relevant passages, and writes an answer based on them.

---

# 🎯 Why This Project?

LLMs are trained on huge amounts of public data, but they have **never seen your private documents**.

If you ask a normal chatbot:

```text
"What does section 4.2 of my rental agreement say?"
```

it can only guess, because the rental agreement was never part of its training data.

There are two obvious ways to give the LLM access to a document:

### Option 1 — Paste the entire document into the prompt

```text
[ 300 pages of text ] + "What does section 4.2 say?"
```

Problems:

- Large documents may not fit in the model's context window.
- Sending all the text for every question is slow and expensive.
- The model has to find a needle in a haystack.

### Option 2 — Retrieve only the relevant parts (RAG)

```text
[ 3 relevant passages ] + "What does section 4.2 say?"
```

Benefits:

- Only a small amount of text is sent to the LLM.
- Works with documents much larger than the context window.
- Answers are grounded in the actual document text.

This project implements **Option 2**.

It demonstrates one of the most important patterns in modern AI applications:

```text
Human
  ↓
Natural Language Question
  ↓
AI Agent
  ↓
Retrieval Tool
  ↓
Vector Store (your documents)
  ↓
Relevant Passages
  ↓
LLM
  ↓
Grounded Answer
```

---

# 📚 What You Can Learn

This project is particularly useful if you are learning **Generative AI, RAG, AI Agents, or LangChain**.

You can learn:

### Python

- Imports
- Functions
- Nested functions and closures
- Decorators
- `pathlib.Path`
- File handling (reading, writing, deleting)
- Exception handling
- List comprehensions and generator expressions

### Retrieval-Augmented Generation (RAG)

- Document loading
- Text extraction from PDFs
- Chunking
- Chunk overlap
- Embeddings
- Vector stores
- Similarity search
- Top-k retrieval
- Grounding answers in context

### LangChain

- Document loaders
- Text splitters
- Embedding models
- Vector stores
- Chat models
- Custom tools with `@tool`
- Agents with `create_agent`
- System prompts

### LangGraph

- Checkpointers
- Conversation threads
- In-memory persistence

### Streamlit

- File uploads
- Buttons
- Chat interfaces
- Session state
- Spinners
- Success and error messages
- Reruns

### Generative AI

- Tool calling
- Agentic RAG
- Prompt engineering
- Hallucination prevention
- Follow-up question handling

---

# ✨ Features

PDF Chatbot supports the following features.

## 1. Multiple PDF Upload

Users can upload **one or more PDFs** at the same time.

```text
📄 employee_handbook.pdf
📄 leave_policy.pdf
📄 code_of_conduct.pdf
```

All of them become part of the same searchable knowledge base.

---

## 2. Automatic Text Extraction

The application reads every page of every PDF and extracts its text.

---

## 3. Smart Chunking

The extracted text is split into chunks of about **1000 characters** with **200 characters of overlap**, so that sentences near chunk boundaries aren't lost.

---

## 4. Semantic Search

The application uses **embeddings**, so it searches by **meaning**, not just keywords.

For example, the question:

```text
How much time off do I get?
```

can find a passage that says:

```text
Employees are entitled to 24 days of annual leave per year.
```

even though the words "time off" never appear in it.

---

## 5. Agentic Retrieval

The LLM doesn't receive the retrieved text automatically.

Instead, it has a **tool** called `retrieve_context` and **decides by itself** when to use it and what to search for.

---

## 6. Follow-Up Questions

The agent remembers the conversation, so follow-up questions work:

```text
User: What is the leave policy?
AI:   Employees get 24 days of annual leave...

User: Can unused days be carried over?
AI:   Yes, up to 5 unused days can be carried over...
```

---

## 7. Grounded Answers

The system prompt instructs the agent to **only use the retrieved passages** for document-specific answers, and to **say clearly** when the answer isn't in the documents.

---

## 8. Clean Uploads

Every time new PDFs are processed, the previous uploads in `doc_files/` are deleted first, so old documents never leak into the new knowledge base.

---

## 9. Friendly Error Handling

If something goes wrong — an invalid PDF, a missing API key, a network error — the application shows a readable error message instead of crashing.

---

# 🧩 What Is RAG?

**RAG** stands for:

```text
R → Retrieval      Find the relevant information
A → Augmented      Add it to the LLM's input
G → Generation     Let the LLM generate an answer from it
```

Every RAG application has **two phases**.

## Phase 1 — Indexing (happens once per upload)

```text
PDF files
   ↓
Load text
   ↓
Split into chunks
   ↓
Create embeddings
   ↓
Store in vector store
```

## Phase 2 — Querying (happens for every question)

```text
User question
   ↓
Create embedding of the question
   ↓
Find the most similar chunks
   ↓
Give the chunks to the LLM
   ↓
LLM writes the answer
```

A useful mental model:

> RAG turns a **closed-book exam** into an **open-book exam**.
>
> The LLM no longer has to remember the answer. It only has to **find the right page and read it**.

---

# 🧱 How the Application Works

At a high level, the application contains six major components:

```text
┌─────────────────────────┐
│        Streamlit        │
│     Upload + Chat UI    │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│        AI Agent         │
│     (create_agent)      │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│           LLM           │
│ Groq · gpt-oss-20b      │
└────────────┬────────────┘
             │  tool call
             ↓
┌─────────────────────────┐
│     Retrieval Tool      │
│    retrieve_context     │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│      Vector Store       │
│  InMemoryVectorStore    │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│    Embedding Model      │
│  Google Gemini          │
└─────────────────────────┘
```

The important idea is:

> The LLM does not read the PDFs directly. It uses a **retrieval tool** that searches a vector store and returns only the most relevant passages.

---

# 🧠 Architecture

The complete architecture, including both phases:

```text
                    ┌──────────────────────────────────┐
                    │              USER                │
                    └───────┬──────────────────┬───────┘
                            │                  │
                    uploads PDFs         asks questions
                            │                  │
                            ▼                  ▼
                    ┌──────────────────────────────────┐
                    │         Streamlit Interface       │
                    └───────┬──────────────────┬───────┘
                            │                  │
        ════════ INDEXING ══╪══════   ═════════╪═══ QUERYING ════════
                            │                  │
                            ▼                  ▼
                 ┌──────────────────┐  ┌──────────────────┐
                 │   doc_files/     │  │    LangChain     │
                 │  (saved PDFs)    │  │      Agent       │
                 └────────┬─────────┘  └────────┬─────────┘
                          │                     │
                          ▼                     ▼
                 ┌──────────────────┐  ┌──────────────────┐
                 │ PyPDFDirectory   │  │    Groq LLM      │
                 │     Loader       │  │   gpt-oss-20b    │
                 └────────┬─────────┘  └────────┬─────────┘
                          │                     │
                          ▼               Tool Calling
                 ┌──────────────────┐           │
                 │ RecursiveChar.   │           ▼
                 │  TextSplitter    │  ┌──────────────────┐
                 └────────┬─────────┘  │ retrieve_context │
                          │            │   (k = 3)        │
                          ▼            └────────┬─────────┘
                 ┌──────────────────┐           │
                 │ Gemini Embeddings│◄──────────┤ embeds the query
                 └────────┬─────────┘           │
                          │                     │
                          ▼                     ▼
                 ┌─────────────────────────────────────────┐
                 │          InMemoryVectorStore             │
                 │  chunk vectors  ←── similarity search    │
                 └─────────────────────────────────────────┘
```

---

# 🔄 Project Flow

The application has two separate flows: **processing PDFs** and **answering questions**.

## Flow A — Processing PDFs

### Step 1 — User selects PDFs

The user chooses one or more `.pdf` files in the file uploader.

---

### Step 2 — User clicks "Process PDFs"

The button only appears after at least one file has been selected.

---

### Step 3 — Old uploads are deleted

Everything inside `doc_files/` is removed so old documents don't mix with new ones.

---

### Step 4 — New PDFs are saved to disk

Each uploaded file is written to:

```text
doc_files/<filename>.pdf
```

---

### Step 5 — PDFs are loaded

`PyPDFDirectoryLoader` reads every PDF in `doc_files/` and creates **one `Document` per page**.

---

### Step 6 — Pages are split into chunks

`RecursiveCharacterTextSplitter` splits the pages into chunks of about 1000 characters with 200 characters of overlap.

---

### Step 7 — Chunks are embedded and stored

Every chunk is converted into a vector by the Gemini embedding model and stored in an `InMemoryVectorStore`.

---

### Step 8 — The agent is created

The LLM, the retrieval tool, the system prompt and the memory are combined into an agent.

---

### Step 9 — The UI switches to chat mode

The agent is saved in `st.session_state`, and the page reruns to show the chat interface.

---

## Flow B — Answering a Question

Suppose the user asks:

```text
"What is the notice period for resignation?"
```

### Step 1 — User enters a message

Streamlit receives the question and displays it in the chat.

---

### Step 2 — Message is sent to the agent

```python
st.session_state.agent.invoke(...)
```

---

### Step 3 — The LLM decides to search

The model sees that the question is about the documents and decides to call:

```python
retrieve_context("notice period for resignation")
```

---

### Step 4 — Similarity search

The query is embedded, and the vector store returns the **3 chunks** most similar to it.

---

### Step 5 — Passages are returned to the LLM

The three chunks are joined into a single string, separated by `---`.

---

### Step 6 — The LLM writes the answer

The model reads the passages and answers based on them:

```text
According to the employee handbook, the notice period for resignation
is 30 days for permanent employees and 15 days during probation.
```

---

### Step 7 — The answer is displayed and saved

The answer is shown in the chat and appended to the chat history.

---

# 🔧 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web UI (file upload + chat) |
| LangChain | LLM application framework |
| LangGraph | Agent checkpointing / conversation memory |
| Groq | LLM provider (`openai/gpt-oss-20b`) |
| Google Gemini | Embedding model (`gemini-embedding-2-preview`) |
| PyPDF | PDF text extraction (used by `PyPDFDirectoryLoader`) |
| LangChain Text Splitters | Splitting documents into chunks |
| `InMemoryVectorStore` | Storing and searching chunk embeddings |
| python-dotenv | Environment variable management |

---

# 📁 Project Structure

```text
RAG_Agent/
│
├── rag_agent.py
├── doc_files/
│   └── <your uploaded PDFs>
└── README.md
```

### `rag_agent.py`

Contains the complete application: document processing, the agent and the Streamlit UI.

### `doc_files/`

Stores the PDFs from the **most recent upload**.

It is created automatically the first time PDFs are processed.

> ⚠️ **Everything inside `doc_files/` is deleted every time you click "Process PDFs".** Don't keep your own files in this folder.

> 📌 `doc_files/` is a **relative path**, so it is created inside whichever directory you run `streamlit run` from. Run the app from the `RAG_Agent/` folder to keep it here.

### `.env`

Stores your API keys. It lives in the repository root (see [Environment Variables](#-environment-variables)).

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd GenAI-Projects
```

---

## 2. Create a Virtual Environment

Creating a virtual environment keeps the project's dependencies isolated.

This project is developed with **Python 3.11**.

### macOS/Linux

```bash
python3 -m venv env
```

Activate it:

```bash
source env/bin/activate
```

### Windows

```bash
python -m venv env
```

Activate it:

```bash
env\Scripts\activate
```

---

## 3. Install Dependencies

Install everything the repository uses:

```bash
pip install -r requirements.txt
```

Or install only what this application needs:

```bash
pip install streamlit langchain langchain-community langchain-text-splitters langchain-groq langchain-google-genai langgraph pypdf python-dotenv
```

| Package | Why it's needed |
|---|---|
| `streamlit` | Web interface |
| `langchain` | `create_agent` and `@tool` |
| `langchain-community` | `PyPDFDirectoryLoader`, `InMemoryVectorStore` |
| `langchain-text-splitters` | `RecursiveCharacterTextSplitter` |
| `langchain-groq` | `ChatGroq` |
| `langchain-google-genai` | `GoogleGenerativeAIEmbeddings` |
| `langgraph` | `InMemorySaver` |
| `pypdf` | Reading PDF files |
| `python-dotenv` | Loading `.env` |

---

# 🔑 Environment Variables

The application uses:

```python
from dotenv import load_dotenv

load_dotenv()
```

This loads variables from a `.env` file. `load_dotenv()` searches upward through parent directories, so a `.env` file in the repository root works.

This project needs **two** API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

| Variable | Used by | Where to get it |
|---|---|---|
| `GROQ_API_KEY` | `ChatGroq` (the LLM) | [console.groq.com/keys](https://console.groq.com/keys) |
| `GOOGLE_API_KEY` | `GoogleGenerativeAIEmbeddings` (the embeddings) | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

Why two providers?

```text
Groq    → fast LLM for reasoning and answering
Google  → embedding model for converting text into vectors
```

The API keys should **never be committed to GitHub**.

---

# 🔐 Keeping Secrets and PDFs Out of Git

Your `.gitignore` should include:

```gitignore
.env
env/
__pycache__/
*.pyc
.DS_Store
doc_files/
```

The `doc_files/` rule is important.

Uploaded PDFs are saved to disk, and they are often **private** — contracts, resumes, reports, invoices. Without this rule, `git add .` would add them to the repository.

---

# 🔍 Understanding the Code

`rag_agent.py` is organized into six sections:

```text
1. Imports
2. Configuration
3. Session State
4. Document Processing     ← process_document()
5. Streamlit UI            ← upload section
6. Chat UI                 ← chat section
```

The concepts inside `process_document()` (loading, chunking, embeddings, the vector store, the tool, the prompt, the agent and memory) each have their own section later in this README.

---

## 1. Imports

```python
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
```

| Import | Role in the project |
|---|---|
| `shutil` | Deletes old sub-folders inside `doc_files/` |
| `Path` | Works with file and folder paths |
| `streamlit` | Builds the web interface |
| `load_dotenv` | Loads API keys from `.env` |
| `PyPDFDirectoryLoader` | Loads every PDF in a folder |
| `RecursiveCharacterTextSplitter` | Splits text into chunks |
| `GoogleGenerativeAIEmbeddings` | Converts text into vectors |
| `ChatGroq` | The LLM |
| `InMemoryVectorStore` | Stores and searches vectors |
| `create_agent` | Builds the agent |
| `tool` | Turns a Python function into a tool the LLM can call |
| `InMemorySaver` | Gives the agent conversation memory |

---

## 2. Configuration

```python
DOC_DIR = Path("./doc_files")
THREAD_ID = "pdf-chat"
```

### `DOC_DIR`

The folder where uploaded PDFs are saved before being loaded.

### `THREAD_ID`

The conversation ID passed to the agent. See [Understanding Memory](#-understanding-memory).

Keeping these values at the top of the file makes them easy to find and change.

---

## 3. Session State

```python
if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []
```

Streamlit **reruns the whole script** after every interaction — every click, every upload, every chat message.

Without session state, every rerun would forget the agent and the vector store, and the PDFs would have to be processed again for every question.

| Key | Initial value | Purpose |
|---|---|---|
| `document_uploaded` | `False` | Switches the page from **upload mode** to **chat mode** |
| `agent` | `None` | The agent built for the uploaded PDFs |
| `vector_store` | `None` | The vector store holding the chunk embeddings |
| `messages` | `[]` | Chat history displayed in the UI |

The `if ... not in` check makes sure each value is only initialized **once per browser session**, not on every rerun.

---

## 4. Document Processing

```python
def process_document(path: Path):
    """Load PDFs, split them into chunks, embed them, and create an agent."""
```

This single function performs the entire **indexing phase** and builds the agent:

```text
process_document(DOC_DIR)
        │
        ├── 1. Load PDFs              → documents
        ├── 2. Split into chunks      → chunks
        ├── 3. Create embeddings      → embeddings
        ├── 4. Build vector store     → vector_store
        ├── 5. Create the LLM         → llm
        ├── 6. Define the tool        → retrieve_context
        ├── 7. Write system prompt    → system_prompt
        ├── 8. Create the agent       → agent
        └── 9. Save to session state
```

Each step is explained in the sections that follow.

The final step saves the results:

```python
st.session_state.vector_store = vector_store
st.session_state.agent = agent
st.session_state.document_uploaded = True
```

These three lines only run if **every previous step succeeded**. If anything fails, an exception is raised before them and the app stays in upload mode.

---

## 5. Upload Section

```python
st.title("📚 PDF Chatbot")
st.caption("Upload your PDFs and ask questions about their contents.")

if not st.session_state.document_uploaded:
    uploaded_files = st.file_uploader(
        "Select PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )
```

The uploader is only shown **before** PDFs have been processed.

- `type=["pdf"]` → the file picker only accepts PDFs.
- `accept_multiple_files=True` → `uploaded_files` is a **list** of files.

---

### The Process Button

```python
if uploaded_files and st.button("Process PDFs", type="primary"):
```

Because of how `and` works in Python, `st.button(...)` is only evaluated when `uploaded_files` is not empty.

So the button **only appears after the user selects at least one file**.

`type="primary"` makes it a highlighted button.

---

### Deleting Old Uploads

```python
DOC_DIR.mkdir(parents=True, exist_ok=True)

for old_file in DOC_DIR.iterdir():
    if old_file.is_file():
        old_file.unlink()
    elif old_file.is_dir():
        shutil.rmtree(old_file)
```

- `mkdir(parents=True, exist_ok=True)` creates `doc_files/` if it doesn't exist and does nothing if it does.
- `unlink()` deletes a file.
- `shutil.rmtree()` deletes a folder and everything inside it.

Why is this needed?

`PyPDFDirectoryLoader` loads **every PDF in the folder**. Without the cleanup, PDFs from a previous upload would silently become part of the new knowledge base.

---

### Saving the New PDFs

```python
for uploaded_file in uploaded_files:
    filename = Path(uploaded_file.name).name

    if not filename.lower().endswith(".pdf"):
        continue

    file_path = DOC_DIR / filename
    file_path.write_bytes(uploaded_file.getvalue())
```

Line by line:

| Code | What it does |
|---|---|
| `Path(uploaded_file.name).name` | Keeps only the file name and drops any folder components |
| `.lower().endswith(".pdf")` | Skips anything that isn't a PDF, including `.PDF` vs `.pdf` differences |
| `DOC_DIR / filename` | Builds the path `doc_files/<filename>` |
| `uploaded_file.getvalue()` | Gets the file's raw bytes |
| `write_bytes(...)` | Writes the bytes to disk |

`Path(...).name` is a small but important **safety measure**. A file name such as:

```text
../../important_file.pdf
```

becomes:

```text
important_file.pdf
```

so an upload can never be written outside `doc_files/`.

---

### Validating and Processing

```python
if not any(DOC_DIR.glob("*.pdf")):
    raise ValueError("Please upload at least one PDF file.")

process_document(DOC_DIR)
```

`DOC_DIR.glob("*.pdf")` finds all PDFs in the folder, and `any(...)` checks that at least one exists.

Then the indexing phase runs.

---

### Success, Rerun and Errors

```python
            st.success("PDFs processed successfully!")
            st.rerun()

        except Exception as exc:
            st.error(f"Could not process the PDFs: {exc}")
```

- `st.rerun()` restarts the script immediately. On the next run, `document_uploaded` is `True`, so the uploader disappears and the chat interface appears.
- Any error — an unreadable PDF, a missing API key, a network failure — is caught and shown as a red error box.

The whole processing step runs inside:

```python
with st.spinner("Processing PDFs and creating embeddings..."):
```

which shows a loading animation, because embedding large PDFs can take a while.

---

## 6. Chat Section

```python
if st.session_state.document_uploaded and st.session_state.agent:
```

The chat interface is shown only after the PDFs have been processed **and** the agent exists.

The chat logic is explained in [Understanding Streamlit](#-understanding-streamlit) and [Complete Request Lifecycle](#-complete-request-lifecycle).

---

# 📄 Understanding PDF Loading

```python
loader = PyPDFDirectoryLoader(str(path))
documents = loader.load()
```

`PyPDFDirectoryLoader` reads **every PDF in a folder** using the `pypdf` library.

It returns a list of LangChain `Document` objects — **one per page**.

For example, uploading a 3-page and a 2-page PDF produces 5 documents:

```text
documents = [
    Document(page 1 of handbook.pdf),
    Document(page 2 of handbook.pdf),
    Document(page 3 of handbook.pdf),
    Document(page 1 of policy.pdf),
    Document(page 2 of policy.pdf),
]
```

Each `Document` has two parts:

```python
Document(
    page_content="Employees are entitled to 24 days of annual leave...",
    metadata={"source": "doc_files/handbook.pdf", "page": 0, ...},
)
```

| Field | Meaning |
|---|---|
| `page_content` | The text extracted from the page |
| `metadata` | Information about where the text came from, such as the file and page number |

The code checks that something was loaded:

```python
if not documents:
    raise ValueError(
        "No readable PDF content found. Please upload valid PDFs."
    )
```

> 📌 PyPDF extracts **text**. A scanned PDF is just images of pages, so it has no text to extract. Scanned PDFs need OCR (optical character recognition) first.

---

# 📐 Understanding Chunking

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
chunks = splitter.split_documents(documents)
```

## Why split documents at all?

A single page can contain several unrelated topics:

```text
Page 12
├── Leave policy
├── Work-from-home rules
└── Expense reimbursement
```

If the whole page were one search unit, a question about expenses would retrieve leave and work-from-home text too.

Smaller chunks mean:

- **More precise retrieval** — each chunk is about one thing.
- **Less noise** for the LLM to read.
- **Fewer tokens** sent to the LLM.

But chunks that are too small lose context:

```text
"...is 30 days."
```

30 days of **what**?

A chunk size of around 1000 characters (roughly a few paragraphs) is a common middle ground.

---

## `chunk_size=1000`

Each chunk contains **at most about 1000 characters**.

---

## `chunk_overlap=200`

Consecutive chunks **share about 200 characters**.

```text
Text:   ████████████████████████████████████████████████

Chunk 1: ██████████████████████
Chunk 2:                 ██████████████████████
Chunk 3:                                 ████████████████
                         ↑↑↑↑↑↑
                       overlap
```

Why overlap?

Without overlap, a sentence on a chunk boundary could be cut in half:

```text
Chunk 1: "...The notice period for permanent"
Chunk 2: "employees is 30 days..."
```

Neither chunk contains the complete fact.

With overlap, the end of one chunk is repeated at the start of the next, so the complete sentence is very likely to exist in at least one chunk.

---

## Why "Recursive"?

`RecursiveCharacterTextSplitter` tries to split on **natural boundaries first**, in this order:

```text
1. "\n\n"   paragraphs
2. "\n"     lines
3. " "      words
4. ""       characters (last resort)
```

It only falls back to a smaller separator when a piece is still bigger than `chunk_size`.

This keeps paragraphs and sentences together whenever possible.

---

The code checks that chunks were created:

```python
if not chunks:
    raise ValueError("No text chunks could be extracted from the PDFs.")
```

This happens, for example, when every page of the PDF is a scanned image with no text.

---

# 🧬 Understanding Embeddings

```python
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview"
)
```

An **embedding** is a list of numbers that represents the **meaning** of a piece of text.

```text
"Employees get 24 days of annual leave."
        ↓  embedding model
[0.021, -0.443, 0.187, 0.902, ..., -0.115]
```

The important property is:

> Texts with **similar meanings** get **similar vectors**, even if they use different words.

```text
"How much vacation do I get?"        → [0.03, -0.41, 0.19, ...]
"Annual leave entitlement is 24 days" → [0.02, -0.44, 0.18, ...]   ← very close
"The cafeteria opens at 8 AM"        → [0.71,  0.12, -0.56, ...]  ← far away
```

This is why the chatbot can find relevant passages even when the question uses different words than the document.

## Keyword Search vs Semantic Search

| Question | Keyword search | Semantic search |
|---|---|---|
| "time off" | Only finds the exact words "time off" | Also finds "annual leave", "vacation", "holidays" |
| "fired" | Only finds "fired" | Also finds "termination", "dismissal" |

The **same embedding model** is used for:

1. Embedding the document chunks (indexing).
2. Embedding the user's search query (querying).

That is essential — vectors from two different models can't be compared.

---

# 🧮 Understanding the Vector Store

```python
vector_store = InMemoryVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
)
```

A **vector store** is a database designed for storing vectors and finding the ones closest to a given vector.

`from_documents(...)` does two things:

```text
1. Calls the embedding model for every chunk
2. Stores (chunk text, metadata, vector) together
```

Conceptually, it looks like this:

```text
┌────┬──────────────────────────────────┬─────────────────────────┐
│ #  │ Chunk text                       │ Vector                  │
├────┼──────────────────────────────────┼─────────────────────────┤
│ 1  │ "Employees are entitled to 24…"  │ [0.02, -0.44, 0.18, …]  │
│ 2  │ "Unused leave of up to 5 days…"  │ [0.05, -0.39, 0.22, …]  │
│ 3  │ "The notice period for perma…"   │ [-0.31, 0.08, 0.67, …]  │
│ …  │ …                                │ …                       │
└────┴──────────────────────────────────┴─────────────────────────┘
```

## Similarity Search

```python
vector_store.similarity_search(query=query, k=3)
```

1. The query is embedded with the same Gemini model.
2. The query vector is compared with every chunk vector (using cosine similarity).
3. The **3 closest** chunks are returned.

```text
Query: "notice period"
            ↓
     [-0.29, 0.11, 0.64, ...]
            ↓
   Compare with all chunks
            ↓
   Top 3 most similar chunks
```

## Why "In Memory"?

`InMemoryVectorStore` keeps everything in **RAM** inside the Python process.

| Advantage | Disadvantage |
|---|---|
| No installation or setup | Lost when the app restarts or the browser session ends |
| Very simple | PDFs must be re-embedded every session |
| Great for learning | Not suitable for very large document collections |

Production applications usually use a persistent vector database such as Chroma, FAISS, pgvector, Pinecone or Qdrant.

---

# 🧠 Understanding the LLM

```python
llm = ChatGroq(model="openai/gpt-oss-20b")
```

The application uses OpenAI's open-weight **GPT-OSS-20B** model, served by **Groq**.

Groq runs models on specialized hardware, which makes responses very fast.

In this project, the LLM is responsible for:

```text
1. Understanding the user's question
2. Deciding whether the documents need to be searched
3. Writing a good search query for the retrieval tool
4. Reading the retrieved passages
5. Writing a grounded answer
6. Understanding follow-up questions using the conversation history
```

Notice that the LLM and the embedding model are **two different models**:

| Model | Job |
|---|---|
| Gemini embedding model | Turns text into vectors |
| GPT-OSS-20B (Groq) | Reasons and writes answers |

---

# 🔎 Understanding the Retrieval Tool

```python
@tool
def retrieve_context(query: str) -> str:
    """Retrieve relevant passages from the uploaded PDF knowledge base."""

    relevant_docs = vector_store.similarity_search(
        query=query,
        k=3,
    )

    if not relevant_docs:
        return "No relevant information was found in the documents."

    context = "\n\n---\n\n".join(
        doc.page_content for doc in relevant_docs
    )

    return context
```

This is the heart of the project. It is the **bridge between the LLM and the documents**.

---

## The `@tool` Decorator

`@tool` turns a normal Python function into a **tool** that the LLM can call.

LangChain uses three pieces of the function to describe the tool to the LLM:

| Part of the function | What the LLM sees |
|---|---|
| Function name | Tool name: `retrieve_context` |
| Docstring | Tool description: "Retrieve relevant passages from the uploaded PDF knowledge base." |
| Type hints | Arguments: `query` (a string) |

The docstring is **not just a comment** — it's how the LLM knows what the tool is for. A vague docstring leads to a model that doesn't know when to use the tool.

---

## `k=3`

The tool returns the **3 most relevant chunks**.

| Smaller `k` | Larger `k` |
|---|---|
| Less noise | More complete context |
| Fewer tokens, cheaper and faster | More tokens, slower |
| May miss information spread across many chunks | More irrelevant text for the LLM |

---

## Joining the Results

```python
context = "\n\n---\n\n".join(
    doc.page_content for doc in relevant_docs
)
```

The three chunks are combined into one string with a clear separator:

```text
Employees are entitled to 24 days of annual leave per year...

---

Unused leave of up to 5 days may be carried over...

---

Leave requests must be submitted at least two weeks in advance...
```

The `---` separators help the LLM see where one passage ends and the next begins.

---

## Why Is the Tool Defined Inside `process_document()`?

The tool is a **nested function**. It uses the `vector_store` variable from the surrounding function.

```text
process_document()
   │
   ├── vector_store = ...      ← created here
   │
   └── retrieve_context()      ← "remembers" vector_store
```

This is called a **closure**. Every time PDFs are processed, a new tool is created that is permanently connected to the new vector store.

---

# 📜 Understanding the System Prompt

```python
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
```

The system prompt defines the agent's behavior. Each line has a purpose:

| Instruction | Why it matters |
|---|---|
| "You are a helpful PDF question-answering assistant." | Gives the agent its role |
| "Use the retrieve_context tool for questions that require information from the uploaded documents." | Tells the agent **when** to search |
| "Base document-specific answers on the retrieved passages." | Grounds answers in the documents |
| "Do not invent facts or claim that information appears in the documents when it does not." | Reduces hallucinations |
| "If the retrieved context does not contain the answer, say so clearly." | Makes "I don't know" an acceptable answer |
| "You may use conversation history to understand follow-up questions." | Enables follow-ups like "What about part-time staff?" |

---

## Why "Say So Clearly" Is So Important

LLMs are trained to be helpful, so they tend to **always produce an answer**.

Without this instruction, a question like:

```text
What is the CEO's salary?
```

might get a confident but invented answer.

With the instruction, the expected answer is:

```text
The uploaded documents don't contain information about the CEO's salary.
```

In a RAG application, **"I couldn't find that in the documents" is a correct answer**, not a failure.

---

# 🤖 Understanding the Agent

```python
memory = InMemorySaver()

agent = create_agent(
    model=llm,
    tools=[retrieve_context],
    system_prompt=system_prompt,
    checkpointer=memory,
)
```

| Argument | Meaning |
|---|---|
| `model=llm` | The LLM that reasons and answers |
| `tools=[retrieve_context]` | The actions the agent is allowed to take |
| `system_prompt=system_prompt` | The agent's instructions |
| `checkpointer=memory` | Gives the agent conversation memory |

---

## What Is an AI Agent?

A simple chatbot does:

```text
User
 ↓
LLM
 ↓
Text response
```

An agent can do:

```text
User
 ↓
LLM
 ↓
Decide what action is required
 ↓
Use a tool
 ↓
Observe the result
 ↓
Decide the next step (use another tool, or answer)
 ↓
Return response
```

`create_agent` builds this loop for you.

---

## Classic RAG vs Agentic RAG

This project uses **agentic RAG**. That's different from the "classic" RAG pipeline that many tutorials show.

### Classic RAG

```text
User question
     ↓
ALWAYS search the vector store with the exact question
     ↓
Paste results into the prompt
     ↓
LLM answers
```

### Agentic RAG (this project)

```text
User question
     ↓
LLM DECIDES:
  ├── Is searching needed?            (no for "Hi!")
  ├── What should I search for?       (rewrites the query)
  └── Do I need to search again?      (can call the tool multiple times)
     ↓
LLM answers
```

| | Classic RAG | Agentic RAG |
|---|---|---|
| Who decides to search? | The code (always) | The LLM |
| Search query | The user's exact words | Written by the LLM |
| Follow-up questions | "What about it?" is a poor search query | LLM rewrites it using the conversation |
| Multiple searches | One per question | As many as needed |
| Small talk ("Thanks!") | Still searches | Answers directly |
| Predictability | Higher | Lower — depends on the LLM's decisions |

### Example: Why Agentic RAG Helps With Follow-Ups

```text
User: What is the leave policy?
AI:   Employees get 24 days of annual leave per year...

User: Can I carry it over?
```

Classic RAG would search the vector store for:

```text
"Can I carry it over?"
```

which says nothing about leave.

The agent, using the conversation history, can search for:

```text
"carry over unused annual leave"
```

which finds the right passage.

---

# 💾 Understanding Memory

There are **two different kinds of history** in this project.

## 1. Streamlit Chat History

```python
st.session_state.messages
```

A list of messages used **only for displaying** the conversation on screen:

```python
[
    {"role": "user", "content": "What is the leave policy?"},
    {"role": "assistant", "content": "Employees get 24 days..."},
]
```

## 2. Agent Memory

```python
memory = InMemorySaver()
```

The **checkpointer** saves the agent's full state after every turn — including user messages, assistant messages, **tool calls and tool results**.

When the agent is invoked, the application only sends the **new** message:

```python
{"messages": [{"role": "user", "content": query}]}
```

The checkpointer supplies the rest of the conversation automatically.

| | `st.session_state.messages` | `InMemorySaver` |
|---|---|---|
| Used by | The UI | The agent |
| Contains | User + assistant text | Everything, including tool calls and retrieved passages |
| Purpose | Re-drawing the chat after reruns | Letting the LLM understand follow-ups |

These are related, but they are **not the same mechanism**.

---

## Understanding `thread_id`

The agent is invoked with:

```python
{
    "configurable": {
        "thread_id": THREAD_ID
    }
}
```

where:

```python
THREAD_ID = "pdf-chat"
```

The `thread_id` tells the checkpointer **which conversation** to load and save.

```text
thread_id = "pdf-chat"
        ↓
InMemorySaver
        ↓
┌──────────────────────────────┐
│ Conversation "pdf-chat"      │
│  - user: What is the...      │
│  - tool call: retrieve_...   │
│  - tool result: ...          │
│  - assistant: Employees...   │
└──────────────────────────────┘
```

In this application, a new `InMemorySaver` is created every time PDFs are processed, and it is stored inside that session's agent. So even though the thread ID is fixed, each browser session gets its **own** memory.

If you later want multiple separate conversations about the same documents, you would use a different `thread_id` for each one:

```text
pdf-chat-001
pdf-chat-002
pdf-chat-003
```

---

# 🌐 Understanding Streamlit

Streamlit lets Python developers build web applications without writing HTML, CSS or JavaScript.

## The Two Modes of the Page

The page shows **one of two views**, controlled by `st.session_state.document_uploaded`:

```text
document_uploaded = False             document_uploaded = True
┌───────────────────────────┐         ┌───────────────────────────┐
│ 📚 PDF Chatbot            │         │ 📚 PDF Chatbot            │
│                           │         │                           │
│ Select PDF files          │         │ 👤 What is the leave...   │
│ [ Browse files ]          │  ────►  │ 🤖 Employees get 24...    │
│                           │         │                           │
│ [ Process PDFs ]          │         │                           │
│                           │         │ [ Ask a question about…]  │
└───────────────────────────┘         └───────────────────────────┘
        UPLOAD MODE                            CHAT MODE
```

---

## Displaying Previous Messages

```python
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

Because Streamlit reruns the script after every interaction, the chat must be **redrawn from session state** every time.

`st.chat_message("user")` and `st.chat_message("assistant")` show the messages with different avatars.

---

## Chat Input

```python
query = st.chat_input("Ask a question about your PDFs...")
```

Creates the input box at the bottom of the page.

`query` is `None` until the user presses Enter, then it contains the question.

---

## Showing and Saving the User's Message

```python
st.session_state.messages.append(
    {"role": "user", "content": query}
)

with st.chat_message("user"):
    st.markdown(query)
```

The question is saved to history (so it survives reruns) and displayed immediately.

---

## Invoking the Agent

```python
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
```

- `st.spinner(...)` shows "Searching your documents..." while the agent works.
- `agent.invoke(...)` runs the agent loop until it produces a final answer.
- `response["messages"]` contains the whole conversation, including tool calls and tool results.
- `[-1]` takes the **last** message, which is the agent's final answer.

---

## Saving the Answer

```python
st.session_state.messages.append(
    {"role": "assistant", "content": answer}
)
```

The answer is added to history so it's shown again on the next rerun.

---

## Error Handling

```python
except Exception as exc:
    st.error(f"An error occurred while answering: {exc}")
```

If the LLM call fails (for example, a rate limit or network error), the user sees an error message instead of a crash.

---

# 🔁 Complete Request Lifecycle

The entire question-answering process can be summarized as:

```text
User
 │
 │ "Can unused leave be carried over?"
 ▼
Streamlit
 │
 │ save + display user message
 ▼
agent.invoke()
 │
 │ + system prompt
 │ + conversation history (from InMemorySaver)
 ▼
LLM (gpt-oss-20b)
 │
 │ "I need the documents for this."
 ▼
Tool call
 │
 │ retrieve_context("carry over unused annual leave")
 ▼
Gemini Embeddings
 │
 │ query → vector
 ▼
InMemoryVectorStore
 │
 │ similarity search → top 3 chunks
 ▼
retrieve_context
 │
 │ chunks joined with "---"
 ▼
LLM (gpt-oss-20b)
 │
 │ read passages, write grounded answer
 ▼
InMemorySaver
 │
 │ save the turn under thread "pdf-chat"
 ▼
Streamlit
 │
 │ display + save assistant message
 ▼
User
```

---

# 💬 Example Conversations

The examples below assume an uploaded file called `employee_handbook.pdf`.

## Example 1 — A Direct Question

### User

```text
How many days of annual leave do employees get?
```

### Agent

Calls the tool:

```python
retrieve_context("annual leave days per year")
```

Possible response:

```text
According to the employee handbook, full-time employees are entitled
to 24 days of paid annual leave per year.
```

---

## Example 2 — A Follow-Up Question

### User

```text
Can unused days be carried over?
```

The question doesn't mention "leave", but the agent understands it from the conversation history.

Possible tool call:

```python
retrieve_context("carry over unused annual leave")
```

Possible response:

```text
Yes. Up to 5 unused days can be carried over to the next year.
They must be used before the end of March.
```

---

## Example 3 — Information That Isn't in the Documents

### User

```text
What is the company's share price?
```

The agent searches, but the retrieved passages are about unrelated topics.

Possible response:

```text
The uploaded documents don't contain any information about the
company's share price.
```

> 📌 Note that `similarity_search` always returns the closest chunks it can find — even if they are not actually relevant. The vector store doesn't know whether a chunk *answers* the question. **The LLM has to judge that**, which is why the system prompt's "say so clearly" instruction matters.

---

## Example 4 — Small Talk

### User

```text
Thanks, that's helpful!
```

The agent doesn't need the documents to reply, so it may answer **without calling the tool**:

```text
You're welcome! Let me know if you have any other questions
about the documents.
```

This is one of the advantages of agentic RAG.

---

## Example 5 — A Question Needing Several Searches

### User

```text
Compare the notice period and the probation period.
```

The agent may call the tool **twice**:

```python
retrieve_context("notice period")
retrieve_context("probation period")
```

and then combine both results into a single answer.

---

## Example 6 — A Summary Request

### User

```text
Summarize the whole handbook.
```

The tool only returns **3 chunks**, so the agent sees a small part of the document.

The answer may be incomplete. See [Limitations](#-limitations).

---

# 🚀 Running the Application

Move into the application folder:

```bash
cd apps/RAG_Agent
```

Then run:

```bash
streamlit run rag_agent.py
```

Streamlit will start a local web server.

You should see something similar to:

```text
Local URL: http://localhost:8501
```

Open that address in your browser.

Then:

```text
1. Click "Browse files" and choose one or more PDFs
2. Click "Process PDFs"
3. Wait for the spinner to finish
4. Ask questions in the chat box
```

> 📌 Run the command from inside `apps/RAG_Agent/`. `doc_files/` is created relative to the directory you run the command from.

---

# 🧪 Testing the Application

After launching the app and processing a PDF, try these one by one.

### Direct question

```text
What is this document about?
```

### Specific fact

```text
What is the deadline mentioned in the document?
```

### Follow-up

```text
Can you explain that in simpler terms?
```

### Information that isn't in the document

```text
What is the weather in Paris today?
```

The agent should say that the documents don't contain this information.

### Small talk

```text
Thank you!
```

The agent should reply without searching.

### Multiple PDFs

Upload two different PDFs and ask about something that appears in only one of them.

### Invalid upload

Upload a scanned PDF (images only, no text). The app should show an error instead of crashing.

---

# 🐛 Troubleshooting

## Problem: `GROQ_API_KEY` error

Make sure `.env` contains:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Problem: Google API key or embedding error

The embedding model needs:

```env
GOOGLE_API_KEY=your_google_api_key
```

Without it, processing fails at the embedding step with an error like:

```text
Could not process the PDFs: ...
```

---

## Problem: "No text chunks could be extracted from the PDFs."

The PDF probably contains **scanned images** instead of real text.

Check by opening the PDF and trying to select text with your mouse. If you can't select any text, the PDF needs OCR before it can be used.

---

## Problem: The upload box disappeared

That's expected — after processing, the app switches to chat mode.

To upload **different PDFs**, refresh the browser page. This starts a new session, and the uploader appears again.

---

## Problem: `doc_files/` was created in the wrong place

`DOC_DIR` is a relative path:

```python
DOC_DIR = Path("./doc_files")
```

It is created inside the directory you ran `streamlit run` from. Run the app from `apps/RAG_Agent/`.

---

## Problem: My files in `doc_files/` disappeared

Everything inside `doc_files/` is deleted each time "Process PDFs" is clicked. Don't store anything there yourself.

---

## Problem: `ModuleNotFoundError: No module named 'pypdf'`

`PyPDFDirectoryLoader` needs the `pypdf` package:

```bash
pip install pypdf
```

---

## Problem: Streamlit command not found

Try:

```bash
python -m streamlit run rag_agent.py
```

instead of:

```bash
streamlit run rag_agent.py
```

---

## Problem: Processing is very slow

Every chunk has to be sent to the embedding model. Large PDFs produce many chunks.

```text
300 pages ≈ hundreds of chunks ≈ hundreds of embeddings
```

Try a smaller PDF first. Free-tier API keys may also hit rate limits.

---

## Problem: The answer is wrong or incomplete

Remember that both retrieval and the LLM are imperfect.

Check:

1. Is the information actually in the PDF as **text** (not inside an image or chart)?
2. Was it split across several chunks? Try a more specific question.
3. Does the question need more than 3 chunks? Try increasing `k`.
4. Is the information spread across many pages (for example, a summary request)?
5. Did the agent call the tool at all? Ask it to "search the documents" explicitly.

---

# 💡 Important Concepts

## RAG

Retrieval-Augmented Generation: retrieving relevant information and giving it to an LLM so it can answer from it.

---

## Document

LangChain's container for text plus metadata:

```python
Document(page_content="...", metadata={...})
```

---

## Chunk

A small piece of a document, used as the unit of search.

---

## Chunk Overlap

The amount of text shared between consecutive chunks, so that information on a boundary isn't lost.

---

## Embedding

A list of numbers representing the meaning of a piece of text.

---

## Vector Store

A database that stores embeddings and finds the most similar ones to a query.

---

## Similarity Search

Finding the stored vectors closest to a query vector.

---

## Top-k

The number of results returned by a similarity search. In this project, `k = 3`.

---

## Grounding

Basing an answer on retrieved source material instead of the model's general knowledge.

---

## Hallucination

When an LLM produces information that sounds confident but isn't true or isn't in the source.

---

## Tool

A function the LLM can call to perform an action. Here, the only tool is `retrieve_context`.

---

## Agent

An LLM-powered system that decides which tools to use, and when, to accomplish a task.

---

## Agentic RAG

RAG where the LLM decides when to retrieve and what to search for, instead of the code always retrieving.

---

## Checkpointer

A component that saves and restores an agent's state for a conversation thread. This project uses `InMemorySaver()`.

---

## Session State

Streamlit's way of keeping values across reruns for one browser session.

---

# 🚧 Limitations

This is an excellent learning project, but it is not yet a production-grade document assistant.

### 1. In-memory vector store

```python
InMemoryVectorStore
```

The embeddings are lost when the browser session ends or the app restarts. The same PDFs have to be processed (and paid for) again every time.

---

### 2. In-memory agent memory

```python
InMemorySaver()
```

Conversation memory is also lost when the session ends or the app restarts.

---

### 3. No source citations

The retrieval tool only returns `doc.page_content`:

```python
doc.page_content for doc in relevant_docs
```

The file name and page number in `doc.metadata` are never passed to the LLM, so the agent **can't tell the user where an answer came from**.

---

### 4. Fixed top-k

`k=3` works well for specific questions but poorly for:

```text
"Summarize the whole document."
"List every deadline mentioned."
```

which need information from many places.

---

### 5. Text-only PDF support

- Scanned PDFs don't work without OCR.
- Images and charts are ignored.
- Table layouts are flattened into plain text.

---

### 6. No way to change documents without refreshing

Once PDFs are processed, the uploader disappears. Adding or replacing documents requires refreshing the page and processing everything again.

---

### 7. Shared upload folder

All browser sessions use the same `doc_files/` folder, and it is emptied on every upload. If two users process PDFs at the same moment, one upload can delete the other's files.

---

### 8. No streaming

The full answer appears only after the agent finishes. Long answers can feel slow.

---

### 9. Prompt-based grounding

The rule "don't invent facts" is only an instruction in the system prompt. The LLM can still occasionally hallucinate.

---

### 10. No authentication

Anyone who can access the app can upload documents and use your API keys.

---

# 🌱 Possible Improvements

This project can be extended significantly.

## 1. Use a Persistent Vector Store

Replace:

```text
InMemoryVectorStore
```

with a persistent store such as:

```text
Chroma
FAISS (saved to disk)
pgvector
Pinecone
Qdrant
```

PDFs would only need to be embedded once, and the knowledge base would survive restarts.

---

## 2. Add Source Citations

Include the file name and page number in the tool output:

```python
context = "\n\n---\n\n".join(
    f"[{Path(doc.metadata['source']).name}, page {doc.metadata['page'] + 1}]\n"
    f"{doc.page_content}"
    for doc in relevant_docs
)
```

Then ask the agent in the system prompt to cite its sources:

```text
According to the handbook (employee_handbook.pdf, page 12)...
```

---

## 3. Add an "Upload New PDFs" Button

Add a button that resets the session state:

```python
if st.button("Upload new PDFs"):
    st.session_state.document_uploaded = False
    st.session_state.agent = None
    st.session_state.vector_store = None
    st.session_state.messages = []
    st.rerun()
```

---

## 4. Stream the Response

Use `agent.stream(...)` with `stream_mode="messages"` to show the answer word by word, as in the LightBot project.

---

## 5. Use a Separate Upload Folder per Session

Use a temporary directory, for example with Python's `tempfile` module, so sessions never delete each other's uploads.

---

## 6. Make Retrieval Settings Adjustable

Add sidebar controls for:

```text
chunk_size
chunk_overlap
k
```

and see how each one changes the answers.

---

## 7. Improve Retrieval Quality

Try more advanced retrieval techniques:

```text
MMR (Maximal Marginal Relevance) → more diverse results
Hybrid search                    → keyword + semantic search
Re-ranking                       → re-score results with a stronger model
Metadata filtering               → search only a specific PDF
```

---

## 8. Support Scanned PDFs

Add an OCR step for pages that have no text.

---

## 9. Add Evaluation

Create a test set:

```text
Question:        "What is the notice period?"
Expected answer: "30 days"
Expected source: employee_handbook.pdf, page 8
```

Then measure:

```text
Retrieval quality  → were the right chunks retrieved?
Faithfulness       → is the answer supported by the chunks?
Answer relevance   → does the answer address the question?
```

---

## 10. Add Observability

Tools such as Langfuse or LangSmith can trace:

```text
LLM calls
Tool calls
Retrieved chunks
Token usage
Latency
Errors
```

This is extremely useful for understanding **why** the agent gave a particular answer.

---

## 11. Support More File Types

LangChain has loaders for:

```text
.docx
.txt
.md
.csv
.html
```

---

## 12. Add Deployment

The application could be deployed using:

```text
Streamlit Community Cloud
Docker
AWS
GCP
Azure
Railway
Render
```

together with a persistent vector database and authentication.

---

# 🧭 Learning Path

If you're using this project to learn RAG and AI agents, don't just copy the code.

Try understanding it in this order:

### Step 1 — Learn File Handling in Python

Understand:

```python
Path(...)
path.mkdir(...)
path.iterdir()
path.write_bytes(...)
path.unlink()
```

---

### Step 2 — Load a PDF

Use `PyPDFDirectoryLoader` on its own and print the documents:

```python
documents = loader.load()
print(len(documents))
print(documents[0].page_content)
print(documents[0].metadata)
```

---

### Step 3 — Experiment With Chunking

Split the same document with different settings and compare:

```text
chunk_size = 200   vs   1000   vs   3000
chunk_overlap = 0  vs   200
```

---

### Step 4 — Understand Embeddings

Embed a few sentences and compare their similarity:

```text
"I love dogs"   vs   "I adore puppies"
"I love dogs"   vs   "The stock market fell"
```

---

### Step 5 — Try Similarity Search

Build a vector store and call `similarity_search` directly, without an LLM. Look at what gets returned for different queries.

---

### Step 6 — Learn Tools

Understand how `@tool` describes a function to an LLM, and why the docstring matters.

---

### Step 7 — Learn Agents

Understand the loop:

```text
LLM
 ↓
Reason about the question
 ↓
Choose tool
 ↓
Execute tool
 ↓
Observe result
 ↓
Continue / finish
```

---

### Step 8 — Learn Memory

Understand checkpointers and `thread_id`, and the difference between UI history and agent memory.

---

### Step 9 — Learn Streamlit

Understand:

```python
st.session_state
st.file_uploader
st.button
st.rerun
st.chat_input
st.chat_message
st.spinner
```

---

### Step 10 — Improve the Project

Once you understand the existing code, add:

```text
source citations
a persistent vector store
streaming
an "Upload new PDFs" button
evaluation
observability
```

This is where the project becomes much more interesting from an AI engineering perspective.

---

# 🔬 What Makes This Project Agentic RAG?

It is important to understand that this is **not simply a chatbot with a PDF pasted into it**.

The interesting part is the combination of:

```text
PDF
 ↓
Chunks
 ↓
Embeddings
 ↓
Vector Store
 ↓
Retrieval Tool
 ↓
Agent (decides when and what to search)
 ↓
LLM
 ↓
Grounded Answer
```

The agent has access to a retrieval tool and decides **when** to use it and **what** to search for, based on the question and the conversation so far.

That is the fundamental agentic RAG pattern.

---

# 🧩 Key Takeaway

The most important architecture to remember from this project is:

```text
                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Streamlit   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   AI Agent   │
                    └──────┬───────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
           ┌───────────┐     ┌────────────────┐
           │    LLM    │     │ Retrieval Tool │
           └───────────┘     └───────┬────────┘
                                     │
                                     ▼
                             ┌───────────────┐
                             │ Vector Store  │
                             │ (your PDFs)   │
                             └───────────────┘
```

The LLM provides the **language understanding**.

The agent provides the **decision-making and tool orchestration**.

The retrieval tool provides **access to the documents**.

The embeddings and vector store provide **semantic search**.

Streamlit provides the **user interface**.

Together, these components create a complete AI-powered document assistant.

---

# 📌 One-Sentence Summary

> **PDF Chatbot is a LangChain-powered agentic RAG application that splits uploaded PDFs into chunks, embeds them into a vector store, and lets an AI agent retrieve the most relevant passages to answer questions through a Streamlit chat interface.**

---

# 🏁 Conclusion

PDF Chatbot is a relatively small project, but it covers the core ideas behind most real-world RAG systems.

The most important thing to learn from it isn't the individual lines of code.

It is the architecture:

```text
Load → Chunk → Embed → Store → Retrieve → Generate
```

Notice how similar it is to the SQL Agent project in this repository:

```text
SQL Agent:    LLM + Agent + SQL tools       → Database
PDF Chatbot:  LLM + Agent + Retrieval tool  → Vector store
```

Only the tool changes. The agent pattern stays the same.

Once you understand this pattern, you can build much more sophisticated applications:

```text
PDF Chatbot
     ↓
Chat with a website
     ↓
Chat with a codebase
     ↓
Company knowledge assistant
     ↓
Research assistant with citations
     ↓
Multi-tool agent (RAG + SQL + web search)
```

The same fundamental idea keeps appearing:

```text
User
 ↓
LLM
 ↓
Agent
 ↓
Tools
 ↓
External Knowledge
 ↓
Result
 ↓
LLM
 ↓
User
```

That is one of the core patterns behind modern **agentic AI applications**.
