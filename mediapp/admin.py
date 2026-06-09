from django.contrib import admin
from .models import Patient, Diagnosis, Prescription


class DiagnosisInline(admin.TabularInline):
    model = Diagnosis
    extra = 0
    fields = ('condition', 'icd_code', 'severity', 'diagnosed_by', 'is_active')
    readonly_fields = ('created_at',)


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0
    fields = ('medication', 'dosage', 'frequency', 'prescribed_by', 'status')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'full_name', 'age', 'gender', 'blood_type', 'status', 'admitted_on')
    list_filter = ('status', 'gender', 'blood_type')
    search_fields = ('patient_id', 'first_name', 'last_name', 'phone')
    inlines = [DiagnosisInline, PrescriptionInline]
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-admitted_on',)


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('patient', 'condition', 'icd_code', 'severity', 'diagnosed_by', 'diagnosed_on', 'is_active')
    list_filter = ('severity', 'is_active')
    search_fields = ('condition', 'icd_code', 'patient__patient_id', 'patient__last_name')
    list_editable = ('is_active',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medication', 'dosage', 'frequency', 'prescribed_by', 'status', 'start_date')
    list_filter = ('status', 'route')
    search_fields = ('medication', 'patient__patient_id', 'patient__last_name', 'prescribed_by')
