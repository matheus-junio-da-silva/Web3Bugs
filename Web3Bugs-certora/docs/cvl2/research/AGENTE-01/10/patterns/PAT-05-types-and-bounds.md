# PAT-05 — Arithmetic, type domain and bounds

Evidence: EV-A1-TYPES and EV-A1-GHOST. In `stackLengthIncreaseIsBounded`, the expression `stackLengthBefore + STACK_INCREASE_BOUND()` participates in a boolean bound and CVL2 arithmetic returns `mathint`; preserve its value domain and overflow semantics rather than introducing arbitrary `require_` assumptions. Other cases that use arithmetic or `address`/uint casts need line-specific assessment.

CVL2 may reject prior implicit conversions, but this is a **migration typing question**, not evidence of missing historical Solidity. Retain method quantification, before/after storage and the original assertion. Never infer that compile success or an added bound proves semantic equivalence.

**Not run.**