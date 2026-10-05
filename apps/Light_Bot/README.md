# ⚡ LightBot — Answer Before You Think

LightBot is a simple **AI agent web application** built with Python.

It combines:

- **Groq** → runs the Large Language Model
- **LangChain** → connects the model with tools
- **LangGraph** → manages the agent workflow and memory/checkpoints
- **Google Serper** → gives the agent access to web search
- **Streamlit** → provides the chat interface
- **python-dotenv** → loads API keys and configuration from `.env`

The goal of this project is not to build a huge production system.

The goal is to understand the fundamental building blocks behind modern AI agents:

> **LLM + Tools + Agent + Memory + Streaming + UI**

---

# 📌 What Does LightBot Do?

At first glance, LightBot looks like a normal chatbot.

You type:

```text
Who is the current CEO of Nvidia?
```

The application sends your question to an AI agent.

The agent can decide:

```text
I need current information.
↓
I should use the web search tool.
↓
Search the web.
↓
Read the result.
↓
Generate an answer.
↓
Stream the answer to the user.
```

So the application is more than:

```text
User → LLM → Answer
```

It is closer to:

```text
                 ┌───────────────┐
                 │     User      │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │   Streamlit   │
                 │  Chat UI      │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    Agent      │
                 │  LangChain    │
                 │  + LangGraph  │
                 └───────┬───────┘
                         │
                 ┌───────┴────────┐
                 │                │
                 ▼                ▼
          ┌────────────┐    ┌──────────────┐
          │    LLM     │    │ Web Search   │
          │   Groq     │    │   Serper     │
          └─────┬──────┘    └──────┬───────┘
                │                  │
                └────────┬─────────┘
                         ▼
                  Final AI response
                         │
                         ▼
                  Streamlit UI
```

---

# 🧠 Before Understanding the Code

There are six important concepts you should understand first.

## 1. LLM

An **LLM (Large Language Model)** is the AI model that understands text and generates responses.

Examples include:

- GPT models
- Llama models
- Qwen models
- Claude models
- Gemini models
- DeepSeek models

In this project, the LLM is accessed through **Groq**.

Your code creates it here:

```python
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    streaming=True
)
```

Think of `llm` as:

```text
llm = the AI brain
```

---

# 2. Tool

An LLM normally only knows what is available within its model/context.

A **tool** gives an AI agent the ability to perform an external action.

Examples:

```text
Web search
Database query
Calculator
Python execution
File reading
API request
Weather lookup
Email sending
```

Your project gives the agent one tool:

```text
Google Web Search
```

So the model can go from:

```text
"I don't know."
```

to:

```text
"I can search for the information."
```

---

# 3. Agent

A normal LLM application might work like this:

```text
User
 ↓
LLM
 ↓
Answer
```

An **agent** is more flexible.

An agent can determine:

```text
What does the user want?
        ↓
Can I answer directly?
        ↓
Do I need a tool?
        ↓
Which tool should I use?
        ↓
Use the tool
        ↓
Look at the result
        ↓
Generate the final answer
```

Therefore:

```text
LLM
+
Tools
+
Decision making
=
Agent
```

Your code creates the agent with:

```python
agent = create_agent(...)
```

---

# 4. Memory

Suppose you ask:

```text
My name is Anshul.
```

Then:

```text
What is my name?
```

A conversational AI should ideally understand that the second question refers to the first message.

That requires some form of **state/memory**.

This project has two separate state mechanisms.

### Streamlit history

```python
st.session_state.history
```

This is mainly used to remember what should be displayed in the UI.

### Agent checkpointing

```python
MemorySaver()
```

This allows the LangGraph agent to preserve its execution state across calls associated with the same thread.

LangGraph's current Python documentation describes in-memory checkpointing as a way to maintain short-term, thread-level state.

These two things should not be confused.

---

# 5. Streaming

Without streaming, the user might experience:

```text
[wait...]
[wait...]
[wait...]
[complete answer appears]
```

With streaming:

```text
Hello
Hello, I
Hello, I think
Hello, I think the
Hello, I think the answer...
```

The response appears progressively.

Your code enables streaming in the model:

```python
streaming=True
```

and then processes the response chunk by chunk.

---

# 6. Streamlit

Streamlit is a Python framework for building interactive web applications.

Instead of manually writing:

```text
HTML
CSS
JavaScript
Backend API
Frontend state management
```

you can create a simple UI directly in Python.

For example:

```python
st.chat_input("Ask Anything")
```

