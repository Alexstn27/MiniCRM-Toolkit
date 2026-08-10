import customtkinter as ctk
from ui.components import FileSelector, log_message
from modules.duplicate_remover import DuplicateRemoverModule

class DuplicateRemover:

    def __init__(self, parent):

        self.page_frame = ctk.CTkFrame(parent)
        self.duplicate_module = DuplicateRemoverModule()
        self.file_selector = FileSelector(self.page_frame)

        self.create_widgets()
        self.layout_widgets()

        self.log_message = lambda message: log_message(
            self.result_box,
            message
        )

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

        self.file_selector.selected_file_label.pack(
            padx=20,
            anchor="w"
        )

        self.file_selector.browse_button.pack(
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

   
    def remove_duplicates(self):

        self.result_box.delete("1.0", "end")

        if self.file_selector.selected_file is None:
            self.log_message("❌ Selectează un fișier Excel.")
            return

        dataframe = self.duplicate_module.load_excel(
            self.file_selector.selected_file
        )

        possible_duplicates = (
            self.duplicate_module.find_possible_duplicates_without_email(
                dataframe
            )
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

        if len(possible_duplicates) > 0:

            self.log_message("")
            self.log_message("⚠ Posibile duplicate fără email:")

            for duplicate in possible_duplicates:

                name = duplicate["name"]
                score = duplicate["score"]

                stars = self.duplicate_module.get_score_stars(
                    score
                )

                self.log_message(
                    f"{stars} {name} ({score}%)"
                )

        self.log_message(
            "✔ Fișier salvat cu succes."
        )

        self.log_message(
            f"📁 {output_path}"
        )
        self.log_message("✅ Operațiunea s-a încheiat cu succes.")
