# Pattern INVOKE — GHO Core

- Documentary basis: [A1 CVL2 migration guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [A1 changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [A2 methods](https://docs.certora.com/en/latest/docs/cvl/methods.html). Specific section: Migration Step 2, removed invoke.
- **1** extracted instances contain this textual signal: incomplete/19.
- Proposed minimal textual *candidate*: Candidate `invoke f(args)` to `f@withrevert(args)`; check whether lastReverted semantics remain.
- Applicability is **not** automatic. Some extracted .spec files include reusable auxiliary declarations not on an active path; inspect the literal rule, import closure, target ABI and summary receiver individually (dossiers hold local snippets).
- Semantic failure conditions: a new assumption suppresses the old counterexample, a receiver changes, a quantified domain narrows, storage/revert paths differ, or induction becomes vacuous.
- Status: INCOMPLETE provenance, **not compiled or proven**; no Phase 2 authorized.

## Anotacao da contrarrevisao 2026-10-19
Propostas por ocorrencia literal nos dossies individuais. Verificar [A1](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html) e [A2](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html); nao alterar receiver, summaries, args, quantificadores, storage, revert ou condicoes antes de fechar ABI historica.

## Segunda auditoria: gate ABIs
A regra do pattern nao e uma prova de implementacao. O campo phase2_readiness_second_review por property e UNRESOLVED; confrontar ABI, receiver, summary, e impacto de revert com o estudo historico do projeto. Sintaxe A1 documentada nao confere autorizacao de migracao.