creates a chat input.

And:

```python
with st.chat_message("assistant"):
```

creates an assistant message container.

Streamlit provides dedicated chat components such as `st.chat_input` and `st.chat_message`, and its session state persists values across script reruns within a user session.

---

# 🏗️ Project Architecture

The complete application can be thought of as five layers.

```text
┌───────────────────────────────────────┐
│              Streamlit UI             │
│                                       │
│  Chat input                           │
│  Conversation display                │
└──────────────────┬────────────────────┘
                   │
                   ▼
┌───────────────────────────────────────┐
│                 Agent                 │
│                                       │
│       LangChain + LangGraph           │
└───────────────┬───────────┬───────────┘
                │           │
                │           │
                ▼           ▼
        ┌────────────┐   ┌──────────────┐
        │    Groq    │   │ Google Search│
        │    LLM     │   │    Tool      │
        └────────────┘   └──────────────┘
                │
                ▼
        ┌────────────────┐
        │   Checkpointer │
        │     Memory     │
        └────────────────┘
```

---

# 📁 Suggested Project Structure

A simple version of the project could look like this:

```text
lightbot/
│
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

Where:

```text
app.py
```

contains the Python application.

```text
.env
```

contains API keys.

```text
requirements.txt
```

contains Python dependencies.

```text
.gitignore
```

prevents sensitive files such as `.env` from being uploaded to GitHub.

```text
README.md
```

contains documentation.

---

# ⚙️ Installation

## Step 1 — Clone the repository

```bash
git clone <your-repository-url>
cd lightbot
```

---

## Step 2 — Create a virtual environment

It is recommended to use a virtual environment so project dependencies do not interfere with your system Python.

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

After activation, your terminal should show something similar to:

```text
(venv)
```

---

# 📦 Step 3 — Install Dependencies

Create:

```text
requirements.txt
```

with:

```text
python-dotenv
streamlit
langchain
langchain-core
langchain-community
langchain-groq
langgraph
```

Then install:

```bash
pip install -r requirements.txt
```

The project uses the `langchain-groq` integration for `ChatGroq`; the integration reads `GROQ_API_KEY` from the environment when no key is passed directly.

The web-search component uses `GoogleSerperAPIWrapper`, which expects a `SERPER_API_KEY`.

---

# 🔑 Step 4 — Create API Keys

This project requires two external services.

## Groq API

The LLM is accessed through Groq.

The environment variable expected by the LangChain Groq integration is:

```text
GROQ_API_KEY
```

---

## Serper API

The web search tool uses Serper.dev.

The expected environment variable is:

```text
SERPER_API_KEY
```

---

# 📝 Step 5 — Create `.env`

Create a file called:

```text
.env
```

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

Do **not** commit this file to GitHub.

---

# 🚫 Step 6 — Add `.env` to `.gitignore`

Your `.gitignore` should contain:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

This is important because API keys are secrets.

Never write:

```python
GROQ_API_KEY = "actual-secret-key"
```

directly into your source code.

---

# ▶️ Step 7 — Run the Application

Assuming the main file is:

```text
app.py
```

run:

```bash
streamlit run app.py
```

Streamlit will start a local web server.

You can then open the URL shown in your terminal.

---

# 🔍 Understanding the Code

Now let's go through the program from beginning to end.

---

# 1. Loading Environment Variables

```python
from dotenv import load_dotenv
load_dotenv()
```

The first line imports the `load_dotenv` function.

The second line executes it.

Its job is to load values from:

```text
.env
```

into the application's environment.

For example:

```env
GROQ_API_KEY=abc123
SERPER_API_KEY=xyz456
```

After:

```python
load_dotenv()
```

the libraries can find those values through environment variables.

Conceptually:

```text
.env
 │
 ▼
load_dotenv()
 │
 ▼
Environment variables
 │
 ├── GROQ_API_KEY
 └── SERPER_API_KEY
```

This lets your Python code avoid hard-coding secrets.

---

# 2. Importing Streamlit

```python
import streamlit as st
```

This imports Streamlit.

The alias:

```python
as st
```

means instead of writing:

```python
streamlit.chat_input(...)
```

you can write:

```python
st.chat_input(...)
```

Most Streamlit applications use this convention.

---

# 3. Importing the Groq LLM

```python
from langchain_groq import ChatGroq
```

This imports LangChain's Groq chat-model integration.

The purpose is to allow LangChain to communicate with a model hosted through Groq.

Think:

```text
Python application
       ↓
