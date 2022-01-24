from .models import AppointmentDate, Appointment, AppointmentHistory, Hospital, Patient, Doctor
from django.contrib import admin

admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(AppointmentDate)
admin.site.register(AppointmentHistory)
