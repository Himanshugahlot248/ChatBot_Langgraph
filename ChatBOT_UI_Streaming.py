import streamlit as st
from ChatBot_Langgraph import workflow, thread_id
from langchain_core.messages import SystemMessage, HumanMessage
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

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
                config={"configurable": {"thread_id": thread_id}},
                stream_mode="messages"
            )
        )
    
    
    st.session_state["message_history"].append({"role": "assistant", "content": bot_response})