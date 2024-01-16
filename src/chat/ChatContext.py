from .Message import Message
import streamlit as st
from .initial_messages import init_message_history
from ..db.Laptop import Laptop
from ..ui import chat_ui as chat_ui
from ..research.Logging import Logger

UI_ROLES = ["assistant", "user"]


class ChatContext:
    logger: Logger
    recommended: bool

    def __init__(self, logger, starting_history: list = []):
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = init_message_history()
        self.logger = logger
        st.session_state.finished = False
        self.recommended = False

    def log(self, output: str):
        self.logger.log_message(st.session_state.messages, output)

    def check_if_done(self) -> None:
        if self.recommended:
            st.session_state.finished = True
            return
        if len(st.session_state.messages) > 55:
            st.session_state.finished = True
            return

    def addMessage(self, message: Message):
        self.log(message.message)
        st.session_state.messages.append(message.toLLMDict())

    def addLaptops(self, laptops: list[Laptop], query: str):
        result = ",".join([chat_ui.laptop_to_markdown(laptop) for laptop in laptops])
        self.logger.log_laptops(laptops, query)
        st.session_state.messages.append(
            {"role": "function", "name": "search_laptops", "content": result}
        )
        self.recommended = True

    def isDone(self) -> tuple[bool, str]:
        if self.recommended:
            return (True, "recommended")
        if len(st.session_state.messages) > 55:
            return (True, "long")
        if st.session_state.finished:
            return (True, "recommended")
        return (False, "")

    def addProfile(self, profile: str):
        self.log(f"set profile={profile}")
        st.session_state.messages.append(
            {
                "role": "function",
                "name": "set_profile",
                "content": f"set profile={profile}",
            }
        )

    def getContext(self):
        return st.session_state.messages

    def getUIContext(self):
        return [
            Message(role=x["role"], message=x["content"])
            for x in st.session_state.messages
            if x["role"] in UI_ROLES
        ]

    def addNoResults(self):
        st.session_state.messages.append(
            {
                "role": "function",
                "name": "search_laptops",
                "content": "NO MATCHES FOUND.",
            }
        )
