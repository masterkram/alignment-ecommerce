import streamlit as st
from src.db.laptop_db import LaptopDatabase
from src.ui.title import show_title
from src.chat.Message import Message
from src.chat.ChatContext import ChatContext
import src.ui.chat_ui as chat_ui
from src.chat.llm import LLM, GPT4
from src.research.ExperimentManager import (
    ExperimentManager,
    ExperimentManagerSetupException,
)
from src.ui.not_found import not_found
from src.chat.Assistant import Assistant
import os
from dotenv import load_dotenv
from src.research.Logging import Logger

from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st

ctx = get_script_run_ctx()
session_id = ctx.session_id

load_dotenv(verbose=True)
is_debug = os.getenv("DEBUG", False) == "True"

experiment_manager = ExperimentManager()
try:
    experiment_manager.setup(st.experimental_get_query_params())
except ExperimentManagerSetupException as ex:
    not_found(ex)

experiment = experiment_manager.getExperimentSetup()
database = LaptopDatabase()
model = GPT4(experiment)
my_logger = Logger(
    experiment_manager.user, experiment.name, experiment.code, session_id
)
chat_context = ChatContext(my_logger)
assistant = Assistant(model, chat_context, database)

show_title()
chat_ui.show_history(chat_context.getUIContext())

prompt = chat_ui.show_chat_input()

experiment_name = experiment.getName()
if is_debug and experiment_name:
    st.toast(f"Using {experiment.getName()} Model.")

if prompt:
    # Display user message in chat message container
    user_message = Message("user", prompt)
    chat_ui.show_message(user_message)
    # Add user message to chat history
    chat_context.addMessage(user_message)
    # Display assistant response in chat message container
    # show_assistant_message()
    assistant.run()
