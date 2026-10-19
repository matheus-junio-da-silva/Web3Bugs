# AGENTE-08 — QA_REPORT — Project 14 (Opyn Gamma Protocol)

## Base e reconciliação
- Base GitHub/main conferida em 2026-10-19: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PropertyGPT/main conferida: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Inventário do índice: 34 chaves distintas (Project ID, Status original, Example ID); 34 complete, 0 incomplete.
- `properties.csv`: 34 linhas de dados; `properties/`: 34 dossiês individuais com caminhos idênticos aos campos `property_report_path`. Sem IDs duplicados e sem caminhos faltantes na verificação GitHub-only.
- `results/spec/spec_buglabel.csv`: 34 relações histórico-label para 34 exemplos únicos, preservadas sem reclassificação.
- Result original: 19 VERIFIED, 15 NOT_STATED; Detection Outcome: 12 NO_FINDING, 7 FINDING, 15 NOT_STATED.
- Fonte e relatório: Six top-level original spec files; 34 source-rule/target instances. Historical run scripts use ControllerHarness, ControllerHarnessExtra, MarginVaultHarness and Whitelist; known Controller mutation script.

## Checagens de documentação efetivamente executadas
1. **PASS estrutural (não-compilatório).** Leitura autenticada do índice CSV e árvore GitHub do commit da branch; parsing CSV com escape e quotes, chave canônica, contagem de arquivos `.md`, comparação de `property_report_path`, unicidade de entradas, conferência contra diretórios originais `.spec` já enumerados por Contents API. Zero ausências observadas.
2. **PASS escopo de alterações (conector GitHub).** Comparação `2a03637b...` → HEAD de pesquisa em andamento: somente caminhos sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-08/`; zero alterações em fontes, specs, scripts, contratos, PDFs ou dataset histórico.
3. **Evidência documental parcial.** Guia Certora A1 e detailed changes lidos em 2026-10-19; sources e commits upstream identificados em evidence_register.csv. Ausência de reproduções em ambiente Prover não permite confirmar compatibilidade CVL2.

## Limitações e validações não executadas
- **NÃO EXECUTADO:** `python scripts/check_specs.py .`; `python scripts/check_contests_csv.py .`; `python scripts/check_contracts.py .`; `git diff --check` contra checkout da HEAD da branch. O computador Remote Desktop autorizado estava offline; a análise utilizou exclusivamente o conector GitHub para o branch remoto. Não há stdout/stderr nem exit code destes comandos, e a conferência estrutural acima NÃO os substitui.
- **NÃO EXECUTADO:** nenhum compilador Solidity/CVL1/CVL2, `certoraRun`, Prover, teste CVL1, replay ou teste de equivalência semântica.
- **NÃO DEMONSTRADO:** fechamento recursivo da reconstrução histórica em todo ambiente original; os blobs e nomes recuperados isoladamente não provam cena de execução idêntica.

## Bloqueios específicos e decisões para revisão
- Dependency-complete is a documentation criterion, not a successful CVL2 compile. #1 has selector-ordered assert true branch, #15–19 narrower solvency cases, and scripts apply harness changes. Changes to methods receiver and summaries can alter proof model.
- Confirmar individualmente cada diagnóstico do dossiê antes de produzir derivado CVL2. Rejeitar qualquer summary, cast require_, target sintético ou flexibilização de asserts que altere comportamento observável.
- A classificação da pasta candidata `DOCUMENTED_CANDIDATE` não constitui promoção a `01_documented` nem prova de compilação.
- **Bloqueio semântico:** #1 tem ramo assert true; #19 e #25 permanecem candidatos UNRESOLVED. Preservar scripts que alteram o input Solidity no prover histórico.

## Critério de aceite do PR documental
Submeter como **DRAFT**, sem merge automático. A revisão independente deve avaliar estes bloqueios e executar validadores reais em um checkout autorizado antes de declarar a pesquisa pronta; Fase 2 exige instrução separada.
