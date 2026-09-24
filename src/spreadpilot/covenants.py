"""Covenant drafting: Ratio -> CovenantDraft.

Contract
---------
draft_covenant(ratio, threshold, operator) -> CovenantDraft

Implementation plan (not yet built): given a computed ratio and a threshold,
ask Claude to draft the covenant clause language (e.g. "Borrower shall
maintain an Interest Coverage Ratio of not less than 1.25x, tested
quarterly."). The draft is returned with status="draft"; only a human
moves it to "approved".

Not implemented yet.
"""
from __future__ import annotations

from .models import CovenantDraft, Ratio


def draft_covenant(ratio: Ratio, threshold: float, operator: str = ">=") -> CovenantDraft:
    raise NotImplementedError(
        "covenants.draft_covenant is not implemented yet: wire Claude to draft "
        "the covenant clause from the computed ratio here."
    )
