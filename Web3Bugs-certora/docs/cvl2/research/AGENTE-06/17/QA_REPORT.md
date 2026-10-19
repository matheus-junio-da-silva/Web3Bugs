# AGENTE-06 P17 — QA de inventário, ainda NÃO de equivalência semântica

- Baseline Web3Bugs 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 confirmado; PropertyGPT 687f654c679ed45ab127b7949e2a29c8f5e491b9 confirmado.
- Árvores Git conferidas: 31 complete e 10 incomplete N.spec; 41 chaves canônicas = 41 dossiês e 41 linhas properties.csv.
- Relações Bug Label 41, excedentes de multi-label 0, sem duplicar exemplos.
- Caminhos e blob SHAs de N.spec/N.md/N.sol/N.txt recuperados da árvore Git imutável e incluídos em cada dossiê.
- Limitação IMPORTANTE: 159 corpos CVL e Solidity NÃO foram todos lidos semanticamente. Este inventário por metadata NÃO encerra a tarefa da fase 1 e não justifica candidaturas específicas de edição.
- Versões de solc e CLI não inventariadas; Remote Desktop Commander offline e container local inacessível.
- Validadores Python, git diff --check, PDF page-by-page, CVL1, CVL2, Prover NÃO executados.
- Bloqueio crítico: Specify .cvl is not equivalent to ordinary CVL1 .spec. The .spclnk aliases and modeled ABI are historical context, not property instances.
- Próximo passo obrigatório antes de revisão para Fase 2: leitura individual dos N.spec, N.md, N.sol e transitive imports, reconstrução histórica com hashes upstream auditados, motivos N.txt e pesquisa official per-case.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## Atualização auditada 2026-10-19

Identificado commit upstream e 5 arquivos byte-idênticos aos archived originals; detalhes em [AUDITED_SOURCE_PROVENANCE.md](AUDITED_SOURCE_PROVENANCE.md). O status incomplete de dez exemplos permanece; sem CVL2 ou Prover.

## Reconciliation update 2026-10-19 — supersedes earlier inventory-only note

- 41 original legacy Specify/CVL source blocks individually inspected; report-confirmed SHA f385d71983ae5c5799faae9b2dfea43e5cf75262; two Solidity and three .cvl files exactly match audited repo; absent synthetic ABI calls and conversion of Specify remain blockers.
- **Confirmed CVL first-pass coverage**: 41/41 individual dossiers now have a source-specific CVL body inspection flag in properties.csv; no `INVENTORY_ONLY_PENDING_SEMANTIC_INSPECTION` remains.
- This only demonstrates documentary reading of archived CVL and candidate-level syntax triage; **not** line-by-line confirmation of complete Solidity dependency closure, not compiler success, not semantic equivalence, and not a historical Certora replay.
- Historical Result and Detection Outcome preserved without promoting original complete/incomplete into compiled/verified CVL2 statuses.
- Structural QA of property key uniqueness and count performed using GitHub fetch and CSV parsing in connector; Python validators and git diff --check still NOT executed on live PR branch.
- GitHub changes are restricted to docs/cvl2/research/AGENTE-06; no changes to contracts, result CSV, specs or scripts.
- **SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**


## AGENTE-06 — QA da contrarrevisão / Fase 1

- 159 no agregado, projeto 17: 41 dossiês individualizados; 31 complete, 10 incomplete; chaves únicas confirmadas.
- N.spec, N.md, N.sol lidos individualmente (hash SHA256 por property no CSV e dossier); N.txt lido para os 10 incompletos e registrado com SHA no recovery_manifest.
- Commit apontado pelo relatório: f385d71983ae5c5799faae9b2dfea43e5cf75262 (P22 NOT_CONFIRMED; não confundir branch upstream pós-auditoria com revisão auditada).
- Escopo de fonte/runner examinado: contracts/17/spec/formal/*.cvl; contracts/17/spec/formal/*.spclnk (JSON aliases).
- Padrões CVL lexicalmente identificados para avaliação, sem edit aplicada: {'E-A2-METHODS': 41, 'E-A2-CALL': 41, 'E-A2-STATIC': 41, 'E-A2-HAVOC': 41, 'E-A2-RULE': 41}.
- PDF original lido textualmente, correspondências exatas do nome da property: 35/41; demais 6 não mapeados literalmente. PDF não foi relido visualmente por todas as páginas/fórmulas; ausência de nome não é prova de ausência da obrigação.
- Resultado dos comandos executados em worktree isolada: python3 scripts/check_specs.py . exit 0; python3 scripts/check_contracts.py . exit 0; python3 scripts/check_contests_csv.py . exit 0. Logs em ../logs/{specs,contracts,contests}.log.
- git diff --check passou após remoção de whitespace gerado; log em ../logs/git-diff-check.log. Reexecutar depois desta escrita, antes do push.
- Não houve execução de solc/CVL1/CVL2/Certora Prover. O resultado histórico VERIFIED/NOT_STATED e a classificação original complete/incomplete permanecem intactos.
- **PENDÊNCIA QUE IMPEDE CONCLUSÃO SEMÂNTICA TOTAL:** Specify 2019 com aliases .spclnk JSON, ambientes, sinvoke/invoke, havoc local e static_assert/static_require não equivale a CVL1 usual. Falta prova da semântica histórica do engine e reversão.


## Segunda revisao independente — fechamento historico

Triagem documental 41 propriedades. Estados conclusivos por familia e condicoes de reabertura no documento HISTORICAL_BLOCKER_CLOSURE.md. Confirmar que historical_blocked e evidencia ausente, enquanto UNRESOLVED_CANDIDATE continua hipotese de CVL2. Nenhuma Fase 2.
