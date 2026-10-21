# AGENTE-06 — consolidacao da segunda revisao independente

PR #38 DRAFT. Coordenador confirmou 159 propriedades e negou Fase 2 (revisao 2026-10-19).
Duas dimensoes independentes: historical_blocked_* = recuperacao historica impossivel com arquivos atualmente comprovados; UNRESOLVED_CANDIDATE = pesquisa de migracao ainda nao validada.

## Projeto 1
Distribuicao exata: historical_blocked_complexity_runner=6, historical_blocked_mock_helper=6, historical_blocked_queue2=14, historical_run_unattributed=44.
Relatorio: 1/HISTORICAL_BLOCKER_CLOSURE.md

## Projeto 17
Distribuicao exata: historical_blocked_specify_semantics=41.
Relatorio: 17/HISTORICAL_BLOCKER_CLOSURE.md

## Projeto 4
Distribuicao exata: historical_blocked_generated_munged=27.
Relatorio: 4/HISTORICAL_BLOCKER_CLOSURE.md

## Projeto 22
Distribuicao exata: historical_blocked_free_symbol=1, historical_blocked_private_getter=1, historical_blocked_runner_scope=6, historical_run_unattributed=13.
Relatorio: 22/HISTORICAL_BLOCKER_CLOSURE.md

## Criterio de parada
Provas primarias inexistentes no snapshot ficam encerradas como historical_blocked. Reabrir so com artefato historico autenticado ou decisao do coordenador. Sem especulacao sobre ABI, execucao ou vacuidade.

## Politica operacional
Nenhum arquivo de codigo/spec/catalogo alterado. Sem Certora Prover, sem compilacao, sem migracao. Preservar PR draft e submeter fechamento para revisao humana.

AGENTE-06 — FASE 1 / PESQUISA — ALERTA LARANJA (intervencao humana).

## Validacoes executadas nesta consolidacao

- python3 scripts/check_specs.py . : exit 0 (1386 exemplos, 1390 relacoes Bug Label no catalogo)
- python3 scripts/check_contracts.py . : exit 0
- python3 scripts/check_contests_csv.py . : exit 0
- integridade do CSV de decisoes: 159 chaves unicas, 102 historical_blocked, 57 historical_run_unattributed
- classificacao historica preservada: P1 36/34, P17 31/10, P4 0/27, P22 19/2 (complete/incomplete)
- todas as 159 candidaturas de migracao permanecem UNRESOLVED_CANDIDATE
- logs em logs/specs-second-review.log, logs/contracts-second-review.log e logs/contests-second-review.log
- git diff --check exit 0; validar outra vez apos staging.
