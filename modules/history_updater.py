import pandas as pd
from datetime import datetime
from core.constants import (
    WEBINAR_HISTORY_COLUMN,
    PHYSICAL_EVENT_HISTORY_COLUMN
)

class HistoryUpdaterModule:

    def load_excel(self, file_path):

        dataframe = pd.read_excel(file_path)

        return dataframe

    def validate_columns(
        self,
        dataframe,
        event_type
    ):

        if event_type == "webinar":

            required_column = WEBINAR_HISTORY_COLUMN

        else:

            required_column = PHYSICAL_EVENT_HISTORY_COLUMN

        if required_column not in dataframe.columns:
            return False

        return True

    def update_history(
        self,
        dataframe,
        event_name,
        event_type
    ):
        if event_type == "webinar":
            history_column = WEBINAR_HISTORY_COLUMN

        else:
            history_column = PHYSICAL_EVENT_HISTORY_COLUMN       

        updated_count = 0
        skipped_count = 0

        for index, row in dataframe.iterrows():

            history = row[history_column]

            if pd.isna(history):

                dataframe.at[index, history_column] = event_name
                updated_count += 1

            else:

                history = history.strip()

                if history.endswith(";"):
                    history = history[:-1].strip()

                if event_name in history:
                    skipped_count += 1

                else:
                    dataframe.at[index, history_column] = (
                        history + "; " + event_name
                    )
                    updated_count += 1

        return updated_count, skipped_count
    
    def save_excel(self, dataframe, event_name):

        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M")

        output_path = (
            f"output/{event_name} - Import MiniCRM - {timestamp}.xlsx"
        )

        dataframe.to_excel(
            output_path,
            index=False
        )

        return output_path