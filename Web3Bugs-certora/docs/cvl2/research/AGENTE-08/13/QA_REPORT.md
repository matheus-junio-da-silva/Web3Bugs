# AGENTE-08 — QA_REPORT — Project 13 (Notional Finance V2)

## Base e reconciliação
- Base GitHub/main conferida em 2026-10-19: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PropertyGPT/main conferida: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Inventário do índice: 58 chaves distintas (Project ID, Status original, Example ID); 0 complete, 58 incomplete.
- `properties.csv`: 58 linhas de dados; `properties/`: 58 dossiês individuais com caminhos idênticos aos campos `property_report_path`. Sem IDs duplicados e sem caminhos faltantes na verificação GitHub-only.
- `results/spec/spec_buglabel.csv`: 58 relações histórico-label para 58 exemplos únicos, preservadas sem reclassificação.
- Result original: 5 VERIFIED, 53 NOT_STATED; Detection Outcome: 5 NO_FINDING, 53 NOT_STATED.
- Fonte e relatório: 15 specs / 131 original source artifacts preserved; source report PDF in resources/13; original historical scripts reference solc 0.7.5, Brownie packages/OpenZeppelin 3.4.0

## Checagens de documentação efetivamente executadas
1. **PASS estrutural (não-compilatório).** Leitura autenticada do índice CSV e árvore GitHub do commit da branch; parsing CSV com escape e quotes, chave canônica, contagem de arquivos `.md`, comparação de `property_report_path`, unicidade de entradas, conferência contra diretórios originais `.spec` já enumerados por Contents API. Zero ausências observadas.
2. **PASS escopo de alterações (conector GitHub).** Comparação `2a03637b...` → HEAD de pesquisa em andamento: somente caminhos sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-08/`; zero alterações em fontes, specs, scripts, contratos, PDFs ou dataset histórico.
3. **Evidência documental parcial.** Guia Certora A1 e detailed changes lidos em 2026-10-19; sources e commits upstream identificados em evidence_register.csv. Ausência de reproduções em ambiente Prover não permite confirmar compatibilidade CVL2.

## Limitações e validações não executadas
- RETIFICADO em 2026-10-19: os validadores check_specs.py, check_contests_csv.py, check_contracts.py e git diff --check foram executados em WSL worktree isolado e passaram após completar sparse checkout; consultar VALIDATION_LOG_2026-10-19.md.
- **NÃO EXECUTADO:** nenhum compilador Solidity/CVL1/CVL2, `certoraRun`, Prover, teste CVL1, replay ou teste de equivalência semântica.
- **NÃO DEMONSTRADO:** fechamento recursivo da reconstrução histórica em todo ambiente original; os blobs e nomes recuperados isoladamente não provam cena de execução idêntica.

## Bloqueios específicos e decisões para revisão
- 48 instances with concrete or inferred target but missing transitive imports; 10 draft Balances.spec declarations lack historically evidenced verification ABI; settlementRatesAreNeverReset has conflicting branch; sanity rules are diagnostics.
- Confirmar individualmente cada diagnóstico do dossiê antes de produzir derivado CVL2. Rejeitar qualquer summary, cast require_, target sintético ou flexibilização de asserts que altere comportamento observável.
- A classificação da pasta candidata `DOCUMENTED_CANDIDATE` não constitui promoção a `01_documented` nem prova de compilação.
- **DIVERGÊNCIA DOCUMENTAL CONCRETA:** `docs/spec_catalog_project_13.md` ainda relata 7 VERIFIED/51 NOT_STATED. Porém o `spec_buglabel.csv` na HEAD atual marca exemplos #32 e #34 como NOT_STATED: são **5 VERIFIED/53 NOT_STATED** no índice vigente. Este relatório segue a fonte canônica CSV e não modifica a documentação histórica. Coordenador deve adjudicar/atualizar somente em tarefa separada.

## Critério de aceite do PR documental
Submeter como **DRAFT**, sem merge automático. A revisão independente deve avaliar estes bloqueios e executar validadores reais em um checkout autorizado antes de declarar a pesquisa pronta; Fase 2 exige instrução separada.

<!-- AGENTE08-R2 -->
## Contrarrevisão P13: targets, imports e 7 versus 5 VERIFIED
O verify.sh original fixa solc7.5, @openzeppelin remapeado para Brownie OpenZeppelin/openzeppelin-contracts@3.4.0-solc-0.7, compound-finance como pacote Brownie e interfaces da árvore histórica. Fonte de destino e checksum das dependências carregadas pelo antigo auditor permanecem indisponíveis. scripts/applyHarness.sh altera Constants.sol de internal constant para public constant, afetando observabilidade do target.
As 48 regras com target definido/inferido dependem de imports transitivos ausentes; os dez exemplos #8-17 de Balances.spec não têm ABI histórica selecionada nos scripts. O PDF original Notional1Nov2021.pdf (páginas 13-16) contém indicadores de provas: docs/spec_catalog_project_13.md menciona sete regras VERIFIED, mas o CSV atual registra #32/#34 NOT_STATED e consequentemente cinco VERIFIED. Esta divergência permanece documentada, sem corrigir silenciosamente o catálogo. #1/#58 são diagnósticos, #7/#57 tautologias, #39 contém um ramo contraditório.

<!-- ROUND2-HISTORIC-DECISION -->
## Fechamento documental apos segunda auditoria (2026-10-19)

- Estado de implementacao: 58/58 UNRESOLVED_CANDIDATE. Preservado apos a segunda revisao, sem promover ou executar.
- [HISTORICAL_BLOCKERS.md](HISTORICAL_BLOCKERS.md): evidencias, itens potencialmente recuperaveis, blockers e decisoes humanas.
- [historical_status.csv](historical_status.csv): adjudicacao explicita por exemplo e Result/Detection Outcome historicos.
- [RECOVERY_SEARCH_LOG.md](RECOVERY_SEARCH_LOG.md): escopo, consultas e resultados das buscas; ausencia de resultados nao significa impossibilidade.
- A versao historica das regras, asserts/assumes, methods universe, harness e compatibilidade CVL2 nao foi modificada. Nao executar Prover sem autorizacao.
