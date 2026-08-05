import pandas as pd
from datetime import datetime

from core.constants import (
    EMAIL_COLUMN,
    NAME_COLUMN,
    PHONE_COLUMN,
    WORKPLACE_COLUMN,
    CITY_COLUMN,
    NAME_SCORE,
    PHONE_SCORE,
    WORKPLACE_SCORE,
    CITY_SCORE
)


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

    def calculate_duplicate_score(
            self,
            row1,
            row2,
            dataframe
        ):

            earned_points = 0
            possible_points = 0

            # Nume
            possible_points += NAME_SCORE

            if row1[NAME_COLUMN] == row2[NAME_COLUMN]:
                earned_points += NAME_SCORE

            # Telefon
            if (
                PHONE_COLUMN in dataframe.columns
                and not pd.isna(row1[PHONE_COLUMN])
                and not pd.isna(row2[PHONE_COLUMN])
            ):

                possible_points += PHONE_SCORE

                if row1[PHONE_COLUMN] == row2[PHONE_COLUMN]:
                    earned_points += PHONE_SCORE

            # Loc de muncă
            if (
                WORKPLACE_COLUMN in dataframe.columns
                and not pd.isna(row1[WORKPLACE_COLUMN])
                and not pd.isna(row2[WORKPLACE_COLUMN])
            ):

                possible_points += WORKPLACE_SCORE

                if row1[WORKPLACE_COLUMN] == row2[WORKPLACE_COLUMN]:
                    earned_points += WORKPLACE_SCORE

            # Oraș
            if (
                CITY_COLUMN in dataframe.columns
                and not pd.isna(row1[CITY_COLUMN])
                and not pd.isna(row2[CITY_COLUMN])
            ):

                possible_points += CITY_SCORE

                if row1[CITY_COLUMN] == row2[CITY_COLUMN]:
                    earned_points += CITY_SCORE

            if possible_points == 0:
                return 0

            percentage = round(
                earned_points / possible_points * 100
            )

            return percentage

    def get_score_stars(self, score):

        if score >= 90:
            return "★★★★★"

        elif score >= 75:
            return "★★★★☆"

        elif score >= 60:
            return "★★★☆☆"

        elif score >= 40:
            return "★★☆☆☆"

        else:
            return "★☆☆☆☆"

    def find_possible_duplicates_without_email(self, dataframe):

        dataframe_without_email = dataframe[
            dataframe[EMAIL_COLUMN].isna()
        ].copy()

        duplicate_rows = dataframe_without_email[
            dataframe_without_email.duplicated(
                subset=[NAME_COLUMN],
                keep=False
            )
        ]

        results = []

        processed_names = []

        for name in duplicate_rows[NAME_COLUMN].unique():

            if name in processed_names:
                continue

            people = duplicate_rows[
                duplicate_rows[NAME_COLUMN] == name
            ]

            if len(people) < 2:
                continue

            row1 = people.iloc[0]
            row2 = people.iloc[1]

            score = self.calculate_duplicate_score(
                row1,
                row2,
                dataframe
            )

            results.append(
                {
                    "name": name,
                    "score": score
                }
            )

            processed_names.append(name)

        return results
    
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