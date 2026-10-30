import os
from pathlib import Path

def generate_pdf():
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    pdf_path = docs_dir / "company_policy.pdf"

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        
        # --- Page 1 ---
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, 750, "Datheno Technologies - Employee & Operations Handbook")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(72, 720, "Section 1: Working Hours & Remote Work Framework")
        c.setFont("Helvetica", 10)
        text_p1 = [
            "1.1 Standard Core Hours:",
            "All employees are expected to be available for synchronous communication between 10:00 AM",
            "and 4:00 PM EST, Monday through Friday.",
            "",
            "1.2 Remote Work & Home Office Setup:",
            "Datheno provides a one-time remote equipment allowance of $1,200 for new full-time hires.",
            "This covers ergonomic chairs, external monitors, keyboards, and desk accessories.",
            "In addition, an internet monthly reimbursement of $75 is credited via payroll expenses.",
            "",
            "1.3 Global Relocation Policy:",
            "Employees working remotely who wish to relocate across state or national borders must notify",
            "People Operations at least 45 business days in advance to ensure legal compliance."
        ]
        y = 690
        for line in text_p1:
            c.drawString(72, y, line)
            y -= 18

        c.showPage()

        # --- Page 2 ---
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, 750, "Section 2: Health Insurance & Wellness Benefits")
        c.setFont("Helvetica", 10)
        text_p2 = [
            "2.1 Comprehensive Medical Coverage:",
            "Employees are eligible for Platinum Health coverage starting on their first calendar day of employment.",
            "The plan covers 100% of employee healthcare premiums and 75% for dependents.",
            "",
            "2.2 Mental Health & Counseling:",
            "Up to 12 free confidential therapy and counseling sessions are offered annually through the Spring Health",
            "Employee Assistance Program (EAP).",
            "",
            "2.3 Annual Wellness Stipend:",
            "Each team member receives a $600 annual wellness credit intended for gym memberships,",
            "fitness equipment, mental health apps, or athletic events."
        ]
        y = 710
        for line in text_p2:
            c.drawString(72, y, line)
            y -= 18

        c.showPage()

        # --- Page 3 ---
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, 750, "Section 3: Paid Time Off (PTO) & Learning Budgets")
        c.setFont("Helvetica", 10)
        text_p3 = [
            "3.1 Flexible PTO Policy:",
            "Full-time staff enjoy flexible, unmetered PTO with a required minimum of 15 days off per year.",
            "Vacations extending beyond 10 consecutive business days require 30 days prior manager approval.",
            "",
            "3.2 Professional Learning & Development:",
            "Each engineer and staff member is allotted an annual education budget of $2,500.",
            "This stipend covers cloud certifications (AWS, GCP, Azure), AI/ML conferences, books,",
            "and technical coursework on platforms such as Coursera and O'Reilly."
        ]
        y = 710
        for line in text_p3:
            c.drawString(72, y, line)
            y -= 18

        c.save()
        print(f"[OK] Successfully created sample 3-page PDF: {pdf_path.resolve()}")

    except ImportError:
        # Fallback to plain text document if reportlab is not installed
        txt_path = docs_dir / "company_policy.txt"
        content = """Datheno Technologies - Employee & Operations Handbook

Section 1: Working Hours & Remote Work Framework (Page 1)
1.1 Standard Core Hours: Available between 10:00 AM and 4:00 PM EST.
1.2 Remote Work Setup: One-time remote equipment allowance of $1,200 for new full-time hires. Monthly internet reimbursement of $75.
1.3 Relocation Policy: Notify People Operations 45 business days in advance.

Section 2: Health Insurance & Wellness Benefits (Page 2)
2.1 Comprehensive Medical Coverage: Platinum Health coverage starting on day 1. 100% employee premium covered, 75% dependents.
2.2 Mental Health: 12 free therapy sessions per year through Spring Health.
2.3 Annual Wellness Stipend: $600 per year for gym, fitness, and wellness apps.

Section 3: Paid Time Off & Learning Budgets (Page 3)
3.1 PTO Policy: Flexible PTO with a mandatory minimum of 15 days per year.
3.2 Professional Learning & Development: $2,500 annual education budget for conferences, certifications, and technical courses.
"""
        txt_path.write_text(content, encoding="utf-8")
        print(f"[OK] Created sample text document: {txt_path.resolve()}")


if __name__ == "__main__":
    generate_pdf()
