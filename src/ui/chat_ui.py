import streamlit as st
from ..chat.Message import Message
from ..db.Laptop import Laptop
import time


def show_chat_input(disabled=False, message="") -> None:
    key = 1 if disabled == False else 0
    text = "What is your preference" if not disabled else message
    return st.chat_input(text, disabled=disabled, key=key)


def show_message(message: Message) -> None:
    with st.chat_message(message.getRole(), avatar=message.getAvatar()):
        st.markdown(message.getMessage())


def show_history(messages: list[Message]):
    for message in messages:
        show_message(message)


def loading_message():
    loading_message = (
        "Hmm, I'm looking for your ideal laptop in our catalog, please wait..."
    )
    st.markdown(loading_message)


def show_laptop(laptop: Laptop):
    formatted_laptop = laptop_to_markdown(laptop)
    st.markdown(formatted_laptop)
    st.link_button("Go To Store :shopping_bags:", laptop.productURL)


PLACEHOLDER_IMAGE = "https://http.cat/status/100"


def laptop_to_markdown(laptop: Laptop):
    image_url = laptop.imageURLs[0] if laptop.imageURLs else PLACEHOLDER_IMAGE
    return f"{laptop.title}\n\n![image of {laptop.title}]({image_url})"
