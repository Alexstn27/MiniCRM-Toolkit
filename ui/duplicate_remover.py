import customtkinter as ctk
from tkinter import filedialog
from modules.duplicate_remover import DuplicateRemoverModule

class DuplicateRemover:

    def __init__(self, parent):

        self.page_frame = ctk.CTkFrame(parent)
        self.selected_file = None
        self.duplicate_module = DuplicateRemoverModule()

        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):

        self.title_label = ctk.CTkLabel(
            self.page_frame,
            text="Eliminare duplicate",
            font=("Segoe UI", 24, "bold")
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
            text="Elimină duplicate",
            command=self.remove_duplicates
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

    def remove_duplicates(self):

        self.result_box.delete("1.0", "end")

        dataframe = self.duplicate_module.load_excel(
            self.selected_file
        )

        if not self.duplicate_module.validate_columns(dataframe):
            self.log_message("❌ Fișier invalid.")
            return

        self.log_message("✔ Fișier valid.")

        original_count = len(dataframe)
        self.log_message("🔄 Se elimină duplicatele...")

        dataframe, removed_count = (
            self.duplicate_module.remove_duplicates(
                dataframe
            )
        )

        output_path = self.duplicate_module.save_excel(
            dataframe
        )

        final_count = len(dataframe)

        self.log_message(
            f"✔ Participanți înainte: {original_count}"
        )

        self.log_message(
            f"✔ Participanți după: {final_count}"
        )

        self.log_message(
            f"✔ Duplicate eliminate: {removed_count}"
        )

        self.log_message(
            "✔ Fișier salvat cu succes."
        )

        self.log_message(
            f"📁 {output_path}"
        )
        self.log_message("✅ Operațiunea s-a încheiat cu succes.")
    
    def log_message(self, message):

        self.result_box.insert("end", message + "\n")
        self.result_box.see("end")