import streamlit as st
from openai import OpenAI, Stream
import json
import elasticsearch
from src.db.laptop_db import LaptopDatabase

database = LaptopDatabase()

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"


def get_messages() -> list:
    """
    Get the full chatgpt message history.
    """
    system = {
        "role": "system",
        "content": "You are Lisa, a friendly assistant. Help the user find a laptop that suits their needs. Please adapt to the user's language level and expertise. Ask as many questions as needed to reduce the possible laptops to an optimal choice.",
    }
    few_shot_prompts = [
        {"role": "user", "content": "I am a gamer"},
        {
            "role": "assistant",
            "content": "I understand you are a gamer, do you need a powerful graphics card?",
        },
    ]
    result = [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]
    result = [*few_shot_prompts, result]
    result.insert(0, system)
    return result


def show_title() -> None:
    st.title(":computer: Laptop Assistant")


def init_message_history() -> None:
    starting_history = [
        {"role": "assistant", "content": x, "avatar": "👩‍💻"}
        for x in [
            "Hi there! I'm Lisa, your digital product advisor. 😊",
            "I'm here to find a suitable laptop for you. Let's go through a few questions to help me understand your preferences...",
            "Let's start: What do you usually use your laptop for?",
        ]
    ]

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = starting_history


def show_message_history() -> None:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if "role" in message:
            avatar = message["avatar"] if "avatar" in message else False
            if avatar:
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


def show_user_message(prompt: str) -> None:
    with st.chat_message("user"):
        st.markdown(prompt)


def add_message_to_history(role: str, content: str) -> None:
    st.session_state.messages.append({"role": role, "content": content})


def request_openai() -> Stream:
    return client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=get_messages(),
        stream=True,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "search_laptops",
                    "description": "Get the available laptops given parameters.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lucene_query": {
                                "type": "string",
                                "description": "A Lucene Query String to search for a laptop. Use units in full e.g 'systemMemoryRam:16 gigabytes' instead of '16gb'. Possible fields are brand, model, modelNumber, title, price, ratingAvgDisplay, ratingNum, ratingAvg, questionNum, batteryLife, totalStorageCapacity, storageType, operatingSystem, processorCores, processorBrand, processorSpeedBase, processorModel, systemMemoryRam, systemMemoryRamType, graphics, screenSize, screenResolution, screenResolutionName, productWeight, color, numberOfUsbPortsTotal, numberOfUsb2Ports, numberOfUsb3Ports, backlitKeyboard, internetConnectivity, bluetoothEnabled, touchScreen, titleStandard",
                            },
                        },
                        "required": ["lucene_query"],
                    },
                },
            }
        ],
    )


def write_response_markdown(placeholder, content):
    placeholder.markdown(content + "▌")


def recover_function_piece(delta, recovered_pieces):
    piece = delta.tool_calls[0]
    recovered_pieces["tool_calls"][piece.index] = recovered_pieces["tool_calls"].get(
        piece.index,
        {
            "id": None,
            "function": {"arguments": "", "name": ""},
            "type": "function",
        },
    )
    if piece.id:
        recovered_pieces["tool_calls"][piece.index]["id"] = piece.id
    if piece.function.name:
        recovered_pieces["tool_calls"][piece.index]["function"][
            "name"
        ] = piece.function.name
    recovered_pieces["tool_calls"][piece.index]["function"][
        "arguments"
    ] += piece.function.arguments


def handle_delta(delta, recovered_pieces) -> str | None:
    if delta.content is None:
        if delta.tool_calls:
            recover_function_piece(delta, recovered_pieces)
        return None

    return delta.content or ""


def add_function_call_to_history(id, function_name, function_response):
    history = {
        "tool_call_id": id,
        "role": "tool",
        "name": function_name,
        "content": function_response,
    }
    st.session_state.messages.append(history)


def handle_response(response, recovered_pieces):
    return handle_delta(response.choices[0].delta, recovered_pieces)


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


def laptop_to_md(laptop) -> str:
    source = laptop["_source"]
    title = source["title"]
    image_url = (
        source["imageURLs"][0]
        if "imageURLs" in source
        else "https://http.cat/status/100"
    )
    return f"{title}\n![image of {title}]({image_url})"


def show_assistant_message() -> None:
    with st.chat_message("assistant", avatar="👩‍💻"):
        message_placeholder = st.empty()
        full_response = ""
        # Stream response
        recovered_pieces = {"content": None, "role": "assistant", "tool_calls": {}}
        for response in request_openai():
            # type the response fancy.
            text = handle_response(response, recovered_pieces)
            if text:
                full_response += text
                write_response_markdown(message_placeholder, full_response)
        # finished first response.
        if len(recovered_pieces["tool_calls"]) > 0:
            # call search.
            loading_message = (
                "Hmm, I'm looking for your ideal laptop :laptop:, please wait..."
            )
            st.markdown(loading_message)
            st.session_state.messages.append(
                {"role": "assistant", "content": loading_message, "avatar": "👩‍💻"}
            )
            argument = recovered_pieces["tool_calls"][0]["function"]["arguments"]
            json_it = json.loads(argument)
            query = json_it["lucene_query"]

            add_function_call_to_history(
                recovered_pieces["tool_calls"][0]["id"], "search_laptops", query
            )

            results = database.search_laptops(query)
            if results and len(results) > 0:
                for i, laptop in enumerate(results):
                    laptop_md = laptop_to_md(laptop)
                    st.markdown(laptop_md)
                    st.session_state.messages.append(laptop_to_md)
                handle_results(results)
            else:
                full_response += "I found no results for these preferences."
                message_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response, "avatar": "👩‍💻"}
                )
                handle_no_results()
        else:
            message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response, "avatar": "👩‍💻"}
            )


show_title()
init_message_history()
show_message_history()

st.sidebar.markdown("**Laptop Assistant Configuration**")
option = st.sidebar.selectbox(label="Chatbot", options=["Aligned", "Unaligned"])

if "chatbot" not in st.session_state:
    st.session_state["chatbot"] = option

prompt = st.chat_input("What is your preference?")


if prompt:
    # Display user message in chat message container
    show_user_message(prompt)
    # Add user message to chat history
    add_message_to_history("user", prompt)
    # Display assistant response in chat message container
    show_assistant_message()
