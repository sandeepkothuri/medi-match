"""
Medi Match - Seed Script
Generates 50+ realistic patient records with diagnoses and prescriptions
"""
import os
import sys
import django
import random
from datetime import date, timedelta

# Setup Django
sys.path.insert(0, '/home/claude/projects/medi-match')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediproject.settings')

from mediapp.models import Patient, Diagnosis, Prescription

first_names = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda",
               "David","Barbara","William","Elizabeth","Richard","Susan","Joseph","Jessica",
               "Thomas","Sarah","Charles","Karen","Ahmed","Priya","Carlos","Maria","Wei","Aisha"]
last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
              "Wilson","Moore","Taylor","Anderson","Thomas","Jackson","White","Harris",
              "Martin","Thompson","Kumar","Patel","Rodriguez","Lopez","Lee","Nguyen"]
conditions = [
    ("Hypertension", "I10", "Persistent high blood pressure above 140/90 mmHg"),
    ("Type 2 Diabetes", "E11", "Insulin resistance with elevated blood glucose levels"),
    ("Asthma", "J45", "Chronic inflammatory disease of the airways"),
    ("Migraine", "G43", "Recurring moderate to severe headaches"),
    ("Atrial Fibrillation", "I48", "Irregular heartbeat causing poor blood flow"),
    ("GERD", "K21", "Gastroesophageal reflux with acid erosion"),
    ("Osteoarthritis", "M15", "Degenerative joint disease in multiple joints"),
    ("Major Depressive Disorder", "F32", "Persistent low mood and anhedonia"),
    ("Chronic Kidney Disease", "N18", "Progressive loss of kidney function"),
    ("Pneumonia", "J18", "Acute inflammation of lung tissue"),
    ("Heart Failure", "I50", "Heart unable to pump sufficient blood"),
    ("Anxiety Disorder", "F41", "Persistent excessive worry affecting daily function"),
]
medications_map = {
    "Hypertension": [("Lisinopril", "10mg", "Once daily", "Oral")],
    "Type 2 Diabetes": [("Metformin", "500mg", "Twice daily with meals", "Oral")],
    "Asthma": [("Albuterol", "2 puffs", "Every 4-6 hrs as needed", "Inhaled")],
    "Migraine": [("Sumatriptan", "50mg", "At onset, repeat after 2hrs if needed", "Oral")],
    "Atrial Fibrillation": [("Warfarin", "5mg", "Once daily", "Oral")],
    "GERD": [("Omeprazole", "20mg", "Once daily before breakfast", "Oral")],
    "Osteoarthritis": [("Naproxen", "500mg", "Twice daily with food", "Oral")],
    "Major Depressive Disorder": [("Sertraline", "50mg", "Once daily in morning", "Oral")],
    "Chronic Kidney Disease": [("Amlodipine", "5mg", "Once daily", "Oral")],
    "Pneumonia": [("Amoxicillin", "500mg", "Three times daily for 7 days", "Oral")],
    "Heart Failure": [("Furosemide", "40mg", "Once daily in morning", "Oral")],
    "Anxiety Disorder": [("Escitalopram", "10mg", "Once daily", "Oral")],
}
doctors = ["Dr. Sarah Chen", "Dr. Michael Roberts", "Dr. Aisha Patel",
           "Dr. James Liu", "Dr. Emily Torres", "Dr. David Kim"]
severities = ['low', 'low', 'medium', 'medium', 'medium', 'high', 'critical']
statuses = ['active', 'active', 'active', 'active', 'discharged', 'critical']
blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
genders = ['Male', 'Female', 'Non-binary']

def run():
    Patient.objects.all().delete()
    Diagnosis.objects.all().delete()
    Prescription.objects.all().delete()

    created = 0
    for i in range(1, 56):
        pid = f"MM{i:04d}"
        dob = date.today() - timedelta(days=random.randint(6570, 29200))

        p = Patient.objects.create(
            patient_id=pid,
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            date_of_birth=dob,
            gender=random.choice(genders),
            blood_type=random.choice(blood_types),
            phone=f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
            email=f"patient{i}@example.com",
            address=f"{random.randint(100,9999)} Main St, City, CA 9{random.randint(1000,9999)}",
            status=random.choice(statuses),
        )

        n_conditions = random.randint(1, 3)
        chosen_conditions = random.sample(conditions, min(n_conditions, len(conditions)))

        for cond_name, icd, cond_desc in chosen_conditions:
            d = Diagnosis.objects.create(
                patient=p,
                condition=cond_name,
                icd_code=icd,
                description=cond_desc,
                severity=random.choice(severities),
                diagnosed_by=random.choice(doctors),
                notes=f"Patient presents with typical symptoms. Follow-up in 4-6 weeks.",
                is_active=random.choice([True, True, True, False]),
            )

            if cond_name in medications_map:
                for med, dosage, freq, route in medications_map[cond_name]:
                    Prescription.objects.create(
                        patient=p,
                        diagnosis=d,
                        medication=med,
                        dosage=dosage,
                        frequency=freq,
                        route=route,
                        prescribed_by=random.choice(doctors),
                        status=random.choice(['active', 'active', 'active', 'completed', 'pending']),
                        start_date=date.today() - timedelta(days=random.randint(0, 180)),
                        end_date=date.today() + timedelta(days=random.randint(7, 90)),
                    )

        created += 1

    print(f"Seeded {created} patients")
    print(f"  Diagnoses created:    {Diagnosis.objects.count()}")
    print(f"  Prescriptions created:{Prescription.objects.count()}")
    print(f"  Active patients:      {Patient.objects.filter(status='active').count()}")
    print(f"  Critical patients:    {Patient.objects.filter(status='critical').count()}")

if __name__ == '__main__':
    run()
