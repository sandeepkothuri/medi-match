"""
Medi Match — Healthcare Workflow Optimization
------------------------------------------------
Built data workflows and supported backend logic for tracking 50+
patient records, diagnoses, and prescriptions in a Django-based app.

Partnered with a 6-member development team to structure and analyze
healthcare data across 3+ core modules.

Contributed to wireframe planning and documented 20+ technical tasks.

Author : Sandeep K | CSULB M.S. Information Systems
Period : Sep 2024 - Nov 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os, warnings
warnings.filterwarnings("ignore")

os.makedirs("outputs", exist_ok=True)

# ── 1. Load Data ───────────────────────────────────────────────────────────────
df = pd.read_csv("data/patient_records.csv")
print(f"Patient records loaded: {len(df)}")
print(f"Columns: {df.columns.tolist()}\n")

# ── 2. Module 1: Patient Summary ───────────────────────────────────────────────
print("── Module 1: Patient Summary ───────────────────")
print(f"Total patients tracked:   {len(df)}")
print(f"Active cases:             {(df['status']=='Active').sum()}")
print(f"Resolved cases:           {(df['status']=='Resolved').sum()}")
print(f"Chronic cases:            {(df['status']=='Chronic').sum()}")
print(f"Critical severity:        {(df['severity']=='Critical').sum()}")
print(f"Age range:                {df['age'].min()} – {df['age'].max()} yrs  |  Mean: {df['age'].mean():.1f} yrs")

# ── 3. Module 2: Diagnosis Analysis ────────────────────────────────────────────
print("\n── Module 2: Diagnosis Breakdown ───────────────")
diag_counts = df["diagnosis"].value_counts()
print(diag_counts.to_string())

severity_counts = df["severity"].value_counts()
print(f"\nSeverity distribution:")
print(severity_counts.to_string())

# ── 4. Module 3: Prescription Analysis ────────────────────────────────────────
print("\n── Module 3: Prescriptions ─────────────────────")
rx_counts = df["prescription"].value_counts()
print(f"Most prescribed medications:")
print(rx_counts.head(8).to_string())

freq_counts = df["dosage_frequency"].value_counts()
print(f"\nDosage frequency breakdown:")
print(freq_counts.to_string())

# ── 5. Dashboard ───────────────────────────────────────────────────────────────
BG    = "#0d1117"
PANEL = "#161b22"
WHITE = "#f0f6fc"
GRAY  = "#8b949e"
RED   = "#e74c3c"
BLUE  = "#3498db"
GREEN = "#2ecc71"
GOLD  = "#f39c12"

SEV_COLORS = {"Low": GREEN, "Moderate": GOLD, "High": RED, "Critical": "#8e44ad"}
STAT_COLORS = {"Active": BLUE, "Resolved": GREEN, "Chronic": GOLD}

fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.50, wspace=0.38)

ax1 = fig.add_subplot(gs[0, :2])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, :2])
ax4 = fig.add_subplot(gs[1, 2])

for ax in [ax1, ax2, ax3, ax4]:
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_edgecolor("#30363d")

# Panel 1 – Top diagnoses
top_diag = diag_counts.head(10).sort_values()
ax1.barh(top_diag.index, top_diag.values, color=BLUE, alpha=0.85, edgecolor=BG)
ax1.set_title("Top 10 Diagnoses (Patient Count)", color=WHITE, fontsize=12, fontweight="bold", pad=10)
ax1.set_xlabel("Number of Patients", color=GRAY, fontsize=10)
ax1.tick_params(colors=GRAY)
for i, (idx, val) in enumerate(zip(top_diag.index, top_diag.values)):
    ax1.text(val + 0.05, i, str(val), va="center", color=GRAY, fontsize=9)

# Panel 2 – Severity pie
sev_counts = df["severity"].value_counts()
ax2.pie(sev_counts.values,
        labels=sev_counts.index,
        colors=[SEV_COLORS.get(s, GRAY) for s in sev_counts.index],
        autopct="%1.0f%%", startangle=90,
        textprops={"color": GRAY, "fontsize": 10},
        wedgeprops={"edgecolor": BG, "linewidth": 1.5})
ax2.set_title("Severity Distribution", color=WHITE, fontsize=12, fontweight="bold", pad=10)

# Panel 3 – Top prescriptions
top_rx = rx_counts.head(8).sort_values()
ax3.barh(top_rx.index, top_rx.values, color=GOLD, alpha=0.85, edgecolor=BG)
ax3.set_title("Top 8 Most Prescribed Medications", color=WHITE, fontsize=12, fontweight="bold", pad=10)
ax3.set_xlabel("Number of Patients", color=GRAY, fontsize=10)
ax3.tick_params(colors=GRAY)
for i, val in enumerate(top_rx.values):
    ax3.text(val + 0.05, i, str(val), va="center", color=GRAY, fontsize=9)

# Panel 4 – Summary
active   = (df["status"] == "Active").sum()
critical = (df["severity"] == "Critical").sum()
doctors  = df["assigned_doctor"].nunique()

ax4.axis("off")
summary = (
    f"  Total patients:     {len(df)}\n\n"
    f"  Active cases:       {active}\n\n"
    f"  Critical severity:  {critical}\n\n"
    f"  Doctors on file:    {doctors}\n\n"
    f"  Conditions tracked: {df['diagnosis'].nunique()}\n\n"
    f"  Medications on file:{df['prescription'].nunique()}\n\n"
    f"  Modules covered:    3\n"
    f"  (Patients, Dx, Rx)"
)
ax4.text(0.08, 0.95, "Workflow Summary", fontsize=12, fontweight="bold",
         color=WHITE, transform=ax4.transAxes, va="top")
ax4.text(0.08, 0.78, summary, fontsize=10, color=GRAY,
         transform=ax4.transAxes, va="top", linespacing=1.6, family="monospace")

fig.suptitle("Medi Match — Healthcare Data Workflow Dashboard",
             fontsize=15, fontweight="bold", color=WHITE, y=0.98)

plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("\nDashboard saved → outputs/dashboard.png")
print("✅  Analysis complete.")
