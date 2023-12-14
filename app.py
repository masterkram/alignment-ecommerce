import streamlit as st
from src.db.laptop_db import LaptopDatabase
from src.ui.title import show_title
from src.chat.Message import Message
from src.chat.ChatContext import ChatContext
import src.ui.chat_ui as chat_ui
from src.chat.llm import LLM, GPT4
from src.research.ExperimentManager import ExperimentManager
from src.ui.not_found import not_found
from src.chat.Assistant import Assistant
from src.ui.assistant_message import show_assistant_message

experiment_manager = ExperimentManager()
experiment_manager.setCode(st.experimental_get_query_params())
experiment = experiment_manager.getExperimentSetup()

database = LaptopDatabase()
model = GPT4()
chat_context = ChatContext()
assistant = Assistant(model, chat_context, database)

if experiment == None:
    not_found()

show_title()
chat_ui.show_history(chat_context.getUIContext())

prompt = chat_ui.show_chat_input()

if prompt:
    # Display user message in chat message container
    user_message = Message("user", prompt)
    chat_ui.show_message(user_message)
    # Add user message to chat history
    chat_context.addMessage(user_message)
    # Display assistant response in chat message container
    # show_assistant_message()
    assistant.run()
