from .llm import LLM
from .ChatContext import ChatContext
import streamlit as st
from .avatars import *
from ..ui.StreamedMessage import StreamedMessage
import json
from ..db.laptop_db import LaptopDatabase
from ..ui import chat_ui as chat_ui
from .Message import Message
from ..research.Logging import Logger
from typing import Union


class Func:
    arguments: str  # json encoded arguments
    name: str

    def __init__(self):
        self.arguments = ""
        self.name = ""


class FunctionCall:
    id: Union(str, None)
    function: Func
    type: str

    def __init__(self):
        self.id = None
        self.function = Func()
        self.type = "function"

    def recovered(self) -> bool:
        return self.id and self.function and self.type

    def parseArgs(self) -> dict:
        return json.loads(self.function.arguments)


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
        print("getting results")
        results = self.database.search_laptops(query)

        print(len(results))

        if results and len(results) > 0:
            self.chat_context.addLaptops(results)
            for laptop in results:
                chat_ui.show_laptop(laptop)
            return True

        return False

    def run_set_user(self, profile: str) -> bool:
        st.session_state.profile = profile
        st.toast(f"User Has Been Classified As ${profile}")
        self.chat_context.addProfile(profile)
        return True

    def recover_function_piece(self, delta, recovered_pieces: FunctionCall):
        piece = delta.tool_calls[0]

        if piece.id:
            recovered_pieces.id = piece.id
        if piece.function.name:
            recovered_pieces.function.name = piece.function.name
        recovered_pieces.function.arguments += piece.function.arguments

    def handle_delta(self, delta, recovered_pieces: FunctionCall) -> Union(str, None):
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
            if chat_message.tmp_response == "":
                chat_message.write("I see.")
            chat_message.flush()
            self.chat_context.addMessage(Message(self.role, chat_message.tmp_response))

            if function_call.recovered():
                # chat_ui.loading_message()
                available_functions = {
                    "search_laptops": {
                        "function": self.run_function,
                        "args": "lucene_query",
                    },
                    "set_profile": {"function": self.run_set_user, "args": "profile"},
                }
                if function_call.function.name in available_functions:
                    my_function = available_functions[function_call.function.name][
                        "function"
                    ]
                    my_argument = json.loads(function_call.function.arguments)[
                        available_functions[function_call.function.name]["args"]
                    ]
                    print(
                        f"calling function {function_call.function.name} with args {function_call.function.arguments}"
                    )
                    return my_function(my_argument)

            return None
