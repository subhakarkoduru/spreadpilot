# SpreadPilot

A personal learning project: upload a borrower's financial statements, extract
structured line items with an LLM, compute covenant ratios **deterministically
in code**, and draft covenant clauses for human approval.

Inspired by the agentic document-processing pattern used in commercial lending
(doc → structured extraction → downstream action with human sign-off). This is
an independent project built only with **public filings** (e.g. SEC EDGAR
10-Ks) — no employer or client data, code, or materials are used.

## Week 1 scope (the smallest shippable slice)

1. Repo skeleton (this).
2. `extractor` for exactly one input type: a 10-K financial-statements PDF.
3. Deterministic ratio computation in code (interest coverage, current ratio,
   debt-to-equity). The LLM never does arithmetic.
4. First 3–5 golden evaluation cases for extraction accuracy.
5. One real end-to-end worked example: one public 10-K → spread → ratios →
   covenant draft.

**Done =** given a public 10-K, the pipeline produces a spread, three computed
ratios, and one covenant draft awaiting human approval, documented in
`examples/worked-example.md`.

## What's real vs stub

- Real: `models.py` (`LineItem`, `FinancialStatement`, `Ratio`,
  `CovenantDraft`); `ratios.py` (deterministic math + tests).
- Stubs (`NotImplementedError`, no fake logic): `extractor.py`,
  `covenants.py`.

## Layout

- `src/spreadpilot/` — models, extractor, ratios, covenant drafting
- `evals/golden/` — golden evaluation cases (extraction accuracy)
- `examples/worked-example.md` — the one real end-to-end run
- `tests/` — unit tests

## Run tests

```bash
pip install -e ".[dev]"
pytest
```
