import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

# Configure page
st.set_page_config(
    page_title="HR Assistant AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Elegant & Simple CSS
st.markdown("""
<style>
    /* Clean minimalist design */
    .main {
        padding: 0;
        background: #ffffff;
    }
    
    /* Header - Simple & Elegant */
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.3px;
    }
    
    .header-container p {
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.85;
    }
    
    /* Chat wrapper - removed for cleaner look */
    
    /* Messages - Simple styling */
    .stChatMessage {
        padding: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    /* User message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #1e293b;
        color: white;
        border-radius: 12px;
        padding: 1rem;
        margin-left: auto;
        margin-right: 0;
        width: 70%;
    }
    
    /* Assistant message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: white;
        color: #1e293b;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        margin-left: 0;
        margin-right: auto;
        width: 70%;
    }
    
    /* Input styling */
    .stChatInputContainer {
        padding: 0 2rem 1.5rem 2rem;
    }
    
    .stChatInputContainer input {
        border: 1px solid #cbd5e1;
        border-radius: 20px;
        padding: 0.75rem 1.5rem;
        font-size: 0.95rem;
        background: #f8fafc;
        transition: all 0.2s ease;
    }
    
    .stChatInputContainer input:focus {
        border-color: #1e293b;
        background: white;
        box-shadow: 0 0 0 2px rgba(30, 41, 59, 0.05);
        outline: none;
    }
    
    /* Divider */
    hr {
        margin: 0;
        border: none;
        height: 1px;
        background: #e2e8f0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers"""
    return f"the sum of {a} and {b} is {a+b}"

def main():
    # Simple elegant header
    st.markdown("""
    <div class="header-container">
        <h1>🤖 HR Assistant</h1>
        <p>Ask anything about HR policies • Instant answers • 100% private</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages naturally
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(msg["content"])
    
    # Input
    user_input = st.chat_input("Type your question...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)
        
        # Get response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                model = ChatOllama(model="mistral", temperature=0)
                tools = [calculator]
                agent_executor = create_react_agent(model, tools)
                
                response_list = []
                for chunk in agent_executor.stream(
                    {"messages": [HumanMessage(content=user_input)]}
                ):
                    if "agent" in chunk and "messages" in chunk["agent"]:
                        for message in chunk["agent"]["messages"]:
                            if hasattr(message, 'content') and message.content:
                                response_list.append(message.content.strip())
                
                response = ""
                if response_list:
                    response = response_list[-1]
                
                # Clean response
                response = response.replace("That's correct! ", "")
                response = response.replace("indeed ", "")
                response = response.replace(" indeed", "")
                response = response.split('\n')[0]
                response = response.strip() if response else "I couldn't generate a response."
                
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()

if __name__ == "__main__":
    main()
