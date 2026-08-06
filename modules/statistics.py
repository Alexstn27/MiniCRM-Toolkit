import pandas as pd

from core.constants import (
    EMAIL_COLUMN,
    NAME_COLUMN,
    STATISTICS_COLUMNS
)


class StatisticsModule:

    def load_excel(self, file_path):

        dataframe = pd.read_excel(file_path)

        return dataframe

    def validate_columns(self, dataframe):

        required_columns = [
            EMAIL_COLUMN,
            NAME_COLUMN
        ]

        for column in required_columns:

            if column not in dataframe.columns:
                return False

        return True

    def get_statistics(self, dataframe):

        total_participants = len(dataframe)

        participants_with_email = (
            dataframe[EMAIL_COLUMN]
            .notna()
            .sum()
        )

        participants_without_email = (
            dataframe[EMAIL_COLUMN]
            .isna()
            .sum()
        )

        unique_emails = (
            dataframe[EMAIL_COLUMN]
            .dropna()
            .nunique()
        )

        duplicate_emails = (
            dataframe[EMAIL_COLUMN]
            .dropna()
            .duplicated()
            .sum()
        )

        dataframe_without_email = dataframe[
            dataframe[EMAIL_COLUMN].isna()
        ]

        possible_duplicates_without_email = (
            dataframe_without_email[
                dataframe_without_email.duplicated(
                    subset=[NAME_COLUMN],
                    keep=False
                )
            ][NAME_COLUMN]
            .nunique()
        )

        column_statistics = {}

        for column_name, display_name in STATISTICS_COLUMNS:

            if column_name in dataframe.columns:

                completed = dataframe[column_name].notna().sum()

                missing = dataframe[column_name].isna().sum()

                column_statistics[display_name] = {

                    "completed": completed,

                    "missing": missing
                }

        return {

            "total_participants": total_participants,

            "participants_with_email": participants_with_email,

            "participants_without_email": participants_without_email,

            "unique_emails": unique_emails,

            "duplicate_emails": duplicate_emails,

            "possible_duplicates_without_email":
                possible_duplicates_without_email,

            "column_statistics": column_statistics
        }