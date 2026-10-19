# PAT-02 — Method literals and removed invocation syntax

Evidence: EV-A1-SELECTOR and EV-A1-INVOKE. Examples include `registry.spec` comparisons to `register(address,bytes32).selector`, `libParam.spec` comparisons to `getParams(bytes32).selector`, `privileged.spec` with `invoke f(...)`, and `sanity.spec` with `sinvoke f(...)`.

Documented minimal candidate: `getParams(bytes32).selector` → `sig:getParams(bytes32).selector` in an affected method-literal occurrence, without altering `f.selector`. `invoke f(e,arg)` → `f@withrevert(e,arg)`; `sinvoke f(e,arg)` → `f(e,arg)` per guide. **Stop** if `at initialStorage` or another storage/revert context cannot be defended in the exact current grammar; do not discard `at` to gain compilation.

Distinguish historical `lastHasThrown` from `lastReverted`; the former is not a universal no-revert property. **Not run.**