LangChain
       ↓
ChatGroq
       ↓
Groq API
       ↓
LLM
```

---

# 4. Importing Google Search

```python
from langchain_community.utilities import GoogleSerperAPIWrapper
```

This provides a wrapper around the Serper.dev search API.

It essentially gives Python a convenient interface for making web searches.

Without it, the model cannot directly search the web.

---

# 5. Importing LangChain's Tool Class

```python
from langchain_core.tools import Tool
```

A `Tool` is a standardized way of exposing an action to an agent.

You can think of a tool as:

```text
Name
Description
Function
```

For example:

```text
Name:
google_search

Description:
Search the web

Function:
search.run
```

The agent can then understand:

```text
There is a tool called google_search.
It can search the internet.
I can use it when necessary.
```

---

# 6. Importing create_agent

```python
from langchain.agents import create_agent
```

This function creates the agent.

The agent connects:

```text
LLM
+
Tools
+
Instructions
+
Optional state/checkpointing
```

into a system capable of deciding how to respond.

---

# 7. Importing MemorySaver

```python
from langgraph.checkpoint.memory import MemorySaver
```

This creates an in-memory checkpoint system.

A checkpoint stores the state of an agent execution.

The important idea is:

```text
Conversation
      ↓
Agent state
      ↓
Checkpoint
      ↓
Can be restored using thread ID
```

Current LangGraph Python documentation uses `InMemorySaver` for in-memory checkpointing and notes that in-memory checkpointing is intended for debugging/testing rather than production persistence. Some references also show `MemorySaver` as the compatible name, so the exact class name can depend on the installed LangGraph version.

---

# 🧠 LLM Section

The code then creates the model:

```python
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    streaming=True
)
```

Let's break this down.

## `ChatGroq`

This creates a Groq-backed chat model.

---

## `model`

```python
model="openai/gpt-oss-20b"
```

This tells Groq which model identifier the application should request.

In other words:

```text
Which model should answer the question?
```

The answer is determined by this value.

---

## `streaming=True`

```python
streaming=True
```

This tells the model interface that the application wants to receive generated output incrementally.

Conceptually:

Without streaming:

```text
LLM
 ↓
[generate entire answer]
 ↓
return answer
```

With streaming:

```text
LLM
 ↓
chunk 1
 ↓
chunk 2
 ↓
chunk 3
 ↓
chunk 4
 ↓
...
```

This allows the UI to feel much more responsive.

---

# 🔎 Creating the Search Tool

Next:

```python
search = GoogleSerperAPIWrapper()
```

This creates the search wrapper.

The wrapper knows how to communicate with Serper.

Now we need to turn it into a tool the agent understands.

---

## Creating the LangChain Tool

```python
search_tool = Tool(
    name="google_search",
    description="Search the web for current or factual information.",
    func=search.run
)
```

There are three particularly important parts.

### `name`

```python
name="google_search"
```

This is the tool's name.

The agent can conceptually think:

```text
Available tool:
google_search
```

---

### `description`

```python
description="Search the web for current or factual information."
```

This is very important.

The description tells the agent what the tool is for.

For example:

```text
User:
Who won the match yesterday?
```

The agent might reason:

```text
This information can change.
I have a web search tool.
The tool description says it is useful for current information.
I should use it.
```

The tool's description therefore helps the agent decide when the tool is appropriate.

---

### `func`

```python
func=search.run
```

This tells the tool what Python function should actually execute.

So:

```text
Agent calls google_search
        ↓
Tool invokes search.run(...)
        ↓
Serper API
        ↓
Search results
```

This is the bridge between:

```text
AI decision
```

and:

```text
real Python function
```

---

# 🧰 Creating the Tool List

```python
tools = [search_tool]
```

The agent expects tools to be supplied as a collection.

Currently you have only one:

```text
tools
 └── google_search
```

Later you could add:

```python
tools = [
    search_tool,
    calculator_tool,
    weather_tool,
    database_tool
]
```

Then the agent could potentially choose between them.

This is one of the most important ideas in agentic AI:

> The LLM doesn't need to contain every capability itself. You can give it tools that extend what it can do.

---

# 🧠 Memory Section

Now the code initializes Streamlit state.

```python
if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()
```

Why do we need this?

Remember that Streamlit reruns the Python script when the user interacts with the application. Session State is what allows values to persist across those reruns for a user's session.

The code checks:

```python
if "memory" not in st.session_state:
```

which means:

```text
Does this Streamlit session already have memory?
```

If not:

```python
st.session_state.memory = MemorySaver()
```

creates it.

The important part is that the object isn't recreated every time the script reruns.

---

# 💬 Conversation History

Next:

```python
if "history" not in st.session_state:
    st.session_state.history = []
