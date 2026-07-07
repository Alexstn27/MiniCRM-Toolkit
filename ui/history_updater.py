import customtkinter as ctk
from tkinter import filedialog
from modules.history_updater import HistoryUpdaterModule

class HistoryUpdater:

    def __init__(self, parent):

        self.page_frame = ctk.CTkFrame(parent)
        self.selected_file = None
        self.history_module = HistoryUpdaterModule()

        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):

        self.title_label = ctk.CTkLabel(
            self.page_frame,
            text="Actualizare istoric",
            font=("Segoe UI", 24, "bold")
        )
        self.event_label = ctk.CTkLabel(
            self.page_frame,
            text="Nume eveniment"
        )

        self.event_entry = ctk.CTkEntry(
            self.page_frame,
            placeholder_text="Ex: SAD 12-13 iunie 2026"
        )

        self.file_label = ctk.CTkLabel(
            self.page_frame,
            text="Fișier Excel"
        )

        self.selected_file_label = ctk.CTkLabel(
            self.page_frame,
            text="Niciun fișier selectat",
            anchor="w"
        )

        self.browse_button = ctk.CTkButton(
            self.page_frame,
            text="Browse...",
            command=self.browse_file
        )

        self.update_button = ctk.CTkButton(
            self.page_frame,
            text="Actualizează istoricul",
            command=self.update_history
        )

        self.result_box = ctk.CTkTextbox(
            self.page_frame,
            height=180
        )

    def layout_widgets(self):

        self.page_frame.pack(
            fill="both",
            expand=True
        )

        self.title_label.pack(
            padx=20,
            pady=20,
            anchor="w"
        )

        self.event_label.pack(
            padx=20,
            pady=(10, 5),
            anchor="w"
        )

        self.event_entry.pack(
            padx=20,
            fill="x"
        )

        self.file_label.pack(
            padx=20,
            pady=(20, 5),
            anchor="w"
        )

        self.selected_file_label.pack(
            padx=20,
            anchor="w"
        )

        self.browse_button.pack(
            padx=20,
            pady=10,
            anchor="w"
        )

        self.update_button.pack(
            padx=20,
            pady=20
        )

        self.result_box.pack(
            padx=20,
            pady=(10, 20),
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

    def update_history(self):

        dataframe = self.history_module.load_excel(
            self.selected_file
        )

        print(dataframe.columns.tolist())