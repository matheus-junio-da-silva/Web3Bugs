# P5 — registro de buscas delimitadas, 2026-10-19
## Fontes verificadas
1. Commit upstream aave-starknet-project/aave-starknet-bridge@4c010c18b08703e4f367db1e0c642c76c25e551b, blobs historicos do recovery_manifest.csv: erc20.spec (b12fec167...), BridgeHarness.sol (850d5a63...), BridgeL2Harness e mocks.
2. certora/scripts/verifyBridge.sh blob 9c4a5a2... e verifyBridgeConstIndex.sh blob b9c2ec7...: target BridgeHarness, solc8.10, --optimistic_loop, --loop_iter 3, -mediumTimeout=700,-depth=12, links multi-contract. Comentario sobre 2 iteracoes e inconsistente com comando executavel.
3. certora/Makefile blob 0e33459... e certora/applyHarness.patch blob f806c1e...: target munged materializa arvore transformada, exigindo baseline upstream correto.
4. Snapshot contracts/5 sem sol fonte de *Harness*.sol e Bridge.sol identificado no catalogo como revisao posterior 71be8e44...; fonte recente nao e byte-equivalente ao pacote auditado.
5. erc20.spec declara metodos ERC20 DISPATCHER(true). Nao define withdrawMessageStatus nem bridgeRewardsMessageStatus, getters presentes em BridgeHarness; nao construir esses getters sinteticamente.
## Estado
Blobs de arquivos especificos sao recuperaveis com proveniencia, mas closure transitiva de imports, mapeamento de packages, hash do solc8.10 usado, tree munged materializada e ABI auditada permanecem sem prova. Encerrar repeticao de buscas pelo mesmo blob sem package lock ou run historico. Nao transformar recuperabilidade parcial em complete.
