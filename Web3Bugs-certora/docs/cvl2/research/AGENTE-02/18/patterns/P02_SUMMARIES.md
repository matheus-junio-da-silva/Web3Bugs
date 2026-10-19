# P02 — summaries and receiver drift

**Authority:** A2-SUMMARY, A2-CVL-METHODS. CVL1 same-signature summary was global; CVL2 defaults to `currentContract`. Conditional candidate only: `function _.f(...) external => NONDET;` *if and only if* the original summary was global and return type/expect rules are resolved. An explicit defining contract may be necessary for inherited methods. Changing from DISPATCHER to NONDET, replacing a ghost, or adding `require` would be semantic changes, not grammar fixes.

Particularly investigate Governor/RulesInProgress and any multi-contract harness. Log ABI, full call-resolution universe, and original receiver coverage before any implementation. Source evidence SRC18-###; syntax A2-SUMMARY. Semantics unproven.
