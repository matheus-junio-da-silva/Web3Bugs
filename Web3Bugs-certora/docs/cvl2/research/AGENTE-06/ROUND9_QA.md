# AGENTE-06 — ROUND9_QA / proveniência dos comandos e controle de integridade

**PR #38 Draft**, branch research/cvl2-agente-06, HEAD de partida 6da9aac35f73a6b0a792807ee6000b7e8b7f077f. Worktree isolado criado em /home/mat/agente06-round9-20261020 sem reset/rebase de branch de colega, base de comparação main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3.

## Antes de qualquer scratch

- WSL DESKTOP-5E26TVU reconfirmado online. Comandos read-only realmente executados: pwd, date -u, python3 --version (3.14.4), git --version (2.53.0), df -h (/dev/sdd com espaço disponível), git status e git rev-parse da worktree preexistente. Nenhum SIGBUS, EIO ou EROFS foi observado nesta sessão.
- Criado novo worktree detached exclusivamente próprio a partir do commit R8. Não houve escrita nos originals sob results/spec, contracts, reports, resources, Bug Labels, nem uso de .env ou token de autenticação.
- Lidos quatro documentos do catálogo e exemplos P1 antes de qualquer commit, e a revisão mais recente do coordenador, PRs #38/#48/#41.

## Integridade do catálogo e matriz

Programa local /tmp/ag06-r9-build.py realmente executado: leitura ROUND8_MATRIX_159.csv e results/spec/spec_buglabel.csv; para cada chave (project_id, original_status, example_id), conferiu Property, Target Contract, Result, Detection Outcome, Original Spec/Lines e todos os Bug Labels. Abertura dos 159 arquivos N.spec originais; SHA256 recalculado e confrontado com SHA anterior. Para cada N.spec, executou git show BASE:Web3Bugs-certora/results/spec/... e verificou igualdade de bytes. **159/159 chaves distintas, zero divergências, P1=70, P4=27, P17=41, P22=21, 159 matches SHA256, 159 matches byte com BASE**. SHA256 do CSV R9: 2b0568adacea2cfbdb611b74680ccdabd5510ea2112765ec47357b7b19e352e4. As três chaves com Bug Labels múltiplos foram preservadas: P1 complete/1, P1 complete/26, P4 incomplete/4.

## Diagnósticos realmente executados (não-Certora)

**Sete invocações Solidity solc-js**, em ordem da investigação: (1) P4 harness combo 0.8.17 EXIT0; (2) P22 FullMath+PoolActions conjunto 0.7.6 EXIT1 devido a PoolActions; (3) P22 FullMath isolado EXIT0; (4) P22 PoolActions isolado EXIT1; (5) P4 harness combo replay EXIT0; (6) P22 PoolActions replay EXIT1; (7) P22 FullMath replay EXIT0. Há **quatro cenários de entrada distintos**, não sete properties compiladas; replays não devem contar como novos resultados. O wrapper Python /tmp/ag06-r9-capture.py capturou stdout, stderr, exit code e resultado JSON dos três replays em [ROUND9_COMPILATION_DIAGNOSTIC_LOG.json](ROUND9_COMPILATION_DIAGNOSTIC_LOG.json), SHA256 0598f24603b784135852284c2b9b74d095996f1d63ed1a6de22f11441e3902cb. Timeouts de 60s por processo. Não se executou certoraRun. Os dois TypeErrors de PoolActions são **SOLIDITY errors**, não CVL2 errors.

Resultados preservados:
- [P4_ABI_RESULT](ROUND9_P4_ABI_RESULT.json): input/file hashes, solc0.8.17, 29 import units, 112 entradas ABI e 87 selectors do target, 0 erros, 8 warnings, EXIT0. Sem job ABI histórico atestado.
- [P22_FULLMATH_ABI](ROUND9_P22_FULLMATH_ABI.json): solc0.7.6, 2 import units, dois selectors, 0 erros, 7 warnings, EXIT0.
- [P22_POOL_ERRORS](ROUND9_P22_POOL_ERRORS.json): solc0.7.6, 17 import units, duas mensagens completas, EXIT1. Nunca publicado ABI inventado para PoolActionsWrapper.
- [P4_SOURCE_MANIFEST](ROUND9_P4_SOURCE_MANIFEST.json) e [P22_SOURCE_MANIFEST](ROUND9_P22_SOURCE_MANIFEST.json): bytes e SHA dos inputs; scratch somente /tmp.

**Importante:** nenhum diagnóstico corresponde a um único N.spec formal compilado. O universo de CVL2 continua **COMPILE_OK=0, COMPILE_ERROR=0, NOT_RUN=159, SEMANTIC_PROVEN=0, MIGRATED_COMPLETE=0/4**. Não extrapolar o erro Solidity para três erros CVL2 nos exemplos PoolActions.

## Quatro checks oficiais após commit

Os checks requeridos na raiz Web3Bugs-certora são exatamente:
- python3 scripts/check_specs.py .
- python3 scripts/check_contests_csv.py .
- python3 scripts/check_contracts.py .
- no root git: git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD

Os quatro comandos FORAM EXECUTADOS após o primeiro commit documental 4abb8cf2a378a1a550f6b0978ea86357e8b08f4c, todos EXIT 0: check_specs (1386 propriedades e 1390 relações), check_contests_csv, check_contracts e git diff --check BASE...HEAD. A comparação registrou 270 arquivos alterados, todos sob AGENTE-06. [ROUND9_VALIDATION_RESULTS.json](ROUND9_VALIDATION_RESULTS.json) preserva argv, working directory, stdout/stderr, códigos de saída e SHA da HEAD efetivamente validada. Após adicionar este registro haverá um segundo commit; os checks devem ser repetidos sobre a HEAD final e relatados no comentário do PR. Nenhum desses checks prova compilação CVL2 ou equivalência semântica.

## Gate humano / semântica

P4 ABI recompilada deve ser cotejada com a versão do audit, não apenas a fonte disponível. P22 biblioteca PoolActions apresenta erro de compilação Solidity no snapshot sem conserto autorizado. P17 Specify 2019 tem semântica de sinvoke/lastReverted/havoc por verificar; P1 runner de setembro não autentica PDF de junho. PR de pesquisa permanece Draft sem merge, não iniciar Prover/CVL1, conversão em lote ou alteração do dataset histórico.

AGENTE-06 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.
