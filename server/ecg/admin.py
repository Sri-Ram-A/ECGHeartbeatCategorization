from django.contrib import admin
from django.db import models
from .models import Doctor, Patient, RecordingSession, Device, SensorReadings


class AutoAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name
            for field in model._meta.fields
            if not isinstance(field, models.TextField)
        ]
        super().__init__(model, admin_site)

admin.site.register(Doctor, AutoAdmin)
admin.site.register(Patient, AutoAdmin)
admin.site.register(Device, AutoAdmin)
admin.site.register(RecordingSession, AutoAdmin)
@admin.register(SensorReadings)
class SensorReadingsAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "timestamp")
    exclude = ("ecg_values",)
