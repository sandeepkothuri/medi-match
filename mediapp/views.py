from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Patient, Diagnosis, Prescription


def dashboard(request):
    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(status='active').count()
    critical_patients = Patient.objects.filter(status='critical').count()
    total_diagnoses = Diagnosis.objects.filter(is_active=True).count()
    active_prescriptions = Prescription.objects.filter(status='active').count()

    recent_patients = Patient.objects.select_related().prefetch_related(
        'diagnoses', 'prescriptions'
    )[:10]

    severity_counts = Diagnosis.objects.filter(is_active=True).values('severity').annotate(
        count=Count('severity')
    )

    context = {
        'total_patients': total_patients,
        'active_patients': active_patients,
        'critical_patients': critical_patients,
        'total_diagnoses': total_diagnoses,
        'active_prescriptions': active_prescriptions,
        'recent_patients': recent_patients,
        'severity_counts': list(severity_counts),
    }
    return render(request, 'mediapp/dashboard.html', context)


def patient_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    patients = Patient.objects.prefetch_related('diagnoses', 'prescriptions').all()

    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(patient_id__icontains=query)
        )

    if status_filter:
        patients = patients.filter(status=status_filter)

    context = {
        'patients': patients,
        'query': query,
        'status_filter': status_filter,
    }
    return render(request, 'mediapp/patient_list.html', context)


def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    diagnoses = patient.diagnoses.all()
    prescriptions = patient.prescriptions.all()

    context = {
        'patient': patient,
        'diagnoses': diagnoses,
        'prescriptions': prescriptions,
        'active_diagnoses': diagnoses.filter(is_active=True).count(),
        'active_prescriptions': prescriptions.filter(status='active').count(),
    }
    return render(request, 'mediapp/patient_detail.html', context)


def analytics(request):
    status_breakdown = Patient.objects.values('status').annotate(count=Count('status'))
    severity_breakdown = Diagnosis.objects.filter(is_active=True).values('severity').annotate(
        count=Count('severity')
    )
    blood_type_breakdown = Patient.objects.values('blood_type').annotate(count=Count('blood_type'))
    top_conditions = Diagnosis.objects.filter(is_active=True).values('condition').annotate(
        count=Count('condition')
    ).order_by('-count')[:10]
    top_medications = Prescription.objects.filter(status='active').values('medication').annotate(
        count=Count('medication')
    ).order_by('-count')[:10]

    context = {
        'status_breakdown': list(status_breakdown),
        'severity_breakdown': list(severity_breakdown),
        'blood_type_breakdown': list(blood_type_breakdown),
        'top_conditions': list(top_conditions),
        'top_medications': list(top_medications),
    }
    return render(request, 'mediapp/analytics.html', context)


def api_stats(request):
    data = {
        'total_patients': Patient.objects.count(),
        'active': Patient.objects.filter(status='active').count(),
        'critical': Patient.objects.filter(status='critical').count(),
        'discharged': Patient.objects.filter(status='discharged').count(),
        'total_diagnoses': Diagnosis.objects.count(),
        'active_prescriptions': Prescription.objects.filter(status='active').count(),
    }
    return JsonResponse(data)
