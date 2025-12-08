import customtkinter as ctk
import threading
import time
from utils.mqtt_client import MQTTPublisher

class SessionDetailScreen(ctk.CTkFrame):
    def __init__(self, parent, app, doctor_data, patient_data):
        super().__init__(parent)
        self.app = app
        self.doctor_data = doctor_data
        self.patient_data = patient_data
        self.session_active = False
        self.mqtt_client = None
        
        # Main container
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main, height=80, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header, text="📋 Session Details", 
                    font=ctk.CTkFont(size=26, weight="bold")).pack(anchor="w")
        
        # Content area
        content = ctk.CTkFrame(main)
        content.pack(fill="both", expand=True)
        
        # Left panel - Info cards
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Doctor card
        self.create_info_card(left, "👨‍⚕️ Doctor Information",
                             [("Name", doctor_data[0]),
                              ("Specialization", doctor_data[1])])
        
        # Patient card
        self.create_info_card(left, "👤 Patient Information",
                             [("Name", patient_data[0]),
                              ("Phone", patient_data[1])])
        
        # Right panel - Control card
        right = ctk.CTkFrame(content, width=350)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)
        
        control = ctk.CTkFrame(right, corner_radius=15)
        control.pack(fill="both", expand=True)
        
        ctk.CTkLabel(control, text="Session Control", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))
        
        # Status
        self.status_frame = ctk.CTkFrame(control, height=60, corner_radius=10)
        self.status_frame.pack(fill="x", padx=20, pady=20)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="⚪ Ready to Start",
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.status_label.pack(pady=15)
        
        # Data display
        data_frame = ctk.CTkFrame(control, corner_radius=10)
        data_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(data_frame, text="Live Data", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        self.temp_label = ctk.CTkLabel(data_frame, text="Temperature: --°C",
                                       font=ctk.CTkFont(size=14))
        self.temp_label.pack(pady=5)
        
        self.time_label = ctk.CTkLabel(data_frame, text="Duration: 00:00",
                                       font=ctk.CTkFont(size=14))
        self.time_label.pack(pady=(5, 15))
        
        # Start button
        self.start_btn = ctk.CTkButton(control, text="▶ Start Session", 
                                       height=50, font=ctk.CTkFont(size=16, weight="bold"),
                                       fg_color="green", hover_color="darkgreen",
                                       command=self.toggle_session)
        self.start_btn.pack(fill="x", padx=20, pady=(0, 20))
        
        # Back button
        back_btn = ctk.CTkButton(control, text="← End & Logout", height=40,
                                fg_color="transparent", border_width=2,
                                command=self.end_session)
        back_btn.pack(fill="x", padx=20, pady=(0, 20))
    
    def create_info_card(self, parent, title, items):
        card = ctk.CTkFrame(parent, corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(card, text=title, 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))
        
        for label, value in items:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(row, text=label, text_color="gray",
                        font=ctk.CTkFont(size=13)).pack(side="left")
            ctk.CTkLabel(row, text=value, 
                        font=ctk.CTkFont(size=13, weight="bold")).pack(side="right")
        
        ctk.CTkFrame(card, height=15).pack()
    
    def toggle_session(self):
        if not self.session_active:
            self.start_session()
        else:
            self.stop_session()
    
    def start_session(self):
        self.session_active = True
        self.start_btn.configure(text="⏹ Stop Session", fg_color="red", hover_color="darkred")
        self.status_label.configure(text="🟢 Session Active")
        
        # Start MQTT publishing
        self.mqtt_client = MQTTPublisher(self.update_data)
        threading.Thread(target=self.mqtt_client.start, daemon=True).start()
        
        # Start timer
        self.start_time = time.time()
        self.update_timer()
    
    def stop_session(self):
        self.session_active = False
        self.start_btn.configure(text="▶ Start Session", fg_color="green", hover_color="darkgreen")
        self.status_label.configure(text="⚪ Session Stopped")
        
        if self.mqtt_client:
            self.mqtt_client.stop()
    
    def update_timer(self):
        if self.session_active:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.time_label.configure(text=f"Duration: {mins:02d}:{secs:02d}")
            self.after(1000, self.update_timer)
    
    def update_data(self, temp):
        self.temp_label.configure(text=f"Temperature: {temp}°C")
    
    def end_session(self):
        if self.session_active:
            self.stop_session()
        from screens.doctor_login import DoctorLoginScreen
        self.app.show_screen(DoctorLoginScreen)