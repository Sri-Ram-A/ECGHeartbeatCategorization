import customtkinter as ctk
from components.form_components import (
    create_label_entry, 
    create_main_button, 
    create_link_button, 
    ErrorLabel,
    create_card,
    create_title_label,
    create_subtitle_label
)
from components.colors import get_colors
from PIL import Image
from pathlib import Path
class DoctorLoginScreen(ctk.CTkFrame):
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.colors = get_colors(is_dark_mode=False)
        file_path = Path().resolve() / "assets" / "bg.png"
        print(file_path)
        # Background Image
        bg_image = ctk.CTkImage(
            light_image=Image.open(str(file_path)),
            dark_image=Image.open(str(file_path)),
            size=(self.winfo_screenwidth(), self.winfo_screenheight())
        )
        bg_label = ctk.CTkLabel(self, image=bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        # Main container centered on screen
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)
        form_container = ctk.CTkFrame(main, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title Section
        create_title_label(form_container, "Doctor Login", self.colors).pack(pady=(0, 10))
        create_subtitle_label(form_container, "Enter credentials to monitor patients", self.colors).pack(pady=(0, 30))
        card, card_content = create_card(form_container, "Login", self.colors)

        # Form Fields
        form = ctk.CTkFrame(card_content, fg_color="transparent")
        form.pack(fill="both", expand=True)
        _, self.doctor_id = create_label_entry(form, "Doctor ID", "D-123456", colors=self.colors)
        _, self.password = create_label_entry(form, "Password", "••••••••", show_char="*", colors=self.colors)
        
        self.error_label = ErrorLabel(form, colors=self.colors)
        
        # Login button
        login_btn = create_main_button(form, "Login", self.login, self.colors)
        login_btn.pack(pady=(0, 20))
        
        # Link to Registration
        register_link = create_link_button(
            form, 
            "Don't have an account? Register Here", 
            self._go_to_registration,
            self.colors
        )
        register_link.pack()
        
        # Bind Enter key
        self.doctor_id.bind("<Return>", lambda e: self.login())
        self.password.bind("<Return>", lambda e: self.login())
    
    def login(self):
        """Handle doctor login with validation."""
        doctor_id = self.doctor_id.get().strip()
        password = self.password.get().strip()
        
        if doctor_id == "D-101" and password == "pass":
            mock_doctor_data = ("D-101", "Dr. Jane Doe", "Cardiologist")
            from screens.patient_login import PatientLoginScreen
            self.app.show_screen(PatientLoginScreen, doctor_data=mock_doctor_data)
        else:
            self.error_label.set_error("Invalid Doctor ID or Password.")
    
    def _go_to_registration(self):
        """Navigate to doctor registration screen."""
        from screens.doctor_registration import DoctorRegistrationScreen
        self.app.show_screen(DoctorRegistrationScreen)