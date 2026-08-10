import customtkinter as ctk
from tkinter import filedialog


class FileSelector:

    def __init__(self, parent):

        self.selected_file = None

        self.selected_file_label = ctk.CTkLabel(
            parent,
            text="Niciun fișier selectat",
            anchor="w"
        )

        self.browse_button = ctk.CTkButton(
            parent,
            text="Browse...",
            command=self.browse_file
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


def log_message(result_box, message):

    result_box.insert(
        "end",
        message + "\n"
    )

    result_box.see("end")