```

This creates a Python list.

Initially:

```python
history = []
```

After the user asks something:

```python
[
    {
        "role": "user",
        "content": "What is Python?"
    }
]
```

Then the AI responds:

```python
[
    {
        "role": "user",
        "content": "What is Python?"
    },
    {
        "role": "assistant",
        "content": "Python is a programming language..."
    }
]
```

This list is used to redraw the chat interface after Streamlit reruns.

This pattern is also used in Streamlit's own conversational-app examples.

---

# 🤖 Creating the Agent

Now the most important part:

```python
agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt=(
        "You are a capable AI agent that can reason, use tools, "
        "and search the web to provide accurate answers."
    )
)
```

This combines all the previous pieces.

---

# `model=llm`

```python
model=llm
```

This tells the agent:

```text
Use this LLM as your brain.
```

---

# `tools=tools`

```python
tools=tools
```

This tells the agent:

```text
Here are the actions you are allowed to use.
```

Currently:

```text
google_search
```

---

# `checkpointer`

```python
checkpointer=st.session_state.memory
```

This gives the agent access to checkpointed state.

The checkpointer is what allows state to be associated with a conversation thread.

---

# `system_prompt`

```python
system_prompt=(
    "You are a capable AI agent that can reason, use tools, "
    "and search the web to provide accurate answers."
)
```

A system prompt provides high-level instructions for the model.

Think of it as:

```text
Role:
You are an AI agent.

Capabilities:
You can reason.
You can use tools.
You can search the web.

Goal:
Provide accurate answers.
```

This isn't the user's question.

It is an instruction describing how the assistant should behave.

---

# 🌐 Web Interface

Now we move away from the AI backend and start building the UI.

```python
st.subheader("⚡️ LightBot — Answer Before You Think ⚡️")
```

This simply displays a heading.

---

# 📜 Displaying Previous Messages

```python
for message in st.session_state.history:

    role = message["role"]
    content = message["content"]

    with st.chat_message(role):
        st.markdown(content)
```

This is responsible for displaying previous conversation messages.

Suppose:

```python
history = [
    {
        "role": "user",
        "content": "Hello"
    },
    {
        "role": "assistant",
        "content": "Hi!"
    }
]
```

The loop goes through each item.

First:

```python
role = "user"
content = "Hello"
```

Then:

```python
with st.chat_message("user"):
    st.markdown("Hello")
```

Then:

```python
role = "assistant"
content = "Hi!"
```

And:

```python
with st.chat_message("assistant"):
    st.markdown("Hi!")
```

Therefore the conversation gets reconstructed visually.

---

# ⌨️ User Input

```python
query = st.chat_input("Ask Anything")
```

This creates the chat input field.

When the user hasn't entered anything:

```python
query = None
```

After the user submits:

```python
query = "What is machine learning?"
```

Streamlit's chat input is designed to trigger the application when the user submits a message.

---

# 🚦 Processing the User's Question

```python
if query:
```

This means:

```text
Did the user actually submit a question?
```

If yes, everything inside the block runs.

---

# 👤 Displaying the User Message

```python
with st.chat_message("user"):
    st.markdown(query)
```

This immediately displays the user's message.

For example:

```text
User:
What is RAG?
```

---

# 💾 Saving the User Message

```python
st.session_state.history.append({
    "role": "user",
    "content": query
})
```

This adds the message to the history list.

Suppose:

```python
query = "What is RAG?"
```

Then:

```python
history
```

becomes:

```python
[
    {
        "role": "user",
        "content": "What is RAG?"
    }
]
```

This is important because Streamlit may rerun the entire script.

Without storing the message, it could disappear from the UI on the next run.

---

# 🧠 Sending the Question to the Agent

Now the application calls:

```python
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
```

This section looks complicated, so let's break it down.

---

# `agent.stream(...)`

Instead of:

```python
agent.invoke(...)
```

the application uses:

```python
agent.stream(...)
```

because we want the response to arrive incrementally.

Think:

```text
invoke()
    ↓
give me the final result

stream()
    ↓
