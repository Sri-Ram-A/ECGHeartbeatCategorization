from django.contrib import admin
# Register your models here.
from .models import Doctor,Patient,RecordingSession,Device
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(RecordingSession)
admin.site.register(Device)
