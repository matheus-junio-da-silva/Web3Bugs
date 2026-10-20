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

## Quarta rodada — triagem documental e cross-audit (2026-10-20)

- Checkout: `/home/mat/cvl2-agent01-isolated/Web3Bugs`, branch exclusiva `research/cvl2-agente-01`, entrada `763f3f38d28f1b37a4686c812e2bfc6699bbc35a`.
- Relatório detalhado: `ROUND4_FINDINGS.md`. Matriz com **266 linhas**: `round4_progress_matrix.csv`, contendo identificação, URLs/commits/blobs, dependências, métodos, status de compilação `NOT_RUN_COORDINATOR_GATE_REQUIRED`, risco, bloqueio e próxima ação.
- Leitura automatizada de 1.062 artefatos originais e reconciliação de hashes Git do corpus: **266 .spec, 266 .sol, 266 .md, 264 .txt**, todos iguais ao `individual_source_audit.csv`. Não confundir esse check de integridade com revisão humana individual completa nesta rodada.
- `semantic_candidate_gate_matrix.csv`: 988 ocorrências iniciais validadas contra textos/linhas originais; **14** `sig:` falsamente ativos dentro do comentário multilinha de `incomplete/11` e `/12` reclassificados; **cinco** chamadas legadas (quatro `invoke`, uma `sinvoke`) incluídas com gates, totalizando **993 registros**. Entrada `source_evidence` da sintaxe `sig:` em targets diversos deixa de usar o LibParamHarness como prova do método do target errado.
- Fonte: `dinngo/furucombo-contract@c90dec1046e5e26edf70f985dd86381403912482`; `OpenZeppelin/openzeppelin-contracts@6be5ffe54fc8982b7c1d0f45d4cb7bbd313107cd` (tag v3.3.0, **não** prova pacote/ABI).
- Triagem de compilação: só `complete/33–34` apresentam source/target/runner auditados e nenhum Perl para o target; contudo **nenhum gate individual autorizou spec derivada, mesmo temporária**. Todos os 266 marcados **NOT_RUN**. Nenhum Prover, CVL1, solc, Perl, CVL2 ou `--compilation_steps_only` executado; nenhum log de compilação existe.
- Revisão cruzada read-only `PR #37`: `PR37_READONLY_AUDIT.md`; em checkout distinto, HEAD `3da04efedfe6d75b049b15fa37a040572260eca4`; 181 chaves, 339 observações ABI, 16 comparações source, dados sem divergências e diff commitado EXIT 0; sem alteração na branch do AGENTE-02.
- **Validação final do commit da Rodada 4:** saída de logs locais `/home/mat/cvl2-agent01-isolated/qa_logs/round4/` e HEAD/exit codes comunicados no PR após o commit. Nunca tratar `git diff --cached --check` como verificação de BASE...HEAD.

## Quinta rodada — 2026-10-20 / qualidade CVL2

- Política consultada antes da escrita: spec_catalog.md, spec_catalog_workflow.md, spec_catalog_project_1.md e standard.md; documentação Certora CVL2 migration/changes; PR #39 mais recente e painel de coordenação PR #47. Baseline e fontes históricas no ROUND5_EVIDENCE.md.
- Fonte cena: commit 2021 Furucombo c90dec1046e5e26edf70f985dd86381403912482. LibParamHarness -> LibParam, dois Solidity em closure, zero imports OZ. sha1(blob) e sha256 copiados na round5/source_manifest.csv. Compilador oficial Solidity 0.6.12 verificado por digest f6cb519b01dabc61cab4c184a3db11aa591d18151e362fcae850e42cffdfb09a.
- EXECUTADO: certora-cli 8.19.0, certoraRun --compilation_steps_only, timeout 85s, cópias CVL originais completas 33 e 34 separadas, sem patch. Dois EXIT 1, erros literais de CVL1 no parser; logs completos e checksums em round5/logs e round5/diagnostics.csv. Não executado: CVL1, Prover, migration script, Perl, patches, scene derivada ou reexecução de resultados históricos.
- EXECUTADO: parser de comentários em 266 arquivos N.spec; 13 seletores tipados ativos, 15 comentados; 1 extra no N.spec incomplete/23 corrigido nesta rodada, além dos 14 da Rodada 4. Sem alterar source.
- Round5_progress_matrix.csv: 266 chaves, 2 testados com erro, 264 não executados, 0 COMPILE_OK, 0 SEMANTIC_PROVEN, 0 MIGRATED_COMPLETE. P1 29, P2 234 (164 Perl e 70 sem wrapper Perl), P3 1, P0 2.
- Auditoria cruzada read-only do PR #37 HEAD 2c32e08521a1a709cad9f86f4c9d2c7cb0954251: complete/3,5,23,46,53 no AGENTE-02; ver PR37_FIVE_CANDIDATES.md e round5/pr37_five_candidate_audit.csv. Nada na branch do AGENTE-02 modificado.
- Comandos de QA estrutural e git diff --check registrados no comentário de entrega com HEAD/exit codes executados após commit/push. Não registrar saída futura como se tivesse rodado agora.

- Integridade dos logs: arquivos .log legíveis sem linhas vazias terminais e cópias originais exatas em .log.b64; conferir colunas raw_log_sha256/readable_log_sha256 no round5/diagnostics.csv. Ajuste motivado exclusivamente pelo diff --check.
