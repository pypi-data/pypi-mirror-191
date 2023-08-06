import pandas as pd


class ReportingEffort:
    def __init__(self, data_paths):
        self.effort_k9 = None
        self.k9_path = data_paths["k9_effort_path"]

    def read_data(self):
        self.effort_k9 = pd.read_csv(self.k9_path)

    def get_maya_effort_distance(self):
        return int(self.effort_k9[self.effort_k9["k9_name"] == "Maya"]["Total_distance"])

    def get_maya_effort_time(self):
        return int(self.effort_k9[self.effort_k9["k9_name"] == "Maya"]["Total_time"])
