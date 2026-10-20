# AGENTE-02 — RODADA 6 / Auditoria cruzada somente leitura do PR #36 (Rocket Joe)

**Data:** 2026-10-20. PR #36 na HEAD `907303e8647bf9e390c481bc4180f736fb21814e` (Draft). Somente leitura, sem commit ou alteração na branch do AGENTE-03. Foram consultados: última revisão do coordenador, `round5_quality_report.md` (blob `5314176ff0f94fcfa732957416e69c7afb4557d5`), `round5_example_evidence.csv` (blob `c1b75747692a6f17bc5a8ade740ae7b4dff45540`), `round5_import_resolution.csv` (blob `1bfc5d1796fed91469fda9e6ff6e71614b776874`), `round5_oz_package_provenance.csv` (blob `7059c5b3645ed24ddff29a4c02dac35ae8ed7e17`) e os arquivos CVL originais por ref GitHub.

## Reconciliação independente do registro de Rodada 5

`round5_example_evidence.csv` contém **164 chaves (24,incomplete,N), todas únicas**; `compile_only_state=NOT_EXECUTED_GATE_UNMET` em 164; `semantic_state=NOT_PROVEN` em 164. Nenhuma instância foi promovida a `COMPILE_OK` ou `SEMANTIC_PROVEN`; correto e conservador.

Recuperei **diretamente** os dois arquivos completos das specs por GitHub nos dois commits fixos:
- `Web3Bugs/main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3:contracts/24/spec/LEHighLevel.spec` e `Certora/rocket-joe-1@dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10:certora/spec/LEHighLevel.spec`: Git blob `0f212bba0969fcc2f8b5caf8e9c1160b91fe7c7b` em ambos.
- `Web3Bugs/main:contracts/24/spec/Staking.spec` e `Certora/rocket-joe-1@dba90f9:certora/spec/Staking.spec`: Git blob `2fd60f3d0e46ec0954abc0ebba31801bd01b5e17` em ambos.

Isso demonstra **identidade dos dois CVL originais arquivados com o fork**, não identidade dos contratos da auditoria `lfj-gg/rocket-joe@ef2ef30248661b5509c52ab30af9bd0fc07f6657` nem do job do Prover.

## Cinco exemplos, relatório versus fonte

| ID P24 incomplete | Property / origem literal | Relação PDF identificada na matriz da fonte | Adjudicação conservadora |
| --- | --- | --- | --- |
| **2** | `hl_depositAdditivity`, LEHighLevel.spec:46–62 | `FORMULA_DIFFERENT`; relatório p.13 assume mesmo remetente e CVL usa remetentes distintos com saldos iniciais iguais | **BLOCKED**; universo de contraexemplos não preservado |
| **5** | `hl_noDepositFrontRun`, LEHighLevel.spec:110–128 | `FORMULA_DIFFERENT`; pós-condição orientada a withdraw na fórmula impressa versus depósito no CVL | **BLOCKED** |
| **7** | `hl_noWithdrawLiquidityFrontRun`, LEHighLevel.spec:155–178 | `DIFFERENT_RULE`; relatório pp.14–16 discute withdrawAVAX, não withdrawLiquidity | **BLOCKED** |
| **147** | `balanceOf_Joe_eq_totalJoeStaked`, Staking.spec:120–124 | `FORMULA_DIFFERENT`; relatório p.17 igualdade, CVL `>=` com preserved guard | **BLOCKED** |
| **150** | `RJPS_only_owner_and_function`, Staking.spec:156–167 | `FORMULA_DIFFERENT`; variáveis diferentes no predicado impresso vs pre/post CVL | **BLOCKED** |

Os qualificadores são interpretações documentadas pelo AGENTE-03 a partir do PDF; nesta Rodada 6 **não houve nova extração independente de PDF nem Prover**. Foram, porém, verificadas por leitura de matriz a identidade e seleção dos cinco IDs, suas linhas e a classificação de bloqueio. Resultados `VERIFIED` do PDF não podem ser transferidos automaticamente para N.spec, todos ainda `incomplete`.

## Hunk 7 e imports — avanço real do AGENTE-03, limite do gate

O novo `round5_quality_report.md` mostra diferença **material** no guard de `LaunchEvent.sol:673–679`: auditado `address(this).balance >= avaxReserve`; fork `address(this).balance - _value >= avaxReserve`. O patch `certora/applyHarness.patch:96–104` espera o guard do fork e modifica a função para `virtual internal`; `LaunchEventHarness.sol:114–116` adiciona override de transferência. Um exemplo algébrico (`balance=100`, `reserve=80`, `_value=30`) separa as fórmulas, **não** prova que esse estado é alcançável em execução. A Rodada 5 do AGENTE-02 já havia reproduzido em scratch `patch --dry-run --batch --fuzz=0` **EXIT 1**, com `Hunk #7 FAILED at 670`; **não foi repetido** nesta Rodada 6 por falha de I/O do dispositivo.

A recuperação de **quatro tarballs publicados** de `@openzeppelin/contracts` e `contracts-upgradeable`, versões 4.4.1 (audited) / 4.4.2 (fork), tem `SHA512 MATCH` para todos os quatro objetos com `yarn.lock`; o CSV publica os hashes SHA-256. A closure estática interna aos tarballs mostra **10 referências diretas, 15 Solidity transitivos** para drivers LaunchEvent e **6 diretas, 11 transitivos** para Staking, com **0 missing dentro desses tarballs**. Isso supera a antiga lacuna de baixar os pacotes, mas **não fecha import graph total, command-line efetiva, ABI, target/harness auditado ou linking**. Persistem `Owner.sol` ausente e casing `certora/spec/staking.spec` divergente. Nenhum patch fuzz=0 válido na revisão auditada foi recuperado.

## Decisão, responsabilidades e próximo gate

**5/5 revisados continuam BLOCKED** para equivalência CVL2; **164/164** do PR #36 seguem sem compilação CVL2 e `SEMANTIC_UNRESOLVED`. Para sair do bloqueio, AGENTE-03/coordenador precisa fixar patch compatível fuzz=0 com código auditado, resolver `Owner.sol`, separar runners Staking e verificar todos os imports/versions/links e ABI histórica. O fork testável isoladamente seria **experimento distinto**, nunca prova da auditoria original.

**AGENTE-02 — RODADA 6 / CONTRARREVISÃO READ-ONLY.**
