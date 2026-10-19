# AGENTE-06 — P4, evidence E-A2-USING

- Source: A2, https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html
- Section: Use of contract name instead of using variable; reviewed 2026-10-19, current docs latest.
- Official rule: For user-defined contract types CVL2 needs concrete contract name; using aliases are still required for calls on secondary contracts.
- Scope: case-specific textual candidate only, no compiler replay; never assume broad wildcard receiver, valid signatures or proof equivalence without review.
- Conservative alternative: UNRESOLVED_CANDIDATE when method reachability or type scope is unverified.
