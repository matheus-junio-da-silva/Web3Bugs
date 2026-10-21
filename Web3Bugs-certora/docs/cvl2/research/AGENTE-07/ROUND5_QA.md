# AGENTE-07 — Rodada 5 / QA executado

**Checkout isolado:** /home/mat/cvl2-agent07-round5-20261020. **Branch de origem:** research/cvl2-agente-07@96257f027dddefdbc231dd136416020535ad0ecb. **Baseline:** 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3.

Executados antes da publicação, na raiz Web3Bugs-certora:
- timeout 120 python3 scripts/check_specs.py . — EXIT 0; 1386 exemplos e 1390 relações.
- timeout 120 python3 scripts/check_contests_csv.py . — EXIT 0.
- timeout 120 python3 scripts/check_contracts.py . — EXIT 0.
- Verificação Python independente — EXIT 0: 156 chaves/hashes N.spec; 42 P8 incluindo 22 W1+1 W2W3; 7 linhas P9; ABI solc phase2 com 53 entries; 5 arquivos P20; nenhum COMPILE_OK CVL2 ou SEMANTIC_PROVEN.
- git -c core.whitespace=cr-at-eol diff --cached --check — EXIT 0.

Diagnóstico efetivo de ABI Solidity:
- solc-js 0.5.13, phase2 Accounts: 24 fontes, 0 erros, 53 ABI entries, exit 0; ABI JSON e source hashes publicados.
- mesmo solc-js, snapshot AccountsHarness: 3 ParserErrors por imports mento-core ausentes; ABI não gerada.
- CVL2 certoraRun --compilation_steps_only: **NÃO EXECUTADO (0)**, pois target histórico, harness, ABI e flags ainda não foram comprovados simultaneamente.
- Prover/CVL1: **NÃO EXECUTADOS (0)**.
- P20 applyHarnesses.sh: reprodução apenas no scratch da Rodada 4; nesta rodada SHA upstream comparado, sem aplicação in-place nova.
- P11 tarballs SRI e closure textual reexecutados no scratch: EXIT 0, 6/6 SRI, 104 nós e 204 imports, sem missing.
- Auditoria somente leitura de PR #43 HEAD 96771fa27f90e56299bccc75a9729937ec4e77cc: diff --check BASE...HEAD EXIT 0, 200 arquivos somente AGENTE-08.

**Após publicação:** os validadores oficiais na raiz Web3Bugs-certora e git diff --check BASE...HEAD serão repetidos na HEAD efetivamente publicada; o relatório de execução terminal é comunicado no PR #41, sem inventar resultados futuros. O checkout do agente-08 não receberá arquivos alterados.

**Escopo autorizado de commit:** somente docs/cvl2/research/AGENTE-07. Nenhum original em results/spec, contracts, reports, resources, csv canônico ou derived results/cvl2 foi modificado.

**Sem promoção:** 50 DOCUMENTED_CANDIDATE, 106 UNRESOLVED_CANDIDATE; 0 COMPILE_OK, 0 SEMANTIC_PROVEN, 0 MIGRATED_COMPLETE. Não fazer merge nem aprovação de Fase 2 sem gate humano.

AGENTE-07 — RODADA 5 — QUALIDADE CVL2
