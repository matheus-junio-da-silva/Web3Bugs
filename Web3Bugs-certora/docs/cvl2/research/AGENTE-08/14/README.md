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

- Estágio de decisão documental: 34 UNRESOLVED_CANDIDATE (apos revisao de 31 promocoes anteriores; #1, #19 e #25 seguem bloqueados), all provisional.
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

<!-- AGENTE08-R2 -->
## Contrarrevisão P14: 31 promoções retiradas
Foram revisitadas 34 instâncias e 510 ocorrências sintáticas. As 31 entradas antes DOCUMENTED_CANDIDATE foram reclassificadas UNRESOLVED_CANDIDATE por ausência de confirmação da ABI do target pós-mutation. Os dossiês registram original/proposto (placeholder documental não executável), linha, fonte A1 e risco de receiver, internal/external, overload, path revert e summaries. A menção [external|internal ABI_UNVERIFIED] NÃO É SINTAXE CVL2 VÁLIDA e não deve ser copiada como script de migração.
O arquivo original contracts/14/specs/scripts/applyHarnesses.sh altera Controller.getProceed, getExcessCollateral, settleVault, _runActions, MarginPool transfer e interfaces/fields. runOrderOfOperations.sh conecta ControllerHarness, MarginPool, MarginCalculatorHarness, OtokenHarnesses e DummyERC20, com solc6.10. A existência de applyHarnesses.sh não prova sua execução em todas as runs, portanto a ABI exata não está confirmada. #1 preserva assert true condicional; #19 não herda solvência global; #25 tem sinvoke seguido de assert false e continua semanticamente bloqueada.

<!-- ROUND2-HISTORIC-DECISION -->
## Fechamento documental apos segunda auditoria (2026-10-19)

- Estado de implementacao: 34/34 UNRESOLVED_CANDIDATE. Preservado apos a segunda revisao, sem promover ou executar.
- [HISTORICAL_BLOCKERS.md](HISTORICAL_BLOCKERS.md): evidencias, itens potencialmente recuperaveis, blockers e decisoes humanas.
- [historical_status.csv](historical_status.csv): adjudicacao explicita por exemplo e Result/Detection Outcome historicos.
- [RECOVERY_SEARCH_LOG.md](RECOVERY_SEARCH_LOG.md): escopo, consultas e resultados das buscas; ausencia de resultados nao significa impossibilidade.
- A versao historica das regras, asserts/assumes, methods universe, harness e compatibilidade CVL2 nao foi modificada. Nao executar Prover sem autorizacao.
