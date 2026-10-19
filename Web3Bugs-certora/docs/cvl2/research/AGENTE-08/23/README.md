# AGENTE-08 — Fase 1 / Pesquisa pré-migração CVL2 — Project 23: Radicle Drips

**Status:** pesquisa documental provisória, sem implementação, sem execução da Certora CLI, sem compilação CVL2 e sem Prover.

## Identidade, baseline e escopo
- Project ID 23; origem PropertyGPT `certora_projects/radicle_drips/`; catálogo GitHub `Web3Bugs-certora/`.
- Input baseline Web3Bugs/main: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PropertyGPT/main observado e confirmado: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Exatamente **46** instâncias canônicas: 0 original_status=complete; 46 original_status=incomplete; múltiplas labels não criam novos exemplos.
- Index source: `results/spec/spec_buglabel.csv` no baseline; Snapshot CSV 46 unique and 46 label rows. 46 N.spec, 46 N.sol, 46 N.md, 46 N.txt.
- Result histórico: **15 VERIFIED, 1 VIOLATED, 30 NOT_STATED**. Detection Outcome histórico: **15 NO_FINDING, 1 FINDING, 1 INCONCLUSIVE, 29 NOT_STATED**. Nenhum significa verificação nova.
- Histórico/pinned audited SHA: 6fe9d38a30765df6aa3e4078634a37aeabbceef1 for the report's production Splits.sol scope; does not prove historical harness revision for other targets.
- Material de origem: Six active CVL spec files: DripsHub, DripsHubBackup, Reserve, SlotTester, Splits and Splits2. Original PDF under resources/23 and report transcript reports/23.md.

## Riscos e reconstrução histórica
Historical source tree omits generated CVT internal calls and DripsHubHarness/ReserveHarness/SlotTester targets. PDF result covers named Splits.sol properties, not Splits2 or other contracts; #36 historical rounding failure, #38 timeout.

- Estágio de decisão documental: 46 UNRESOLVED_CANDIDATE.
- Proveniência e recuperação: 7 registered sources; five missing harness/wrapper families in recovery manifest, currently unresolved.

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
## Contrarrevisão P23: provedores de CVT não encontrados
O PDF de seis páginas (sobretudo páginas 3-5) restringe a verificação formal a Splits.sol. A árvore do commit oficial Certora/drips-contracts@6fe9d38a30765df6aa3e4078634a37aeabbceef1 contém produção e testes, mas não os CVT wrappers esperados; isso não prova inexistência em servidores ou artefatos gerados históricos. DripsHubHarness (#1-12), UpdateReceiverStatesHarness (#13-18), ReserveHarness/mocks (#19-23), SlotTester/getters (#24) e wrappers Splits/Splits2 (#25-46) permanecem não recuperados. #36 VIOLATED/FINDING por arredondamento, #38 NOT_STATED/INCONCLUSIVE por timeout e #39-41 VERIFIED apenas nas suas instâncias Splits.spec. O limite de unrolling (2) e receiver weights (até 1000000) não foram ampliados.
