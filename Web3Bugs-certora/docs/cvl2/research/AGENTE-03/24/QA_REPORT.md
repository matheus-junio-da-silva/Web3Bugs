# QA_REPORT — AGENTE-03 / Project 24

## Reconciliação verificável
- Web3Bugs main: 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; PropertyGPT main: 687f654c679ed45ab127b7949e2a29c8f5e491b9. Ambos equivalem aos HEADs fornecidos.
- 164 linhas do spec_buglabel.csv para Project ID 24, exatamente 164 chaves canônicas (24,incomplete,id).
- Evidence matrix: 164 linhas; nome e id cruzados por correspondência estrita com index principal.
- GitHub contents API: 657 entradas em incomplete/24, sendo 164 .spec, 164 .txt, 164 .md, 164 .sol e .gitattributes.
- 8 specs originais consultadas com blob SHA-1; JSON das declarações CVL originais decodificado individualmente para 164 dossiês.
- 164 relatórios de propriedade gerados; 164 linhas de properties.csv; 164 candidatos não resolvidos.
- Risco textual: MEDIUM=115, HIGH=49. Padrões: P01=164, P02=164, P03=164, P09=164, P04=75, P06=29, P05=27, P10=3, P08=5, P07=20.
- 10 arquivos de patterns; 17 fontes documentais; 5 grupos de dependências ausentes.

## Evidência positiva e negativas
- Source histórica das oito specs verificada via GitHub; 164 regras CVL individuais da matriz, com fórmulas de falha hipotéticas, não contraexemplos reais.
- Árvore da revisão upstream ef2ef302 com 94 entradas, sem spec/harness Certora ou .conf; auditar dependências em commit diferente não as recupera.
- Relatório correto Certora, audit SHA ef2ef302, e atribuições retracted vs snapshot; comparação histórica LaunchEvent/Staking distinta.
- Casos críticos: 2/5/7/147/150 fonte vs PDF, 12/13/152/154 quantificação-vacuity, 163 require vs assert, 164 reachability.

## Controle de escopo e validações
- Validações **efetuadas por leitura/gerador em memória**: IDs, campos de origem, contagem dos arquivos no GitHub, existência de sha .spec/.sol/.md/.txt por ID, JSON decoding, enum original.
- Validações **não efetuadas**: scripts Python do repositório, git diff --check local, PDF página a página, execução CVL1, CVL2, solc, Certora Prover, análise dinâmica de satisfatibilidade, teste de equivalência.
- Estrutura versionada neste PR restringe-se a docs/cvl2/research/AGENTE-03/24/. Nunca alterou contracts/24, resources/24, results/spec/24 nem scripts.

## Gate para o coordenador
- NÃO promover 164 casos a unchanged/documented/indirect sem Fase 2 expressa.
- Pesquisa adicional permitida: localizar helper histórico com path, commit, blob, licença; restaurar symbolic harness/ABI/config provados; resolver SHA e diferenças de Solidity.
- PR deve permanecer draft, sem merge até revisão independente.
