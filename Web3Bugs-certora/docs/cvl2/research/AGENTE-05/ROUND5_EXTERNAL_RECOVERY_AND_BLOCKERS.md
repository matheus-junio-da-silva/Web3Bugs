# AGENTE-05 — Rodada 5: recuperação verificável e bloqueios externos P3/P6/P19/P21

**Escopo:** estudo documental sem alterar originais, pacotes, `requirements`, `asserts`, `contracts` ou `results`. Todas as recuperações foram feitas em `/tmp/`; descoberta da origem não é validação de um job Certora auditado.

## P3 — AAVE Rescue Mission (incomplete/1,2,3)

**Nova prova histórica positiva: submódulo recuperado.** No upstream `bgd-labs/rescue-mission-phase-1@33c1aeca28d6d61659c1b28775ad2644b7e2ac6e`, `git ls-tree` registra entrada gitlink `160000 lib/solidity-utils` para **`49f2bd22950cf8dfe32d3f01e30a221b1f2f95dd`**. `.gitmodules` aponta `https://github.com/bgd-labs/solidity-utils`. Esse commit existe no upstream, foi clonado e colocado em detached HEAD exclusivamente em `/tmp/cvl2_ag05_round5_research/solidity-utils`. `git rev-parse HEAD^{tree}` dá **`36cb441858e6d959387713deb832e47e4377efe5`**. Foram encontrados 26 arquivos `.sol`; `src/contracts/oz-common/interfaces/IERC20.sol` existe com Git blob **`053588c2c388d41f281c5662f72c8c6e8b0f7192`**.

Esta última interface é **exatamente o caminho** importado por `contracts/3/contracts/LendToAaveMigrator.sol:4` via `solidity-utils/contracts/oz-common/interfaces/IERC20.sol`. O runner upstream `certora/scripts/verifyRescueLendMigrator.sh` usa `--packages solidity-utils/contracts=lib/solidity-utils/src/contracts` e linka `LEND=DummyERC20Impl`, `AAVE=DummyERC20Impl2`, com `--solc_map` solc8.0/solc7.5 e `--optimistic_loop`. O runner fornece **`--rule $1`**: isso não constitui registro de quais rules foram executadas. Os helpers de Certora e scripts já recuperados na Rodada 4 permanecem separados da árvore do catálogo.

| ID | Fonte CVL / target | Evidência adicional | Bloqueio ainda aberto |
| --- | --- | --- | --- |
| P3/incomplete/1 `LendIsBackedByAave` | `contracts/3/specs/rescueLendMigrator.spec`; `LendToAaveMigrator` | gitlink + remapping + IERC20 autenticamente recuperados | reconstrução transitiva completa de harnesses, libs, solc_map, linkings e identidade da execução auditada |
| P3/incomplete/2 `LendIsBackedByAaveIncInitialize` | Mesma spec/target com initialization | mesmas evidências, mas precondições e call-path diferentes | inicialização original, LINK/token scene e resultado por rule ainda sem atribuição exata |
| P3/incomplete/3 `StkAaveIsBackedByAave` | `contracts/3/specs/rescueSTKAAVE.spec`; `StakedTokenV2Rev4` | submódulo recuperado, upstream com scripts/harnesses STK a pesquisar por target | não extrapolar o runner LEND para stkAAVE; versão auditada/PDF e links STAKED_TOKEN/REWARD_TOKEN não reproduzidos |

**Conclusão:** causa histórica `lib/solidity-utils` mudou de `NOT_RECOVERED` para **`PIN_AND_FILES_RECOVERED`**; os três seguem `incomplete` no catálogo e `02_unresolved` em migração. Não compilar Solidity recomposto nem Prover antes de closure completo; não chamar `COMPLETE` ou verificação histórica.

## P19 — Origin OUSD (incomplete/3–37; não repetir math/1–2)

Foram recuperados em scratch **exatamente os pacotes e tarballs referidos pelo `contracts/19/contracts/yarn.lock:522–530`**, sem instalar scripts ou alterar `node_modules` do projeto:

| Pacote | Versão | SHA-512 base64 calculado dos bytes `.tgz` | Igual ao lock |
| --- | --- | --- | --- |
| `@openzeppelin/contracts` | `2.5.0` | `t3jm8FrhL9tkkJTofkznTqo/XXdHi21w5yXwalEnaMOp22ZwZ0f/mmKdlgMMLPFa6bSVHbY88mKESwJT/7m5Lg==` | **SIM** |
| `@openzeppelin/upgrades` | `2.8.0` | `LzjTQPeljPsgHDPdZyH9cMCbIHZILgd2cpNcYEkdsC2IylBYRHShlbEDXJV9snnqg9JWfzPiKIqyj3XVliwtqQ==` | **SIM** |

`npm pack --ignore-scripts` produziu tarballs em `/tmp/cvl2_ag05_round5_npm`, e a extração em diretórios temporários encontrou **84 Solidity** em `contracts@2.5.0` e **17 Solidity** em `upgrades@2.8.0`. A inspeção das imports Solidity diretas sob `contracts/19/` encontrou **38 referências a `@openzeppelin/contracts` e 8 a `@openzeppelin/upgrades`**, todas com arquivos correspondentes nos dois pacotes recuperados. Isso é **resolução de caminhos diretos OZ**, não prova de import closure transitivo ou sucesso de compilação.

