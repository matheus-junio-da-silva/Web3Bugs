# P3 — CVL1→CVL2 documentary patterns (not automated patches)

Analyzed 3 individually keyed examples; applicability is given in each `properties/` report by original line, direct textual candidate and evidence IDs. This reference **never** authorizes applying a generic edit to all specs.

1. **E-METHOD / E-RECEIVER**: CVL2 requires `function`, `internal|external`, terminator in methods. CVL1 receiver-unspecified summaries may cover all matching contracts whereas CVL2 defaults to currentContract. Inspect actual target/function visibility/ABI before picking `_.method`, internal or external. https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#step-4-review-your-methods-blocks
2. **E-SEMICOLON**: using/import/invariant require semicolon in CVL2 except invariants continued by preserved/filtered. Exact source declaration must govern. https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#required-in-more-places
3. **E-REMOVED**: invoke/sinvoke/static_assert changes are documented; preserving revert observation takes priority over a mechanical replacement. https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#removed-features
4. **E-TYPES**: arithmetic returns mathint; no ungrounded `require_uint*` or `assert_uint*` insertions, especially inside quantifiers or havoc. https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#changes-to-integer-types

Project-specific pitfall: Specs coincidem com Certora Review 33c1aeca; Solidity de PropertyGPT é master posterior. O relatório também cita mitigação c905eaf; não há versão única demonstrada para todos os resultados.

State of every change is provisional until authorized future compilation and semantic cross-review. Nothing in Phase 1 changed historical sources.
