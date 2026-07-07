import pandas as pd


class HistoryUpdaterModule:

    def load_excel(self, file_path):

        dataframe = pd.read_excel(file_path)

        return dataframe