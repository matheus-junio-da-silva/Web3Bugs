# AGENTE-06 P1 — QA de inventário, ainda NÃO de equivalência semântica

- Baseline Web3Bugs 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 confirmado; PropertyGPT 687f654c679ed45ab127b7949e2a29c8f5e491b9 confirmado.
- Árvores Git conferidas: 36 complete e 34 incomplete N.spec; 70 chaves canônicas = 70 dossiês e 70 linhas properties.csv.
- Relações Bug Label 72, excedentes de multi-label 2, sem duplicar exemplos.
- Caminhos e blob SHAs de N.spec/N.md/N.sol/N.txt recuperados da árvore Git imutável e incluídos em cada dossiê.
- Limitação IMPORTANTE: 159 corpos CVL e Solidity NÃO foram todos lidos semanticamente. Este inventário por metadata NÃO encerra a tarefa da fase 1 e não justifica candidaturas específicas de edição.
- Versões de solc e CLI não inventariadas; Remote Desktop Commander offline e container local inacessível.
- Validadores Python, git diff --check, PDF page-by-page, CVL1, CVL2, Prover NÃO executados.
- Bloqueio crítico: queue2 and _mock are potentially missing helpers; complexity.spec may depend on an unarchived harness. Do not treat queue2 as Solidity ABI.
- Próximo passo obrigatório antes de revisão para Fase 2: leitura individual dos N.spec, N.md, N.sol e transitive imports, reconstrução histórica com hashes upstream auditados, motivos N.txt e pesquisa official per-case.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## Pesquisa histórica atualizada 2026-10-19

Commit da revisão do relatório P1 comprovado por upstream: `303bd3e16c8d3465325389a72564126c3bacc4f9`. Cinco contratos comparados; diferenças de pragma/comment documentadas em [AUDITED_SOURCE_PROVENANCE.md](AUDITED_SOURCE_PROVENANCE.md). Target/verificação CVL específicos ainda não reconstruídos. Sem replay.

## Reconciliation update 2026-10-19 — supersedes earlier inventory-only note

- 70 original CVL rule/invariant bodies individually inspected; 36 complete and 34 incomplete; report-confirmed audited commit 303bd3e16c8d3465325389a72564126c3bacc4f9; five bridge contract snapshots differ only in pragma/comment in the inspected pairwise comparisons; missing queue2/_mock and complexity harness remain.
- **Confirmed CVL first-pass coverage**: 70/70 individual dossiers now have a source-specific CVL body inspection flag in properties.csv; no `INVENTORY_ONLY_PENDING_SEMANTIC_INSPECTION` remains.
- This only demonstrates documentary reading of archived CVL and candidate-level syntax triage; **not** line-by-line confirmation of complete Solidity dependency closure, not compiler success, not semantic equivalence, and not a historical Certora replay.
- Historical Result and Detection Outcome preserved without promoting original complete/incomplete into compiled/verified CVL2 statuses.
- Structural QA of property key uniqueness and count performed using GitHub fetch and CSV parsing in connector; Python validators and git diff --check still NOT executed on live PR branch.
- GitHub changes are restricted to docs/cvl2/research/AGENTE-06; no changes to contracts, result CSV, specs or scripts.
- **SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
