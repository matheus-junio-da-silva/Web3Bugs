# AGENTE-02 / RODADA 5 — contrarrevisão P24 / Rocket Joe, SOMENTE LEITURA

Em 2026-10-20, examinei o [PR #36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36) na HEAD `1838bed460b471d860af1b1a1788c50d3b7d3c32`, sua revisão mais recente, o arquivo `round4_example_blocker_matrix.csv`, `source_provenance_matrix.csv`, `pdf_formula_review.md` e `historical_closure_resolution.md`. Nenhuma branch ou arquivo do AGENTE-03 foi alterado. Conferi os originais `contracts/24/spec/` somente por leitura e hash.

## Identidade do fork e aplicação estrita do patch

Fork histórico `Certora/rocket-joe-1@dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10`. Git blob de `certora/applyHarness.patch`: `abfb1eae851307c9a3e7d17a7b3e913962952845`; SHA-256 `e06f5a9d5503e82310ffccfab55214b9cb847d2146656f2558271e0777e27fdb`. Independente: `LEHighLevel.spec` SHA Git `0f212bba0969fcc2f8b5caf8e9c1160b91fe7c7b`, `Staking.spec` SHA Git `2fd60f3d0e46ec0954abc0ebba31801bd01b5e17` — iguais entre snapshot e fork nos caminhos documentados.

**Teste realmente executado (sem editar fork):** copiei `contracts/` do fork para `/home/mat/cvl2-agente02-round5-scratch/rocketjoe-audited-hybrid-fuzz0/`, substituí **somente nessa cópia** `LaunchEvent.sol` e `RocketJoeStaking.sol` pelos objetos de `lfj-gg/rocket-joe@ef2ef30248661b5509c52ab30af9bd0fc07f6657`, e executei:

```bash
patch --dry-run --batch --fuzz=0 -p0 -d <scratch>/rocketjoe-audited-hybrid-fuzz0 < <fork>/certora/applyHarness.patch
```

**Resultado: exit 1, `Hunk #7 FAILED at 670`, `1 out of 7 hunks FAILED` em `LaunchEvent.sol`.** Evidência integral de stdout e stderr, SHA-256 e caminho em `round5_rocketjoe_patch.csv` e `round5_logs/rocketjoe_fuzz0.*.txt`. Não houve aplicação do patch à árvore compartilhada; `--fuzz=0` impediu equivalência textual permissiva. Os dois arquivos substituídos têm SHA-256 consignados no CSV.

## Cinco propriedades examinadas independentemente

| P24 incomplete ID | Spec (hash idêntico fork) | Divergência fórmula CVL vs relatório e ligação ao job | Fechamento |
|---|---|---|---|
| **2** `hl_depositAdditivity` | `LEHighLevel.spec` | PDF p.13 exprime depósito de mesmo sender; regra arquivada trata dois remetentes e igualdade de saldo inicial | **BLOCKED**: regra não idêntica à fórmula reportada, fuzz0 falha; script `verifyLEHighLevel.sh` não certifica runner |
| **5** `hl_noDepositFrontRun` | `LEHighLevel.spec` | PDF p.14 contém pós-condição orientada a withdraw, diferente do incremento deposit `msg.value` arquivado | **BLOCKED**: divergência semântica, fuzz0 falha, imports externos não fechados |
| **7** `hl_noWithdrawLiquidityFrontRun` | `LEHighLevel.spec` | PDF pp.14–16 nomeia `withdrawAVAX`, não `withdrawLiquidity` | **BLOCKED**: target/efeito e relação rule-PDF não demonstrados |
| **147** `balanceOf_Joe_eq_totalJoeStaked` | `Staking.spec` | PDF p.17 usa igualdade; CVL arquivado usa comparação mais fraca `>=` e condição `preserved` | **BLOCKED**: divergência do predicado, target fork diferente do auditado e inputs OZ não fechados |
| **150** `RJPS_only_owner_and_function` | `Staking.spec` | PDF pp.17–18 usa nomes `userBalance_` no corpo impresso, CVL usa `RJPS_pre/post` | **BLOCKED**: não transportar `Result`/dedução para fórmula diferente; `verifyStaking.sh` vs `stakingRule.sh` divergem |

Para os casos 2/5/7, a matriz do AGENTE-03 identifica ~10 imports externos OpenZeppelin na closure estática de LaunchEvent; para 147/150, ~6 no runner Staking. Confirmei que **nenhum diretório local `node_modules/@openzeppelin/contracts` ou `@openzeppelin/contracts-upgradeable` está presente no checkout do fork revisado**. Isto é prova negativa apenas dessa cópia local, não de inexistência histórica. `yarn.lock` auditado fixa **4.4.1**, fork **4.4.2**, sem resolução binária comum. A closure real depende dos arquivos externos, dos linkings e da ABI depois do patch; uma relação textual de imports não constitui compilação da scene.

**Adjudicação:** 5/5 **BLOCKED**. Dois blobs de spec conferidos por hash, um patch estrito testado e fracassado, sem closure executável. Não executei solc, CVL1, Prover nem Certora desses cinco casos e não alterei o PR #36. É preciso fornecer patch que aplique com fuzz 0 aos bytes auditados e fechar imports externos/binários antes de gate individual.

**AGENTE-02 — RODADA 5 — QUALIDADE CVL2 / contrarrevisão independente.**
