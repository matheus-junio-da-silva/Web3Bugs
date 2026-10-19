# AGENTE-06 — P1 Audit Commit e comparação upstream

**FASE 1 — Somente proveniência, nenhuma alteração em CVL, Solidity ou runners.**

O relatório `reports/1.md`, página 1, afirma que o último commit revisado pelo Prover foi `303bd3e1`. O upstream [Certora/governance-crosschain-bridges](https://github.com/Certora/governance-crosschain-bridges/commit/303bd3e16c8d3465325389a72564126c3bacc4f9) resolve esse prefixo para `303bd3e16c8d3465325389a72564126c3bacc4f9`, árvore `3622915d221893a6efd32bae3770349254fd2a46`.
Web3Bugs main de comparação: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.

## Comparação direta por blob e texto

| Arquivo | Git blob do audit commit | Blob arquivo Web3Bugs | Diferença observada |
|---|---|---|---|
| `contracts/bridges/BridgeExecutorBase.sol` | `e825e5f201365b39288bd8bad2ac5b6886d219ab` | `e6095a1ee6dad8cfc4e7cb69321bb4c574a0a43a` | pragma and comment line 32 |
| `contracts/bridges/PolygonBridgeExecutor.sol` | `644f1f6d93b0552bda196b9ef776bce2b8a09bdf` | `2951535c64679dfad1288c86e181e93f3a930bc7` | pragma |
| `contracts/bridges/L2BridgeExecutor.sol` | `0b587c4c5e6960b6accabfaad79b281c081cdbe6` | `d2b496981dd7cc5426b055ff261d9c3f9830dc96` | pragma |
| `contracts/bridges/OptimismBridgeExecutor.sol` | `3f6117314f84009616392bd077d94968fd6713ed` | `598c1b676517ba717c27f009152a7400b33d9e88` | pragma |
| `contracts/bridges/ArbitrumBridgeExecutor.sol` | `09e54ca1f168d5396951d809632e1eb1111769ba` | `327247372ab5a3f7836a340a4afe41119321f42a` | pragma |

As fontes originais diferem no literal `pragma solidity 0.8.10;` versus `pragma solidity ^0.8.10;` no snapshot. Em `BridgeExecutorBase.sol` também difere o comentário de map `_queuedActions`, linha 32. Comparação textual das cinco fontes identificou essas diferenças, mas isso **não certifica** identidade de todo o build/ABI pois Solidity permite outras versões com pragma diferente.

No commit auditado não foram encontradas as `specs` do dataset; o CVL histórico extraído ainda precisa de lastro específico em outro commit de verificação. O report descreve restrições de modelagem em outros trechos e esse trabalho não reproduziu o run.

## Efeito sobre status original
- 70 exemplos mantêm sua chave canônica e status original (36 complete/34 incomplete).
- `_mock`, `queue2`, getters e harness de `complexity.spec` não são substituídos com a ABI da revisão auditada.
- A atualização de `source_commit_audited` apenas identifica commit do **relatório para Solidity**, não comprova compilação ou equivalência individual de todos os N.spec.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
