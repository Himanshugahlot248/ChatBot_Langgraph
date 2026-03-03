# 🤖 LangGraph Chatbot (Streamlit + Ollama)

A conversational chatbot built using **LangGraph**, **LangChain**, **Ollama**, and **Streamlit**.  
This chatbot maintains conversation memory using LangGraph's **MemorySaver** and supports thread-based persistence.

---

## 🚀 Features

✅ Built with LangGraph state machine  
✅ Persistent memory using `thread_id`  
✅ Streamlit web interface  
✅ Local LLM powered by Ollama  
✅ Clean modular architecture  
✅ Easy to extend with tools or agents  

---

## 🧠 How It Works

1. User enters a message in the Streamlit UI  
2. The message is passed into a LangGraph workflow  
3. The chat node calls the Ollama model  
4. The AI response is appended to conversation history  
5. MemorySaver stores conversation using a unique `thread_id`  
6. Context is preserved across messages  

---

## 📂 Project Structure
ChatBOT/
│
├── ChatBOT_UI.py # Streamlit frontend
├── ChatBot_Langgraph.py # LangGraph workflow logic
├── requirements.txt
└── README.md

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd ChatBOT

2️⃣ Install Python Dependencies
bash
pip install -r requirements.txt
3️⃣ Install Ollama
Download and install from:
👉 https://ollama.com/

Start the Ollama server:

bash
ollama serve
Pull the model:

bash
ollama pull llama3.2:1b
▶️ Run the App Locally
bash
streamlit run ChatBOT_UI.py
Then open the local URL shown in your terminal.

🧵 Memory System
The chatbot uses LangGraph's MemorySaver:

python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
workflow = graph.compile(checkpointer=checkpointer)
Each conversation is stored using:

python
config={"configurable": {"thread_id": "your-thread-id"}}
This allows:

Persistent conversations

Multiple parallel chat sessions

Resume previous chat threads

☁️ Deployment Warning
⚠️ Ollama does NOT work on Streamlit Cloud.

If deploying to cloud:

Replace ChatOllama with ChatOpenAI, ChatGroq, or another API-based model

Add required API keys as Streamlit secrets

Ollama works only for local development.

🛠 Tech Stack-
Python 3.10+
LangGraph
LangChain Core
Ollama
Streamlit
Pydantic

🔮 Future Improvements-
Streaming responses
Database-backed memory (SQLite/Postgres)
Conversation export feature
Tool calling / Agents
Authentication system
Multi-user thread management

👨‍💻 Author
Himanshu

📄 License
This project is open-source and free to use.
