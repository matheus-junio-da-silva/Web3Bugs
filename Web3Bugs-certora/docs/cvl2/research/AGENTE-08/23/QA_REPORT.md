# AGENTE-08 — QA_REPORT — Project 23 (Radicle Drips)

## Base e reconciliação
- Base GitHub/main conferida em 2026-10-19: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PropertyGPT/main conferida: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Inventário do índice: 46 chaves distintas (Project ID, Status original, Example ID); 0 complete, 46 incomplete.
- `properties.csv`: 46 linhas de dados; `properties/`: 46 dossiês individuais com caminhos idênticos aos campos `property_report_path`. Sem IDs duplicados e sem caminhos faltantes na verificação GitHub-only.
- `results/spec/spec_buglabel.csv`: 46 relações histórico-label para 46 exemplos únicos, preservadas sem reclassificação.
- Result original: 15 VERIFIED, 1 VIOLATED, 30 NOT_STATED; Detection Outcome: 15 NO_FINDING, 1 FINDING, 1 INCONCLUSIVE, 29 NOT_STATED.
- Fonte e relatório: Six active CVL spec files: DripsHub, DripsHubBackup, Reserve, SlotTester, Splits and Splits2. Original PDF under resources/23 and report transcript reports/23.md.

## Checagens de documentação efetivamente executadas
1. **PASS estrutural (não-compilatório).** Leitura autenticada do índice CSV e árvore GitHub do commit da branch; parsing CSV com escape e quotes, chave canônica, contagem de arquivos `.md`, comparação de `property_report_path`, unicidade de entradas, conferência contra diretórios originais `.spec` já enumerados por Contents API. Zero ausências observadas.
2. **PASS escopo de alterações (conector GitHub).** Comparação `2a03637b...` → HEAD de pesquisa em andamento: somente caminhos sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-08/`; zero alterações em fontes, specs, scripts, contratos, PDFs ou dataset histórico.
3. **Evidência documental parcial.** Guia Certora A1 e detailed changes lidos em 2026-10-19; sources e commits upstream identificados em evidence_register.csv. Ausência de reproduções em ambiente Prover não permite confirmar compatibilidade CVL2.

## Limitações e validações não executadas
- **NÃO EXECUTADO:** `python scripts/check_specs.py .`; `python scripts/check_contests_csv.py .`; `python scripts/check_contracts.py .`; `git diff --check` contra checkout da HEAD da branch. O computador Remote Desktop autorizado estava offline; a análise utilizou exclusivamente o conector GitHub para o branch remoto. Não há stdout/stderr nem exit code destes comandos, e a conferência estrutural acima NÃO os substitui.
- **NÃO EXECUTADO:** nenhum compilador Solidity/CVL1/CVL2, `certoraRun`, Prover, teste CVL1, replay ou teste de equivalência semântica.
- **NÃO DEMONSTRADO:** fechamento recursivo da reconstrução histórica em todo ambiente original; os blobs e nomes recuperados isoladamente não provam cena de execução idêntica.

## Bloqueios específicos e decisões para revisão
- Historical source tree omits generated CVT internal calls and DripsHubHarness/ReserveHarness/SlotTester targets. PDF result covers named Splits.sol properties, not Splits2 or other contracts; #36 historical rounding failure, #38 timeout.
- Confirmar individualmente cada diagnóstico do dossiê antes de produzir derivado CVL2. Rejeitar qualquer summary, cast require_, target sintético ou flexibilização de asserts que altere comportamento observável.
- A classificação da pasta candidata `DOCUMENTED_CANDIDATE` não constitui promoção a `01_documented` nem prova de compilação.
- **Risco histórico:** #36 VIOLATED/FINDING por rounding; #38 NOT_STATED/INCONCLUSIVE por timeout; #39–41 têm VERIFIED somente no escopo Splits.spec. Não extrapolar a Splits2.

## Critério de aceite do PR documental
Submeter como **DRAFT**, sem merge automático. A revisão independente deve avaliar estes bloqueios e executar validadores reais em um checkout autorizado antes de declarar a pesquisa pronta; Fase 2 exige instrução separada.
