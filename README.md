# AI HR Chatbot Assistant

An intelligent chatbot built with Streamlit and Ollama that answers questions using a local Mistral language model. Designed to assist junior HR staff by providing answers based on company knowledge and policies.

## 🎯 Overview

This project implements a **Retrieval Augmented Generation (RAG)** chatbot that:
- Runs **completely offline** on your local machine using Ollama
- Uses **Mistral 7B** language model (4.4GB)
- Provides a **beautiful web interface** via Streamlit
- Supports **tool calling** (built-in calculator for math questions)
- Maintains **chat history** for context
- **No API keys required** - no data sent to external services

### Perfect For:
- HR departments needing instant answers to common questions
- Companies wanting to automate HR support
- Training junior staff with consistent, accurate responses
- Organizations prioritizing data privacy

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────┐
│         User (Streamlit Web Interface)              │
│         http://localhost:8501                       │
└────────────────────┬────────────────────────────────┘
                     │ User Input
                     ▼
┌─────────────────────────────────────────────────────┐
│         Streamlit Application (streamlit_app.py)    │
│  - Chat UI / Message History / Response Filtering   │
└────────────────┬────────────────────────────────────┘
                 │ Chat Messages
                 ▼
┌─────────────────────────────────────────────────────┐
│    LangChain Agent (create_react_agent)             │
│  - Routes requests to LLM or tools                  │
│  - Manages agentic reasoning                        │
└────────────────┬────────────────────────────────────┘
                 │ Processed Request
                 ▼
┌─────────────────────────────────────────────────────┐
│    Ollama Server (localhost:11434)                  │
│  - Mistral 7B Language Model                        │
│  - Text generation & reasoning                      │
└────────────────┬────────────────────────────────────┘
                 │ LLM Response
                 ▼
┌─────────────────────────────────────────────────────┐
│    Tool Executor (Calculator Tool)                  │
│  - Optional: Handles math calculations              │
│  - Performs simple arithmetic                       │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Features

### Core Features
- ✅ **Local Inference** - No internet required, complete privacy
- ✅ **Chat History** - Maintains conversation context
- ✅ **Tool Integration** - Built-in calculator for arithmetic
- ✅ **Clean UI** - Beautiful Streamlit interface
- ✅ **Response Filtering** - Removes unnecessary commentary
- ✅ **Offline First** - Runs entirely on your machine

### Advanced Features (Roadmap)
- 📋 Document Upload & RAG (coming soon)
- 🔒 User Authentication (coming soon)
- 📊 Analytics & Audit Logs (coming soon)
- 🌐 Web Deployment Guide (coming soon)

---

## 📋 Prerequisites

- **macOS** (tested on M1/M2 Mac)
- **Python 3.11+**
- **8GB+ RAM** (for Mistral model)
- **4GB+ Disk Space** (for model download)
- **uv** package manager (or pip)

---

## 🔧 Installation

### Step 1: Install Ollama

```bash
# Install via Homebrew
brew install ollama

# Start Ollama service
brew services start ollama
```

### Step 2: Download Mistral Model

```bash
# Pull Mistral 7B model (4.4GB download)
ollama pull mistral

# Verify installation
ollama list
```

### Step 3: Clone Repository & Install Dependencies

```bash
# Navigate to project directory
cd /path/to/project-python/project1

# Create virtual environment
uv venv .venv --python python3.11
source .venv/bin/activate

# Install Python dependencies
uv pip install -r requirements.txt
# OR manually:
uv pip install streamlit langchain-ollama langchain python-dotenv langgraph
```

### Step 4: Run the Application

```bash
# Ensure Ollama is running
brew services start ollama

# Start Streamlit app
.venv/bin/python -m streamlit run streamlit_app.py
```

Visit: **http://localhost:8501** in your browser

---

## 📁 Project Structure

```
project1/
├── streamlit_app.py       # Main Streamlit web app
├── main.py               # CLI version of the app
├── pyproject.toml        # Project dependencies
├── .env                  # Environment variables
├── README.md             # This file
├── hr_docs/              # (Coming soon) HR knowledge base
│   ├── policies.pdf
│   └── procedures.txt
└── vector_store/         # (Coming soon) Vector database
```

