import json
from typing import Dict, Any

INVOICE_FEW_SHOT_EXAMPLE = {
    "raw": """
    INVOICE #INV-2024-001
    Issued: 2024-01-15 | Due: 2024-02-15
    From: CloudTech Solutions, 100 Tech Blvd, Austin, TX. contact@cloudtech.io
    Bill To: Global Retail Corp, 45 Market St, Chicago, IL. ap@globalretail.com
    Items:
    1. Cloud Hosting Services - 1 mo @ $1200.00 = $1200.00
    2. Maintenance & Support - 10 hrs @ $150.00 = $1500.00
    Subtotal: $2700.00
    Tax (10%): $270.00
    Total: $2970.00 USD
    """,
    "parsed": {
        "invoice_number": "INV-2024-001",
        "invoice_date": "2024-01-15",
        "due_date": "2024-02-15",
        "vendor": {
            "name": "CloudTech Solutions",
            "address": "100 Tech Blvd, Austin, TX",
            "email": "contact@cloudtech.io",
            "phone": None
        },
        "customer": {
            "name": "Global Retail Corp",
            "address": "45 Market St, Chicago, IL",
            "email": "ap@globalretail.com"
        },
        "items": [
            {
                "description": "Cloud Hosting Services",
                "quantity": 1.0,
                "unit_price": 1200.0,
                "total": 1200.0
            },
            {
                "description": "Maintenance & Support",
                "quantity": 10.0,
                "unit_price": 150.0,
                "total": 1500.0
            }
        ],
        "subtotal": 2700.0,
        "tax_amount": 270.0,
        "discount_amount": 0.0,
        "total_amount": 2970.0,
        "currency": "USD"
    }
}

RESUME_FEW_SHOT_EXAMPLE = {
    "raw": """
    Alex Mercer
    San Francisco, CA | alex.mercer@email.com | (555) 019-2834
    Senior Backend Engineer with 6+ years in distributed systems and cloud architecture.
    
    SKILLS: Python, Go, Docker, Kubernetes, AWS, PostgreSQL, Redis, FastAPI
    
    WORK EXPERIENCE:
    Lead Software Engineer - DataSphere (2021 - Present) - SF, CA
    - Architected real-time streaming pipeline processing 2M events/sec.
    - Mentored 5 junior engineers and led migration to microservices.
    
    Software Engineer - FinTech Labs (2018 - 2021) - Remote
    - Developed payment gateway integrations with 99.99% reliability.
    
    EDUCATION:
    B.S. in Computer Science - University of California, Berkeley (2014 - 2018)
    
    CERTIFICATIONS: AWS Certified Solutions Architect Professional
    """,
    "parsed": {
        "full_name": "Alex Mercer",
        "email": "alex.mercer@email.com",
        "phone": "(555) 019-2834",
        "location": "San Francisco, CA",
        "summary": "Senior Backend Engineer with 6+ years in distributed systems and cloud architecture.",
        "skills": ["Python", "Go", "Docker", "Kubernetes", "AWS", "PostgreSQL", "Redis", "FastAPI"],
        "experience": [
            {
                "title": "Lead Software Engineer",
                "company": "DataSphere",
                "location": "SF, CA",
                "start_date": "2021",
                "end_date": "Present",
                "responsibilities": [
                    "Architected real-time streaming pipeline processing 2M events/sec.",
                    "Mentored 5 junior engineers and led migration to microservices."
                ]
            },
            {
                "title": "Software Engineer",
                "company": "FinTech Labs",
                "location": "Remote",
                "start_date": "2018",
                "end_date": "2021",
                "responsibilities": [
                    "Developed payment gateway integrations with 99.99% reliability."
                ]
            }
        ],
        "education": [
            {
                "degree": "B.S. in Computer Science",
                "institution": "University of California, Berkeley",
                "graduation_year": "2018",
                "gpa": None
            }
        ],
        "certifications": ["AWS Certified Solutions Architect Professional"]
    }
}


def build_prompt(doc_type: str, raw_text: str, schema_json: Dict[str, Any]) -> str:
    """Builds a parameterized prompt with few-shot context and schema constraints."""
    if doc_type.lower() == "invoice":
        few_shot = INVOICE_FEW_SHOT_EXAMPLE
    else:
        few_shot = RESUME_FEW_SHOT_EXAMPLE

    prompt = f"""You are an expert data extraction AI. Your job is to extract structured information from unstructured text documents and strictly output valid JSON matching the provided schema.

Target JSON Schema:
{json.dumps(schema_json, indent=2)}

---
Here is an example of raw input and the target extracted JSON:
EXAMPLE INPUT:
{few_shot['raw'].strip()}

EXAMPLE OUTPUT JSON:
{json.dumps(few_shot['parsed'], indent=2)}
---

Now, carefully extract all relevant details from the following input document. 
Rules:
1. Do not invent or hallucinate information not present in the document.
2. If optional fields are absent, use null or an empty list.
3. Numeric values must be numbers (float or int), not strings with symbols.
4. Return ONLY valid JSON. Do not add conversational text or markdown code fences.

INPUT DOCUMENT:
{raw_text.strip()}
"""
    return prompt
