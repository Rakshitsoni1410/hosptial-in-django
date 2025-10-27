from django.contrib import admin
from .models import Patient, Doctor

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "dob", "gender", "blood_group", "medical_history", "address", "created_at")
    search_fields = ("name", "email", "phone")

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "gender", "specialization", "degree", "experience", "clinic_address", "created_at")
    search_fields = ("name", "email", "phone", "specialization")
