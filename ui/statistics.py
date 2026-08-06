import customtkinter as ctk
from tkinter import filedialog

from modules.statistics import StatisticsModule


class Statistics:

    def __init__(self, parent):

        self.statistics_module = StatisticsModule()

        self.selected_file = None

        self.page_frame = ctk.CTkFrame(
            parent,
            fg_color="#3A3A3A"
        )

        self.page_frame.pack(
            fill="both",
            expand=True
        )

        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):

        self.title_label = ctk.CTkLabel(
            self.page_frame,
            text="Statistici",
            font=("Segoe UI", 24, "bold")
        )

        self.browse_button = ctk.CTkButton(
            self.page_frame,
            text="Selecteaza fisierul",
            command=self.browse_file
        )

        self.selected_file_label = ctk.CTkLabel(
            self.page_frame,
            text="Niciun fișier selectat"
        )

        self.statistics_button = ctk.CTkButton(
            self.page_frame,
            text="Generează statistici",
            command=self.generate_statistics
        )

        self.result_box = ctk.CTkTextbox(
            self.page_frame,
            width=700,
            height=350
        )

    def layout_widgets(self):

        self.title_label.pack(
            pady=(20, 10)
        )

        self.browse_button.pack(
            pady=10
        )

        self.selected_file_label.pack(
            pady=5
        )

        self.statistics_button.pack(
            pady=10
        )

        self.result_box.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

    def browse_file(self):

        file_path = filedialog.askopenfilename(
            title="Selectează fișierul Excel",
            filetypes=[
                ("Excel files", "*.xlsx")
            ]
        )

        if file_path:

            self.selected_file = file_path

            self.selected_file_label.configure(
                text=file_path
            )

    def log_message(self, message):

        self.result_box.insert(
            "end",
            message + "\n"
        )

    def generate_statistics(self):

        self.result_box.delete(
            "1.0",
            "end"
        )

        dataframe = self.statistics_module.load_excel(
            self.selected_file
        )

        if not self.statistics_module.validate_columns(
            dataframe
        ):

            self.log_message(
                "❌ Fișier invalid."
            )

            return

        self.log_message(
            "✔ Fișier valid."
        )

        statistics = (
            self.statistics_module.get_statistics(
                dataframe
            )
        )

        self.log_message("")
        self.log_message("📊 Statistici")
        self.log_message("")

        self.log_message(
            f"✔ Participanți: {statistics['total_participants']}"
        )

        self.log_message(
            f"✔ Participanți cu email: {statistics['participants_with_email']}"
        )

        self.log_message(
            f"✔ Participanți fără email: {statistics['participants_without_email']}"
        )

        self.log_message(
            f"✔ Emailuri unice: {statistics['unique_emails']}"
        )

        self.log_message(
            f"✔ Emailuri duplicate: {statistics['duplicate_emails']}"
        )

        self.log_message(
            f"✔ Posibile duplicate fără email: {statistics['possible_duplicates_without_email']}"
        )

        for column_name, values in statistics["column_statistics"].items():

            self.log_message("")

            self.log_message(
                f"✔ {column_name} completat: {values['completed']}"
            )

            self.log_message(
                f"✔ {column_name} lipsă: {values['missing']}"
            )

        self.log_message("")
        self.log_message("✔ Statistici generate cu succes."
        )