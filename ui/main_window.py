import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.history_updater import HistoryUpdater
from ui.duplicate_remover import DuplicateRemover

class MainWindow:
    def __init__(self):
        self.main_window = ctk.CTk()

        self.current_page = None

        self.main_window.title("MiniCRM Toolkit")
        self.main_window.geometry("1000x700")
        self.main_window.minsize(900, 600)

        self.sidebar = Sidebar(
            self.main_window,
            self.on_dashboard_clicked,
            self.on_history_updater_clicked,
            self.on_duplicate_remover_clicked
        )

        
        self.content = ctk.CTkFrame(
        self.main_window,
        fg_color="#3A3A3A"
        )

        self.content.pack(side="right", fill="both", expand=True)

        self.show_page(Dashboard)


    def show_page(self, page_class):
        
        if self.current_page is not None:
            self.current_page.page_frame.destroy()

        self.current_page = page_class(self.content)

    def on_history_updater_clicked(self):
        self.show_page(HistoryUpdater)

    def on_dashboard_clicked(self):
        self.show_page(Dashboard)
        
    def run(self):
        self.main_window.mainloop()

    def on_duplicate_remover_clicked(self):
        self.show_page(DuplicateRemover)