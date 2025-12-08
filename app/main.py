import customtkinter as ctk
from screens.doctor_login import DoctorLoginScreen

class MedicalMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Medical Monitoring System")
        self.geometry("1200x750")
        # self.attributes('-fullscreen', True)
        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        top_bar = ctk.CTkFrame(self, height=60, fg_color="transparent")
        top_bar.pack(side="top", fill="x", padx=20, pady=10)  
        # Exit button on right
        exit_btn = ctk.CTkButton(
            top_bar,text="Exit",
            width=100,height=40,
            hover_color="#b02424",fg_color="#3c00ff",
            command=self.destroy
        )
        exit_btn.pack(side="right", padx=20, pady=5)  # Pack to right
        # Container for screens
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        # Current screen
        self.current_screen = None
        # Show doctor login
        self.show_screen(DoctorLoginScreen)
    
    def show_screen(self, screen_class, **kwargs):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self.container, self, **kwargs)
        self.current_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MedicalMonitorApp()
    app.mainloop()