from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# from timescale.db.models.models import TimescaleModel

class Doctor(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def __str__(self):
        return self.full_name or f"Doctor {self.id}"

class Patient(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def __str__(self):
        return self.full_name or f"Patient {self.id}"

class RecordingSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="recording_sessions")
    doctor_id: int # Automatically created b Django
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="recording_sessions")
    patient_id: int # Automatically created b 
    started_at = models.DateTimeField(auto_now_add=True)
    stopped_at = models.DateTimeField(null=True, blank=True)
    verdict = models.CharField(max_length=50, default='pending')
    class Meta:
        ordering = ['-started_at']
    def __str__(self):
        return f"Session {self.id} - Dr.{self.doctor_id} - Pt.{self.patient_id}"

class Device(models.Model):
    device_id = models.CharField(max_length=255, unique=True, db_index=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.device_id
    
class SensorReadings(models.Model):
    id = models.BigAutoField(primary_key=True)
    session = models.ForeignKey(RecordingSession,on_delete=models.CASCADE,related_name="sensor_readings")
    timestamp = models.DateTimeField(db_index=True)
    ecg_values = models.JSONField() # 187 ECG values stored together
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "timestamp"],
                name="unique_sample"
            )
        ]

    def __str__(self):
        return f"ECG @ {self.timestamp} | Session {self.id}"