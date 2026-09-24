"""LLM extraction: PDF bytes -> FinancialStatement.

Contract
--------
extract(pdf_bytes, company, period_end) -> FinancialStatement

Implementation plan (not yet built): send the PDF to Claude with structured
outputs constrained to the LineItem schema (name, value, currency, period,
statement, source_page). Prefer explicit line-item names; keep every value
traceable to a source page for the audit trail.

Not implemented yet.
"""
from __future__ import annotations

from .models import FinancialStatement


def extract(pdf_bytes: bytes, company: str, period_end: str) -> FinancialStatement:
    raise NotImplementedError(
        "extractor.extract is not implemented yet: wire Claude structured "
        "outputs against the LineItem schema here."
    )
