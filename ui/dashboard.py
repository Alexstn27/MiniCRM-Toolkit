import customtkinter as ctk


class Dashboard:
    def __init__(self, parent):

        self.page_frame = ctk.CTkFrame(parent)

        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):

        self.dashboard_title = ctk.CTkLabel(
            self.page_frame,
            text="Dashboard",
            font=("Segoe UI", 24, "bold")
        )

    def layout_widgets(self):

        self.page_frame.pack(
            fill="both",
            expand=True
        )

        self.dashboard_title.pack(
            padx=20,
            pady=20,
            anchor="w"
        )