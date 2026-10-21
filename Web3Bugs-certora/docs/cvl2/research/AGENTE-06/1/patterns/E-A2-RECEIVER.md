# AGENTE-06 — P1, evidence E-A2-RECEIVER

- Source: A2, https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html
- Section: Summaries only apply to one contract by default; reviewed 2026-10-19, current docs latest.
- Official rule: A CVL1 summary matched signature across all contracts; CVL2 defaults to currentContract and wildcard `_` requires explicit justification, with different return/optional restrictions.
- Scope: case-specific textual candidate only, no compiler replay; never assume broad wildcard receiver, valid signatures or proof equivalence without review.
- Conservative alternative: UNRESOLVED_CANDIDATE when method reachability or type scope is unverified.
