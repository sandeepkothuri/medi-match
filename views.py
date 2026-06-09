"""
Medi Match – Django Views
Handles all patient, diagnosis, and prescription API + web views.

Author: Sandeep K
Date: Sep–Nov 2024
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse

from .models import Patient, Doctor, Diagnosis, Prescription, Medication
from .forms import PatientForm, DiagnosisForm, PrescriptionForm


# ─── Auth helper ──────────────────────────────────────────────────────────────

def is_doctor(user):
    return hasattr(user, "doctor")


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """Main dashboard showing key metrics across all 3 modules."""
    context = {
        "total_patients":      Patient.objects.count(),
        "active_diagnoses":    Diagnosis.objects.filter(status="ACTIVE").count(),
        "active_prescriptions": Prescription.objects.filter(status="ACTIVE").count(),
        "critical_cases":      Diagnosis.objects.filter(severity="CRITICAL", status="ACTIVE").count(),
        "recent_patients":     Patient.objects.order_by("-created_at")[:5],
        "recent_diagnoses":    Diagnosis.objects.filter(status="ACTIVE").order_by("-diagnosed_at")[:5],
        "recent_prescriptions": Prescription.objects.filter(status="ACTIVE").order_by("-prescribed_at")[:5],
    }

    # 7-day trend data for charts
    from datetime import date, timedelta
    today = date.today()
    trend = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        trend.append({
            "date":          day.strftime("%b %d"),
            "new_patients":  Patient.objects.filter(created_at__date=day).count(),
            "prescriptions": Prescription.objects.filter(prescribed_at__date=day).count(),
        })
    context["trend_data"] = trend

    return render(request, "mediMatch/dashboard.html", context)


# ─── Patient CRUD ──────────────────────────────────────────────────────────────

@login_required
def patient_list(request):
    query = request.GET.get("q", "")
    patients = Patient.objects.all()
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(contact_email__icontains=query)
        )
    return render(request, "mediMatch/patient_list.html", {"patients": patients, "query": query})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    diagnoses     = patient.diagnoses.order_by("-diagnosed_at")
    prescriptions = patient.prescriptions.filter(status="ACTIVE").order_by("-prescribed_at")
    return render(request, "mediMatch/patient_detail.html", {
        "patient":       patient,
        "diagnoses":     diagnoses,
        "prescriptions": prescriptions,
    })


@login_required
@user_passes_test(is_doctor)
def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f"Patient {patient.full_name} added successfully.")
            return redirect("patient_detail", pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, "mediMatch/patient_form.html", {"form": form, "action": "Add Patient"})


@login_required
@user_passes_test(is_doctor)
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient record updated.")
            return redirect("patient_detail", pk=pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, "mediMatch/patient_form.html", {"form": form, "action": "Edit Patient", "patient": patient})


# ─── Diagnosis CRUD ───────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_doctor)
def diagnosis_create(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == "POST":
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.patient = patient
            diagnosis.doctor  = request.user.doctor
            diagnosis.save()
            messages.success(request, f"Diagnosis '{diagnosis.condition_name}' added.")
            return redirect("patient_detail", pk=patient_pk)
    else:
        form = DiagnosisForm()
    return render(request, "mediMatch/diagnosis_form.html", {"form": form, "patient": patient})


@login_required
@user_passes_test(is_doctor)
def diagnosis_resolve(request, pk):
    """Mark a diagnosis as resolved."""
    diagnosis = get_object_or_404(Diagnosis, pk=pk)
    diagnosis.status      = "RESOLVED"
    diagnosis.resolved_at = timezone.now()
    diagnosis.save()
    messages.success(request, f"Diagnosis '{diagnosis.condition_name}' marked as resolved.")
    return redirect("patient_detail", pk=diagnosis.patient.pk)


# ─── Prescription CRUD ────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_doctor)
def prescription_create(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == "POST":
        form = PrescriptionForm(request.POST, patient=patient)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            prescription.doctor  = request.user.doctor
            prescription.save()
            messages.success(request, f"Prescription for {prescription.medication.name} created.")
            return redirect("patient_detail", pk=patient_pk)
    else:
        form = PrescriptionForm(patient=patient)
    return render(request, "mediMatch/prescription_form.html", {"form": form, "patient": patient})


# ─── Reporting API (JSON) ──────────────────────────────────────────────────────

@login_required
def report_summary(request):
    """Returns a JSON summary used by the Power BI / Tableau integration."""
    data = {
        "total_patients":       Patient.objects.count(),
        "active_diagnoses":     Diagnosis.objects.filter(status="ACTIVE").count(),
        "active_prescriptions": Prescription.objects.filter(status="ACTIVE").count(),
        "diagnoses_by_severity": list(
            Diagnosis.objects.filter(status="ACTIVE")
                             .values("severity")
                             .annotate(count=Count("id"))
        ),
        "top_medications": list(
            Prescription.objects.filter(status="ACTIVE")
                                .values("medication__name")
                                .annotate(count=Count("id"))
                                .order_by("-count")[:10]
        ),
        "generated_at": timezone.now().isoformat(),
    }
    return JsonResponse(data)
