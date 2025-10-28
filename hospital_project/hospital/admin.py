from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "dob", "gender", "blood_group", "medical_history", "address", "created_at")
    search_fields = ("name", "email", "phone")
