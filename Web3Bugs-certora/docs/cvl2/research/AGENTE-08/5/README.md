# AGENTE-08 — Fase 1 / Pesquisa pré-migração CVL2 — Project 5: AAVE StarkNet Bridge

**Status:** pesquisa documental provisória, sem implementação, sem execução da Certora CLI, sem compilação CVL2 e sem Prover.

## Identidade, baseline e escopo
- Project ID 5; origem PropertyGPT `certora_projects/aave_starknet_bridge/`; catálogo GitHub `Web3Bugs-certora/`.
- Input baseline Web3Bugs/main: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PropertyGPT/main observado e confirmado: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Exatamente **17** instâncias canônicas: 0 original_status=complete; 17 original_status=incomplete; múltiplas labels não criam novos exemplos.
- Index source: `results/spec/spec_buglabel.csv` no baseline; Snapshot CSV 17 unique and 17 label rows. 17 N.spec, 17 N.sol, 17 N.md, 17 N.txt.
- Result histórico: **6 VERIFIED, 4 VIOLATED, 7 NOT_STATED**. Detection Outcome histórico: **6 NO_FINDING, 3 FINDING, 1 ACCEPTED_BEHAVIOR, 7 NOT_STATED**. Nenhum significa verificação nova.
- Histórico/pinned audited SHA: 4c010c18b08703e4f367db1e0c642c76c25e551b is a directly inspected 2022-10-19 upstream verification-package commit; no complete reproducible historical prover run.
- Material de origem: Three original specs with active rules/invariants (bridge.spec 13, setup.spec 2, bridgeConstIndex.spec 2); erc20.spec declares methods but no active rules. PDF under resources/5.

## Riscos e reconstrução histórica
Missing BridgeHarness/BridgeL2Harness/erc20.spec and mocks in PropertyGPT snapshot; exact files in pinned upstream. Supplied Bridge.sol is newer than report version. Preserve contract links, ray arithmetic, L2 mocks, method summaries, solc8.10, optimistic_loop and --loop_iter 3.

- Estágio de decisão documental: 17 UNRESOLVED_CANDIDATE.
- Proveniência e recuperação: 8 registered sources and 14 pinned upstream blobs including verification scripts; recovery remains partial until transitive closure/revisions/config are independently checked.

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
## Contrarrevisão P5: scripts, remappings e ABI
No commit 4c010c18b08703e4f367db1e0c642c76c25e551b, erc20.spec blob b12fec167edd76a2f59a64bc80bc33a9eeb04f65 contém somente methods ERC20 DISPATCHER(true). Os getters withdrawMessageStatus/bridgeRewardsMessageStatus aparecem no BridgeHarness.sol blob 850d5a63fa375ee6f9754c8377990d5d48c09c07, não no erc20.spec.
Os scripts verifyBridge.sh e verifyBridgeConstIndex.sh fixam BridgeHarness e seus mocks, nove links, solc8.10, optimistic_loop, loop_iter 3 e settings -mediumTimeout=700,-depth=12. Comentário de texto diz 2 iterações; comando executável usa 3. Não há argumento packages/path explícito nos scripts; imports indiretos continuam exigindo fechamento. Makefile target munged copia contratos e aplica applyHarness.patch (blob f806c1e6957b164a0a8419fa6f5c8015de5dd95c), inclusive alterações virtual em Bridge.sol. O snapshot contém Bridge.sol de revisão posterior, e os 17 exemplos seguem incomplete. A recuperação dos blobs não prova ABI transitiva nem equivalência de prova.

<!-- ROUND2-HISTORIC-DECISION -->
## Fechamento documental apos segunda auditoria (2026-10-19)

- Estado de implementacao: 17/17 UNRESOLVED_CANDIDATE. Preservado apos a segunda revisao, sem promover ou executar.
- [HISTORICAL_BLOCKERS.md](HISTORICAL_BLOCKERS.md): evidencias, itens potencialmente recuperaveis, blockers e decisoes humanas.
- [historical_status.csv](historical_status.csv): adjudicacao explicita por exemplo e Result/Detection Outcome historicos.
- [RECOVERY_SEARCH_LOG.md](RECOVERY_SEARCH_LOG.md): escopo, consultas e resultados das buscas; ausencia de resultados nao significa impossibilidade.
- A versao historica das regras, asserts/assumes, methods universe, harness e compatibilidade CVL2 nao foi modificada. Nao executar Prover sem autorizacao.
