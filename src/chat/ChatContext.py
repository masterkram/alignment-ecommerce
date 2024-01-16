from .Message import Message
import streamlit as st
from .initial_messages import init_message_history
from ..db.Laptop import Laptop
from ..ui import chat_ui as chat_ui
from ..research.Logging import Logger
import random

UI_ROLES = ["assistant", "user"]


class ChatContext:
    logger: Logger
    messages: list = None

    def __init__(self, logger):
        self.instance_key = random.randint(0, 100)
        # Initialize chat history
        # if "messages" not in st.session_state:
        #     st.session_state.messages = starting_history
        # if self.messages:
        # del self.messages
        self.messages = init_message_history()
        self.logger = logger
        # st.session_state.recommended = False
        # st.session_state.finished = False

    def get_messages(self):
        print(self.instance_key)
        return self.messages

    def set_messages(self, messages, cache=False):
        # if not self.messages == None and not cache:
        self.messages = messages

    def log(self, output: str):
        self.logger.log_message(self.get_messages(), output)

    def addMessage(self, message: Message):
        self.log(message.message)
        self.get_messages().append(message.toLLMDict())

    def addLaptops(self, laptops: list[Laptop], query: str):
        result = ",".join([chat_ui.laptop_to_markdown(laptop) for laptop in laptops])
        self.logger.log_laptops(laptops, query)
        self.get_messages().append(
            {"role": "function", "name": "search_laptops", "content": result}
        )
        # st.session_state.recommended = True
        # print(st.session_state.recommended)

    def isDone(self) -> tuple[bool, str]:
        # if st.session_state.recommended:
        # st.session_state.finished = True
        return (False, "recommended")

    # if len(self.get_messages()) > 55:
    # st.session_state.finished = True
    # return (True, "long")
    # return (False, "")

    def addProfile(self, profile: str):
        self.log(f"set profile={profile}")
        self.get_messages().append(
            {
                "role": "function",
                "name": "set_profile",
                "content": f"set profile={profile}",
            }
        )

    def getContext(self):
        return self.messages

    def getUIContext(self):
        return [
            Message(role=x["role"], message=x["content"])
            for x in self.get_messages()
            if x["role"] in UI_ROLES
        ]

    def addNoResults(self):
        self.get_messages().append(
            {
                "role": "function",
                "name": "search_laptops",
                "content": "NO MATCHES FOUND.",
            }
        )
