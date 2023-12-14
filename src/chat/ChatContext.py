from .Message import Message
import streamlit as st
from .initial_messages import init_message_history
from ..db.Laptop import Laptop
from ..ui import chat_ui as chat_ui

UI_ROLES = ["assistant", "user"]


class ChatContext:
    def __init__(self, starting_history: list = init_message_history()):
        # Initialize chat history
        # if "messages" not in st.session_state:
        st.session_state.messages = starting_history

    def addMessage(self, message: Message):
        st.session_state.messages.append(message.toLLMDict())

    def addLaptops(self, laptops: list[Laptop]):
        result = ",".join([chat_ui.laptop_to_markdown(laptop) for laptop in laptops])
        st.session_state.messages.append(
            {"role": "function", "name": "search_laptops", "content": result}
        )

    # def addFunction(self, function: Function):

    def getContext(self):
        return st.session_state.messages

    def getUIContext(self):
        return [
            Message(role=x["role"], message=x["content"])
            for x in st.session_state.messages
            if x["role"] in UI_ROLES
        ]
