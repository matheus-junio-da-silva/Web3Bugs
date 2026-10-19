# QA AGENTE-04 / Project 12

- SHA Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, Project PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Inventário do CSV: 26 linhas, 26 chaves exclusivas, **17 complete e 9 incomplete**.
- 26 arquivos .spec lidos individualmente no GitHub; 9 N.txt diagnósticos lidos e vinculados; 26 dossiês e índice `properties.csv` reconciliados via chaves. Os Git blobs armazenados são hashes da extração, não hashes SHA256 dos arquivos upstream auditados.
- Evidências: 38 registros A1/C2; recovery manifest 9 entries, zero reconstruções confirmadas.
- N.md e PDF original não foram auditados página a página neste lote; o relatório catalogado é insumo secundário. Não foram identificados arquivos .conf completos para execução histórica.
- QA realizado: CSV parser com aspas, unicidade de chaves, contagem e existência .spec/N.txt via GitHub. NÃO executados scripts de check specs, `git diff --check`, CVL1, CVL2, Prover, solc, nem teste de equivalência.
- Limites: versões Solidity e CLI exatas; checagem upstream do commit, config, casts e prova de não vacuidade — revisão independente ainda requerida.

**Todos os buckets são provisórios.**
