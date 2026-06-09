from django.db import models
from django.utils import timezone


class Patient(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'), ('discharged', 'Discharged'), ('critical', 'Critical'),
    ]

    patient_id = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    blood_type = models.CharField(max_length=4, choices=BLOOD_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='active')
    admitted_on = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-admitted_on']

    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = timezone.now().date()
        b = self.date_of_birth
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))


class Diagnosis(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnoses')
    condition = models.CharField(max_length=200)
    icd_code = models.CharField(max_length=20, blank=True, help_text='ICD-10 Code')
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    diagnosed_by = models.CharField(max_length=150)
    diagnosed_on = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-diagnosed_on']
        verbose_name_plural = 'Diagnoses'

    def __str__(self):
        return f"{self.patient.patient_id} - {self.condition} ({self.severity})"


class Prescription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'), ('completed', 'Completed'),
        ('cancelled', 'Cancelled'), ('pending', 'Pending'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True, blank=True)
    medication = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    route = models.CharField(max_length=50, default='Oral', help_text='e.g., Oral, IV, Topical')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    prescribed_by = models.CharField(max_length=150)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.patient.patient_id} - {self.medication} ({self.dosage})"
