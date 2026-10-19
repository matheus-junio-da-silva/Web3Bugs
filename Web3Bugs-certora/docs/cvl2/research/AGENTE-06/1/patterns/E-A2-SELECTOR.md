# AGENTE-06 — P1, evidence E-A2-SELECTOR

- Source: A2, https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html
- Section: Method literals require sig:; reviewed 2026-10-19, current docs latest.
- Official rule: A method type literal in a selector comparison needs the `sig:` prefix. Do not change selector logic or method quantification.
- Scope: case-specific textual candidate only, no compiler replay; never assume broad wildcard receiver, valid signatures or proof equivalence without review.
- Conservative alternative: UNRESOLVED_CANDIDATE when method reachability or type scope is unverified.
