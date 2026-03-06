import streamlit as st
from ChatBot_Langgraph import workflow, thread_id
from langchain_core.messages import SystemMessage, HumanMessage
import uuid

# ******************************************* Utility Functions  *******************************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(generate_thread_id())

def reset_chat():
    thread_id=str(generate_thread_id())
    st.session_state["thread_id"] = thread_id
    add_chat_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []

def add_chat_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_chat_thread(thread_id):
    return workflow.get_state(
    config={"configurable": {"thread_id": thread_id}}
).values["messages"]

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_chat_thread(st.session_state["thread_id"])








# ******************************************* SIDEBAR Start *******************************************

st.sidebar.title("ChatPPT")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.title("Last Chats")


for thread in st.session_state["chat_threads"][::-1]:

   if st.sidebar.button(thread):
    st.session_state["thread_id"] = thread
    loaded_messages = load_chat_thread(thread)

    temp_message_history = []
    for msg in loaded_messages:
        if isinstance(msg, HumanMessage):
            role="user"
        else:
            role="assistant"
        temp_message_history.append({"role": role, "content": msg.content})
    
    st.session_state["message_history"] = temp_message_history
# ******************************************* SIDEBAR END *******************************************


# message_history=[]

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])
# with st.chat_message("user"):
#     st.write("Hii")

# with st.chat_message("assistant"):
#     st.write("Hii, how can I help you?")


# with st.chat_input():
user_input = st.chat_input("Type your message here...")

if user_input:

    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)


    # chat_result = workflow.invoke( {"messages": [HumanMessage(content=user_input)]},config={"configurable": {"thread_id": thread_id}})
    # bot_response = chat_result["messages"][-1]


   
    with st.chat_message("assistant"):
       bot_response= st.write_stream(
           message_chunk.content for message_chunk,metadata in workflow.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"thread_id": st.session_state["thread_id"]}},
                stream_mode="messages"
            )
        )
    
    
    st.session_state["message_history"].append({"role": "assistant", "content": bot_response})