Os **35 `N.txt` de P19 incomplete** mencionam dependências/imports ausentes; 29 contêm `OUSDHarness`, 34 fazem referência a OpenZeppelin. A fonte `contracts/19/spec/harnesses/OUSDHarness.sol:1–4` é Solidity 0.5.11 e importa uma implementação OUSD local; o script `contracts/19/spec/scripts/applyHarnesses.sh:1–5` injeta mudanças no Solidity **inclusive um `require(nonRebasingCreditsPerToken[_account] <= 1e18)`**. Executar o script sobre a fonte preservada violaria a imutabilidade e mudar essa precondição sem evidência do job poderia mudar o universo de contraexemplos. Portanto o script foi apenas **lido**, não executado. O runner `runOUSDSpec.sh` escolhe `OUSDHarness:../spec/ousd.spec` e `--solc solc5.11`, mas isso não prova seleção de todas as 35 properties nem autentica o payload pós-script.

**Priorização P19:** reabrir import closure nos 35 incomplete com os tarballs *autenticados*; recuperar o estado efetivo pós-script e flags/solc dos runners por spec. `incomplete/3 totalSupplyIsBelowMaxSupply` e `incomplete/4 neverRevert_BalanceOf` são primeiros para levantamento de import graph e `@withrevert`, **não** para promoção, compilação sem cena ou inclusão em `results/cvl2`. P19/complete/1–2 continuam `02_unresolved` no PR #46 por `RCPT=0` e semântica CVL1.

## P6 — Static aToken (incomplete/1–32)

Confronto de fonte:
- `reports/6.md:5–17,37–47` e PDF **arquivado** `resources/6/Formal_Verification_Report_staticAToken.pdf` (SHA-256 `f81737f4c9b9f64072601d74c6dda27ce2eb2620b0a40e1a3a6d49faf775c507`) dão período Jan 18–Mar 31, 2023 e `ac92951` como última revisão.
- [Página oficial Certora publicada em 04/04/2023](https://www.certora.com/reports/aave-static-a-token) apresenta o mesmo assunto e período, mas indica `51d46b1`. O relatório público foi identificado no estudo anterior; os **bytes** da publicação pública não foram autenticados como iguais aos recursos arquivados. Não igualar commits por data/título similares.
- Tentativas documentais de resolver ambos os SHAs abreviados via API GitHub em `aave/aave-v3-periphery`, `bgd-labs/aave-v3-periphery` e `aave/aave-v3-core` não retornaram commit correspondente. Isso **não prova inexistência** (repositório upstream incorreto, revisão privada, git-history distinta ou abreviação), apenas que a pesquisa nesses três candidatos foi negativa.
- O snapshot `StaticATokenLM.sol` está associado no catálogo a `13a004738c533f11710400c1757b9570ef1e0466`, anterior; não se pode classificar o snapshot como a revisão auditada apenas por similaridade de nome.

**Conclusão:** 32/32 `incomplete`, sem target histórico/ABI/runner autenticados e sem compilação CVL2. O coordenador precisa identificar repositório upstream, commit completo e PDF/runner que correspondam aos exemplos; não transferir o resultado do relatório público de outro hash.

## P21 — Lido DSM (incomplete/1–2)

`contracts/21/specs/DSM.spec:3–6,11–38` emprega `using DepositSecurityModuleHarness as DSMH` e o método `getGuardianLength()` sem implementação no snapshot. Busca por nomes dentro de todos os 59 arquivos de `contracts/21` encontrou apenas as menções à spec, **zero arquivos Harness**. O arquivo Solidity real `contracts/21/0.8.9/DepositSecurityModule.sol:211–235` fornece `getGuardianQuorum()` e `getGuardians()` (array), **não** `getGuardianLength()`. Atribuir automaticamente `getGuardianLength() := getGuardians().length` criaria helper novo: proibido sem bytes e runner originais.

**Evidência semântica mais forte:** `DepositSecurityModule.sol:218–227` deixa o owner definir `quorum` e comenta explicitamente na linha 223 que **permite quorum maior que o número de guardians**. Assim, a intenção de `incomplete/2 quorumLeGuardian`, assertando `getGuardianLength() >= getGuardianQuorum()`, é **incompatível com comportamento permitido pelo contrato real** sob interpretação natural de `Length` como número de guardians. Não declarar uma violação CVL formal: o getter ausente e o harness não foram reconstruídos. Em `incomplete/1 depositBufferEtherRevertCheck`, o corpo usa `depositBufferedEtherHarness@withrevert` e assevera `!lastReverted` sem condições de sucesso; o contrato real pode reverter por vários motivos, e a cena do harness/signatures está ausente. O PDF público tem 18 nomes de propriedades não correspondentes às duas originais catalogadas. Ambas continuam sem target migrável comprovado.

## Evidência necessária antes de novos gates

1. **P3:** fechar todos os imports/harnesses no commit da auditoria, linkings e versões de compiladores dos jobs *de cada rule*; gitlink agora fixado, mas isso isoladamente não é execução.
2. **P19:** autenticar a árvore pós-`applyHarnesses.sh` que realmente participou do job, sem editar a original; comparar 35 chamadas com seu receiver e seus `N.txt` antes de liberar experimento.
3. **P6:** reconciliar PDF arquivado e publicação 2023 com URLs, commits completos e scripts, mantendo `ac92951` distinto de `51d46b1`.
4. **P21:** obter bytes e hash do `DepositSecurityModuleHarness`, definição real `getGuardianLength()` e report que inclua as duas rules; aceitar que `quorumLeGuardian` pode não ser invariante válida do Solidity preservado.

**Estado de todos:** no máximo recuperação de fonte/hipótese, nenhum `SEMANTIC_PROVEN`, `MIGRATED_COMPLETE`, novo `COMPILE_OK` ou alteração do catálogo histórico.
