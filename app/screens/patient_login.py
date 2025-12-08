import customtkinter as ctk
from components.form_components import (
    create_label_entry, 
    create_accent_button,
    create_link_button, 
    ErrorLabel,
    create_card,
    create_info_row
)
from components.colors import get_colors


class PatientLoginScreen(ctk.CTkFrame):
    def __init__(self, parent, app, doctor_data):
        super().__init__(parent)
        self.app = app
        self.doctor_data = doctor_data
        self.colors = get_colors(is_dark_mode=False)
        
        # Main container
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        # Doctor Info Header
        doctor_id, doctor_name, specialization = self.doctor_data
        doctor_card, doc_content = create_card(main, f"{doctor_name}", self.colors)
        
        ctk.CTkLabel(
            doc_content, 
            text=f"Specialization: {specialization}",
            font=ctk.CTkFont(size=16),
            text_color=self.colors["text_secondary"]
        ).pack(anchor="w", pady=5)
        
        ctk.CTkLabel(
            doc_content, 
            text=f"ID: {doctor_id}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(anchor="w")

        # Title
        ctk.CTkLabel(
            main, 
            text="Patient Session Login",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(pady=(20, 10), anchor="w")
        
        ctk.CTkLabel(
            main, 
            text="Retrieve a patient record to start monitoring",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        ).pack(pady=(0, 30), anchor="w")
        
        # Login Card
        card, card_content = create_card(main, "Retrieve Record", self.colors)
        
        form = ctk.CTkFrame(card_content, fg_color="transparent")
        form.pack(fill="both", expand=True)

        # Form Fields
        _, self.patient_id = create_label_entry(
            form, "Patient ID", "P-987654", colors=self.colors
        )
        _, self.patient_dob = create_label_entry(
            form, "Date of Birth (YYYY-MM-DD)", "1990-01-01", colors=self.colors
        )
        
        self.error_label = ErrorLabel(form, colors=self.colors)
        
        # Buttons
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 20))
        
        login_btn = create_accent_button(
            btn_frame, "Retrieve Record →", self.login, self.colors
        )
        login_btn.pack(side="right")
        
        # Link to Registration
        register_link = create_link_button(
            form, 
            "Patient not registered? Register Patient", 
            self._go_to_registration,
            self.colors
        )
        register_link.pack()

    def login(self):
        """Handle patient login and retrieve record."""
        patient_id = self.patient_id.get().strip()
        patient_dob = self.patient_dob.get().strip()
        
        if patient_id and patient_dob:
            mock_patient_data = (patient_id, "Patient Max Power", "45", "+1 (123) 456-7890")
            from screens.session_detail import SessionDetailScreen
            self.app.show_screen(
                SessionDetailScreen, 
                doctor_data=self.doctor_data, 
                patient_data=mock_patient_data
            )
        else:
            self.error_label.set_error("Please enter Patient ID and Date of Birth.")
    
    def _go_to_registration(self):
        """Navigate to patient registration screen."""
        from screens.patient_registration import PatientRegistrationScreen
        self.app.show_screen(
            PatientRegistrationScreen, 
            doctor_data=self.doctor_data
        )


