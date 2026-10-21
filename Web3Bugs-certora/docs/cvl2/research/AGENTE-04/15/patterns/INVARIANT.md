# Pattern INVARIANT — GHO Core

- Documentary basis: [A1 CVL2 migration guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [A1 changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [A2 methods](https://docs.certora.com/en/latest/docs/cvl/methods.html). Specific section: Required semicolons and invariant preservation.
- **57** extracted instances contain this textual signal: incomplete/1, incomplete/34, incomplete/37, incomplete/38, incomplete/39, incomplete/40, incomplete/41, incomplete/42, incomplete/43, incomplete/44, incomplete/45, incomplete/46, incomplete/47, incomplete/48, incomplete/49, incomplete/53, incomplete/55, incomplete/56, incomplete/57, incomplete/58, incomplete/59, incomplete/62, incomplete/63, incomplete/64, incomplete/65, incomplete/66, incomplete/67, incomplete/69, incomplete/70, incomplete/71, incomplete/90, incomplete/91, incomplete/92, incomplete/93, incomplete/94, incomplete/95, incomplete/96, incomplete/97, incomplete/98, incomplete/99, incomplete/100, incomplete/101, incomplete/102, incomplete/103, incomplete/104, incomplete/105, incomplete/106, incomplete/107, incomplete/108, incomplete/109, incomplete/110, incomplete/111, incomplete/112, incomplete/113, incomplete/114, incomplete/115, incomplete/116.
- Proposed minimal textual *candidate*: Check `preserved` and `filtered` exception before adding any semicolon; no inductive hypothesis added.
- Applicability is **not** automatic. Some extracted .spec files include reusable auxiliary declarations not on an active path; inspect the literal rule, import closure, target ABI and summary receiver individually (dossiers hold local snippets).
- Semantic failure conditions: a new assumption suppresses the old counterexample, a receiver changes, a quantified domain narrows, storage/revert paths differ, or induction becomes vacuous.
- Status: INCOMPLETE provenance, **not compiled or proven**; no Phase 2 authorized.

## Anotacao da contrarrevisao 2026-10-19
Propostas por ocorrencia literal nos dossies individuais. Verificar [A1](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html) e [A2](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html); nao alterar receiver, summaries, args, quantificadores, storage, revert ou condicoes antes de fechar ABI historica.

## Segunda auditoria: gate ABIs
A regra do pattern nao e uma prova de implementacao. O campo phase2_readiness_second_review por property e UNRESOLVED; confrontar ABI, receiver, summary, e impacto de revert com o estudo historico do projeto. Sintaxe A1 documentada nao confere autorizacao de migracao.