give me pieces of the result as they become available
```

---

# 📩 Message Input

This:

```python
{
    "messages": [
        {
            "role": "user",
            "content": query
        }
    ]
}
```

represents the input being sent to the agent.

If:

```python
query = "Explain RAG"
```

then conceptually:

```python
{
    "messages": [
        {
            "role": "user",
            "content": "Explain RAG"
        }
    ]
}
```

The agent receives that message and begins processing it.

---

# 🧵 What Is `thread_id`?

This:

```python
{
    "configurable": {
        "thread_id": "1"
    }
}
```

is extremely important for memory.

A thread ID tells LangGraph:

```text
Which conversation does this state belong to?
```

For example:

```text
thread_id = "user_123"
```

could represent one conversation.

Another:

```text
thread_id = "user_456"
```

could represent another.

Conceptually:

```text
Thread 1
 ├── User message
 ├── Agent response
 ├── User message
 └── Agent response

Thread 2
 ├── User message
 └── Agent response
```

LangGraph's persistence model uses `thread_id` to associate checkpoints with a conversation/thread.

Your current project uses:

```python
thread_id="1"
```

which is perfectly fine for a simple learning project.

For a larger application, you would normally generate or assign unique conversation IDs.

---

# 📡 `stream_mode="messages"`

```python
stream_mode="messages"
```

This tells the agent streaming mechanism that you want message-level streaming output.

The result can therefore be iterated over:

```python
for chunk, metadata in response:
```

---

# 🤖 Displaying the AI Response

First:

```python
message = ""
```

This creates an empty string.

Initially:

```text
message = ""
```

Then:

```python
with st.chat_message("assistant"):
```

creates an assistant chat container.

---

# 🧩 Placeholder

```python
space = st.empty()
```

`st.empty()` creates an empty placeholder.

We can later replace its contents.

This is useful for streaming.

Imagine the response arrives like this:

```text
chunk 1 = "Hello"
chunk 2 = " there"
chunk 3 = "!"
```

Instead of creating three different UI messages, the application keeps updating the same placeholder.

---

# 🔄 Receiving Chunks

```python
for chunk, metadata in response:
```

The response is streamed piece by piece.

For example:

```text
chunk 1 → "Hello"
chunk 2 → "!"
chunk 3 → " How"
chunk 4 → " are"
chunk 5 → " you?"
```

Each iteration processes another piece.

---

# Checking Content

```python
if chunk.content:
```

Not every streamed event necessarily needs to be displayed as text.

So the code checks whether the chunk contains actual content.

---

# Building the Complete Response

```python
message += chunk.content
```

Suppose:

```text
chunk 1 = "Hello"
chunk 2 = " there"
chunk 3 = "!"
```

The variable changes like this:

```text
message = ""

message = "Hello"

message = "Hello there"

message = "Hello there!"
```

---

# Updating the UI

```python
space.markdown(message)
```

The placeholder is updated with the current response.

So the user sees:

```text
Hello
```

then:

```text
Hello there
```

then:

```text
Hello there!
```

This produces the streaming effect.

---

# 💾 Saving the Final Assistant Message

Once streaming finishes, the complete message is stored:

```python
st.session_state.history.append({
    "role": "assistant",
    "content": message
})
```

So the history becomes:

```python
[
    {
        "role": "user",
        "content": "What is RAG?"
    },
    {
        "role": "assistant",
        "content": "RAG stands for Retrieval-Augmented Generation..."
    }
]
```

The next time Streamlit reruns, the earlier messages can be displayed again.

---

# 🔁 Complete Execution Flow

Let's put the entire application together.

Suppose the user asks:

```text
Who is the CEO of Nvidia?
```

The flow looks like this:

```text
1. User enters question
            │
            ▼
2. Streamlit receives input
            │
            ▼
3. Save user message
            │
            ▼
4. Send message to agent
            │
            ▼
5. Agent receives question
            │
            ▼
6. LLM decides whether a tool is needed
            │
            ▼
7. Agent chooses Google Search
            │
            ▼
8. Google Search executes
            │
            ▼
9. Search result is returned
            │
            ▼
10. LLM processes search result
            │
            ▼
11. Agent generates final answer
            │
            ▼
12. Response streams chunk-by-chunk
            │
            ▼
13. Streamlit displays chunks
            │
            ▼
14. Complete answer is saved
```

---

# 🧠 Why Use an Agent Instead of Directly Calling the LLM?

You could create a chatbot like:

```python
response = llm.invoke(query)
```

This would work.

But then:

```text
User
 ↓
LLM
 ↓
Answer
```

The LLM doesn't automatically have access to your search API.

Your agent adds another layer:

```text
User
 ↓
