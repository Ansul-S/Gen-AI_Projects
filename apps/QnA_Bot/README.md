# 🤖 Answers Of Your Questions

A beginner-friendly **AI Question & Answer chatbot** built with **Python, Streamlit, LangChain, and Google Gemini**.

The goal of this project is to demonstrate how to connect a Large Language Model (LLM) to a simple web interface and create an interactive chatbot.

> **Project level:** Beginner → Intermediate
> **Main concepts:** LLMs, Generative AI, LangChain, Streamlit, API keys, chat history, environment variables

---

# 📌 Table of Contents

1. [What is this project?](#-what-is-this-project)
2. [What does the application do?](#-what-does-the-application-do)
3. [What does the application look like?](#-what-does-the-application-look-like)
4. [Technologies Used](#-technologies-used)
5. [How the Application Works](#-how-the-application-works)
6. [Project Structure](#-project-structure)
7. [Requirements](#-requirements)
8. [Installation](#-installation)
9. [Getting a Google Gemini API Key](#-getting-a-google-gemini-api-key)
10. [Creating the `.env` File](#-creating-the-env-file)
11. [Complete Code](#-complete-code)
12. [Understanding the Code](#-understanding-the-code)
13. [How `load_dotenv()` Works](#-how-loaddotenv-works)
14. [How LangChain Works](#-how-langchain-works)
15. [How Gemini Works](#-how-gemini-works)
16. [How Streamlit Works](#-how-streamlit-works)
17. [Understanding `st.session_state`](#-understanding-stsession_state)
18. [Understanding `llm.invoke()`](#-understanding-llminvoke)
19. [How the Chat History Works](#-how-the-chat-history-works)
20. [Running the Application](#-running-the-application)
21. [Common Errors](#-common-errors)
22. [Security](#-security)
23. [Git and GitHub](#-git-and-github)
24. [Deployment](#-deployment)
25. [Possible Improvements](#-possible-improvements)
26. [Learning Path](#-learning-path)
27. [Conclusion](#-conclusion)

---

# 🧠 What is this project?

This project is a simple **Generative AI chatbot**.

You type a question:

```text
What is Generative AI?
```

The application sends your question to Google's Gemini Large Language Model.

Gemini generates an answer:

```text
Generative AI is a type of artificial intelligence
that can create new content such as text, images,
audio, video, and code...
```

The answer is then displayed on the website.

The entire process looks like this:

```text
                 USER
                  │
                  │
                  ▼
          ┌───────────────┐
          │   Streamlit   │
          │   Web UI      │
          └───────┬───────┘
                  │
                  │ Question
                  ▼
          ┌───────────────┐
          │   LangChain   │
          └───────┬───────┘
                  │
                  │ API Request
                  ▼
          ┌───────────────┐
          │ Google Gemini │
          │     LLM       │
          └───────┬───────┘
                  │
                  │ Generated Answer
                  ▼
          ┌───────────────┐
          │   Streamlit   │
          │   Chat UI     │
          └───────┬───────┘
                  │
                  ▼
                 USER
```

---

# 🚀 What does the application do?

The chatbot currently provides:

* 💬 Interactive chat interface
* 🤖 Google Gemini as the AI model
* 🔗 LangChain integration
* 🖥️ Streamlit web interface
* 🧠 Chat history displayed during the session
* 🔐 API key stored using environment variables
* 🐍 Completely Python-based implementation

---

# 🖥️ What does the application look like?

The application contains:

```text
Answers Of Your Questions 😀

My QnA Bot with LangChain and Google Gemini!

User:
[ Ask Anything?                         ]
```

When you ask a question, it displays:

```text
User
What is GenAI?

AI
GenAI stands for Generative Artificial Intelligence...
```

---

# 🛠️ Technologies Used

## 1. Python

Python is the programming language used to build the entire application.

Python is popular in AI and Machine Learning because it has a huge ecosystem of libraries.

---

## 2. Google Gemini

Gemini is the Large Language Model responsible for generating the answers.

We communicate with Gemini through an API.

The model used in this project is:

```text
gemini-3.5-flash-lite
```

The model receives a question and generates a response.

---

## 3. LangChain

LangChain provides a convenient framework for working with Large Language Models.

Instead of manually handling every API request, we can create:

```python
llm = ChatGoogleGenerativeAI(...)
```

and then call:

```python
llm.invoke(query)
```

---

## 4. Streamlit

Streamlit turns our Python code into a web application.

Without Streamlit, we would need to build:

* HTML
* CSS
* JavaScript
* Backend routes
* Frontend logic

With Streamlit, we can create a basic interface directly using Python.

For example:

```python
st.title("My AI Bot")
```

creates a title.

And:

```python
st.chat_input("Ask Anything?")
```

creates a chat input box.

---

## 5. python-dotenv

`python-dotenv` allows us to load environment variables from a `.env` file.

This is useful for storing secrets such as API keys.

Instead of writing:

```python
API_KEY = "my-secret-key"
```

inside our Python code, we keep it inside:

```text
.env
```

---

# 🔄 How the Application Works

The entire application can be understood in six steps.

### Step 1 — Load environment variables

```python
load_dotenv()
```

This loads values from `.env`.

---

### Step 2 — Create Gemini LLM

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)
```

This creates our connection to Gemini through LangChain.

---

### Step 3 — Create Streamlit interface

```python
st.title(...)
st.markdown(...)
```

This creates the website's title and description.

---

### Step 4 — Create chat history

```python
st.session_state.messages
```

This stores messages while the Streamlit session is running.

---

### Step 5 — Receive the user's question

```python
query = st.chat_input("Ask Anything?")
```

The user enters a question.

---

### Step 6 — Ask Gemini

```python
res = llm.invoke(query)
```

The question is sent to Gemini.

Then we extract the answer:

```python
answer = res.content[0]["text"]
```

Finally, we display it:

```python
st.chat_message("ai").markdown(answer)
```

---

# 📁 Project Structure

A simple project structure can look like:

```text
QnA-Bot/
│
├── QnA_Bot.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

Let's understand every file.

---

## `QnA_Bot.py`

This is the main Python program.

It contains:

* Gemini configuration
* Streamlit interface
* Chat history
* User input
* AI response handling

---

## `.env`

This contains secret environment variables.

Example:

```text
GOOGLE_API_KEY=your_api_key_here
```

**Never upload this file to GitHub.**

---

## `.gitignore`

This tells Git which files it should not upload to the repository.

Example:

```gitignore
.env
.env.*
notebooks/
__pycache__/
.venv/
```

---

## `README.md`

This file explains the project.

It is the document you are reading right now.

---

## `requirements.txt`

This file contains the Python packages required by the project.

Example:

```text
streamlit
langchain-google-genai
python-dotenv
```

---

# 💻 Requirements

Before starting, you need:

* Python 3.10+
* Internet connection
* Google Gemini API key
* Basic command-line knowledge

You don't need to know HTML, CSS, or JavaScript to build this version.

---

# 📦 Installation

## Step 1 — Clone the repository

If you downloaded the project from GitHub:

```bash
git clone YOUR_REPOSITORY_URL
```

Then:

```bash
cd QnA-Bot
```

---

# 🐍 Step 2 — Create a Virtual Environment

A virtual environment keeps this project's packages separate from your other Python projects.

Run:

```bash
python -m venv .venv
```

---

## Activate the environment on macOS/Linux

```bash
source .venv/bin/activate
```

---

## Activate on Windows

```bash
.venv\Scripts\activate
```

After activation, your terminal may show:

```text
(.venv)
```

That means the environment is active.

---

# 📥 Step 3 — Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit langchain-google-genai python-dotenv
```

---

# 🔑 Getting a Google Gemini API Key

You need an API key so that your application can communicate with Google's Gemini API.

Create an API key through Google's Gemini/AI developer platform.

Your key will look approximately like:

```text
AIzaSy................................
```

Keep this key private.

---

# 🔐 Creating the `.env` File

Inside your project folder, create:

```text
.env
```

Put your API key inside it.

For example:

```env
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

Replace:

```text
YOUR_API_KEY_HERE
```

with your actual key.

---

# ⚠️ IMPORTANT: Never Commit `.env`

Your `.env` file contains a secret.

Your `.gitignore` should contain:

```gitignore
.env
.env.*
```

This prevents Git from tracking it.

Never do this:

```python
GOOGLE_API_KEY = "AIzaSy........"
```

inside your source code.

---

# 🧑‍💻 Complete Code

The complete `QnA_Bot.py` file:

```python
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

    # Extract the actual text
    answer = res.content[0]["text"]

    # Display AI response
    st.chat_message("ai").markdown(answer)

    # Save AI response
    st.session_state.messages.append({
        "role": "ai",
        "content": answer
    })
```

---

# 🔍 Understanding the Code

Now let's understand **every important part**.

---

## 1. Importing `load_dotenv`

```python
from dotenv import load_dotenv
```

This imports the `load_dotenv` function from the `python-dotenv` package.

Think of it like telling Python:

> "I want to use the function that reads my `.env` file."

---

# 2. Loading `.env`

```python
load_dotenv()
```

This searches for a `.env` file and loads the variables stored inside it.

For example:

```env
GOOGLE_API_KEY=abc123
```

can then be accessed by libraries that look for environment variables.

---

# 3. Importing Gemini integration

```python
from langchain_google_genai import ChatGoogleGenerativeAI
```

This imports LangChain's Google Gemini chat model integration.

In simple terms:

```text
Python
  ↓
LangChain
  ↓
Google Gemini
```

LangChain acts as a convenient interface between your Python application and the Gemini model.

---

# 4. Importing Streamlit

```python
import streamlit as st
```

This imports Streamlit.

We give it the shorter name:

```python
st
```

That's why we can write:

```python
st.title()
```

instead of:

```python
streamlit.title()
```

---

# 5. Creating the Gemini model

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)
```

This creates an LLM object.

`llm` stands for:

```text
Large Language Model
```

The model name tells LangChain which Gemini model to use.

You can think of it as:

```text
llm = our AI
```

Then we can ask it questions.

---

# 6. Creating the title

```python
st.title("Answers Of Your Questions 😀")
```

This creates the main title of the Streamlit application.

---

# 7. Creating the description

```python
st.markdown(
    "My QnA Bot with LangChain and Google Gemini!"
)
```

`st.markdown()` displays Markdown text.

Markdown lets you format text using things like:

```text
**bold**
*italic*
# headings
```

---

# 8. Understanding Session State

This is one of the most important parts:

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

Streamlit reruns your Python script whenever the user interacts with the application.

Without session state, variables could disappear between reruns.

`st.session_state` gives us a place to store information during the user's session.

We create:

```python
st.session_state.messages
```

and make it an empty list:

```python
[]
```

---

# 9. Why do we need a list?

Because we need to store multiple messages.

For example:

```python
[
    {
        "role": "user",
        "content": "What is GenAI?"
    },
    {
        "role": "ai",
        "content": "GenAI stands for Generative AI..."
    }
]
```

The list can continue growing:

```text
User message
      ↓
AI message
      ↓
User message
      ↓
AI message
      ↓
...
```

---

# 10. Displaying Previous Messages

We use:

```python
for message in st.session_state.messages:
```

This means:

> "Go through every message stored in our chat history."

For example:

```python
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "ai", "content": "Hi!"}
]
```

The loop processes:

```text
Hello
Hi!
```

one at a time.

---

# 11. Getting the Role

Inside the loop:

```python
role = message["role"]
```

The role can be:

```text
user
```

or:

```text
ai
```

For example:

```python
{
    "role": "user",
    "content": "Hello"
}
```

gives:

```python
role = "user"
```

---

# 12. Getting the Message

```python
content = message["content"]
```

This retrieves the actual text.

For:

```python
{
    "role": "user",
    "content": "Hello"
}
```

we get:

```text
Hello
```

---

# 13. Displaying Chat Messages

```python
st.chat_message(role).markdown(content)
```

This creates a Streamlit chat message.

If:

```python
role = "user"
```

Streamlit displays it as a user message.

If:

```python
role = "ai"
```

it displays it as an AI message.

---

# 14. Creating the Chat Input

```python
query = st.chat_input("Ask Anything?")
```

This creates the input box at the bottom of the application.

When the user enters:

```text
What is GenAI?
```

the value of:

```python
query
```

becomes:

```text
"What is GenAI?"
```

---

# 15. Checking if the User Entered Something

```python
if query:
```

This means:

> "Only continue if the user actually entered a question."

If the input is empty, the code inside the `if` block doesn't execute.

---

# 16. Displaying the User Question

```python
st.chat_message("user").markdown(query)
```

This displays the question in the chat interface.

For example:

```text
👤 User

What is GenAI?
```

---

# 17. Saving the User Question

```python
st.session_state.messages.append({
    "role": "user",
    "content": query
})
```

`.append()` adds something to the end of a list.

So:

```python
[]
```

becomes:

```python
[
    {
        "role": "user",
        "content": "What is GenAI?"
    }
]
```

---

# 18. Sending the Question to Gemini

This is the most important line:

```python
res = llm.invoke(query)
```

`invoke()` sends the question to the LLM.

Conceptually:

```text
query
  ↓
LangChain
  ↓
Gemini API
  ↓
Gemini model
  ↓
response
```

For example:

```python
query = "Who is Cristiano Ronaldo?"
```

Gemini processes the question and returns a response.

---

# 19. Understanding `res`

The result is stored in:

```python
res
```

It is not simply a Python string.

It is a LangChain message object containing the model's response and metadata.

The text response can be extracted from the content structure.

In this project we use:

```python
answer = res.content[0]["text"]
```

---

# 20. Understanding `res.content[0]["text"]`

This looks complicated at first.

Break it down.

### `res`

The complete response.

### `.content`

The content returned by the model.

### `[0]`

Get the first content block.

### `["text"]`

Get the actual text from that block.

So:

```python
res.content[0]["text"]
```

means:

> "Give me the text inside the first content block of the Gemini response."

---

# 21. Displaying the AI Answer

```python
st.chat_message("ai").markdown(answer)
```

This displays the Gemini response in the chat interface.

---

# 22. Saving the AI Answer

Finally:

```python
st.session_state.messages.append({
    "role": "ai",
    "content": answer
})
```

This saves the AI response into our chat history.

Now our list looks like:

```python
[
    {
        "role": "user",
        "content": "What is GenAI?"
    },
    {
        "role": "ai",
        "content": "Generative AI is..."
    }
]
```

---

# 🔁 Complete Data Flow

Let's put everything together.

Suppose the user types:

```text
What is RAG?
```

The following happens:

```text
                    USER
                      │
                      │
                "What is RAG?"
                      │
                      ▼
              st.chat_input()
                      │
                      ▼
                   query
                      │
                      ▼
             llm.invoke(query)
                      │
                      ▼
               LangChain
                      │
                      ▼
              Google Gemini
                      │
                      ▼
                 Response
                      │
                      ▼
             res.content
                      │
                      ▼
          res.content[0]["text"]
                      │
                      ▼
                  answer
                      │
                      ▼
             st.chat_message()
                      │
                      ▼
                    USER
```

At the same time, both messages are stored in:

```python
st.session_state.messages
```

---

# ⚠️ Important: UI History vs AI Memory

There is an important concept beginners should understand.

This application currently **stores the previous messages in Streamlit**.

However, the code sends only:

```python
llm.invoke(query)
```

to Gemini.

That means Gemini receives only the current question.

For example:

```text
User:
Who is Cristiano Ronaldo?

AI:
Cristiano Ronaldo is a Portuguese footballer...

User:
Which country does he represent?
```

The application visually remembers the previous question.

But Gemini itself receives:

```text
Which country does he represent?
```

It does not automatically receive:

```text
Who is Cristiano Ronaldo?
```

So the current version has **chat history in the UI**, but not full conversational memory for the LLM.

A future version can solve this by sending the conversation history to Gemini.

---

# ▶️ Running the Application

Don't run the Streamlit application using:

```bash
python QnA_Bot.py
```

Instead use:

```bash
streamlit run QnA_Bot.py
```

Streamlit will start a local web server.

You should see something similar to:

```text
Local URL: http://localhost:8501
```

Open that URL in your browser.

---

# 🧪 Example

Ask:

```text
What is Generative AI?
```

Gemini might respond with an explanation.

Then ask:

```text
Give me three examples.
```

The application will display both messages.

---

# 🐛 Common Errors

## Error 1 — `ModuleNotFoundError`

Example:

```text
ModuleNotFoundError: No module named 'streamlit'
```

Solution:

```bash
pip install streamlit
```

---

## Error 2 — LangChain package missing

If you see:

```text
No module named 'langchain_google_genai'
```

run:

```bash
pip install langchain-google-genai
```

---

## Error 3 — dotenv missing

If you see:

```text
No module named 'dotenv'
```

run:

```bash
pip install python-dotenv
```

---

## Error 4 — API key problem

If Gemini cannot authenticate, check:

```text
.env
```

Make sure it contains your API key.

For example:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Also make sure you haven't accidentally written:

```env
GOOGLE_API_KEY = YOUR_API_KEY
```

or added unnecessary quotation marks.

---

## Error 5 — `.env` isn't loading

Make sure `.env` is in the project directory:

```text
QnA-Bot/
│
├── QnA_Bot.py
├── .env
└── README.md
```

Then:

```python
load_dotenv()
```

should be able to find it.

---

# 🔐 Security

API keys are secrets.

Never upload:

```text
.env
```

to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
.env.*
```

A good `.gitignore` for this project:

```gitignore
# Environment variables
.env
.env.*

# Virtual environments
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]

# Jupyter
.ipynb_checkpoints/
notebooks/

# IDE
.vscode/
.idea/
```

---

# 🐙 Git and GitHub

After creating the project, initialize Git:

```bash
git init
```

Add your files:

```bash
git add .
```

Check what will be committed:

```bash
git status
```

Make sure `.env` does **not** appear.

Then commit:

```bash
git commit -m "feat: build Gemini QnA chatbot"
```

Connect your GitHub repository:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

Push:

```bash
git branch -M main
git push -u origin main
```

---

# 🚀 Deployment

Once the application works locally, it can be deployed so other people can access it through a browser.

A typical deployment architecture looks like:

```text
GitHub Repository
       │
       ▼
Cloud Deployment Platform
       │
       ▼
Streamlit Application
       │
       ▼
Gemini API
```

### Important

When deploying, **do not upload your `.env` file**.

Instead, add your API key through the deployment platform's **Secrets / Environment Variables** settings.

Conceptually:

```text
Local:

.env
   ↓
GOOGLE_API_KEY


Deployment:

Platform Secrets
   ↓
GOOGLE_API_KEY
```

This keeps the secret out of your GitHub repository.

---

# 🎨 Possible Improvements

This project is intentionally simple.

There are many ways to make it more advanced.

## Level 1 — UI Improvements

Add:

* Custom CSS
* Better colors
* Custom avatars
* Sidebar
* Clear chat button
* Loading indicator
* Better typography
* Responsive design

---

## Level 2 — Better Chat Memory

Instead of sending only:

```python
llm.invoke(query)
```

send the conversation history to the model.

This allows questions like:

```text
User:
Who is Albert Einstein?

AI:
Albert Einstein was...

User:
Where was he born?

AI:
He was born in...
```

The model understands what "he" refers to because previous messages are included.

---

## Level 3 — Streaming

Instead of waiting for the entire answer:

```text
Generating...
...
...
Complete answer appears
```

we can stream the response:

```text
Albert...
Albert Einstein...
Albert Einstein was...
Albert Einstein was a physicist...
```

This makes the application feel much more like a production AI chatbot.

---

# 📚 Level 4 — RAG

The next major improvement is **Retrieval-Augmented Generation (RAG)**.

Instead of asking Gemini only general questions, the chatbot could answer questions about your own documents.

For example:

```text
PDF
 │
 ▼
Document Loader
 │
 ▼
Text Splitting
 │
 ▼
Embeddings
 │
 ▼
Vector Database
 │
 ▼
Retriever
 │
 ▼
Relevant Context
 │
 ▼
Gemini
 │
 ▼
Answer
```

Then you could upload:

```text
Resume.pdf
ResearchPaper.pdf
CompanyDocumentation.pdf
Book.pdf
```

and ask:

```text
What are the main findings of this paper?
```

The system retrieves relevant information and gives it to Gemini.

---

# 🤖 Level 5 — Agentic AI

The chatbot could eventually become an AI agent.

For example:

```text
User
 │
 ▼
AI Agent
 │
 ├── Search Tool
 ├── Calculator
 ├── Database
 ├── Weather API
 └── Other Tools
```

Instead of simply generating text, the AI can decide which tool it needs to accomplish a task.

---

# 📊 Level 6 — LLM Evaluation

A production GenAI application needs evaluation.

You could evaluate:

* Answer correctness
* Relevance
* Faithfulness
* Hallucination
* Latency
* Token usage
* Cost

For example:

```text
Question
   ↓
AI Answer
   ↓
Evaluation
   ├── Correctness: 0.92
   ├── Relevance: 0.95
   └── Faithfulness: 0.89
```

This is an important step toward production-grade GenAI engineering.

---

# ☁️ Level 7 — Production Deployment

A more advanced architecture could eventually look like:

```text
                 ┌──────────────┐
                 │    User      │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   Frontend   │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   FastAPI    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   LangChain  │
                 └──────┬───────┘
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
       ┌──────────┐          ┌──────────┐
       │   RAG    │          │   Tools  │
       └────┬─────┘          └────┬─────┘
            │                     │
            └──────────┬──────────┘
                       ▼
                 ┌──────────────┐
                 │ Gemini / LLM │
                 └──────────────┘
```

---

# 🧭 Recommended Learning Path

If you're learning GenAI and want to understand this project deeply, learn the concepts in roughly this order:

```text
Python
  ↓
APIs
  ↓
LLMs
  ↓
Prompting
  ↓
LangChain
  ↓
Streamlit
  ↓
Conversation Memory
  ↓
RAG
  ↓
Vector Databases
  ↓
Agents
  ↓
Tool Calling
  ↓
MCP
  ↓
LLM Evaluation
  ↓
FastAPI
  ↓
Deployment
  ↓
MLOps
```

You don't need to master everything before building.

The best approach is:

```text
Learn
  ↓
Build
  ↓
Break something
  ↓
Debug
  ↓
Understand
  ↓
Improve
  ↓
Build something harder
```

---

# 🧩 What You Learn From This Project

By completing this project, you practice several important GenAI concepts:

### Python

You use:

* Variables
* Functions
* Lists
* Dictionaries
* Loops
* Conditions
* Imports
* Environment variables

### Generative AI

You learn:

* What an LLM is
* How an LLM receives prompts
* How an LLM generates responses
* How an API connects your application to an LLM

### LangChain

You learn:

* Chat model integration
* `ChatGoogleGenerativeAI`
* `invoke()`
* AI message objects
* Model abstraction

### Streamlit

You learn:

* Creating a web UI using Python
* Chat interfaces
* Session state
* User input
* Dynamic UI updates

### Software Engineering

You learn:

* `.env`
* `.gitignore`
* Virtual environments
* `requirements.txt`
* Git
* GitHub
* Deployment concepts

---

# 🎯 Project Goal

The purpose of this project isn't simply to create a chatbot.

The real goal is to understand the complete pipeline:

```text
Python Application
       ↓
Web Interface
       ↓
LLM Framework
       ↓
LLM API
       ↓
Generated Response
       ↓
Web Interface
```

Once you understand this pipeline, you can start building much more sophisticated Generative AI applications.

---

# ⭐ Future Version

A future version of this project can include:

* [ ] Conversation memory
* [ ] Streaming responses
* [ ] Custom UI
* [ ] Clear chat button
* [ ] System prompts
* [ ] RAG
* [ ] PDF upload
* [ ] Vector database
* [ ] Source citations
* [ ] Tool calling
* [ ] AI agents
* [ ] MCP
* [ ] LLM evaluation
* [ ] FastAPI backend
* [ ] Production deployment

---

# 🏁 Conclusion

This project starts with a very simple idea:

> **Ask an AI a question and display its answer.**

But underneath that simple interface are several important concepts:

```text
Python
  +
Streamlit
  +
LangChain
  +
Google Gemini
  +
Environment Variables
  +
Session State
  =
AI QnA Application
```

The current application is intentionally simple so that each component can be understood independently.

From here, the project can gradually evolve from:

```text
Simple QnA Bot
       ↓
Conversational Chatbot
       ↓
RAG Chatbot
       ↓
Tool-Using AI
       ↓
Agentic AI
       ↓
Production GenAI Application
```

The important thing is not just to copy the code.

**Understand what every component is doing, change something, break it, fix it, and then build the next version.** 🚀

---

## 👨‍💻 Author

Built as a hands-on Generative AI project using:

* Python
* LangChain
* Google Gemini
* Streamlit

---

## ⭐ If You Found This Project Useful

Give the repository a ⭐ on GitHub and feel free to experiment with the code!
