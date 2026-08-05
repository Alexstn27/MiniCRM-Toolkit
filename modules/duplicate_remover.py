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

        dataframe_with_email = dataframe[
            dataframe[EMAIL_COLUMN].notna()
        ].copy()

        dataframe_without_email = dataframe[
            dataframe[EMAIL_COLUMN].isna()
        ].copy()

        dataframe_with_email = dataframe_with_email.drop_duplicates(
            subset=[EMAIL_COLUMN],
            keep="first"
        )

        dataframe = pd.concat(
            [
                dataframe_with_email,
                dataframe_without_email
            ],
            ignore_index=True
        )

        removed_count = original_count - len(dataframe)

        return dataframe, removed_count

    def find_possible_duplicates_without_email(self, dataframe):

        dataframe_without_email = dataframe[
            dataframe[EMAIL_COLUMN].isna()
        ].copy()

        duplicate_rows = dataframe_without_email[
            dataframe_without_email.duplicated(
                subset=["Contact: Nume"],
                keep=False
            )
        ]

        duplicate_names = (
            duplicate_rows["Contact: Nume"]
            .drop_duplicates()
            .tolist()
        )

        return duplicate_names
    
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