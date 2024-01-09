from humanloop import Humanloop
import streamlit as st
from langfuse import Langfuse
import json
from ..db.Laptop import Laptop


class Logger:
    user: str
    session_id: str

    def __init__(self, user, session_id):
        self.user = user
        self.session_id = session_id

    def log_message(self, messages: list, output: str):
        pass

    def log_laptops(self, messages: list, output: str):
        pass


class LangFuseLogger:
    langfuse: Langfuse

    def __init__(self, user: str, experiment: str, session_id: str):
        super.__init__(user, session_id)
        self.langfuse = Langfuse(
            public_key=st.secrets["LANGFUSE_PUBLIC_KEY"],
            secret_key=st.secrets["LANGFUSE_SECRET_KEY"],
        )
        self.trace = self.langfuse.trace("laptop-recommendation", tags=[experiment])

    def log_message(self, messages: list, output: str):
        generation = self.trace.generation(
            session_id=self.session_id,
            user_id=self.user,
            name="chat",
            model="gpt-3.5-turbo",
            input=messages,
        )
        generation.end(output=output)

    def log_laptops(self, laptops: list[Laptop], query: str):
        json_laptops = json.dump([laptop.toJSON() for laptop in laptops])
        event = self.trace.event(
            name="laptop-retrieval", input=query, output=json_laptops
        )

    def flush(self):
        self.langfuse.flush()


class HumanLoopLogger:
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

    def log_laptops(self, laptops: list):
        self.log_message()
