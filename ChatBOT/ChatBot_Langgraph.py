# # from langgraph.graph import StateGraph, START, END
# # from typing import TypedDict, Literal,Annotated
# # from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
# # from langchain_ollama import ChatOllama
# # from langchain_core.prompts import ChatPromptTemplate
# # from pydantic import BaseModel, Field
# # # from langgraph.checkpoint.memory import MemoryCheckpoint
# # from langgraph.checkpoint.memory import MemorySaver  

# # model=ChatOllama(model="llama3.2:1b", temperature=0)

# # class BotState(TypedDict):
# #     messages:Annotated[list[BaseMessage], Field(description="The conversation history between the user and the bot.")]

# # def chat_node(state: BotState):

# #     message=state['messages']

# #     response=model.invoke(message).content
# #     return {"messages":[response]}

# # graph=StateGraph(BotState)
# # checkpointer=MemorySaver()
# # graph.add_node("chat_node",chat_node)
# # graph.add_edge(START,"chat_node")
# # graph.add_edge("chat_node",END)
# # workflow=graph.compile(checkpointer=checkpointer)

# # initial_state = {
# #     "messages":[HumanMessage(content="What is the capital of France?")]
# # }

# # # chat_result = workflow.invoke(initial_state)

# # # print(chat_result)
# # # print(workflow.get_graph().draw_ascii())
# # # print(chat_result["messages"])
# # thread_id = "1"

# # while True:
# #     user_input = input("User: ")

# #     if user_input.lower() in ["exit", "quit", "bye"]:
# #         print("Exiting chat.")
# #         break

# #     chat_result = workflow.invoke(
# #         {"messages": [HumanMessage(content=user_input)]},
# #         config={"configurable": {"thread_id": thread_id}}
# #     )

# #     print("Bot:", chat_result["messages"][-1].content)



# from langgraph.graph import StateGraph, START, END
# from typing import TypedDict, Annotated
# from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
# from langchain_ollama import ChatOllama
# from pydantic import Field
# from langgraph.checkpoint.memory import MemorySaver

# # Initialize model
# model = ChatOllama(model="llama3.2:1b", temperature=0)

# # State definition
# class BotState(TypedDict):
#     messages: Annotated[list[BaseMessage], Field(description="The conversation history between the user and the bot.")]

# # Node definition
# def chat_node(state: BotState):
#     response = model.invoke(state["messages"])
#     return {"messages": [AIMessage(content=response.content)]}

# # Build graph
# graph = StateGraph(BotState)
# graph.add_node("chat_node", chat_node)
# graph.add_edge(START, "chat_node")
# graph.add_edge("chat_node", END)

# # Use memory checkpointer
# checkpointer = MemorySaver()
# workflow = graph.compile(checkpointer=checkpointer)

# # Thread ID for memory
# thread_id = "1"

# # Chat loop
# while True:
#     user_input = input("User: ")

#     if user_input.lower() in ["exit", "quit", "bye"]:
#         print("Exiting chat.")
#         break

#     # Invoke workflow with new user message and memory thread
#     chat_result = workflow.invoke(
#         {"messages": [HumanMessage(content=user_input)]},
#         config={"configurable": {"thread_id": thread_id}}
#     )

#     # Get bot response (as AIMessage object)
#     bot_response = chat_result["messages"][-1]
#     print("Bot:", bot_response.content)


from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from pydantic import Field
from langgraph.checkpoint.memory import MemorySaver

# Initialize the model
model = ChatOllama(model="llama3.2:1b", temperature=0)

# Define state
class BotState(TypedDict):
    messages: Annotated[list[BaseMessage], Field(description="Conversation history between user and bot.")]

# Node that handles chat
def chat_node(state: BotState):
    """
    Receives the current conversation history in state['messages'],
    sends it to the model, and appends the AI response to the state.
    """
    # Generate bot response
    response = model.invoke(state["messages"])
    
    # Append new AIMessage to existing messages
    new_state_messages = state["messages"] + [AIMessage(content=response.content)]
    
    # Return full updated message history
    return {"messages": new_state_messages}

# Build the graph
graph = StateGraph(BotState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Initialize MemorySaver for persistent conversation
checkpointer = MemorySaver()
workflow = graph.compile(checkpointer=checkpointer)

# Thread ID for memory (each conversation can have its own thread)
thread_id = "1"

print("Chatbot ready! Type 'exit', 'quit', or 'bye' to end the conversation.\n")

# Chat loop
while True:
    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting chat.")
        break

    # Invoke workflow with just the new user message
    # MemorySaver will automatically load previous messages
    chat_result = workflow.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": thread_id}}
    )

    # Get the latest bot response
    bot_response = chat_result["messages"][-1]  # AIMessage object
    print("Bot:", bot_response.content)