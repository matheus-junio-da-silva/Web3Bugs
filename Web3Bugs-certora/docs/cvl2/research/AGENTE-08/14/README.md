# AGENTE-08 — Fase 1 / Pesquisa pré-migração CVL2 — Project 14: Opyn Gamma Protocol

**Status:** pesquisa documental provisória, sem implementação, sem execução da Certora CLI, sem compilação CVL2 e sem Prover.

## Identidade, baseline e escopo
- Project ID 14; origem PropertyGPT `certora_projects/opyn_gamma_protocol/`; catálogo GitHub `Web3Bugs-certora/`.
- Input baseline Web3Bugs/main: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PropertyGPT/main observado e confirmado: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Exatamente **34** instâncias canônicas: 34 original_status=complete; 0 original_status=incomplete; múltiplas labels não criam novos exemplos.
- Index source: `results/spec/spec_buglabel.csv` no baseline; Snapshot CSV 34 unique and 34 label rows. 34 N.spec, 34 N.sol, 34 N.md; no incomplete N.txt.
- Result histórico: **19 VERIFIED, 15 NOT_STATED**. Detection Outcome histórico: **12 NO_FINDING, 7 FINDING, 15 NOT_STATED**. Nenhum significa verificação nova.
- Histórico/pinned audited SHA: Source and PDF version recorded in Project 14 catalog; exact original audit commit not newly verified for this research.
- Material de origem: Six top-level original spec files; 34 source-rule/target instances. Historical run scripts use ControllerHarness, ControllerHarnessExtra, MarginVaultHarness and Whitelist; known Controller mutation script.

## Riscos e reconstrução histórica
Dependency-complete is a documentation criterion, not a successful CVL2 compile. #1 has selector-ordered assert true branch, #15–19 narrower solvency cases, and scripts apply harness changes. Changes to methods receiver and summaries can alter proof model.

- Estágio de decisão documental: 31 DOCUMENTED_CANDIDATE and 3 UNRESOLVED_CANDIDATE (#1, #19, #25), all provisional.
- Proveniência e recuperação: 6 registered sources, including original runOrderOfOperations.sh blob 358435625300bed273971f8058e0219e516fb88c; empty recovery_manifest.csv by design.

## Conteúdo desta pasta
- `properties.csv`: uma entrada por exemplo original, sem duplicação de Bug Labels; independe do status futuro da reconstrução.
- `properties/complete/N.md`: uma análise fonte-específica para cada exemplo, com fórmulas/guards visíveis, source blob, N.txt se incompleto, cenários de contraexemplo e planos provisórios.
- `patterns/migration_decisions.md`: padrões e casos semânticos críticos; não substitui decisão por exemplo.
- `evidence_register.csv`: evidências A1/A2/B1 verificadas ou consultadas, com URL e cautelas.
- `recovery_manifest.csv`: dependências históricas candidatas/ausentes, sua prova disponível e estado; não modifica o snapshot.
- `QA_REPORT.md`: cobertura, divergências, verificações estruturais executadas, validações NÃO executadas e encaminhamento.

## Regras rígidas de preservação
Fontes originais `.spec`, Solidity, PDFs, configs, CSVs do catálogo e contracts/ históricos permanecem intactos. Trechos `N.sol` são documentos, não alvos compiláveis. Não executar o script de migração in-place em contratos históricos. Compilar futuramente um arquivo sem prova de mesma ABI, overrides, receiver, assumptions e paths de revert não demonstra equivalência.

**Próxima etapa apenas com autorização expressa do coordenador:** revisar origin/harness/prova de import closure, selecionar alterações textuais mínimas documentadas, construir derivados separados e só então executar compilação e provas.