Agent
 ↓
┌───────────────┐
│ Does the      │
│ question need │
│ a tool?       │
└───────┬───────┘
        │
    ┌───┴───┐
    │       │
   No      Yes
    │       │
    ▼       ▼
   LLM    Search
            │
            ▼
           LLM
            │
            ▼
         Answer
```

This is the fundamental idea behind tool-using agents.

---

# 🆚 Chatbot vs Agent

## Basic chatbot

```text
User
 ↓
LLM
 ↓
Response
```

Examples:

```text
"What is Python?"
```

The model can answer from its existing knowledge.

---

## Tool-using agent

```text
User
 ↓
Agent
 ↓
Decision
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Answer
```

Example:

```text
"What happened in the stock market today?"
```

The agent can recognize that current information is required and use the search tool.

---

# 🧩 Why LangChain?

You could build everything manually.

For example:

```python
if user_needs_search:
    call_search_api()

send_result_to_model()

generate_answer()
```

But as the application grows, this becomes complicated.

LangChain provides abstractions for things like:

```text
Models
Tools
Messages
Agents
Structured interactions
Integrations
```

This allows you to focus on the application's behavior rather than implementing every integration yourself.

---

# 🧩 Why LangGraph?

LangGraph is useful when applications need stateful, multi-step workflows.

Conceptually, an agent may do:

```text
START
 ↓
Understand request
 ↓
Decide whether tool is needed
 ↓
Call tool
 ↓
Read result
 ↓
Generate answer
 ↓
END
```

That is a graph-like workflow.

The checkpointer allows state from that workflow to be persisted by thread.

---

# 🧠 Two Different Types of "History" in This Project

This is one of the most important things to understand.

Your code has:

```python
st.session_state.history
```

and:

```python
st.session_state.memory
```

They are not the same thing.

---

## `history`

```python
st.session_state.history
```

Purpose:

```text
UI conversation history
```

It stores:

```text
user message
assistant message
user message
assistant message
```

so Streamlit knows what to display.

---

## `memory`

```python
st.session_state.memory = MemorySaver()
```

Purpose:

```text
Agent checkpoint/state
```

This is related to LangGraph's state persistence.

---

# ⚠️ Important Limitation of the Current Memory Setup

Your current code uses:

```python
MemorySaver()
```

which stores state **in memory**.

That means it is useful for learning, development and testing, but it is not a proper production database.

If the process disappears, the in-memory state disappears too.

Current LangGraph documentation recommends persistent checkpoint backends such as PostgreSQL for production workloads rather than an in-memory saver.

A production architecture could eventually look like:

```text
Streamlit / API
      │
      ▼
    Agent
      │
      ▼
PostgreSQL
      │
      ├── conversation state
      ├── checkpoints
      └── application data
```

---

# ⚠️ Another Important Limitation: Fixed Thread ID

The code currently contains:

```python
"thread_id": "1"
```

This means every invocation inside this application session is assigned to the same thread.

That's useful for learning because it creates one continuous conversation.

For a real application with many users or many conversations, you should generate a distinct ID.

For example:

```python
thread_id = str(uuid.uuid4())
```

or derive it from your authenticated user/conversation ID.

Conceptually:

```text
User A
 └── thread-a

User B
 └── thread-b

User C
 └── thread-c
```

rather than:

```text
Everyone
   │
   └── thread-1
```

---

# 🧪 Example: Question That Doesn't Need Search

User:

```text
What is a Python list?
```

Possible flow:

```text
User question
     ↓
Agent
     ↓
LLM determines search isn't necessary
     ↓
Generate answer
     ↓
Stream answer
```

No external tool may be required.

---

# 🌐 Example: Question That Needs Search

User:

```text
What is the latest version of Python?
```

Possible flow:

```text
User question
      ↓
Agent
      ↓
Information may have changed
      ↓
Use google_search
      ↓
Serper
      ↓
Search results
      ↓
LLM
      ↓
Final answer
```

The key idea is that **the agent decides whether a tool should be used**.

---

# 🛠️ Adding Another Tool

One of the easiest ways to learn agentic AI is to add another tool.

Suppose you create:

```python
calculator_tool
```

You could then have:

```python
tools = [
    search_tool,
    calculator_tool
]
```

The agent now has two capabilities:

```text
google_search
calculator
```

The architecture becomes:

```text
                    ┌── Google Search
                    │
User → Agent ───────┤
                    │
                    └── Calculator
