# QA AGENTE-01 — Revisão independente P10

- Base Web3Bugs 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; upstream auditado c90dec1046e5e26edf70f985dd86381403912482.
- 266 N.spec, 266 N.sol, 266 N.md e 264 N.txt lidos integralmente e vinculados por ID, property, target e blob no individual_source_audit.csv.
- 264 incomplete + 2 complete; 266 dossiês atualizados. Páginas 26–31 de resources/10/FurucomboMay2021.pdf lidas diretamente de seus streams e mapeamento ToUnicode; 23 células None por página, 138 pares, registrados sem individual VERIFIED.
- 22 fontes Solidity distintas do catálogo divergentes do commit auditado; target_revision_matrix.csv registra cada comparação e import closure do target root. A closure completa dos demais seeds e o ABI post-Perl permanecem NÃO comprovados.
- Código fonte não alterado. Nenhum script histórico de transformação, Solidity compilation, CVL1, CVL2 ou Prover foi executado.
- Para métodos com overload/multiline, posição e candidato são esqueleto textual, exigindo reconciliação manual; nenhuma visibilidade external/internal ou receiver declarada equivalente sem ABI.
- Comandos de validação e exit codes serão acrescentados abaixo somente após execução real.

## Recovery update: official OpenZeppelin 3.3.0 tag
- 28 target rows, 6 unique tagged OpenZeppelin Solidity imports reachable from all documented 2021 script seeds, hashes recorded in recovery_manifest.csv.
- Only a documentary source recovery; exact npm tarball/Perl-transformed ABI/Prover not reconstructed.

## Execução real dos checks não-Prover

- cwd `/home/mat/cvl2-agent01-isolated/Web3Bugs/Web3Bugs-certora`:
  - `python3 scripts/check_specs.py .` — exit code **0**; log `/home/mat/cvl2-agent01-isolated/qa_logs/check_specs.log`; últimas linhas: Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
  - `python3 scripts/check_contracts.py .` — exit code **0**; log `/home/mat/cvl2-agent01-isolated/qa_logs/check_contracts.log`; últimas linhas: Check passed! /  / 	'./contracts' is consistant with './reports'
  - `python3 scripts/check_contests_csv.py .` — exit code **0**; log `/home/mat/cvl2-agent01-isolated/qa_logs/check_contests_csv.log`; últimas linhas: Check passed! /  / 	'./results/contests.csv' is consistant with './reports'
- cwd `/home/mat/cvl2-agent01-isolated/Web3Bugs`: `git diff --check` — exit code **0** após normalização de CSV CRLF e espaços à direita nos documentos desta pasta; log `/home/mat/cvl2-agent01-isolated/qa_logs/git_diff_check_final.log` (arquivo vazio).
- Checkout dedicado: `/home/mat/cvl2-agent01-isolated/Web3Bugs`, branch `research/cvl2-agente-01`; status original preservado e outros agentes não impactados.
- Reconciliação: 28 targets nomeados, 20 caminhos Solidity distintos; 28 targets com diferenças de SHA.
- cwd `/home/mat/cvl2-agent01-isolated/Web3Bugs`: `git diff --cached --check` (incluindo 277 arquivos staged, todos na pasta autorizada) — exit code **0**, log `/home/mat/cvl2-agent01-isolated/qa_logs/git_diff_cached_check.log` vazio. Nenhum Prover ou compilador executado.

## Segunda revisão independente — proveniência e condições de mudança (19/10/2026)
- Revisão lida: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39#pullrequestreview-5577009787
- Exatos 266 pares status/ID mantidos, 2 complete e 264 incomplete. Original historical files não alterados.
- semantic_candidate_gate_matrix.csv: 988 ocorrências textuais, não 988 propriedades/compilações. Cada linha inclui o N.spec/linha, original, candidata quando fundamentada, classificação REQUIRED/BLOCKED/PRESERVE/NO_CAST, source evidence e risco.
- perl_getter_scope_matrix.csv: 28 contextos de target; comparação do Perl auditado e do snapshot. A aplicação literal de injeção está documentada separadamente de ABI efetivamente compilada.
- Exemplo complete/33: 2 methods do target external justificados por specs/harnesses/LibParamHarness.sol:10 e :14. LibParamHarness usa specs/scripts/libParam.sh sem Perl de handlers. O selector getParams requer sig, sem mudar o ramo com duas assumptions.
- Exemplo complete/34: preserve N.spec:9 require false, que exclui selector getParams. N.spec:13 assert !lastReverted é booleano; alerta de cast genérico removido. N.spec:34 não inclui methods block próprio.
- Busca negativa no checkout do commit auditado: find *.abi, *.bin, *certora*.json, *certora*.conf, *certora*.log, package-lock.json, yarn.lock, além de git ls-tree e grep nos scripts; nenhum ABI/bin/lock de tais nomes, porém scripts certoraRun/--verify/--settings localizados. Resultado documentado em patterns/PAT-08-independent-second-review.md; log de execução do WSL em /home/mat/cvl2-agent01-isolated/qa_logs/negative_historical_search.log.
- Não executado: Perl, solc, CLI CVL1/CVL2, Prover, teste de equivalência. Source ABI parcial de complete/33 e 34 recuperada; demais ABI post-Perl e receivers são bloqueios, não condições automaticamente satisfeitas.

### Checks desta segunda rodada — execução real e logs
- WSL device DESKTOP-5E26TVU, working tree isolado /home/mat/cvl2-agent01-isolated/Web3Bugs, subdiretório Web3Bugs-certora.
- python3 scripts/check_specs.py . — exit 0; log /home/mat/cvl2-agent01-isolated/qa_logs/second_round/check_specs.log (1.386 exemplos e 1.390 relações).
- python3 scripts/check_contracts.py . — exit 0; log /home/mat/cvl2-agent01-isolated/qa_logs/second_round/check_contracts.log.
- python3 scripts/check_contests_csv.py . — exit 0; log /home/mat/cvl2-agent01-isolated/qa_logs/second_round/check_contests_csv.log.
- git diff --cached --check — exit 0 após normalização de whitespace apenas nos documentos; log /home/mat/cvl2-agent01-isolated/qa_logs/second_round/staged_diff_check_final.log, vazio.
- git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 — exit 0 antes do commit; log /home/mat/cvl2-agent01-isolated/qa_logs/second_round/full_base_diff_check.log.
- Status final dos três validadores será novamente verificado após o commit. Comparação baseline...HEAD integral a ser executada e registrada antes do retorno à revisão.
