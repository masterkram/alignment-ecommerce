from .llm import LLM
from .ChatContext import ChatContext
import streamlit as st
from .avatars import *
from ..ui.StreamedMessage import StreamedMessage
import json
from ..db.laptop_db import LaptopDatabase
from ..ui import chat_ui as chat_ui
from .Message import Message


class FunctionCall:
    id: str | None
    function: dict
    type: str

    def __init__(self):
        self.id = None
        self.function = {"arguments": "", "name": ""}
        self.type = "function"

    def recovered(self) -> bool:
        return self.id and self.function and self.type

    def argument(self) -> str:
        argument = self.function["arguments"]
        json_it = json.loads(argument)
        return json_it["lucene_query"]


class Assistant:
    model: LLM
    chat_context: ChatContext
    database: LaptopDatabase
    role = "assistant"

    def __init__(self, model: LLM, chat_context: ChatContext, db: LaptopDatabase):
        self.model = model
        self.chat_context = chat_context
        self.database = db

    def _respond(self):
        return self.model.chat(self.chat_context.getContext())

    def run(self, recursive=True):
        my_case = self._initial_message()

        if my_case == False and recursive:
            self._handle_no_results()
        elif my_case == True and recursive:
            self._handle_results()

    def _handle_no_results(self):
        return self.run(recursive=False)

    def _handle_results(self):
        return self.run(recursive=False)

    def run_function(self, query: str) -> bool:
        results = self.database.search_laptops(query)

        if results and len(results) > 0:
            self.chat_context.addLaptops(results)
            for laptop in results:
                chat_ui.show_laptop(laptop)
            return True

        return False

    def run_set_user(self, profile: str) -> None:
        st.session_state.profile = profile
        st.toast(f"User Has Been Classified As ${profile}")

    def recover_function_piece(self, delta, recovered_pieces: FunctionCall):
        piece = delta.tool_calls[0]

        if piece.id:
            recovered_pieces.id = piece.id
        if piece.function.name:
            recovered_pieces.function["name"] = piece.function.name
        recovered_pieces.function["arguments"] += piece.function.arguments

    def handle_delta(self, delta, recovered_pieces: FunctionCall) -> str | None:
        if delta.content is None:
            if delta.tool_calls:
                self.recover_function_piece(delta, recovered_pieces)
            return None

        return delta.content or ""

    def handle_response(self, response, recovered_pieces: FunctionCall):
        return self.handle_delta(response.choices[0].delta, recovered_pieces)

    def _initial_message(self):
        print(avatars[self.role])
        with st.chat_message("assistant", avatar="👩‍💻"):
            chat_message = StreamedMessage()
            function_call = FunctionCall()

            for response in self._respond():
                text = self.handle_response(response, function_call)
                if text:
                    chat_message.write(text)
            # done
            chat_message.flush()
            self.chat_context.addMessage(Message(self.role, chat_message.tmp_response))

            if function_call.recovered():
                chat_ui.loading_message()
                query = json.loads(function_call.function["arguments"])["lucene_query"]
                return self.run_function(query)

            return None
