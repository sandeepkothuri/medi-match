from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from .models import Patient, Diagnosis, Prescription


@login_required
def dashboard(request):
    context = {
        "total_patients":       Patient.objects.count(),
        "active_diagnoses":     Diagnosis.objects.filter(status="Active").count(),
        "active_prescriptions": Prescription.objects.filter(status="Active").count(),
        "critical_cases":       Diagnosis.objects.filter(severity="Critical", status="Active").count(),
        "recent_patients":      Patient.objects.order_by("-created_at")[:5],
    }
    return render(request, "mediapp/dashboard.html", context)


@login_required
def patient_list(request):
    query    = request.GET.get("q", "")
    patients = Patient.objects.all()
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    return render(request, "mediapp/patient_list.html", {"patients": patients, "query": query})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "mediapp/patient_detail.html", {
        "patient":       patient,
        "diagnoses":     patient.diagnoses.order_by("-diagnosed_at"),
        "prescriptions": patient.prescriptions.filter(status="Active"),
    })


@login_required
def report_api(request):
    """JSON endpoint for Power BI / Tableau integration."""
    return JsonResponse({
        "total_patients":       Patient.objects.count(),
        "active_diagnoses":     Diagnosis.objects.filter(status="Active").count(),
        "active_prescriptions": Prescription.objects.filter(status="Active").count(),
        "diagnoses_by_severity": list(
            Diagnosis.objects.filter(status="Active")
                             .values("severity")
                             .annotate(count=Count("id"))
        ),
        "top_medications": list(
            Prescription.objects.filter(status="Active")
                                .values("medication")
                                .annotate(count=Count("id"))
                                .order_by("-count")[:10]
        ),
        "generated_at": timezone.now().isoformat(),
    })
