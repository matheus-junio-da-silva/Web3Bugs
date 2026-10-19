# QA AGENTE-04 / Project 12

- SHA Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, Project PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Inventário do CSV: 26 linhas, 26 chaves exclusivas, **17 complete e 9 incomplete**.
- 26 arquivos .spec lidos individualmente no GitHub; 9 N.txt diagnósticos lidos e vinculados; 26 dossiês e índice `properties.csv` reconciliados via chaves. Os Git blobs armazenados são hashes da extração, não hashes SHA256 dos arquivos upstream auditados.
- Evidências: 38 registros A1/C2; recovery manifest 9 entries, zero reconstruções confirmadas.
- N.md e PDF original não foram auditados página a página neste lote; o relatório catalogado é insumo secundário. Não foram identificados arquivos .conf completos para execução histórica.
- QA realizado: CSV parser com aspas, unicidade de chaves, contagem e existência .spec/N.txt via GitHub. NÃO executados scripts de check specs, `git diff --check`, CVL1, CVL2, Prover, solc, nem teste de equivalência.
- Limites: versões Solidity e CLI exatas; checagem upstream do commit, config, casts e prova de não vacuidade — revisão independente ainda requerida.

**Todos os buckets são provisórios.**

## Contrarrevisao 2026-10-19
StableDebtToken auditado contem constructor de cinco parametros, mas snapshot tem initialize de sete parametros e getter nao virtual com retorno interface; incompatibilidade de versao nao e defeito CVL2. Nenhum dos nove incomplete recebeu substituicao Solidity.

Dossies atualizados 26/26; entradas methods por instancia 22; nomes literais encontrados em PDF 5. Propostas report-only e condicionais; nao houve compilacao, Prover, teste CVL1 ou modificacao de fonte. Buscas negativas nao demonstram inexistencia fora da arvore examinada.


## Validação estrutural em WSL após contrarrevisão — execução efetiva

A afirmação antiga de que o desktop estava indisponível e de que os validadores não tinham sido executados descreve SOMENTE a primeira entrega; está **superada** pela retomada de 2026-10-19. Device remoto DESKTOP-5E26TVU online; checkout isolado em /tmp/cvl2-agent04-20261019/repo (não interfere nos demais agentes).

Diretório de execução dos três validadores: /tmp/cvl2-agent04-20261019/repo/Web3Bugs-certora
- python3 scripts/check_specs.py . — exit 0; saída: Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . — exit 0; saída: Check passed! results/contests.csv consistent with reports.
- python3 scripts/check_contracts.py . — exit 0; saída: Check passed! contracts consistent with reports.

Diretório de execução Git: /tmp/cvl2-agent04-20261019/repo
- git diff --check — após normalizar exclusivamente docs/cvl2/research/AGENTE-04, exit 0. O diff inicial contra base detectou whitespace nos dossiês originais; foi sanado APENAS em documentos.
- O comando git diff --check origin/main...HEAD falhou com exit 128 por clone --single-branch sem ref origin/main. Não é resultado negativo do dataset. Para comparação final usar explicitamente o commit base 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 e o novo SHA, cujo exit deve ser registrado após publicação.

Nota sobre QA: o uso de 1386/1390 é a contagem da main congelada; os índices adicionais de pesquisa (157 chaves) não alteram o catálogo. Nenhuma execução de certoraRun, solc, CVL1, CVL2 ou Prover. Os status históricos continuam intocados.

## Segunda auditoria do coordenador (2026-10-19)
As observacoes antigas de que N.md e PDF nao haviam sido revisitados refletem a PRIMEIRA etapa: 100% dos N.md desta familia foram lidos na etapa posterior, com SHA256 e contexto em dossies, e todas as paginas PDF extraidas (P15 13; P12 25; P2 6). Estudo de pacote/harness/ABI atualizado no diretorio deste projeto. Os indices distinguem SINTAXE, ABI, DEPENDENCIA e RISCO SEMANTICO para cada propriedade. Nao promover DOCUMENTED a READY.
