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
            model="gpt-4",
            messages=messages,
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
