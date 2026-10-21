# P22 — summary receiver semantics

Certora A2: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html, section `Summaries only apply to one contract by default`.

CVL1 methods summaries applied to matching method signatures in all contracts; CVL2 defaults to currentContract. A wildcard receiver must only be proposed after confirming original scope and library/contract relationships. Candidate only; no recompilation or Prover.
