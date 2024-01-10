import streamlit as st
from src.db.laptop_db import LaptopDatabase
from src.ui.title import show_title
from src.ui.redirect_button import redirect_button
from src.chat.Message import Message
from src.chat.ChatContext import ChatContext
import src.ui.chat_ui as chat_ui
from src.chat.llm import LLM, GPT4
from src.research.ExperimentManager import (
    ExperimentManager,
    ExperimentManagerSetupException,
)
from src.research.link_to_survey import get_link_to_survey
from src.ui.not_found import not_found
from src.chat.Assistant import Assistant
from src.research.Logging import Logger, LangFuseLogger

from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st

ctx = get_script_run_ctx()
session_id = ctx.session_id

is_debug = st.secrets["DEBUG"] == "True"

st.set_page_config(
    page_title="Laptop Recommender",
    page_icon="computer",
)
st.session_state["finished"] = False
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

experiment_manager = ExperimentManager()
try:
    experiment_manager.setup(st.experimental_get_query_params())
except ExperimentManagerSetupException as ex:
    not_found(ex)

experiment = experiment_manager.getExperimentSetup()
database = LaptopDatabase()
model = GPT4(experiment)
my_logger = LangFuseLogger(experiment_manager.user, experiment.getName(), session_id)
chat_context = ChatContext(my_logger)
assistant = Assistant(model, chat_context, database)

show_title()
chat_ui.show_history(chat_context.getUIContext())

experiment_name = experiment.getName()
if is_debug and experiment_name:
    st.toast(f"Using {experiment.getName()} Model.")

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

    done: tuple[bool, str] = chat_context.isDone()
    if done[0]:
        redirect_button(get_link_to_survey(experiment_manager.user), done[1])
