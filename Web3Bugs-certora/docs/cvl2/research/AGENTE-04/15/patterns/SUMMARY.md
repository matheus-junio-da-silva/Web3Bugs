# Pattern SUMMARY — GHO Core

- Documentary basis: [A1 CVL2 migration guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [A1 changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [A2 methods](https://docs.certora.com/en/latest/docs/cvl/methods.html). Specific section: Migration Step 4, receiver contract.
- **60** extracted instances contain this textual signal: incomplete/1, incomplete/2, incomplete/3, incomplete/4, incomplete/5, incomplete/6, incomplete/7, incomplete/8, incomplete/9, incomplete/10, incomplete/11, incomplete/12, incomplete/13, incomplete/14, incomplete/15, incomplete/16, incomplete/17, incomplete/18, incomplete/19, incomplete/20, incomplete/21, incomplete/22, incomplete/23, incomplete/24, incomplete/25, incomplete/26, incomplete/27, incomplete/28, incomplete/29, incomplete/30, incomplete/31, incomplete/32, incomplete/33, incomplete/34, incomplete/35, incomplete/65, incomplete/66, incomplete/67, incomplete/68, incomplete/69, incomplete/70, incomplete/71, incomplete/72, incomplete/73, incomplete/74, incomplete/75, incomplete/76, incomplete/77, incomplete/78, incomplete/79, incomplete/80, incomplete/81, incomplete/82, incomplete/83, incomplete/84, incomplete/85, incomplete/86, incomplete/87, incomplete/88, incomplete/89.
- Proposed minimal textual *candidate*: Determine specific receiver/wildcard from original inter-contract effect; do not automatically broaden.
- Applicability is **not** automatic. Some extracted .spec files include reusable auxiliary declarations not on an active path; inspect the literal rule, import closure, target ABI and summary receiver individually (dossiers hold local snippets).
- Semantic failure conditions: a new assumption suppresses the old counterexample, a receiver changes, a quantified domain narrows, storage/revert paths differ, or induction becomes vacuous.
- Status: INCOMPLETE provenance, **not compiled or proven**; no Phase 2 authorized.

## Anotacao da contrarrevisao 2026-10-19
Propostas por ocorrencia literal nos dossies individuais. Verificar [A1](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html) e [A2](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html); nao alterar receiver, summaries, args, quantificadores, storage, revert ou condicoes antes de fechar ABI historica.

## Segunda auditoria: gate ABIs
A regra do pattern nao e uma prova de implementacao. O campo phase2_readiness_second_review por property e UNRESOLVED; confrontar ABI, receiver, summary, e impacto de revert com o estudo historico do projeto. Sintaxe A1 documentada nao confere autorizacao de migracao.
