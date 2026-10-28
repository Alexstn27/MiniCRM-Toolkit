import customtkinter as ctk
from ui.components import FileSelector, log_message
from modules.duplicate_remover import DuplicateRemoverModule, compare_and_filter_files

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


        self.comparison_title = ctk.CTkLabel(
            self.page_frame,
            text="Compară două fișiere Excel",
            font=ctk.CTkFont(size=16, weight="bold"),
        )

        self.main_file_label = ctk.CTkLabel(
            self.page_frame,
            text="1. Lista principală",
        )

        self.main_file_selector = FileSelector(self.page_frame)

        self.comparison_file_label = ctk.CTkLabel(
            self.page_frame,
            text="2. Lista cu participanții de eliminat",
        )

        self.comparison_file_selector = FileSelector(self.page_frame)

        self.compare_files_button = ctk.CTkButton(
            self.page_frame,
            text="Compară Excelurile și elimină persoanele comune",
            command=self.compare_and_remove_common,
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

        self.comparison_title.pack(
            anchor="w", padx=20, pady=(24, 10)
        )

        self.main_file_label.pack(
            anchor="w", padx=20, pady=(4, 2)
        )
        self.main_file_selector.selected_file_label.pack(
            anchor="w", fill="x", padx=20, pady=2
        )
        self.main_file_selector.browse_button.pack(
            anchor="w", padx=20, pady=(2, 10)
        )

        self.comparison_file_label.pack(
            anchor="w", padx=20, pady=(4, 2)
        )
        self.comparison_file_selector.selected_file_label.pack(
            anchor="w", fill="x", padx=20, pady=2
        )
        self.comparison_file_selector.browse_button.pack(
            anchor="w", padx=20, pady=(2, 10)
        )

        self.compare_files_button.pack(
            anchor="w", padx=20, pady=(5, 15)
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


    def compare_and_remove_common(self):

        self.result_box.delete("1.0", "end")

        main_file = self.main_file_selector.selected_file
        comparison_file = self.comparison_file_selector.selected_file

        if main_file is None:
            self.log_message("❌ Selectează fișierul Excel principal.")
            return

        if comparison_file is None:
            self.log_message(
                "❌ Selectează fișierul Excel cu persoanele de eliminat."
            )
            return

        if main_file == comparison_file:
            self.log_message(
                "❌ Selectează două fișiere Excel diferite."
            )
            return

        try:
            self.log_message("🔄 Se compară cele două fișiere Excel...")

            result = compare_and_filter_files(
                main_file,
                comparison_file
            )

            self.log_message("")
            self.log_message("========== REZULTAT COMPARARE ==========")

            self.log_message(
                f"Persoane în lista principală: {result['main_count']}"
            )

            self.log_message(
                f"Persoane în lista de comparație: "
                f"{result['comparison_count']}"
            )

            self.log_message(
                f"Eliminate prin email: {result['removed_by_email']}"
            )

            self.log_message(
                f"Eliminate prin nume: {result['removed_by_name']}"
            )

            self.log_message(
                f"Total persoane eliminate: {result['removed_count']}"
            )

            self.log_message(
                f"Persoane rămase: {result['remaining_count']}"
            )

            review_records = result["review_records"]

            self.log_message("")
            self.log_message(
                f"========== DE VERIFICAT MANUAL: "
                f"{len(review_records)} cazuri =========="
            )

            if not review_records:
                self.log_message(
                    "✅ Nu au fost identificate cazuri care necesită verificare."
                )

            else:
                for number, person in enumerate(review_records, start=1):

                    self.log_message("")
                    self.log_message(f"--- Cazul {number} ---")

                    self.log_message(
                        f"Motiv: {person['Motiv verificare']}"
                    )

                    self.log_message(
                        f"Nume - lista principală: "
                        f"{person['Nume lista principala'] or '(lipsă)'}"
                    )

                    self.log_message(
                        f"Email - lista principală: "
                        f"{person['Email lista principala'] or '(lipsă)'}"
                    )

                    self.log_message(
                        f"Nume - lista achitați: "
                        f"{person['Nume lista achitati'] or '(lipsă)'}"
                    )

                    self.log_message(
                        f"Email - lista achitați: "
                        f"{person['Email lista achitati'] or '(lipsă)'}"
                    )

            self.log_message("")
            self.log_message("✅ Fișierul rezultat a fost salvat.")
            self.log_message(f"📁 {result['output_path']}")
            self.log_message(
                "📄 Fișierul conține sheet-urile "
                "'Participanti ramasi' și 'De verificat'."
            )

        except Exception as error:
            self.log_message(
                f"❌ Eroare la compararea fișierelor: {error}"
            )