import pandas as pd
from datetime import datetime


def load_excel(file_path):

    dataframe = pd.read_excel(file_path)

    return dataframe


def save_excel(dataframe, filename_prefix):

    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M")

    output_path = (
        f"output/{filename_prefix} - {timestamp}.xlsx"
    )

    dataframe.to_excel(
        output_path,
        index=False
    )

    return output_path