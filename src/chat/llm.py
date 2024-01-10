from humanloop import Humanloop
import streamlit as st
import openai
from ..research.ExperimentManager import Experiment


class LLM:
    experiment: Experiment

    def __init__(self, model, experiment: Experiment):
        self.model = model
        self.experiment = experiment

    def chat():
        pass


class HumanLoop(LLM):
    def __init__(self):
        super(Humanloop(api_key=st.secrets["HUMANLOOP_API_KEY"]))

    def chat(self, messages: list):
        return self.model.chat_deployed_stream(messages, "ecommerce")


class GPT4(LLM):
    def __init__(self, experiment: Experiment):
        super().__init__(
            openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"]), experiment
        )

    def chat(self, messages: list):
        system = self.experiment.system_prompt
        messages = [{"role": "system", "content": system}, *messages]
        return self.model.chat.completions.create(
            model=st.session_state.openai_model,
            messages=messages,
            seed=447,
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
                                    "description": "A Lucene Query String to search for a laptop. Instead of using units in text fields just put the number, for example 'systemMemoryRam:8 gigabytes' should be 'systemMemoryRam:8'. For Storage use regex to give better recommendations, for example 'totalStorageCapacity: 500 gigabytes' should be 'totalStorageCapacity: /5[0-9]{2,}/', For price use ranges for example: 'price:[1000 TO 1500]'. For screen size also use regex to add the decimal point: 'screenSize:16' should be 'screenSize:/16\.[0-9]/' optionally a range can also be specified as 'screenSize:/1[4-8]\\.[0-9]/'. Possible fields are brand: text, model: text, modelNumber: text, title: text, price: long, ratingAvgDisplay: float, ratingNum: long, ratingAvg: float, questionNum: long, batteryLife: text e.g 2.0 hours, totalStorageCapacity: text e.g 512 gigabytes, storageType: text e.g HDD or SSD, operatingSystem: text, processorCores: text e.g 1-core, processorBrand: text e.g Intel, processorSpeedBase: text e.g 2.4 gigahertz, processorModel: text e.g Core i5, systemMemoryRam: text 2 gigabytes, systemMemoryRamType: text e.g DDR3 SDRAM, graphics: text e.g Integrated, screenSize: text e.g 15.6 inches, productWeight: text e.g 5.53, color: text e.g silver, numberOfUsbPortsTotal: long, numberOfUsb2Ports: long, numberOfUsb3Ports: long, backlitKeyboard: text e.g No, touchScreen: text e.g No",
                                },
                            },
                            "required": ["lucene_query"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "set_profile",
                        "description": "Set the profile of the user.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "profile": {
                                    "type": "string",
                                    "description": "A string representing a profile out of: Gamer, Student, Programmer, Creative, Professional or Novice User.",
                                },
                            },
                            "required": ["profile"],
                        },
                    },
                },
            ],
        )
