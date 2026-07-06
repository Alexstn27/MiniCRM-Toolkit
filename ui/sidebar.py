import customtkinter as ctk


class Sidebar:
    def __init__(self, parent, on_dashboard_clicked, on_history_clicked):

        self.sidebar_frame = ctk.CTkFrame(
            parent,
            width=220,
            fg_color="#2B2B2B"
        )

        self.sidebar_frame.pack(
            side="left",
            fill="y"
        )
        self.on_dashboard_clicked = on_dashboard_clicked
        self.on_history_clicked = on_history_clicked
        
        self.create_widgets()
        self.layout_widgets()
    
    def create_widgets(self):
        self.sidebar_title = ctk.CTkLabel(
      
        self.sidebar_frame,
        text="MiniCRM Toolkit",
        font=("Segoe UI", 16, "bold")
        )

        self.general_label = ctk.CTkLabel(
        self.sidebar_frame,
        text="GENERAL",
        font=("Segoe UI", 11, "bold")
        )
        
        self.dashboard_button = self.create_sidebar_button(
             "Dashboard",
             self.on_dashboard_clicked
        )

        self.minicrm_label = ctk.CTkLabel(
        self.sidebar_frame,
        text="MINICRM",
        font=("Segoe UI", 11, "bold")
        )

        self.history_button = self.create_sidebar_button(
        "Actualizare istoric",
        self.on_history_clicked
        )

        self.unique_emails_button = self.create_sidebar_button(
        "Emailuri unice",
        lambda: print("Unique Emails clicked")
        )

        self.duplicates_button = self.create_sidebar_button(
        "Eliminare duplicate",
        lambda: print("Duplicates clicked")
        )

    def layout_widgets(self):
        self.sidebar_title.pack(
        padx=20,
        pady=(20, 10),
        anchor="w"
        )

        self.general_label.pack(
        padx=20,
        pady=(15, 5),
        anchor="w"
        )

        self.dashboard_button.pack(
        padx=10,
        pady=10,
        fill="x"
        )

        self.minicrm_label.pack(
        padx=20,
        pady=(20, 5),
        anchor="w"
        )

        self.history_button.pack(
        padx=10,
        pady=5,
        fill="x"
        )

        self.unique_emails_button.pack(
        padx=10,
        pady=5,
        fill="x"
        )

        self.duplicates_button.pack(
        padx=10,
        pady=5,
        fill="x"
        )
    

    def create_sidebar_button(self, text, command):
        return ctk.CTkButton(
        self.sidebar_frame,
        text=text,
        command=command
    )

    def on_dashboard_clicked(self):
        print("Dashboard clicked")