```

This is the beginning of a multi-tool agent.

---

# 💡 Possible Tools You Can Add

Once the basic application works, interesting next tools include:

```text
Calculator
Weather API
Wikipedia
SQL database
PostgreSQL
Python execution
File search
PDF search
GitHub API
News search
Vector database
```

For example:

```text
User:
What is the population of India and what is 15% of it?

Agent:
1. Search current population
2. Send number to calculator
3. Generate answer
```

Now the agent becomes a multi-step system.

---

# 📚 What You Should Learn From This Project

This small project teaches several important AI engineering concepts.

## Beginner Level

Understand:

```text
Python imports
Environment variables
APIs
Streamlit
LLMs
Prompting
Chat interfaces
```

---

## Intermediate Level

Understand:

```text
LangChain
Tools
Agents
Streaming
Message objects
Session state
Thread IDs
Checkpointing
```

---

## Advanced Next Steps

After understanding this project, explore:

```text
LangGraph workflows
Agent state
Tool calling
Structured output
RAG
Vector databases
Evaluation
Observability
MCP
Agentic workflows
MLOps
Production memory
```

---

# 🧪 How to Learn This Code Efficiently

Don't memorize the entire code.

Instead, understand these five relationships:

```text
LLM
 ↓
provides intelligence

Tool
 ↓
provides capabilities

Agent
 ↓
decides how to use capabilities

Checkpointer
 ↓
preserves agent state

Streamlit
 ↓
provides the user interface
```

Once those five concepts are clear, most of the code becomes straightforward.

---

# 🗺️ Recommended Learning Order

If you are completely new to this project, learn in this order:

```text
1. Python basics
      ↓
2. Environment variables
      ↓
3. APIs
      ↓
4. LLMs
      ↓
5. LangChain models
      ↓
6. LangChain tools
      ↓
7. Agents
      ↓
8. LangGraph
      ↓
9. Memory / checkpointing
      ↓
10. Streaming
      ↓
11. Streamlit
      ↓
12. Production architecture
```

Do not jump directly into complicated agent frameworks without understanding what an LLM, API, tool and Python function are doing first.

---

# 🔐 Security

Never commit:

```text
.env
```

to GitHub.

Your `.env` contains credentials such as:

```text
GROQ_API_KEY
SERPER_API_KEY
```

Use:

```gitignore
.env
```

If a key accidentally gets pushed to GitHub, revoke it and generate a new one.

---

# 🐛 Common Problems

## 1. `GROQ_API_KEY` error

You may see an error indicating that the Groq API key is missing.

Check:

```text
.env
```

contains:

```env
GROQ_API_KEY=your_key
```

and that:

```python
load_dotenv()
```

runs before the model is created.

The Groq LangChain integration expects `GROQ_API_KEY` unless a key is passed directly.

---

## 2. `SERPER_API_KEY` error

Check:

```env
SERPER_API_KEY=your_key
```

The `GoogleSerperAPIWrapper` expects this environment variable unless the key is supplied explicitly.

---

## 3. Agent doesn't search

Check the tool description:

```python
description="Search the web for current or factual information."
```

The model uses the available tool definitions to understand what the tool is for.

You should therefore write tool descriptions that are:

```text
clear
specific
accurate
```

---

## 4. Memory disappears

Remember that:

```python
MemorySaver()
```

is in-memory storage.

It is not permanent database storage.

Restarting the application can therefore remove the stored state.

---

## 5. `.env` doesn't work

Check that:

```text
.env
```

is in the correct project directory.

For example:

```text
lightbot/
├── app.py
├── .env
└── requirements.txt
```

and that you are running:

```bash
streamlit run app.py
```

from the project environment.

---

# 🚀 Possible Improvements

This project is intentionally simple.

A more advanced version could add:

## 1. Unique conversation IDs

Instead of:

```python
thread_id="1"
```

use a unique ID for each conversation.

---

## 2. Persistent memory

Replace in-memory checkpointing with a production storage system such as PostgreSQL.

LangGraph's current documentation lists PostgreSQL-based checkpointing as an appropriate production option.

---

## 3. More tools

Add:

```text
Calculator
Weather
Database
Wikipedia
File search
```

---

## 4. Better UI

Add:

```text
Sidebar
New conversation
Conversation list
Clear chat
Model selection
Tool status
Loading indicators
Error messages
```

---

## 5. Tool visibility

Display something like:

```text
🔎 Searching the web...
```

before showing the final answer.

This makes the agent's behavior easier to understand.

---

## 6. Observability

For a production AI application, eventually add tracing and monitoring.

You may want to track:

```text
Latency
Token usage
Tool calls
Errors
Model responses
Costs
User feedback
```

---

## 7. Evaluation

Don't only ask:

```text
"Does the chatbot work?"
```

Create test questions and measure:

```text
Answer correctness
Tool selection
Tool accuracy
Latency
Failure rate
```

This becomes especially important as the number of tools and complexity of the agent increase.

---

# 🧠 The Most Important Mental Model

When looking at this entire project, remember:

```text
                 ┌─────────────┐
                 │    USER     │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  STREAMLIT  │
                 │     UI      │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │    AGENT    │
                 └──────┬──────┘
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
        ┌─────────┐          ┌────────────┐
        │   LLM   │          │   TOOLS    │
        │  Groq   │          │  Search    │
        └────┬────┘          └─────┬──────┘
             │                     │
             └──────────┬──────────┘
                        ▼
                 ┌─────────────┐
                 │    STATE    │
                 │ Checkpoints │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │   ANSWER    │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  STREAMLIT  │
                 │   DISPLAY   │
                 └─────────────┘
