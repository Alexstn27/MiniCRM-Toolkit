import pandas as pd
from datetime import datetime

from core.constants import EMAIL_COLUMN


class DuplicateRemoverModule:

    def load_excel(self, file_path):

        dataframe = pd.read_excel(file_path)

        return dataframe


    def validate_columns(self, dataframe):

        required_columns = [
            EMAIL_COLUMN
        ]

        for column in required_columns:

            if column not in dataframe.columns:
                return False

        return True


    def remove_duplicates(self, dataframe):

        original_count = len(dataframe)

        dataframe = dataframe.drop_duplicates(
            subset=[EMAIL_COLUMN],
            keep="first"
        )

        removed_count = original_count - len(dataframe)

        return dataframe, removed_count
    
    def save_excel(self, dataframe):

        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M")

        output_path = (
            f"output/MiniCRM - Participanți fără duplicate - {timestamp}.xlsx"
        )

        dataframe.to_excel(
            output_path,
            index=False
        )

        return output_path