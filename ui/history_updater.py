import customtkinter as ctk
from ui.components import FileSelector, log_message
from modules.history_updater import HistoryUpdaterModule

class HistoryUpdater:

    def __init__(self, parent):

        self.page_frame = ctk.CTkFrame(parent)
        self.event_type = ctk.StringVar(value="webinar")
        self.history_module = HistoryUpdaterModule()
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

        self.event_type_label = ctk.CTkLabel(
            self.page_frame,
            text="Tip eveniment"
        )

        self.webinar_radio = ctk.CTkRadioButton(
            self.page_frame,
            text="Webinar",
            variable=self.event_type,
            value="webinar"
        )

        self.physical_event_radio = ctk.CTkRadioButton(
            self.page_frame,
            text="Eveniment fizic",
            variable=self.event_type,
            value="physical"
        )

        self.file_label = ctk.CTkLabel(
            self.page_frame,
            text="Fișier Excel"
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

        self.event_type_label.pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        self.webinar_radio.pack(
            anchor="w",
            padx=20
        )

        self.physical_event_radio.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
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

   
    def update_history(self):

        self.result_box.delete("1.0", "end")

        event_name = self.event_entry.get().strip()
        event_type = self.event_type.get()

        if event_name == "":
            self.log_message("❌ Introdu numele evenimentului.")
            return

        if self.file_selector.selected_file is None:
            self.log_message("❌ Selectează un fișier Excel.")
            return

        dataframe = self.history_module.load_excel(
            self.file_selector.selected_file
        )

        if not self.history_module.validate_columns(
            dataframe,
            event_type
        ):
            self.log_message("❌ Fișier invalid.")
            return

        self.log_message(
            f"✔ Fișier valid pentru {event_type}."
        )
        
        updated_count, skipped_count = self.history_module.update_history(
            dataframe,
            event_name,
            event_type
        )

        output_path = self.history_module.save_excel(
            dataframe,
            event_name
        )

        self.log_message(f"✔ Istorice actualizate: {updated_count}")
        self.log_message(
            f"⚠ Participanți care aveau deja evenimentul: {skipped_count}"
        )

        self.log_message("✔ Fișier salvat cu succes.")
        self.log_message(f"📁 {output_path}")
    
  