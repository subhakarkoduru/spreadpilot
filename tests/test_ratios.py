"""Tests for deterministic ratio computation."""
from spreadpilot.models import FinancialStatement, LineItem
from spreadpilot.ratios import compute_ratios


def _statement(*pairs: tuple[tuple[str, str], float]) -> FinancialStatement:
    items = [
        LineItem(name=name, value=value, statement=stmt, source_page=1)
        for (name, stmt), value in pairs
    ]
    return FinancialStatement(company="Acme Corp", period_end="2025-12-31", line_items=items)


def test_interest_coverage():
    fs = _statement(
        (("EBIT", "income_statement"), 500.0),
        (("Interest expense", "income_statement"), 100.0),
    )
    ratios = {r.name: r for r in compute_ratios(fs)}
    assert ratios["interest_coverage"].value == 5.0
    assert ratios["interest_coverage"].formula == "EBIT / interest_expense"


def test_zero_interest_expense_returns_none():
    fs = _statement(
        (("EBIT", "income_statement"), 500.0),
        (("Interest expense", "income_statement"), 0.0),
    )
    ratios = {r.name: r for r in compute_ratios(fs)}
    assert ratios["interest_coverage"].value is None


def test_missing_inputs_return_none():
    fs = _statement((("EBIT", "income_statement"), 500.0))
    ratios = {r.name: r for r in compute_ratios(fs)}
    assert ratios["interest_coverage"].value is None
    assert ratios["current_ratio"].value is None
    assert ratios["debt_to_equity"].value is None


def test_current_ratio_and_debt_to_equity():
    fs = _statement(
        (("Total current assets", "balance_sheet"), 300.0),
        (("Total current liabilities", "balance_sheet"), 150.0),
        (("Total liabilities", "balance_sheet"), 400.0),
        (("Total stockholders' equity", "balance_sheet"), 600.0),
    )
    ratios = {r.name: r for r in compute_ratios(fs)}
    assert ratios["current_ratio"].value == 2.0
    assert abs(ratios["debt_to_equity"].value - (400.0 / 600.0)) < 1e-9
