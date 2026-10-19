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
