# 🏥 Medi Match — Healthcare Workflow Optimization App

> A Django-based patient management system tracking 50+ patient records across diagnoses, prescriptions, and clinical workflows.

## Overview

Medi Match is a full-stack healthcare application that streamlines clinical data workflows. It supports tracking patient records, diagnoses, and prescriptions across 3 core modules, providing healthcare providers with a unified dashboard, real-time summaries, and data export capabilities for Power BI / Tableau reporting.

Built collaboratively by a **6-member team**, with Sandeep contributing to data workflows, backend logic, wireframe planning, and technical documentation across 20+ tracked tasks.

---

## Features

- **Patient Management** — CRUD for 50+ patient records with search and filtering
- **Diagnosis Tracking** — ICD-10 coded conditions with severity levels and resolution workflow
- **Prescription Management** — Medication linking with dosage, frequency, and refill tracking
- **Role-Based Access** — Doctor vs. read-only staff permissions
- **Reporting API** — JSON endpoint for Power BI / Tableau integration
- **7-Day Trend Dashboard** — Live metrics: new patients, active diagnoses, active prescriptions

---

## Data Models

```
Patient → Diagnosis (many)
Patient → Prescription (many)
Prescription → Medication (FK)
Prescription → Diagnosis (FK, optional)
Doctor → Diagnosis / Prescription (FK)
```

---

## Setup & Installation

```bash
# 1. Clone the repo
git clone https://github.com/sandeepkothuri/medi-match.git
cd medi-match

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations && python manage.py migrate

# 5. Create a superuser (doctor account)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

---

## Reporting API

`GET /api/report/summary/` returns JSON for Power BI / Tableau:

```json
{
  "total_patients": 52,
  "active_diagnoses": 31,
  "active_prescriptions": 44,
  "diagnoses_by_severity": [...],
  "top_medications": [...],
  "generated_at": "2024-11-15T14:32:00Z"
}
```

---

## Tech Stack

**Django 4.2** · **PostgreSQL** · **Bootstrap 5** · **Figma** · **Power BI** · **Tableau**

---

## Author

**Sandeep K** — Data workflows, backend logic, wireframe planning, technical documentation

[LinkedIn](https://www.linkedin.com/in/sandeep-kothuri-9b99142b6/) · [GitHub](https://github.com/sandeepkothuri)

*CSULB – Master of Science in Information Systems | Sep–Nov 2024*
