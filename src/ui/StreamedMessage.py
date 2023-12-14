import streamlit as st


class StreamedMessage:
    tmp_response: str
    recovered_pieces: dict

    def __init__(self):
        self.tmp_response = ""
        self.placeholder = st.empty()

    def write(self, content: str) -> None:
        self.tmp_response += content
        self.placeholder.markdown(self.tmp_response + "▌")

    def flush(self) -> None:
        self.placeholder.markdown(self.tmp_response)
