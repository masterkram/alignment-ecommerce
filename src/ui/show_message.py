from ..chat.Message import Message
import streamlit as st


def show_message(message: Message):
    with st.chat_message(message.getRole(), avatar=message.getAvatar()):
        st.markdown(message.getMessage())
