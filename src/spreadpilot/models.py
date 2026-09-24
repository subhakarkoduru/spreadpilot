"""Core data models for SpreadPilot.

Everything downstream (spread, ratios, covenants) builds on these.
A covenant draft never becomes operative without explicit human approval.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LineItem:
    """One extracted financial line item, with provenance back to the source."""

    name: str  # e.g. "Total current assets"
    value: float  # in the filing's currency
    currency: str = "USD"
    period: str = ""  # e.g. "FY2025"
    statement: str = ""  # "balance_sheet" | "income_statement" | "cash_flow"
    source_page: int | None = None  # page in the source PDF


@dataclass
class FinancialStatement:
    """All line items extracted from one filing."""

    company: str
    period_end: str
    line_items: list[LineItem] = field(default_factory=list)

    def get(self, name: str, statement: str = "") -> LineItem | None:
        """Find a line item by name (case-insensitive), optionally scoped to a statement."""
        name_l = name.lower()
        for li in self.line_items:
            if li.name.lower() == name_l and (not statement or li.statement == statement):
                return li
        return None


@dataclass
class Ratio:
    """A deterministically computed financial ratio.

    Ratios are computed in code from extracted line items. The LLM never
    performs arithmetic; it only extracts values and drafts language.
    """

    name: str  # e.g. "interest_coverage"
    value: float | None  # None when inputs are missing or divide-by-zero
    formula: str  # e.g. "EBIT / interest_expense"
    inputs: dict[str, float | None] = field(default_factory=dict)


@dataclass
class CovenantDraft:
    """A draft covenant clause derived from a computed ratio.

    status moves from "draft" to "approved" by a human only.
    """

    ratio_name: str
    operator: str  # e.g. ">=", "<="
    threshold: float
    test_frequency: str = "quarterly"
    language: str = ""
    status: str = "draft"
