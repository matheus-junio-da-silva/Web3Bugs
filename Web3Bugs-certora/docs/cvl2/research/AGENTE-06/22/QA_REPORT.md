# AGENTE-06 P22 — QA de inventário, ainda NÃO de equivalência semântica

- Baseline Web3Bugs 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 confirmado; PropertyGPT 687f654c679ed45ab127b7949e2a29c8f5e491b9 confirmado.
- Árvores Git conferidas: 19 complete e 2 incomplete N.spec; 21 chaves canônicas = 21 dossiês e 21 linhas properties.csv.
- Relações Bug Label 21, excedentes de multi-label 0, sem duplicar exemplos.
- Caminhos e blob SHAs de N.spec/N.md/N.sol/N.txt recuperados da árvore Git imutável e incluídos em cada dossiê.
- Limitação IMPORTANTE: 159 corpos CVL e Solidity NÃO foram todos lidos semanticamente. Este inventário por metadata NÃO encerra a tarefa da fase 1 e não justifica candidaturas específicas de edição.
- Versões de solc e CLI não inventariadas; Remote Desktop Commander offline e container local inacessível.
- Validadores Python, git diff --check, PDF page-by-page, CVL1, CVL2, Prover NÃO executados.
- Bloqueio crítico: Archived runner selects only PopsicleV3Optimizer.spec with solc7.6 and links. PoolActionsWrapper totalSupply is private, not an external getter.
- Próximo passo obrigatório antes de revisão para Fase 2: leitura individual dos N.spec, N.md, N.sol e transitive imports, reconstrução histórica com hashes upstream auditados, motivos N.txt e pesquisa official per-case.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## Snapshot provenance update 2026-10-19

Certora branch upstream 3cb9cb7279a3fb1790b55251a029bb3065606dc8 matches six exact Git blobs, including the four original source .spec files and runner. It is NOT declared audited commit because the report ends verification in October and upstream commit is dated November 4. See [AUDITED_SOURCE_PROVENANCE.md](AUDITED_SOURCE_PROVENANCE.md).

## Reconciliation update 2026-10-19 — supersedes earlier inventory-only note

- 21 original CVL bodies individually inspected. Six archival source Git blobs match upstream certora branch SHA 3cb9cb7279a3fb1790b55251a029bb3065606dc8; dated 2021-11-04, this commit is NOT proven as the historical audited revision. Optimizer-only runner and absent PoolActionsWrapper getter remain blockers.
- **Confirmed CVL first-pass coverage**: 21/21 individual dossiers now have a source-specific CVL body inspection flag in properties.csv; no `INVENTORY_ONLY_PENDING_SEMANTIC_INSPECTION` remains.
- This only demonstrates documentary reading of archived CVL and candidate-level syntax triage; **not** line-by-line confirmation of complete Solidity dependency closure, not compiler success, not semantic equivalence, and not a historical Certora replay.
- Historical Result and Detection Outcome preserved without promoting original complete/incomplete into compiled/verified CVL2 statuses.
- Structural QA of property key uniqueness and count performed using GitHub fetch and CSV parsing in connector; Python validators and git diff --check still NOT executed on live PR branch.
- GitHub changes are restricted to docs/cvl2/research/AGENTE-06; no changes to contracts, result CSV, specs or scripts.
- **SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
