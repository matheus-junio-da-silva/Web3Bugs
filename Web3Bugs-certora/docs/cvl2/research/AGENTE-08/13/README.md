# AGENTE-08 — Fase 1 / Pesquisa pré-migração CVL2 — Project 13: Notional Finance V2

**Status:** pesquisa documental provisória, sem implementação, sem execução da Certora CLI, sem compilação CVL2 e sem Prover.

## Identidade, baseline e escopo
- Project ID 13; origem PropertyGPT `certora_projects/notional_finance_v2/`; catálogo GitHub `Web3Bugs-certora/`.
- Input baseline Web3Bugs/main: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PropertyGPT/main observado e confirmado: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Exatamente **58** instâncias canônicas: 0 original_status=complete; 58 original_status=incomplete; múltiplas labels não criam novos exemplos.
- Index source: `results/spec/spec_buglabel.csv` no baseline; Snapshot CSV 58 unique and 58 label rows. 58 N.spec, 58 N.sol, 58 N.md, 58 N.txt.
- Result histórico: **5 VERIFIED, 53 NOT_STATED**. Detection Outcome histórico: **5 NO_FINDING, 53 NOT_STATED**. Nenhum significa verificação nova.
- Histórico/pinned audited SHA: NOT_CONFIRMED; original PDF describes 2021 verification, without a source SHA independently pinned here.
- Material de origem: 15 specs / 131 original source artifacts preserved; source report PDF in resources/13; original historical scripts reference solc 0.7.5, Brownie packages/OpenZeppelin 3.4.0

## Riscos e reconstrução histórica
48 instances with concrete or inferred target but missing transitive imports; 10 draft Balances.spec declarations lack historically evidenced verification ABI; settlementRatesAreNeverReset has conflicting branch; sanity rules are diagnostics.

- Estágio de decisão documental: 58 UNRESOLVED_CANDIDATE.
- Proveniência e recuperação: 6 registered sources; recovery manifest lists six distinct missing-source or target families; list is not an exhaustive lockfile.

## Conteúdo desta pasta
- `properties.csv`: uma entrada por exemplo original, sem duplicação de Bug Labels; independe do status futuro da reconstrução.
- `properties/incomplete/N.md`: uma análise fonte-específica para cada exemplo, com fórmulas/guards visíveis, source blob, N.txt se incompleto, cenários de contraexemplo e planos provisórios.
- `patterns/migration_decisions.md`: padrões e casos semânticos críticos; não substitui decisão por exemplo.
- `evidence_register.csv`: evidências A1/A2/B1 verificadas ou consultadas, com URL e cautelas.
- `recovery_manifest.csv`: dependências históricas candidatas/ausentes, sua prova disponível e estado; não modifica o snapshot.
- `QA_REPORT.md`: cobertura, divergências, verificações estruturais executadas, validações NÃO executadas e encaminhamento.

## Regras rígidas de preservação
Fontes originais `.spec`, Solidity, PDFs, configs, CSVs do catálogo e contracts/ históricos permanecem intactos. Trechos `N.sol` são documentos, não alvos compiláveis. Não executar o script de migração in-place em contratos históricos. Compilar futuramente um arquivo sem prova de mesma ABI, overrides, receiver, assumptions e paths de revert não demonstra equivalência.

**Próxima etapa apenas com autorização expressa do coordenador:** revisar origin/harness/prova de import closure, selecionar alterações textuais mínimas documentadas, construir derivados separados e só então executar compilação e provas.

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
