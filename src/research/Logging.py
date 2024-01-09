from humanloop import Humanloop
import streamlit as st
import os

location = os.getenv("LOCATION", "Local")


class Logger:
    humanloop: Humanloop
    project_id = "pr_d5KduisjOoAh3iQPUJLUC"
    user: str
    experiment_name: str
    experiment_code: str
    session_id: str

    def __init__(self, user, experiment_name, experiment_code, session_id):
        self.humanloop = Humanloop(api_key=st.secrets["HUMANLOOP_API_KEY"])
        self.user = user
        self.experiment_name = experiment_name
        self.experiment_code = experiment_code
        self.session_id = session_id

    def log_message(self, messages: list, output: str):
        self.humanloop.log(
            project_id=self.project_id,
            messages=messages,
            config={"model": st.session_state.openai_model},
            output=output,
        )
