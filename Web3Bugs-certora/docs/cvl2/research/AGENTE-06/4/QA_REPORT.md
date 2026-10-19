# AGENTE-06 P4 — QA de inventário, ainda NÃO de equivalência semântica

- Baseline Web3Bugs 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 confirmado; PropertyGPT 687f654c679ed45ab127b7949e2a29c8f5e491b9 confirmado.
- Árvores Git conferidas: 0 complete e 27 incomplete N.spec; 27 chaves canônicas = 27 dossiês e 27 linhas properties.csv.
- Relações Bug Label 28, excedentes de multi-label 1, sem duplicar exemplos.
- Caminhos e blob SHAs de N.spec/N.md/N.sol/N.txt recuperados da árvore Git imutável e incluídos em cada dossiê.
- Limitação IMPORTANTE: 159 corpos CVL e Solidity NÃO foram todos lidos semanticamente. Este inventário por metadata NÃO encerra a tarefa da fase 1 e não justifica candidaturas específicas de edição.
- Versões de solc e CLI não inventariadas; Remote Desktop Commander offline e container local inacessível.
- Validadores Python, git diff --check, PDF page-by-page, CVL1, CVL2, Prover NÃO executados.
- Bloqueio crítico: Original StakedAaveV3Harness relies on missing generated certora/munged/ and src/ tree. Do not substitute root Solidity for verified target.
- Próximo passo obrigatório antes de revisão para Fase 2: leitura individual dos N.spec, N.md, N.sol e transitive imports, reconstrução histórica com hashes upstream auditados, motivos N.txt e pesquisa official per-case.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## Atualização 2026-10-19: proveniência auditada

Ver [AUDITED_SOURCE_PROVENANCE.md](AUDITED_SOURCE_PROVENANCE.md). O PDF identifica 4cf8837, expandido para 4cf8837121a4351cc0e21703bb1df76036205114; fontes base recuperáveis com blobs, mas harness gerado ainda ausente. Os N.md antigos podem registrar SHA não confirmado por propriedade, o que permanece válido para reconstrução completa. Nenhuma compilação/Prover foi executada.

## Reconciliation update 2026-10-19 — supersedes earlier inventory-only note

- 27 original CVL bodies individually inspected, all historically incomplete. Original PDF reviewed on pages 1 and 3, audited SHA 4cf8837121a4351cc0e21703bb1df76036205114; audited src recovered with blobs but munged/harness not recovered; modeling limitations retained.
- **Confirmed CVL first-pass coverage**: 27/27 individual dossiers now have a source-specific CVL body inspection flag in properties.csv; no `INVENTORY_ONLY_PENDING_SEMANTIC_INSPECTION` remains.
- This only demonstrates documentary reading of archived CVL and candidate-level syntax triage; **not** line-by-line confirmation of complete Solidity dependency closure, not compiler success, not semantic equivalence, and not a historical Certora replay.
- Historical Result and Detection Outcome preserved without promoting original complete/incomplete into compiled/verified CVL2 statuses.
- Structural QA of property key uniqueness and count performed using GitHub fetch and CSV parsing in connector; Python validators and git diff --check still NOT executed on live PR branch.
- GitHub changes are restricted to docs/cvl2/research/AGENTE-06; no changes to contracts, result CSV, specs or scripts.
- **SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
