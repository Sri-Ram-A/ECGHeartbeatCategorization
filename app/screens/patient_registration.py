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


class PatientRegistrationScreen(ctk.CTkFrame):
    def __init__(self, parent, app, doctor_data):
        super().__init__(parent)
        self.app = app
        self.doctor_data = doctor_data
        self.colors = get_colors(is_dark_mode=False)
        
        # Main container centered on screen
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        form_container = ctk.CTkFrame(main, fg_color="transparent")
        form_container.pack(fill="both", expand=True)
        
        # Title Section
        ctk.CTkLabel(
            form_container, 
            text="Patient Registration",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(pady=(0, 10), anchor="w")
        
        ctk.CTkLabel(
            form_container, 
            text="Register a new patient record",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        ).pack(pady=(0, 30), anchor="w")
        
        # Registration Card
        card, card_content = create_card(form_container, "Create Patient Record", self.colors)
        
        form = ctk.CTkFrame(card_content, fg_color="transparent")
        form.pack(fill="both", expand=True)

        # Form Fields
        _, self.patient_id = create_label_entry(
            form, "Patient ID (P-XXXX)", "P-900001", colors=self.colors
        )
        _, self.name = create_label_entry(
            form, "Full Name", "Patient Jane Doe", colors=self.colors
        )
        _, self.age = create_label_entry(
            form, "Age", "e.g., 35", colors=self.colors
        )
        _, self.phone = create_label_entry(
            form, "Contact Number", "+1 (555) 123-4567", colors=self.colors
        )
        
        self.error_label = ErrorLabel(form, colors=self.colors)
        self.status_label = StatusLabel(form, colors=self.colors)
        
        # Register button
        register_btn = create_main_button(form, "Register Patient", self.register, self.colors)
        register_btn.pack(pady=(0, 20))
        
        # Back to Patient Login link
        login_link = create_link_button(
            form, 
            "Already Registered? Back to Patient Login", 
            self.go_to_patient_login,
            self.colors
        )
        login_link.pack()
    
    def register(self):
        """Handle patient registration with validation."""
        self.error_label.clear()
        self.status_label.clear()
        
        patient_id = self.patient_id.get().strip()
        name = self.name.get().strip()
        age = self.age.get().strip()
        phone = self.phone.get().strip()
        
        if not all([patient_id, name, age, phone]):
            self.error_label.set_error("All fields must be filled.")
            return

        self.status_label.set_success(f"Successfully registered Patient ID: {patient_id}. Proceed to login.")
        
        # Clear fields
        self.patient_id.delete(0, 'end')
        self.name.delete(0, 'end')
        self.age.delete(0, 'end')
        self.phone.delete(0, 'end')
    
    def go_to_patient_login(self):
        """Navigate back to patient login screen."""
        from screens.patient_login import PatientLoginScreen
        self.app.show_screen(PatientLoginScreen, doctor_data=self.doctor_data)
        