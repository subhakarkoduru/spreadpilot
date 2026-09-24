"""Deterministic ratio computation.

Ratios are computed in code from extracted line items. The LLM never does
arithmetic; it only extracts values and drafts covenant language.
"""
from __future__ import annotations

from .models import FinancialStatement, Ratio


def _safe_div(numer: float | None, denom: float | None) -> float | None:
    if numer is None or denom is None or denom == 0:
        return None
    return numer / denom


def _first_value(fs: FinancialStatement, names: list[str], statement: str = "") -> float | None:
    for name in names:
        li = fs.get(name, statement)
        if li is not None:
            return li.value
    return None


def compute_ratios(fs: FinancialStatement) -> list[Ratio]:
    """Compute the standard covenant ratios from an extracted statement."""
    ebit = _first_value(fs, ["EBIT", "Operating income", "Income from operations"], "income_statement")
    interest_expense = _first_value(fs, ["Interest expense"], "income_statement")
    current_assets = _first_value(fs, ["Total current assets"], "balance_sheet")
    current_liabilities = _first_value(fs, ["Total current liabilities"], "balance_sheet")
    total_liabilities = _first_value(fs, ["Total liabilities"], "balance_sheet")
    equity = _first_value(
        fs, ["Total stockholders' equity", "Total equity"], "balance_sheet"
    )

    return [
        Ratio(
            name="interest_coverage",
            value=_safe_div(ebit, interest_expense),
            formula="EBIT / interest_expense",
            inputs={"ebit": ebit, "interest_expense": interest_expense},
        ),
        Ratio(
            name="current_ratio",
            value=_safe_div(current_assets, current_liabilities),
            formula="total_current_assets / total_current_liabilities",
            inputs={
                "total_current_assets": current_assets,
                "total_current_liabilities": current_liabilities,
            },
        ),
        Ratio(
            name="debt_to_equity",
            value=_safe_div(total_liabilities, equity),
            formula="total_liabilities / total_equity",
            inputs={"total_liabilities": total_liabilities, "total_equity": equity},
        ),
    ]
