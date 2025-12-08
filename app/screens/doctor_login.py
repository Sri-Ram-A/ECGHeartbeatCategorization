import customtkinter as ctk
from screens.patient_login import PatientLoginScreen

class DoctorLoginScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#f8f9fa")
        self.app = app
        
        # Left side - Branding
        left = ctk.CTkFrame(self, fg_color="#1976D2", corner_radius=0)
        left.pack(side="left", fill="both", expand=True)
        
        brand_container = ctk.CTkFrame(left, fg_color="transparent")
        brand_container.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(brand_container, text="🏥", 
                    font=ctk.CTkFont(size=80)).pack(pady=(0, 20))
        
        ctk.CTkLabel(brand_container, text="MediMonitor", 
                    font=ctk.CTkFont(size=36, weight="bold"),
                    text_color="white").pack()
        
        ctk.CTkLabel(brand_container, text="Professional Healthcare Monitoring", 
                    font=ctk.CTkFont(size=14),
                    text_color="white").pack(pady=(10, 30))
        
        # Feature badges
        features = [
            "✓ Real-time Patient Monitoring",
            "✓ Secure Data Transmission",
            "✓ HIPAA Compliant System"
        ]
        for feature in features:
            badge = ctk.CTkFrame(brand_container, fg_color="white", corner_radius=8)
            badge.pack(fill="x", pady=5)
            ctk.CTkLabel(badge, text=feature, 
                        font=ctk.CTkFont(size=13),
                        text_color="#1976D2").pack(padx=15, pady=8)
        
        # Right side - Login form
        right = ctk.CTkFrame(self, fg_color="#f8f9fa", corner_radius=0)
        right.pack(side="right", fill="both", expand=True)
        
        form_container = ctk.CTkFrame(right, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header
        header_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        header_frame.pack(pady=(0, 40))
        
        ctk.CTkLabel(header_frame, text="Doctor Login", 
                    font=ctk.CTkFont(size=32, weight="bold"),
                    text_color="#1a1a1a").pack()
        
        ctk.CTkLabel(header_frame, text="Please enter your credentials to continue", 
                    font=ctk.CTkFont(size=13),
                    text_color="#666666").pack(pady=(5, 0))
        
        # Login card
        card = ctk.CTkFrame(form_container, fg_color="white", 
                           corner_radius=12, border_width=1, border_color="#e0e0e0")
        card.pack()
        
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(padx=40, pady=40)
        
        # Doctor ID field
        id_frame = ctk.CTkFrame(form, fg_color="transparent")
        id_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(id_frame, text="Doctor ID", 
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="#333333").pack(anchor="w", pady=(0, 8))
        
        self.doctor_id = ctk.CTkEntry(id_frame, width=340, height=45, 
                                      placeholder_text="Enter your doctor ID",
                                      font=ctk.CTkFont(size=13),
                                      border_width=1,
                                      corner_radius=8)
        self.doctor_id.pack()
        
        # Doctor Name field
        name_frame = ctk.CTkFrame(form, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(name_frame, text="Full Name", 
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="#333333").pack(anchor="w", pady=(0, 8))
        
        self.doctor_name = ctk.CTkEntry(name_frame, width=340, height=45,
                                       placeholder_text="Dr. John Smith",
                                       font=ctk.CTkFont(size=13),
                                       border_width=1,
                                       corner_radius=8)
        self.doctor_name.pack()
        
        # Specialization field
        spec_frame = ctk.CTkFrame(form, fg_color="transparent")
        spec_frame.pack(fill="x", pady=(0, 25))
        
        ctk.CTkLabel(spec_frame, text="Specialization", 
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="#333333").pack(anchor="w", pady=(0, 8))
        
        self.specialization = ctk.CTkEntry(spec_frame, width=340, height=45,
                                          placeholder_text="e.g., Cardiologist, Neurologist",
                                          font=ctk.CTkFont(size=13),
                                          border_width=1,
                                          corner_radius=8)
        self.specialization.pack()
        
        # Error label
        self.error_label = ctk.CTkLabel(form, text="", 
                                       text_color="#d32f2f", 
                                       font=ctk.CTkFont(size=12))
        self.error_label.pack(pady=(0, 15))
        
        # Login button
        login_btn = ctk.CTkButton(form, text="Continue to Patient Login →", 
                                 width=340, height=48,
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 fg_color="#1976D2",
                                 hover_color="#1565C0",
                                 corner_radius=8,
                                 command=self.login)
        login_btn.pack()
        
        # Footer info
        footer = ctk.CTkFrame(form_container, fg_color="transparent")
        footer.pack(pady=(25, 0))
        
        ctk.CTkLabel(footer, text="Secure session • End-to-end encryption", 
                    font=ctk.CTkFont(size=11),
                    text_color="#999999").pack()
        
        # Bind Enter key
        self.specialization.bind("<Return>", lambda e: self.login())
        self.doctor_name.bind("<Return>", lambda e: self.login())
        self.doctor_id.bind("<Return>", lambda e: self.login())
    
    def login(self):
        doctor_id = self.doctor_id.get().strip()
        doctor_name = self.doctor_name.get().strip()
        specialization = self.specialization.get().strip()
        
        if not doctor_id or not doctor_name or not specialization:
            self.error_label.configure(text="⚠ Please fill all fields")
            return
        
        doctor_data = (doctor_id, doctor_name, specialization)
        self.app.show_screen(PatientLoginScreen, doctor_data=doctor_data)