---

## 🔍 Code Explanation

### `streamlit_app.py` - Main Application

#### Imports & Setup
```python
import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
```

**What each import does:**
- `streamlit` - Web UI framework
- `langchain_core` - Chat message types
- `ChatOllama` - Interface to Ollama LLM
- `tool` - Decorator for creating callable tools
- `create_react_agent` - Creates ReAct (Reasoning + Acting) agent
- `load_dotenv` - Loads environment variables from .env

#### Calculator Tool
```python
@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers"""
    return f"the sum of {a} and {b} is {a+b}"
```

**What it does:**
- Decorated with `@tool` to make it callable by the agent
- Takes two numbers as input
- Returns their sum as a string
- Agent decides when to call this automatically

#### Page Configuration
```python
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)
```

**Configuration options:**
- `page_title` - Browser tab title
- `page_icon` - Emoji shown in browser
- `layout` - "wide" for full-screen, "centered" for normal
- `sidebar_state` - Hide/show sidebar by default

#### Session State Management
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

**What it does:**
- Streamlit reruns entire script on every interaction
- `session_state` persists data across reruns
- Stores chat history in memory during session

#### Chat Display
```python
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])
```

**What it does:**
- Loops through stored messages
- Displays user messages in blue (right-aligned)
- Displays assistant messages in gray (left-aligned)
- `markdown()` renders text with formatting

#### User Input
```python
user_input = st.chat_input("💬 Type your message...", key="user_input")
```

**What it does:**
- Creates input box at bottom of screen
- Waits for user to press Enter
- Returns user's message or None

#### LLM Initialization
```python
model = ChatOllama(model="mistral", temperature=0)
tools = [calculator]
agent_executor = create_react_agent(model, tools)
```

**What it does:**
- Initializes Mistral model connection
- `temperature=0` means deterministic (no randomness)
- Creates agent with calculator tool
- Agent can now choose to use calculator when helpful

#### Agent Streaming
```python
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=user_input)]}
):
    if "agent" in chunk and "messages" in chunk["agent"]:
        for message in chunk["agent"]["messages"]:
            if hasattr(message, 'content') and message.content:
                response_list.append(message.content.strip())
```

**What it does:**
- Streams response from agent (shows thinking in real-time)
- `chunk` contains intermediate steps
- Extracts final response message
- Appends to response list

#### Response Filtering
```python
response = response.replace("That's correct! ", "")
response = response.replace("indeed ", "")
response = response.split('\n')[0]  # Get first line only
```

**What it does:**
- Removes common filler phrases the model adds
- Takes only first line (removes extra commentary)
- Results in cleaner, more professional output

#### Chat History
```python
st.session_state.messages.append({"role": "assistant", "content": response})
```

**What it does:**
- Saves assistant response to memory
- Allows multi-turn conversations with context

---

### `main.py` - CLI Version

Same logic as `streamlit_app.py` but for command-line use:
```bash
python main.py
# Then type questions interactively
```

---

## ⚙️ Configuration

### Temperature Setting
```python
model = ChatOllama(model="mistral", temperature=0)
```

**Temperature = Randomness Level:**
- `0.0` → Deterministic, factual (best for HR)
- `0.5` → Balanced creativity
- `1.0` → Creative, may hallucinate

**Recommendation:** Keep at `0` for HR questions

### Ollama Server Configuration

If running Ollama on different machine:
```python
model = ChatOllama(
    model="mistral",
    base_url="http://192.168.1.100:11434"  # Remote server IP
)
```

### Environment Variables (`.env`)

Currently not used, but can be extended:
```bash
# .env file
OLLAMA_HOST=localhost:11434
APP_NAME=HR Chatbot
```

---

## 🎮 Usage Examples

### Basic Arithmetic
**User:** "What's 5 + 3?"
**Bot:** "The sum of 5.0 and 3.0 is 8.0"

### General Knowledge
**User:** "What is company culture?"
**Bot:** Uses trained knowledge to explain

### HR Questions (Future - with RAG)
**User:** "What's our leave policy?"
**Bot:** Searches HR docs → Provides accurate answer

---

