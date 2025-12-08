import customtkinter as ctk
from screens.session_detail import SessionDetailScreen

class PatientLoginScreen(ctk.CTkFrame):
    def __init__(self, parent, app, doctor_data):
        super().__init__(parent)
        self.app = app
        self.doctor_data = doctor_data
        
        # Center container
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = ctk.CTkLabel(center, text=f"Welcome, Dr. {doctor_data[0]}", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(center, text=f"{doctor_data[1]} • Patient Login", 
                               font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(pady=(0, 30))
        
        # Login card
        card = ctk.CTkFrame(center, width=400, height=300, corner_radius=15)
        card.pack(padx=20, pady=20)
        card.pack_propagate(False)
        
        # Form
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(form, text="Patient Name", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        self.patient_name = ctk.CTkEntry(form, width=300, height=40, placeholder_text="Enter patient name")
        self.patient_name.pack(pady=(0, 15))
        
        ctk.CTkLabel(form, text="Phone Number", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        self.phone = ctk.CTkEntry(form, width=300, height=40, placeholder_text="Enter phone number")
        self.phone.pack(pady=(0, 20))
        
        self.error_label = ctk.CTkLabel(form, text="", text_color="red", font=ctk.CTkFont(size=12))
        self.error_label.pack(pady=(0, 10))
        
        login_btn = ctk.CTkButton(form, text="Continue", width=300, height=40,
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 command=self.login)
        login_btn.pack()
        
        # Back button
        back_btn = ctk.CTkButton(center, text="← Back", width=150,
                                fg_color="transparent", hover_color="gray25",
                                command=self.back)
        back_btn.pack(pady=(15, 0))
        
        # Bind Enter key
        self.phone.bind("<Return>", lambda e: self.login())
    
    def login(self):
        patient_name = self.patient_name.get().strip()
        phone = self.phone.get().strip()
        
        if not patient_name or not phone:
            self.error_label.configure(text="Please fill all fields")
            return
        
        patient_data = (patient_name, phone)
        self.app.show_screen(SessionDetailScreen, 
                           doctor_data=self.doctor_data, 
                           patient_data=patient_data)
    
    def back(self):
        from screens.doctor_login import DoctorLoginScreen
        self.app.show_screen(DoctorLoginScreen)