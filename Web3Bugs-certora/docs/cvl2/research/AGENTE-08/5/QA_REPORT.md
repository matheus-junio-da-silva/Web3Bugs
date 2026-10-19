# AGENTE-08 — QA_REPORT — Project 5 (AAVE StarkNet Bridge)

## Base e reconciliação
- Base GitHub/main conferida em 2026-10-19: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PropertyGPT/main conferida: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Inventário do índice: 17 chaves distintas (Project ID, Status original, Example ID); 0 complete, 17 incomplete.
- `properties.csv`: 17 linhas de dados; `properties/`: 17 dossiês individuais com caminhos idênticos aos campos `property_report_path`. Sem IDs duplicados e sem caminhos faltantes na verificação GitHub-only.
- `results/spec/spec_buglabel.csv`: 17 relações histórico-label para 17 exemplos únicos, preservadas sem reclassificação.
- Result original: 6 VERIFIED, 4 VIOLATED, 7 NOT_STATED; Detection Outcome: 6 NO_FINDING, 3 FINDING, 1 ACCEPTED_BEHAVIOR, 7 NOT_STATED.
- Fonte e relatório: Three original specs with active rules/invariants (bridge.spec 13, setup.spec 2, bridgeConstIndex.spec 2); erc20.spec declares methods but no active rules. PDF under resources/5.

## Checagens de documentação efetivamente executadas
1. **PASS estrutural (não-compilatório).** Leitura autenticada do índice CSV e árvore GitHub do commit da branch; parsing CSV com escape e quotes, chave canônica, contagem de arquivos `.md`, comparação de `property_report_path`, unicidade de entradas, conferência contra diretórios originais `.spec` já enumerados por Contents API. Zero ausências observadas.
2. **PASS escopo de alterações (conector GitHub).** Comparação `2a03637b...` → HEAD de pesquisa em andamento: somente caminhos sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-08/`; zero alterações em fontes, specs, scripts, contratos, PDFs ou dataset histórico.
3. **Evidência documental parcial.** Guia Certora A1 e detailed changes lidos em 2026-10-19; sources e commits upstream identificados em evidence_register.csv. Ausência de reproduções em ambiente Prover não permite confirmar compatibilidade CVL2.

## Limitações e validações não executadas
- **NÃO EXECUTADO:** `python scripts/check_specs.py .`; `python scripts/check_contests_csv.py .`; `python scripts/check_contracts.py .`; `git diff --check` contra checkout da HEAD da branch. O computador Remote Desktop autorizado estava offline; a análise utilizou exclusivamente o conector GitHub para o branch remoto. Não há stdout/stderr nem exit code destes comandos, e a conferência estrutural acima NÃO os substitui.
- **NÃO EXECUTADO:** nenhum compilador Solidity/CVL1/CVL2, `certoraRun`, Prover, teste CVL1, replay ou teste de equivalência semântica.
- **NÃO DEMONSTRADO:** fechamento recursivo da reconstrução histórica em todo ambiente original; os blobs e nomes recuperados isoladamente não provam cena de execução idêntica.

## Bloqueios específicos e decisões para revisão
- Missing BridgeHarness/BridgeL2Harness/erc20.spec and mocks in PropertyGPT snapshot; exact files in pinned upstream. Supplied Bridge.sol is newer than report version. Preserve contract links, ray arithmetic, L2 mocks, method summaries, solc8.10, optimistic_loop and --loop_iter 3.
- Confirmar individualmente cada diagnóstico do dossiê antes de produzir derivado CVL2. Rejeitar qualquer summary, cast require_, target sintético ou flexibilização de asserts que altere comportamento observável.
- A classificação da pasta candidata `DOCUMENTED_CANDIDATE` não constitui promoção a `01_documented` nem prova de compilação.
- **Recuperação parcial verificada:** commits e blobs de erc20.spec, BridgeHarness e mocks foram localizados; falta full import closure, contrato munged, remappings, solc e configuração de Prover. Nenhum arquivo foi copiado para histórico.

## Critério de aceite do PR documental
Submeter como **DRAFT**, sem merge automático. A revisão independente deve avaliar estes bloqueios e executar validadores reais em um checkout autorizado antes de declarar a pesquisa pronta; Fase 2 exige instrução separada.
