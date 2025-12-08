import customtkinter as ctk
from components.form_components import (
    create_label_entry, 
    create_main_button, 
    create_link_button, 
    ErrorLabel, 
    StatusLabel,
    create_card
)
from components.colors import get_colors


class DoctorRegistrationScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.colors = get_colors(is_dark_mode=False)
        
        # Main container centered on screen
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)

        form_container = ctk.CTkFrame(main, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title Section
        ctk.CTkLabel(
            form_container, 
            text="Doctor Registration",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            form_container, 
            text="Create your professional account",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        ).pack(pady=(0, 30))
        
        # Registration Card
        card, card_content = create_card(form_container, "Create Account", self.colors)
        
        form = ctk.CTkFrame(card_content, fg_color="transparent")
        form.pack(fill="both", expand=True)

        # Form Fields
        _, self.doctor_id = create_label_entry(
            form, "Doctor ID (D-XXXX)", "D-654321", colors=self.colors
        )
        _, self.name = create_label_entry(
            form, "Full Name", "Dr. Robert Smith", colors=self.colors
        )
        _, self.specialization = create_label_entry(
            form, "Specialization", "e.g., General Practitioner", colors=self.colors
        )
        _, self.password = create_label_entry(
            form, "Password", "••••••••", show_char="*", colors=self.colors
        )
        
        self.error_label = ErrorLabel(form, colors=self.colors)
        self.status_label = StatusLabel(form, colors=self.colors)

        # Register button
        register_btn = create_main_button(form, "Register Account", self.register, self.colors)
        register_btn.pack(pady=(0, 20))
        
        # Back to Login link
        login_link = create_link_button(
            form, 
            "Already registered? Back to Login", 
            self._go_to_login,
            self.colors
        )
        login_link.pack()
    
    def register(self):
        """Handle doctor registration with validation."""
        self.error_label.clear()
        self.status_label.clear()
        
        doctor_id = self.doctor_id.get().strip()
        name = self.name.get().strip()
        specialization = self.specialization.get().strip()
        password = self.password.get().strip()
        
        if not all([doctor_id, name, specialization, password]):
            self.error_label.set_error("All fields must be filled.")
            return

        self.status_label.set_success(f"Successfully registered Doctor ID: {doctor_id}")
        
        # Clear fields
        self.doctor_id.delete(0, 'end')
        self.name.delete(0, 'end')
        self.specialization.delete(0, 'end')
        self.password.delete(0, 'end')
        
    def _go_to_login(self):
        """Navigate to doctor registration screen."""
        from screens.doctor_login import DoctorLoginScreen
        self.app.show_screen(DoctorLoginScreen)