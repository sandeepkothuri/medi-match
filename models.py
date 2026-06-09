"""
Medi Match – Healthcare Workflow Optimization App
models.py: Core data models for patient records, diagnoses, and prescriptions.

Author: Sandeep K
Date: Sep–Nov 2024
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Patient(models.Model):
    """Tracks core patient identity and demographics."""

    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    patient_id    = models.AutoField(primary_key=True)
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender        = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
    blood_group   = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    address       = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __str__(self):
        return f"[{self.patient_id}] {self.full_name} (Age {self.age})"

    class Meta:
        ordering = ["-created_at"]


class Doctor(models.Model):
    """Healthcare provider linked to a system user account."""

    SPECIALIZATIONS = [
        ("GP",      "General Practitioner"),
        ("CARDIO",  "Cardiology"),
        ("NEURO",   "Neurology"),
        ("ORTHO",   "Orthopedics"),
        ("PEDS",    "Pediatrics"),
        ("PSYCH",   "Psychiatry"),
        ("ONCO",    "Oncology"),
        ("DERM",    "Dermatology"),
        ("OTHER",   "Other"),
    ]

    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number  = models.CharField(max_length=50, unique=True)
    specialization  = models.CharField(max_length=10, choices=SPECIALIZATIONS)
    department      = models.CharField(max_length=100)
    phone           = models.CharField(max_length=20, blank=True)
    years_experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.get_specialization_display()})"


class Diagnosis(models.Model):
    """Links a patient to a confirmed diagnosis at a point in time."""

    SEVERITY_CHOICES = [
        ("LOW",      "Low"),
        ("MODERATE", "Moderate"),
        ("HIGH",     "High"),
        ("CRITICAL", "Critical"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE",   "Active"),
        ("RESOLVED", "Resolved"),
        ("CHRONIC",  "Chronic / Ongoing"),
        ("REFERRED", "Referred"),
    ]

    patient        = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="diagnoses")
    doctor         = models.ForeignKey(Doctor,  on_delete=models.SET_NULL, null=True, related_name="diagnoses")
    icd10_code     = models.CharField(max_length=10, blank=True, help_text="ICD-10 diagnostic code")
    condition_name = models.CharField(max_length=200)
    description    = models.TextField(blank=True)
    severity       = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="LOW")
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    diagnosed_at   = models.DateTimeField(default=timezone.now)
    resolved_at    = models.DateTimeField(null=True, blank=True)
    notes          = models.TextField(blank=True)

    def __str__(self):
        return f"{self.condition_name} ({self.get_status_display()}) – {self.patient.full_name}"

    class Meta:
        ordering  = ["-diagnosed_at"]
        verbose_name_plural = "Diagnoses"


class Medication(models.Model):
    """Master medication reference table."""

    DRUG_CLASS_CHOICES = [
        ("ANTIBIOTIC",    "Antibiotic"),
        ("ANALGESIC",     "Analgesic / Pain Relief"),
        ("ANTIVIRAL",     "Antiviral"),
        ("ANTIDIABETIC",  "Antidiabetic"),
        ("CARDIOVASCULAR","Cardiovascular"),
        ("ANTIDEPRESSANT","Antidepressant"),
        ("ANTIHISTAMINE", "Antihistamine"),
        ("OTHER",         "Other"),
    ]

    name          = models.CharField(max_length=200, unique=True)
    generic_name  = models.CharField(max_length=200, blank=True)
    drug_class    = models.CharField(max_length=20, choices=DRUG_CLASS_CHOICES)
    dosage_forms  = models.CharField(max_length=200, help_text="e.g. Tablet, Capsule, Injection")
    manufacturer  = models.CharField(max_length=200, blank=True)
    requires_prescription = models.BooleanField(default=True)
    contraindications = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_drug_class_display()})"


class Prescription(models.Model):
    """A prescribing event linking a patient, diagnosis, and medication."""

    STATUS_CHOICES = [
        ("ACTIVE",    "Active"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
        ("ON_HOLD",   "On Hold"),
    ]

    FREQUENCY_CHOICES = [
        ("OD",   "Once daily"),
        ("BD",   "Twice daily"),
        ("TDS",  "Three times daily"),
        ("QDS",  "Four times daily"),
        ("PRN",  "As needed"),
        ("STAT", "Immediately (single dose)"),
    ]

    patient     = models.ForeignKey(Patient,    on_delete=models.CASCADE,   related_name="prescriptions")
    doctor      = models.ForeignKey(Doctor,     on_delete=models.SET_NULL,  related_name="prescriptions", null=True)
    diagnosis   = models.ForeignKey(Diagnosis,  on_delete=models.SET_NULL,  related_name="prescriptions", null=True, blank=True)
    medication  = models.ForeignKey(Medication, on_delete=models.PROTECT,   related_name="prescriptions")

    dosage      = models.CharField(max_length=100, help_text="e.g. 500mg")
    frequency   = models.CharField(max_length=5,   choices=FREQUENCY_CHOICES)
    duration_days = models.PositiveIntegerField()
    start_date  = models.DateField(default=timezone.now)
    end_date    = models.DateField(null=True, blank=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    instructions = models.TextField(blank=True, help_text="e.g. Take with food, Avoid alcohol")
    prescribed_at = models.DateTimeField(auto_now_add=True)
    refills_remaining = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        from datetime import timedelta
        if not self.end_date and self.start_date and self.duration_days:
            self.end_date = self.start_date + timedelta(days=self.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.medication.name} {self.dosage} {self.get_frequency_display()} "
            f"x{self.duration_days}d — {self.patient.full_name}"
        )

    class Meta:
        ordering = ["-prescribed_at"]
