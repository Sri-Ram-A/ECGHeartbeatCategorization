import customtkinter as ctk
from screens.doctor_login import DoctorLoginScreen
from components.colors import get_colors


class MedicalMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HeartRace - Professional Healthcare System")
        self.geometry("1200x750")
        self.minsize(900, 600)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        colors = get_colors(is_dark_mode=False)
        # Main container for header and content
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # --- TOP HEADER BAR ---
        self.header_frame = ctk.CTkFrame(
            main_container, 
            height=60, 
            fg_color=colors["card_background"],
            border_width=1,
            border_color=colors["border"]
        )
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)
        # Title and Header Content
        header_content = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=25, pady=10)
        # Left: Title
        ctk.CTkLabel(
            header_content, 
            text="HeartRace ♡",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=colors["primary"]
        ).pack(side="left")
        # Right: Exit Button
        exit_btn = ctk.CTkButton(
            header_content, 
            text="✕ Exit",
            width=100, 
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=colors["error"],
            hover_color=colors["error_hover"],
            command=self.destroy
        )
        exit_btn.pack(side="right")
        
        # --- CONTENT CONTAINER ---
        self.container = ctk.CTkFrame(
            main_container, 
            fg_color=colors["background"]
        )
        self.container.pack(fill="both", expand=True)
        self.current_screen = None
        
        # Show initial screen
        self.show_screen(DoctorLoginScreen)
    
    def show_screen(self, screen_class, **kwargs):
        """
        Switches the current screen to the desired class.
        Args:
            screen_class: The screen class to display
            **kwargs: Additional arguments to pass to the screen
        """
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self.container, self, **kwargs)
        self.current_screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = MedicalMonitorApp()
    app.mainloop()