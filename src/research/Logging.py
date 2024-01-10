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


class LangFuseLogger(Logger):
    langfuse: Langfuse

    def __init__(self, user: str, experiment: str, session_id: str):
        # TODO: add user id.
        super().__init__(user, session_id)
        self.langfuse = Langfuse(
            public_key=st.secrets["LANGFUSE_PUBLIC_KEY"],
            secret_key=st.secrets["LANGFUSE_SECRET_KEY"],
        )
        self.trace = self.langfuse.trace(
            name="laptop-recommendation",
            tags=[experiment],
            session_id=session_id,
            metadata={"experiment": experiment},
        )

    def log_message(self, messages: list, output: str):
        try:
            generation = self.trace.generation(
                session_id=self.session_id,
                user_id=self.user,
                name="chat",
                model=st.session_state.openai_model,
                input=messages,
            )
            generation.end(output=output)
        except:
            pass

    def log_laptops(self, laptops: list[Laptop], query: str):
        try:
            json_laptops = json.dumps([laptop.toJSON() for laptop in laptops])
            event = self.trace.event(
                name="laptop-retrieval", input=query, output=json_laptops
            )
        except:
            pass

    def finish_log(self, success: bool) -> None:
        try:
            output = json.dumps({"success": success})
            self.trace.event(name="redirect", input="", output=output)
        except:
            pass

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
