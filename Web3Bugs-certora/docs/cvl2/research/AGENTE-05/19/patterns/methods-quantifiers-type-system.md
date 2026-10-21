# P19 official-document migration controls (research only)

1. **E-METHOD**: methods entries use `function`, `internal/external`, `;`; select visibility only with Solidity historical ABI. https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#changes-to-methods-block-entries
2. **E-SCOPE**: CVL1 summaries can cover all matching contracts; CVL2 without explicit receiver applies to currentContract. Exact source method and receiver must be adjudicated. https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#step-4-review-your-methods-blocks
3. **E-SEMICOLON**: using/import/invariant need terminators; preserved/filtered continuation is an exception. https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#required-in-more-places
4. **E-CAST**: CVL2 arithmetic returns mathint; require_ casts can remove counterexample states and cannot be inserted just to satisfy typechecking. https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#changes-to-integer-types
5. **E-REMOVED**: deprecated invoke/sinvoke/static_assert are mapped case-by-case; retain revert paths, meaning of summaries and preconditions. https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#removed-features

**Project-specific:** Unvendored historical @openzeppelin packages; scripts alter harness state/caps and target; 36 declarations become 37 target-specific instances; privilegedOperation must not be inferred as ACL.

Individual dossier must quote exact original line, targeted textual candidate (if justified), and the corresponding E-ID; otherwise explicitly state evidence insufficient. No blanket rewrite to historical sources.
