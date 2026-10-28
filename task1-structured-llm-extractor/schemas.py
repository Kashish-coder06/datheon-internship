from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Invoice Schemas
# ---------------------------------------------------------------------------

class InvoiceItem(BaseModel):
    description: str = Field(description="Description of the product or service")
    quantity: float = Field(default=1.0, description="Quantity of items")
    unit_price: float = Field(description="Unit price of the item")
    total: float = Field(description="Total price for this line item (quantity * unit_price)")


class VendorInfo(BaseModel):
    name: str = Field(description="Vendor or company issuing the invoice")
    address: Optional[str] = Field(default=None, description="Physical address of vendor")
    email: Optional[str] = Field(default=None, description="Contact email of vendor")
    phone: Optional[str] = Field(default=None, description="Contact phone of vendor")


class CustomerInfo(BaseModel):
    name: str = Field(description="Customer or billing target name")
    address: Optional[str] = Field(default=None, description="Billing address of customer")
    email: Optional[str] = Field(default=None, description="Customer email")


class InvoiceSchema(BaseModel):
    invoice_number: str = Field(description="Invoice identification number / code")
    invoice_date: Optional[str] = Field(default=None, description="Date the invoice was issued (YYYY-MM-DD)")
    due_date: Optional[str] = Field(default=None, description="Payment due date (YYYY-MM-DD)")
    vendor: VendorInfo
    customer: CustomerInfo
    items: List[InvoiceItem] = Field(default_factory=list, description="List of line items billed")
    subtotal: float = Field(description="Subtotal before taxes/discounts")
    tax_amount: float = Field(default=0.0, description="Total tax applied")
    discount_amount: float = Field(default=0.0, description="Discount deducted if any")
    total_amount: float = Field(description="Final total balance due")
    currency: str = Field(default="USD", description="Currency symbol or 3-letter ISO code")


# ---------------------------------------------------------------------------
# Resume Schemas
# ---------------------------------------------------------------------------

class Education(BaseModel):
    degree: str = Field(description="Degree or program title (e.g. B.S. Computer Science)")
    institution: str = Field(description="University, college, or school name")
    graduation_year: Optional[str] = Field(default=None, description="Graduation year or dates attended")
    gpa: Optional[str] = Field(default=None, description="GPA if mentioned")


class Experience(BaseModel):
    title: str = Field(description="Job title or role")
    company: str = Field(description="Organization or company name")
    location: Optional[str] = Field(default=None, description="Job location or Remote")
    start_date: Optional[str] = Field(default=None, description="Start date")
    end_date: Optional[str] = Field(default=None, description="End date or Present")
    responsibilities: List[str] = Field(default_factory=list, description="Key tasks and accomplishments")


class ResumeSchema(BaseModel):
    full_name: str = Field(description="Full name of candidate")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    location: Optional[str] = Field(default=None, description="City, State, or Country")
    summary: Optional[str] = Field(default=None, description="Professional summary or objective")
    skills: List[str] = Field(default_factory=list, description="Technical, soft, and specialized skills")
    experience: List[Experience] = Field(default_factory=list, description="Work history")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    certifications: List[str] = Field(default_factory=list, description="Licenses and certifications")
