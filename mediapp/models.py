from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Patient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),
        ("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"),
    ]
    patient_id    = models.AutoField(primary_key=True)
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender        = models.CharField(max_length=10, choices=[("M","Male"),("F","Female"),("O","Other")])
    blood_group   = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"[{self.patient_id}] {self.full_name}"

    class Meta:
        ordering = ["-created_at"]


class Diagnosis(models.Model):
    SEVERITY_CHOICES = [("Low","Low"),("Moderate","Moderate"),("High","High"),("Critical","Critical")]
    STATUS_CHOICES   = [("Active","Active"),("Resolved","Resolved"),("Chronic","Chronic")]

    patient        = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="diagnoses")
    condition_name = models.CharField(max_length=200)
    icd10_code     = models.CharField(max_length=10, blank=True)
    severity       = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="Low")
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    diagnosed_at   = models.DateTimeField(default=timezone.now)
    notes          = models.TextField(blank=True)

    def __str__(self):
        return f"{self.condition_name} ({self.status}) - {self.patient.full_name}"

    class Meta:
        ordering = ["-diagnosed_at"]
        verbose_name_plural = "Diagnoses"


class Prescription(models.Model):
    FREQUENCY_CHOICES = [
        ("Once daily","Once daily"),("Twice daily","Twice daily"),
        ("Three times daily","Three times daily"),("As needed","As needed"),
    ]
    STATUS_CHOICES = [("Active","Active"),("Completed","Completed"),("Cancelled","Cancelled")]

    patient    = models.ForeignKey(Patient,   on_delete=models.CASCADE,  related_name="prescriptions")
    diagnosis  = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, related_name="prescriptions", null=True, blank=True)
    medication = models.CharField(max_length=200)
    dosage     = models.CharField(max_length=100)
    frequency  = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField(default=timezone.now)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    prescribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication} {self.dosage} - {self.patient.full_name}"

    class Meta:
        ordering = ["-prescribed_at"]