```

In one sentence:

> **LightBot is a Streamlit chat application that uses a Groq-hosted LLM inside a LangChain/LangGraph agent, gives that agent a Serper web-search tool, maintains conversational state, and streams the generated response back to the user.**

---

# 📦 Complete Minimal Code

For reference, the complete application is:

```python
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    streaming=True
)


# ============================================================
# TOOL - GOOGLE SEARCH
# ============================================================

search = GoogleSerperAPIWrapper()

search_tool = Tool(
    name="google_search",
    description="Search the web for current or factual information.",
    func=search.run
)

tools = [search_tool]


# ============================================================
# MEMORY
# ============================================================

if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# AGENT
# ============================================================

agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt=(
        "You are a capable AI agent that can reason, use tools, "
        "and search the web to provide accurate answers."
    )
)


# ============================================================
# WEB INTERFACE
# ============================================================

st.subheader("⚡️ LightBot — Answer Before You Think ⚡️")


# Display previous conversation
for message in st.session_state.history:

    role = message["role"]
    content = message["content"]

    with st.chat_message(role):
        st.markdown(content)


# Get user input
query = st.chat_input("Ask Anything")


if query:

    # Display user message
    with st.chat_message("user"):
        st.markdown(query)

    # Save user message
    st.session_state.history.append({
        "role": "user",
        "content": query
    })

    # Run agent
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

    # Stream response
    message = ""

    with st.chat_message("assistant"):

        space = st.empty()

        for chunk, metadata in response:

            if chunk.content:

                message += chunk.content

                space.markdown(message)

    # Save final response
    st.session_state.history.append({
        "role": "assistant",
        "content": message
    })


# ============================================================
# END
# ============================================================
```

---

# 📚 Key Concepts to Remember

| Concept | Meaning |
|---|---|
| LLM | The AI model that generates text |
| Groq | Provider used to access the model |
| LangChain | Framework providing model/tool/agent abstractions |
| LangGraph | Framework for stateful agent workflows |
| Agent | System that can decide when/how to use tools |
| Tool | External capability available to the agent |
| Serper | Service used to perform web searches |
| `Tool` | LangChain wrapper exposing a Python function to the agent |
| Checkpointer | Saves agent execution state |
| `MemorySaver` | In-memory checkpoint implementation |
| `thread_id` | Identifier for a conversation/thread |
| Streamlit | Python framework used for the web UI |
| Session State | State that survives Streamlit reruns during a session |
| Streaming | Returning generated output incrementally |
| `.env` | Local file containing configuration/secrets |

---

# 🎯 What This Project Represents

This project is small, but conceptually it contains the basic architecture of a modern AI agent:

```text
             MODERN AI AGENT
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼           ▼           ▼
      LLM        TOOLS       STATE
       │           │           │
       │           │           │
       └───────────┼───────────┘
                   │
                   ▼
                AGENT
                   │
                   ▼
              APPLICATION
```

Once you understand this project properly, you have a strong foundation for moving toward more advanced systems such as:

```text
RAG
Agentic RAG
Multi-agent systems
MCP
Tool-use agents
LLM evaluation
Agent observability
Production memory
AI APIs
MLOps
```

The most important thing is not memorizing the syntax.

The important thing is understanding **why each component exists and how the components communicate with one another**.