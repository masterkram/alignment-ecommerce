import streamlit as st
from openai import OpenAI, Stream
import json
import elasticsearch

es_host = "http://localhost:9200"
es = elasticsearch.Elasticsearch([es_host])

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


def get_messages() -> list:
    """
    Get the full chatgpt message history.
    """
    system = {
        "role": "system",
        "content": "You are Lisa, a friendly assistant. Help the user find a laptop that suits their needs. Please adapt to the user's language level and expertise. Ask as many questions as needed to reduce the possible laptops to an optimal choice.",
    }
    result = [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]
    result.insert(0, system)
    return result


def search_laptops(lucene_query: str) -> list:
    """Search ElasticSearch index with a lucene query."""

    # Define the search query
    search_body = {
        "query": {
            "query_string": {
                "query": lucene_query,
                "default_field": "brand",  # Specify the default field to search
            }
        }
    }

    # Perform the search
    result = es.search(index="laptops", body=search_body)

    # Return the results
    if result and "hits" in result and "hits" in result["hits"]:
        return result["hits"]["hits"]
    return []


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


def add_function_call_to_history():
    pass


def handle_response(response, recovered_pieces):
    return handle_delta(response.choices[0].delta, recovered_pieces)


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
            argument = recovered_pieces["tool_calls"][0]["function"]["arguments"]
            json_it = json.loads(argument)
            query = json_it["lucene_query"]
            print(query)

            results = search_laptops(query)
            amount_of_laptops = len(results)
            if results and len(results) > 0:
                laptop_columns = message_placeholder.columns(amount_of_laptops)
                for i, laptop in enumerate(results):
                    print("laptops: ", laptop)
                    laptop_columns[i].markdown(laptop["titleStandard"])
                    laptop_columns[i].markdown(f"![image]({laptop['imageUrls'][0]})")
            else:
                full_response += "I found no results for these preferences."
                message_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response, "avatar": "👩‍💻"}
                )
        else:
            message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response, "avatar": "👩‍💻"}
            )


show_title()
init_message_history()
show_message_history()

prompt = st.chat_input("What is up?")

if prompt:
    # Display user message in chat message container
    show_user_message(prompt)
    # Add user message to chat history
    add_message_to_history("user", prompt)
    # Display assistant response in chat message container
    show_assistant_message()
