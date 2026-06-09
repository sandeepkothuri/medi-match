from django.contrib import admin
from .models import Patient, Diagnosis, Prescription


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display  = ["patient_id", "first_name", "last_name", "gender", "blood_group", "created_at"]
    search_fields = ["first_name", "last_name", "contact_email"]
    list_filter   = ["gender", "blood_group"]


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display  = ["condition_name", "patient", "severity", "status", "diagnosed_at"]
    list_filter   = ["severity", "status"]
    search_fields = ["condition_name", "patient__first_name", "patient__last_name"]


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display  = ["medication", "patient", "frequency", "status", "prescribed_at"]
    list_filter   = ["frequency", "status"]
    search_fields = ["medication", "patient__first_name"]
