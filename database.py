import pandas as pd

class Database:
    def __init__(self):
        self.data = pd.read_csv("encode/data.csv")

    def get_data(self):
        return self.data