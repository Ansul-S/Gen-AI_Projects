from dotenv import load_dotenv

load_dotenv()

import uuid
from pathlib import Path

import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================
# DATABASE
# ============================================================

# Resolve the DB next to this file so it's the same DB no matter where
# `streamlit run` is launched from
DB_PATH = Path(__file__).resolve().parent / "my_tasks.db"

db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

db.run(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK (
            status IN ('pending', 'in_progress', 'completed')
        ) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)


# ============================================================
# LLM
# ============================================================

model = ChatGroq(
    model="openai/gpt-oss-20b"
)


# ============================================================
# SQL TOOLS
# ============================================================

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)

tools = toolkit.get_tools()


# ============================================================
# SYSTEM PROMPT
# ============================================================

system_prompt = """
You are TaskBot, a task management assistant that manages tasks
stored in a SQL database.

DATABASE:
The database contains one table called `tasks`.

Table schema:

- id: INTEGER PRIMARY KEY
- title: TEXT NOT NULL
- description: TEXT
- status: TEXT
  Allowed values: pending, in_progress, completed
- created_at: TIMESTAMP

CRUD OPERATIONS:

CREATE:
Use INSERT INTO tasks.

READ:
Use SELECT queries.

UPDATE:
Use UPDATE tasks.

DELETE:
Use DELETE FROM tasks.

IMPORTANT RULES:

1. Never modify the database structure.
   Do not CREATE, DROP, ALTER, or TRUNCATE tables.

2. For SELECT queries:
   - Return a maximum of 10 tasks.
   - Prefer ordering by created_at DESC.
   - Example:
     SELECT *
     FROM tasks
     ORDER BY created_at DESC
     LIMIT 10;

3. After every INSERT, UPDATE, or DELETE:
   - Run a SELECT query to verify that the operation succeeded.
   - Only tell the user the operation succeeded after verification.

4. When creating a task:
   - title is required.
   - description is optional.
   - status defaults to 'pending'.
   - Only use these statuses:
     pending
     in_progress
     completed

5. When updating or deleting a task:
   - Prefer using the task ID when available.
   - If the user provides a title instead, search for the matching task first.
   - If multiple tasks have the same title, ask the user which task they mean.

6. Never invent task IDs or task information.

7. If a requested task does not exist, clearly tell the user.

8. For task lists, present the results in a clean Markdown table.

9. Keep responses concise and useful.

10. Before executing a destructive operation such as DELETE,
    make sure the intended task is unambiguous.
"""


# ============================================================
# AGENT
# ============================================================

@st.cache_resource
def get_agent():
    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
    )

    return agent


agent = get_agent()


# ============================================================
# STREAMLIT UI
# ============================================================

st.title("📜 TaskBot")
st.caption("Manage your tasks using natural language.")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# One conversation thread per browser session (the cached agent is shared
# across all sessions, so a fixed thread_id would mix everyone's chats)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input("Ask me to manage your tasks...")


if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Processing..."):

            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ]
                },
                {
                    "configurable": {
                        "thread_id": st.session_state.thread_id
                    }
                },
            )

            result = response["messages"][-1].content

            st.markdown(result)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result,
        }
    )