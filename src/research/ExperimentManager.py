class Experiment:
    code: str
    llm: str

    def __init__(self):
        pass


EXPERIMENTS = {"mvoqvr": Experiment(), "hdttzt": Experiment()}


class ExperimentManager:
    code: str = ""

    def setCode(self, query_parameters: dict):
        try:
            self.code = query_parameters["code"][0]
        except:
            self.code = ""

    def getExperimentSetup(self):
        print(self.code)
        if self.code in EXPERIMENTS:
            return EXPERIMENTS[self.code]
        return None
