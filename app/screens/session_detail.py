import customtkinter as ctk
import threading
import time
from utils.mqtt_client import MQTTPublisher
from components.form_components import create_card, create_info_row
from components.colors import get_colors


class SessionDetailScreen(ctk.CTkFrame):
    def __init__(self, parent, app, doctor_data, patient_data):
        super().__init__(parent)
        self.app = app
        self.colors = get_colors(is_dark_mode=False)
        
        # Unpack data
        self.doctor_id, self.doctor_name, self.doctor_spec = doctor_data
        self.patient_id, self.patient_name, self.patient_age, self.patient_phone = patient_data
        
        self.session_active = False
        self.mqtt_client = None
        self.start_time = None
        
        # UI Initialization
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)
        
        self._create_header(main)
        
        # Content area
        content = ctk.CTkFrame(main, fg_color="transparent")
        content.pack(fill="both", expand=True, pady=(20, 0))
        
        # Left Panel (Info Cards)
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Right Panel (Control)
        right = ctk.CTkFrame(content, width=380, fg_color="transparent")
        right.pack(side="right", fill="y", padx=(20, 0))
        right.pack_propagate(False)
        
        # Build UI sections
        self._create_patient_card(left)
        self._create_doctor_card(left)
        self._create_control_panel(right)
        
        self.app.protocol("WM_DELETE_WINDOW", self._on_app_close)

    def _create_header(self, parent):
        """Create the session header with title and info."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        ctk.CTkLabel(
            header, 
            text="Patient Monitoring Session", 
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header, 
            text=f"Doctor: {self.doctor_name} | Patient: {self.patient_id}",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))

    def _create_patient_card(self, parent):
        """Create patient information card."""
        card, content = create_card(parent, "Patient Details", self.colors)
        create_info_row(content, "Patient Name", self.patient_name, self.colors)
        create_info_row(content, "Patient ID", self.patient_id, self.colors)
        create_info_row(content, "Age", self.patient_age, self.colors)
        create_info_row(content, "Contact", self.patient_phone, self.colors)

    def _create_doctor_card(self, parent):
        """Create doctor information card."""
        card, content = create_card(parent, "Clinician Details", self.colors)
        create_info_row(content, "Doctor Name", self.doctor_name, self.colors)
        create_info_row(content, "Doctor ID", self.doctor_id, self.colors)
        create_info_row(content, "Specialization", self.doctor_spec, self.colors)

    def _create_control_panel(self, parent):
        """Create session control and monitoring panel."""
        control = ctk.CTkFrame(
            parent, 
            fg_color=self.colors["card_background"], 
            corner_radius=12, 
            border_width=1, 
            border_color=self.colors["border"]
        )
        control.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            control, 
            text="Monitoring Control", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(pady=(20, 5))
        
        # Status Display
        self.status_frame = ctk.CTkFrame(
            control, 
            height=50, 
            corner_radius=8, 
            fg_color=self.colors["status_bg"]
        )
        self.status_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="⚪ Ready to Start",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_secondary"]
        )
        self.status_label.pack(pady=10)
        
        # Live Data Display
        data_frame = ctk.CTkFrame(control, fg_color=self.colors["background"], corner_radius=8)
        data_frame.pack(fill="x", padx=30, pady=(10, 20))
        
        ctk.CTkLabel(
            data_frame, 
            text="LIVE DATA FEED", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["primary"]
        ).pack(pady=(15, 5))
        
        self.temp_label = ctk.CTkLabel(
            data_frame, 
            text="Body Temperature: --°C", 
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_primary"]
        )
        self.temp_label.pack(pady=5)
        
        self.time_label = ctk.CTkLabel(
            data_frame, 
            text="Session Duration: 00:00", 
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_primary"]
        )
        self.time_label.pack(pady=(5, 15))
        
        # Start/Stop Button
        self.start_btn = ctk.CTkButton(
            control, 
            text="▶  Start Session", 
            height=55, 
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color=self.colors["accent"], 
            hover_color=self.colors["accent_hover"],
            corner_radius=10,
            command=self.toggle_session
        )
        self.start_btn.pack(fill="x", padx=30, pady=(0, 10))
        
        # End & Logout Button
        back_btn = ctk.CTkButton(
            control, 
            text="← End & Logout", 
            height=45,
            fg_color="transparent", 
            border_width=2,
            border_color=self.colors["primary"], 
            text_color=self.colors["primary"],
            hover_color=self.colors["background"],
            corner_radius=10,
            command=self.end_session
        )
        back_btn.pack(fill="x", padx=30, pady=(10, 30))

    def toggle_session(self):
        """Toggle between start and stop session."""
        if not self.session_active:
            self.start_session()
        else:
            self.stop_session()
    
    def start_session(self):
        """Start monitoring session."""
        self.session_active = True
        self.start_btn.configure(
            text=" Stop Session", 
            fg_color=self.colors["error"], 
            hover_color=self.colors["error_hover"]
        )
        self.status_frame.configure(fg_color=self.colors["accent"])
        self.status_label.configure(
            text=" Session Active", 
            text_color=self.colors["card_background"]
        )
        
        # Start MQTT publishing
        try:
            self.mqtt_client = MQTTPublisher(self.update_data) 
            threading.Thread(target=self.mqtt_client.start, daemon=True).start()
        except NameError:
            print("Warning: MQTTPublisher class not found. Skipping MQTT setup.")
        
        # Start timer
        self.start_time = time.time() 
        self.update_timer()
    
    def stop_session(self):
        """Stop monitoring session."""
        self.session_active = False
        self.start_btn.configure(
            text="▶ Start Session", 
            fg_color=self.colors["accent"], 
            hover_color=self.colors["accent_hover"]
        )
        self.status_frame.configure(fg_color=self.colors["status_bg"])
        self.status_label.configure(
            text="⚪ Session Stopped", 
            text_color=self.colors["text_secondary"]
        )
        
        if self.mqtt_client:
            self.mqtt_client.stop()
            self.mqtt_client = None

    def update_timer(self):
        """Update session duration timer."""
        if self.session_active and self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.time_label.configure(text=f"Session Duration: {mins:02d}:{secs:02d}")
            self.after(1000, self.update_timer)

    def update_data(self, temp):
        """Update live data display."""
        self.temp_label.configure(text=f"Body Temperature: {temp}°C")

    def end_session(self):
        """End session and return to doctor login."""
        if self.session_active:
            self.stop_session()
            
        try:
            from screens.doctor_login import DoctorLoginScreen
            self.app.show_screen(DoctorLoginScreen)
        except ImportError:
            print("Error: Could not navigate to login screen.")
            self.app.destroy()

    def _on_app_close(self):
        """Handle application window close button."""
        if self.session_active:
            self.stop_session()
        self.app.destroy()