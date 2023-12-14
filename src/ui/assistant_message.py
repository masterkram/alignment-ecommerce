import streamlit as st
from .StreamedMessage import StreamedMessage
from ..chat.Message import Message
from . import chat_ui as chat_ui
import json
from ..chat.Assistant import Assistant
from ..db.laptop_db import LaptopDatabase


class FunctionCall:
    id: str | None
    function: dict
    type: str

    def __init__(self, id: str, role: str, tool_calls: dict):
        self.id = None
        self.function = {"arguments": "", "name": ""}
        self.type = "function"

    def recovered(self) -> bool:
        return self.id and self.function and self.type

    def argument(self) -> str:
        argument = self.function["arguments"]
        json_it = json.loads(argument)
        return json_it["lucene_query"]


def recover_function_piece(delta, recovered_pieces: FunctionCall):
    piece = delta.tool_calls[0]

    if piece.id:
        recovered_pieces.id = piece.id
    if piece.function.name:
        recovered_pieces.function["name"] = piece.function.name
    recovered_pieces.function["arguments"] += piece.function.arguments


def handle_delta(delta, recovered_pieces: FunctionCall) -> str | None:
    if delta.content is None:
        if delta.tool_calls:
            recover_function_piece(delta, recovered_pieces)
        return None

    return delta.content or ""


def handle_response(response, recovered_pieces: FunctionCall):
    return handle_delta(response.choices[0].delta, recovered_pieces)


def handle_function_call(call: FunctionCall):
    pass


def add_function_call_to_history(id, function_name, function_response):
    history = {
        "tool_call_id": id,
        "role": "tool",
        "name": function_name,
        "content": function_response,
    }
    st.session_state.messages.append(history)


def handle_no_results():
    """handle the situation with no results."""
    with st.chat_message("assistant", avatar="👩‍💻"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=get_messages(),
            stream=True,
        ):
            if response.content:
                full_response += response.content
                write_response_markdown(message_placeholder, full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response, "avatar": "👩‍💻"}
        )


def handle_results(results):
    """handle the situation with results."""
    with st.chat_message("assistant", avatar="👩‍💻"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=get_messages(),
            stream=True,
        ):
            if response.content:
                full_response += response.content
                write_response_markdown(message_placeholder, full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response, "avatar": "👩‍💻"}
        )

    # with st.chat_message("assistant", avatar="👩‍💻"):
    #     chat_message = StreamedMessage()
    #     function_call = FunctionCall()

    #     for response in request():
    #         # type the response fancy.
    #         text = handle_response(response, function_call)
    #         if text:
    #             chat_message.write(text)

    #     # finished first response.
    #     chat_message.flush()

    #     if function_call.recovered():
    #         # call search.
    #         loading_message = Message(
    #             "assistant",
    #             "Hmm, I'm looking for your ideal laptop :laptop:, please wait...",
    #         )
    #         chat_ui.show_message(loading_message)

    #         # add_function_call_to_history(
    #         #     recovered_pieces["tool_calls"][0]["id"], "search_laptops", query
    #         # )

    #         results = database.search_laptops(query)

    #         if results and len(results) > 0:
    #             for i, laptop in enumerate(results):
    #                 laptop_md = laptop_to_markdown(laptop)
    #                 st.markdown(laptop_md)
    #                 st.session_state.messages.append(laptop_md)
    #             handle_results(results)
    #         else:
    #             full_response += "I found no results for these preferences."
    #             message_placeholder.markdown(full_response)
    #             st.session_state.messages.append(
    #                 {"role": "assistant", "content": full_response, "avatar": "👩‍💻"}
    #             )
    #             handle_no_results()


from ..chat.avatars import *

ROLE = "assistant"


def run_function(database: LaptopDatabase, query: str) -> bool:
    results = database.search_laptops(query)

    if results and len(results) > 0:
        for laptop in results:
            chat_ui.show_laptop(laptop)

        return True

    return False


def initial_message(assistant: Assistant) -> bool | None:
    with st.chat_message(ROLE, avatars[ROLE]):
        chat_message = StreamedMessage()
        function_call = FunctionCall()

        for response in assistant.respond():
            text = handle_response(response, function_call)
            if text:
                chat_message.write(text)
        # done
        chat_message.flush()
        if function_call.recovered():
            chat_ui.loading_message()
            return run_function()

        return None


def show_assistant_message():
    my_case = initial_message()


def query_my_assistant(assistant: Assistant) -> None:
    print("heeellooo")
    # my_case = initial_message(assistant)

    # if my_case == False:
    #     handle_no_results()
    # elif my_case == True:
    #     handle_results()
