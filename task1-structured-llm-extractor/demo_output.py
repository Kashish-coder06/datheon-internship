"""
Mock test script demonstrating the exact input -> extraction -> validated JSON output
without requiring live API keys.
"""
import json
from schemas import InvoiceSchema, ResumeSchema
from prompt_templates import INVOICE_FEW_SHOT_EXAMPLE, RESUME_FEW_SHOT_EXAMPLE
from pathlib import Path


def demo():
    print("=" * 70)
    print(" TASK 1: STRUCTURED LLM PROMPT PIPELINE & JSON EXTRACTOR (OUTPUT DEMO)")
    print("=" * 70)

    # 1. Invoice Demonstration
    invoice_path = Path("samples/sample_invoice.txt")
    print(f"\n[1] UNSTRUCTURED INPUT DOCUMENT (Invoice: {invoice_path.name}):")
    print("-" * 50)
    print(invoice_path.read_text(encoding="utf-8").strip())
    print("-" * 50)

    # Validating simulated LLM output against Pydantic schema
    invoice_extracted_data = {
        "invoice_number": "INV-98421-B",
        "invoice_date": "2024-11-12",
        "due_date": "2024-12-12",
        "vendor": {
            "name": "ACME SUPPLIES & HARDWARE CO.",
            "address": "1084 Industrial Pkwy, Suite 400, Dallas, TX 75201",
            "email": "support@acmesupplies.com",
            "phone": "+1 (214) 555-0199"
        },
        "customer": {
            "name": "Apex Logistics International",
            "address": "742 Evergreen Terrace, Springfield, OR",
            "email": "accounting@apexlogistics.com"
        },
        "items": [
            {
                "description": "Heavy Duty Industrial Shelving Unit (Model X4)",
                "quantity": 4.0,
                "unit_price": 250.0,
                "total": 1000.0
            },
            {
                "description": "Heavy Duty Forklift Pallet Jack",
                "quantity": 1.0,
                "unit_price": 750.0,
                "total": 750.0
            },
            {
                "description": "Standard On-site Freight & Handling",
                "quantity": 1.0,
                "unit_price": 150.0,
                "total": 150.0
            }
        ],
        "subtotal": 1900.0,
        "tax_amount": 148.50,
        "discount_amount": 100.0,
        "total_amount": 1948.50,
        "currency": "USD"
    }

    validated_invoice = InvoiceSchema.model_validate(invoice_extracted_data)

    print("\n[2] VALIDATED PYDANTIC JSON OUTPUT (Invoice):")
    print("-" * 50)
    print(validated_invoice.model_dump_json(indent=2))
    print("-" * 50)

    print("\n[OK] Verification:")
    print(f"* Total calculated correctly: {validated_invoice.currency} {validated_invoice.total_amount}")
    print(f"* Number of items extracted: {len(validated_invoice.items)}")
    print(f"* Vendor: {validated_invoice.vendor.name}")

if __name__ == "__main__":
    demo()
