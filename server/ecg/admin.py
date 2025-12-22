from django.contrib import admin
from .models import Doctor,Patient,RecordingSession,Device
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(RecordingSession)
admin.site.register(Device)
# Register your models here.