## 🛠️ Troubleshooting

### "Connection refused" error
```bash
# Check if Ollama is running
brew services list | grep ollama

# Start if not running
brew services start ollama
```

### "Model not found" error
```bash
# Pull the model again
ollama pull mistral

# List available models
ollama list
```

### Slow responses (10-30 seconds)
- **Normal for local inference** on CPU
- First response is slower (model loading)
- Subsequent responses are faster
- Consider upgrading to GPU or using smaller model (neural-chat)

### High CPU usage
- Ollama runs model on CPU by default
- This is normal during inference
- Use `ollama list` to see model size
- Stop Ollama when not in use: `brew services stop ollama`

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >=1.28.0 | Web UI framework |
| langchain | >=1.2.0 | LLM orchestration |
| langchain-ollama | >=1.0.0 | Ollama integration |
| langgraph | >=1.0.5 | Agent framework |
| python-dotenv | >=1.2.1 | Environment variables |

See `pyproject.toml` for exact versions.

---

## 🚀 Future Roadmap

### Phase 1: RAG Enhancement (Next)
- [ ] Load HR documents (PDF, TXT, MD)
- [ ] Create vector embeddings
- [ ] Search documents before answering
- [ ] Upload UI for senior HR

### Phase 2: Web Deployment
- [ ] Deploy to DigitalOcean/AWS
- [ ] Add domain name
- [ ] Enable HTTPS

### Phase 3: Authentication & Analytics
- [ ] User login system
- [ ] Audit logs
- [ ] Question analytics
- [ ] Feedback system

### Phase 4: Advanced Features
- [ ] Multi-language support
- [ ] Custom model fine-tuning
- [ ] Integration with HR systems (ADP, Workday)

---

## 📝 How It Works (Detailed)

### 1. User Sends Message
User types "What's 3 + 4?" in Streamlit UI

### 2. Message Processing
- Message stored in `session_state.messages`
- Passed to LangChain agent

### 3. Agent Decision Making (ReAct)
- **Think:** Agent reads question, decides if calculator needed
- **Act:** Calls calculator tool with args (3, 4)
- **Observe:** Tool returns "the sum is 7"
- **Reason:** Generates final response

### 4. Response Generation
- Mistral model generates text response
- Response streamed back chunk-by-chunk
- Filters out unnecessary phrases
- Displays in UI

### 5. History Storage
- Response saved to `session_state.messages`
- Available for context in next message
- Persists during user session only

---

## 🔒 Privacy & Security

✅ **Fully Local & Private**
- No data sent to OpenAI, Google, or any external service
- Everything runs on your machine
- No internet required after model download
- Models stored locally on disk

⚠️ **Considerations**
- Chat history stored in browser session memory (lost on refresh)
- .env file should contain only non-sensitive config
- Don't commit API keys to GitHub (use `.gitignore`)

---

## 💡 Tips & Best Practices

1. **Keep questions specific** - "What's our leave policy?" works better than "Tell me about HR"
2. **Use calculator for math** - Agent learns when to use the tool
3. **Keep Ollama running** - Start service before using: `brew services start ollama`
4. **Monitor performance** - First message takes 15-20s, others are faster
5. **Scale gradually** - Test with small doc base before expanding

---

## 🤝 Contributing

Contributions welcome! To improve:
1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📞 Support

For issues or questions:
1. Check **Troubleshooting** section above
2. Review Ollama docs: https://ollama.ai
3. Check LangChain docs: https://python.langchain.com
4. Open an issue on GitHub

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **Ollama** - Local LLM inference
- **Mistral AI** - 7B language model
- **LangChain** - LLM framework
- **Streamlit** - Web UI framework
- **LangGraph** - Agent orchestration

---

## 🎯 Getting Started Quickly

```bash
# 1. Install Ollama
brew install ollama && brew services start ollama

# 2. Pull model
ollama pull mistral

# 3. Install dependencies
cd project1 && uv pip install streamlit langchain-ollama langchain langgraph python-dotenv

# 4. Run app
.venv/bin/python -m streamlit run streamlit_app.py

# 5. Open browser
# Visit http://localhost:8501
```

**That's it! Start chatting!** 🚀
