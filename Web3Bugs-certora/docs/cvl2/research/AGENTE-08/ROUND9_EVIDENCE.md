# AGENTE-08 — Rodada 9 / evidências, teste controlado e contrarrevisão

**PR:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43 (Draft; não abrir PR novo, sem merge).
**Branch:** `research/cvl2-agente-08`; HEAD de partida confirmada `f38d9089e6ceeb85b1c54d2df07a44f7cea577ce`.
**Baseline catalogado imutável:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; upstream PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
**Escopo:** P5 StarkNet 17, P13 Notional 58, P14 Opyn Gamma 34, P23 Radicle 46: 155 propriedades.

A coordenação informou recuperação parcial do WSL na revisão R8 do [PR #43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43). Confirmei nesta rodada saúde básica do filesystem, leitura/escrita de um diretório temporário, clone isolado limpo e versões de solc/CLI antes de qualquer diagnóstico. **Não houve Prover completo, CVL1, alteração de fonte histórica ou uso de credenciais.** A única tentativa CVL2 foi original, byte-idêntica, em scratch. Fatos, inferências e evidências ainda ausentes são separados abaixo e por linha em [ROUND9_MATRIX_155.csv](ROUND9_MATRIX_155.csv).

## Contagem, autoria e limites da compilação

| Indicador exclusivo AG08 R9 | Contagem |
|---|---:|
| Propriedades documentadas e reconciliadas | 155 / 155 |
| Tentativas CVL2 originais `--compilation_steps_only` | **1** |
| Tentativas CVL2 derivadas / lexicais | **0** |
| Propriedades com `COMPILE_OK` CVL2 | **0** |
| Propriedades com `COMPILE_ERROR` CVL2 real | **1** — P5/incomplete/14 |
| Propriedades CVL2 `NOT_RUN` | **154** |
| `PREFLIGHT_AUTH_BLOCKED` | 0 |
| `SEMANTIC_PROVEN` / projetos integralmente migrados | **0 / 0** |

A compilação Solidity da R5 e seus 111 arquivos ABI não são compilações CVL2. A contagem global do coordenador (18 tentativas em 16 properties, incluindo duas properties que tiveram erro original e sucesso derivado) pertence a outros grupos até este resultado novo R9 e **não deve ser somada como se a cardinalidade das propriedades fosse o número de tentativas**.

## P5 — StarkNet, incomplete/14 `alwaysUnSent`: COMPILE_ERROR original CONFIRMADO

### source_or_report_fact / entradas fixadas

- **CVL original:** [`results/spec/incomplete/5/14.spec:1-17`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/5/14.spec#L1-L17), SHA256 `0c0e05b80677a46deccfe1494e205cf09b966efab14785e6206c37a0a92e2031`, verificado com `cmp` e SHA256 antes e depois. O N.spec não foi editado. É um fragmento extraído, **não a spec global**.
- **Runner declarado:** `aave-starknet-project/aave-starknet-bridge@4c010c18b08703e4f367db1e0c642c76c25e551b`, [`certora/scripts/verifyBridge.sh:1-30`](https://github.com/aave-starknet-project/aave-starknet-bridge/blob/4c010c18b08703e4f367db1e0c642c76c25e551b/certora/scripts/verifyBridge.sh#L1-L30), Git blob `9c4a5a2f9a2094eab044346e203d064865b1285a`. Declara exatamente **11 Solidity seeds** e **10 ligações `--link`**, target `BridgeHarness`, `solc8.10`, `--optimistic_loop --loop_iter 3`; o runner histórico usa `--verify BridgeHarness:certora/specs/bridge.spec` e `--cloud`. A R9 substituiu **somente o caminho de spec**, para testar N14 original isolado, acrescentou `--compilation_steps_only`, e **não executou `--cloud` nem o Prover**. Não incluiu as opções de solver `--settings` porque o objetivo se encerra no typechecker e não é execução de prova. **Portanto, não é reprodução do job histórico completo**.
- **Pin de compilador:** CLI direto `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun` identificado como `certora-cli 8.19.0`; `/home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10` = `Version: 0.8.10+commit.fc410830.Linux.g++`. O upstream e o patch Git correspondem aos da pesquisa R4 (`applyHarness.patch` Git blob `f806c1e6957b164a0a8419fa6f5c8015de5dd95c`). `certora/munged/l1/Bridge.sol` é arquivo físico copiado byte a byte, SHA256 `f7852c1be61e44e70a46be76606c4a8d9dbdb6ecd9441d2e2bce9df00709058d`.
- **Pacotes pré-existentes no scratch:** `@aave/core-v3@1.16.2` e `@aave/protocol-v2@1.0.1`, tarballs autenticados contra o `yarn.lock` nas R4/R5, sem reinstalação nesta rodada. A compilação prévia Solidity R5 cobriu 11 seeds, gerando 40 ABI, inclusive 34 funções do `BridgeHarness`; ainda não autentica a ABI de um run Prover histórico.
- **Manifests/logs preservados no PR:** [`ROUND9_P5_N14_INPUT_MANIFEST.csv`](ROUND9_P5_N14_INPUT_MANIFEST.csv) (sha256 de N.spec, 11 seeds, três spec globais de referência, patched Bridge.sol, patch), [`ROUND9_P5_N14_command.txt`](ROUND9_P5_N14_command.txt) (argumentos literais executados), [`ROUND9_P5_N14_stdout.log.b64`](ROUND9_P5_N14_stdout.log.b64) (**saída bruta integral codificada reversivelmente em Base64; `base64 -d` reproduz exatamente stdout, SHA256 do conteúdo decodificado preservado**), [`ROUND9_P5_N14_stderr.log`](ROUND9_P5_N14_stderr.log) (vazio, SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`) e [`ROUND9_P5_N14_seed_sha256.txt`](ROUND9_P5_N14_seed_sha256.txt).

### EXECUTADO — erro atribuível ao arquivo original e ao parser CVL2

Uma única chamada original em scratch isolado com `HOME` novo, `env -i` (variáveis de credenciais não herdadas), `timeout -k 5s 68s`, `--compilation_steps_only`, 11 seeds, 10 links e versão solc pinada retornou **exit 1**. Não foi erro EIO/EROFS, token, network, timeout ou solc ABI.

**Diagnóstico observado no stdout (arquivo completo no PR):**
- `14.spec:8:5` — entrada em `methods` exige `function`.
- `14.spec:8:64` — entrada em `methods` exige `;`.
- `14.spec:9:5` — segunda entrada exige `function`.
- `14.spec:9:46` — segunda entrada exige `;`.

O typechecker bloqueou nessa etapa, **antes** de avaliar a correção da cena completa, outros seletores, summaries, linking ou solc. **Status correto: `COMPILE_ERROR` para UM exemplo histórico P5/incomplete/14.** A distinção entre `COMPILE_ERROR` e `NOT_RUN` é documentada individualmente na nova matriz; não se adicionou a segunda tentativa derivada, e nenhum outro exemplo P5 foi testado.

### inference / missing_proof

O texto original nas linhas 7–17 contém `methods`, `messageSentFilter` e `invariant alwaysUnSent`; a [full `bridge.spec`](https://github.com/aave-starknet-project/aave-starknet-bridge/blob/4c010c18b08703e4f367db1e0c642c76c25e551b/certora/specs/bridge.spec#L1-L9) importa [`setup.spec`](https://github.com/aave-starknet-project/aave-starknet-bridge/blob/4c010c18b08703e4f367db1e0c642c76c25e551b/certora/specs/setup.spec#L167-L204) e ativa a regra com contexto global. Os getters `withdrawMessageStatus`/`bridgeRewardsMessageStatus` são `external view` em [`BridgeHarness.sol:37-42`](https://github.com/aave-starknet-project/aave-starknet-bridge/blob/4c010c18b08703e4f367db1e0c642c76c25e551b/certora/harness/BridgeHarness.sol#L37-L42), mas o filtro exclui dois seletores e os métodos L2 podem atualizar as flags. **Propor `function`/`;` sem fixar receiver e universo de métodos não prova equivalência ou non-vacuity.** Nenhum `sig:` ou `require` foi acrescentado. A próxima **variante lexical derivada** só pode ser estudada em scratch após gate do coordenador, preservando N.spec original, sem Prover.

## P14 — Opyn Gamma: confronto com o Controller PÓS-PATCH realmente produzido em R4

**source_or_report_fact:** `contracts/14/specs/scripts/applyHarnesses.sh` Git blob `70b216936e2b50d02b2f9387a9be8a0dda658564`, [linhas 4,6,8,10,12,14,18,20](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/14/specs/scripts/applyHarnesses.sh#L4-L20). A R9 **leu e comparou sem executar** os dois arquivos existentes: Controller original SHA256 `b4f2706b5d94fa776f32ee9fb6a052eaf5f52350665826630bb8a0f063d79a49` e Controller pós-transformação scratch R4 SHA256 `dd846a47818dafa7c6c517957d92c4ac260c9b4b51d195fe368f051ad17cb487`.

O `diff -u` **efetivo** mostrou: **(a)** novos `cheapGetVault` internal e `anOtokenA/B`/`dummyERC20C` public na declaração `using SafeMath` da região de linha 68; **(b)** as três substituições `getExcessCollateral(vault,typeVault)` por `getExcessCollateral(vault.shortAmounts[0],vault.longAmounts[0],vault.collateralAmounts[0],typeVault)` em [getProceed:467–475](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/14/contracts/core/Controller.sol#L467-L475), [_verifyFinalState:678–683](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/14/contracts/core/Controller.sol#L678-L683), [_settleVault:924–979](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/14/contracts/core/Controller.sol#L924-L979); **(c)** `_runActions` com `virtual`; **(d)** substituição do bloco `hasLong` por `if (long==anOtokenB)` seguido de `if(long==anOtokenA)...else{burn original}`. O `else` pertence ao segundo `if`, portanto **a possível repetição de burn B e fallback** depende de reachability e dos tipos/estado reais.

**Achado de precisão:** as regex da linha 4 e da linha 8 destinadas a trocar `memory` por `storage` **não casaram** com o Controller original; o patch efetivo manteve `MarginVault.Vault memory vault` nessas três funções. Também a substituição de `pool.transferToUser` da linha 18 **não aparece no diff do Controller**. Não extrapolar transformação textual simplesmente por sua presença no script.

**inference:** com `vault.shortAmounts.length==0` OU `longAmounts.length==0` OU `collateralAmounts.length==0`, qualquer leitura nova `[0]` da chamada do calculator pode reverter antes da chamada. Na função `_settleVault`, `require(hasShort||hasLong,"C30")` testa os arrays de **tokens**, não os de quantidades/colateral. Isso é uma **condição discriminadora possível**, não contraprova: não demonstramos que esse estado é alcançável depois de validar vault, expiry e pool, nem que o calculator original com struct inteira não revertia. A R5 obteve **39→42 funções ABI Solidity** pós-patch, sem provar o domínio do relatório. Manter **34 UNRESOLVED**, incluindo 31 candidaturas DOCUMENTED previamente rebaixadas; nenhuma execução CVL2 nova no P14.

## P23 — Radicle: produção auditada versus harness posterior

**source_or_report_fact:** [`reports/23.md:14–16`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/reports/23.md#L14-L16) restringe o Prover à revisão de produção `Certora/drips-contracts@6fe9d38a30765df6aa3e4078634a37aeabbceef1` (2022-08-18), contrato `Splits.sol`, blob `1bba377bf1b114b929a08bd61dca537613953d5b`. A branch posterior [`certora@8d1db123de7fb4e1c3536bdddfd10a085aa36095`](https://github.com/Certora/drips-contracts/tree/8d1db123de7fb4e1c3536bdddfd10a085aa36095) (2023-01-08) contém seis specs e fonte `Splits.sol` byte-idênticas ao **snapshot**, com fonte `Splits.sol` blob **`b66fc88780e860d2ebbc51cab534da8ad4197a76`**, diferente do código do relatório.

Os runners `runSplits.sh` e `runSplits2.sh` declaram **SplitsHarness** (`SplitsHarness.sol` blob `a0992b3555f299ad788ccdc6ab9e6d7af605bd5e`), **solc8.15**, `--loop_iter 2`, `--send_only --rule_sanity`; `SplitsHarness` tem arrays locais de receivers (linhas 10–11) e wrappers `split`/`splitResults` (linhas 54–70), que mudam a cena de métodos/estado. O submódulo OZ no gitlink `64e48203cecad94f02de9891ecdeed4d629c6dae` é uma dependência declarada do source, não build autenticado. As árvores públicas `certora` e `6fe9d38` foram pesquisadas na R8 sem pathname de generated CVT; não comprova ausência em logs privados/outras refs. **Nenhuma implementação CVT gerada, runner auditado ou Prover log autenticado**.

**inference:** esse cenário posterior permite pesquisa de ABI, mas não provar Splits2 contra resultados Splits de produção. Preservar `P23/36 VIOLATED/FINDING` arredondamento e `P23/38 NOT_STATED/INCONCLUSIVE` timeout, e os resultados distintos em `Splits2`. Não transportar `VERIFIED`.

## P13 — Notional: runners e solc por família

Da lista de dez scripts sob `contracts/13/certora/scripts/run*.sh`, **41/58** exemplos possuem correspondência literal entre `Original Spec` e `--verify target:spec`; **17/58** não possuem runner correspondente naqueles scripts (Balances #8–17, CashGroup #50, GovernanceAction #51–52, oldAccountContext #54–57). Os runners mapeados ao `Target Contract` canônico constam linha a linha na matriz R8/R9 e no manifesto R7. **Não foi compilado nenhum desses targets nesta rodada.**

Compiladores declarados **não homogêneos**: `runAccountContext`/SetAccountContext → GetterSetterHarness `solc7.6`; `runAccountPortfolio`/AccountPortfolio → AccountPortfolioHarness `solc7.6`; `runActiveCurrencies` → AccountPortfolioHarness `solc7.6`; `runDateTime` → DateTimeHarness `solc7.5`; `runGovenanceOwner` → GovernanceActionHarness `${SOLC}/solc7.5`; `runLiquidityCurve` → LiquidityCurveHarness `solc7.6`; `runPortfolio` → AccountPortfolioHarness `solc7.6`; `runSanity` → FreeCollateralExternal `solc7.6`; `runSettlement` → SettlementHarness `${SOLC}/solc7.5`; `runValuation` → ValuationHarness `${SOLC}/solc7.5`. O `verify.sh` principal cita Brownie OpenZeppelin 3.4.0-solc-0.7 e Compound, sem package hashes do run. A diferença de versão é bloqueio semântico/ABI; **5 VERIFIED/53 NOT_STATED** do catálogo permanecem, não alterar #32/#34 a partir de agregado documental antigo.

## Contrarrevisão READ-ONLY — PR #39 (AGENTE-01), Furucombo

PR existente [#39](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39) HEAD `8267dcdf8114dd856e0bffca7c3e6de36b0102d5`, consultadas revisão e evidências R8 do AGENTE-01. Fonte histórica `dinngo/furucombo-contract@c90dec1046e5e26edf70f985dd86381403912482`:
- [`specs/libParam.spec:1–31`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L31), blob `096f9f704226a7aa77c3d0da3862644db5051eb3`: `noThrow` e `noRevert` são regras **distintas**. `complete/10/33.spec` mantém `methods` `envfree`, guardas, `getParams@withrevert`, `f@withrevert`, `assert !lastHasThrown`; `complete/10/34.spec` mantém **`require false;` no ramo `getParams`** e `assert !lastReverted` para o `else`. O ramo excluído não é comprovado. `envfree` não é summary; o `LibParamHarness.sol` externo não é função interna pure da biblioteca.
- [`LibParamHarness.sol:10–14`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L10-L14), blob `e31683f3b63a95d3522f897748d0d13159388a15`: `isStatic`/`getParams`/`getNumOfReferences` externos, mas receiver pós migração exige adjudicação. [`libParam.sh:1–4`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/libParam.sh#L1-L4) seleciona `LibParamHarness` sem o Perl de handlers.
- `libParam.spec` **não declara ghost nem hook**; isso não permite introduzir ghost/hook do outro cluster. Para as regras existentes, `@withrevert` e os observáveis `lastHasThrown` versus `lastReverted` não devem ser unificados sem justificar semântica histórica e caminhos de revert. Há **15 method literals em comentários** inventariados no PR AGENTE-01, que não geram erro parser ativo (14 em incomplete/11–12 e um em /23). Os dois parser failures históricos P10/complete/33–34 eram do AGENTE-01 R5; não são novos resultados deste agente.
- Na R8 de AGENTE-01, hipótese Solidity `stack_slot` é identificador gerado para variáveis em inline assembly solc0.6.12; também há 20 fontes na união textual Proxy e HMaker/HBalancer/HSCompound ainda não compilados. Sem alterações no PR #39.

## Próximos dois gates individuais

1. **P5/incomplete/14, única nova tentativa original desta rodada:** o erro CVL2 agora está demonstrado. Solicitar ao coordenador autorização explícita **apenas para variante lexical em scratch** corrigindo `methods` com `function` e `;` depois de fixar receiver, ABI e comparativo com full `bridge.spec`. Essa variante ainda **não foi criada nem executada**; preservar invariants, filters, selectors, asserts, ghost/hook e reverts. Mesmo compile OK derivado não provaria equivalência.
2. **P14/19 (NoBankruptcy)**: verificar se a cadeia `getProceed/_verifyFinalState/_settleVault` realmente alcança arrays vazios e se a implementação original do calculator podia processá-los, recuperando ABI/runner auditado pós `applyHarnesses`. Apenas diagnóstico documental e, com gate, compilação em scratch de cena exata — nunca inserir precondição `require` para ocultar esse estado.

**Risco VERMELHO:** a transformação Opyn pode mudar domínio de revert/duplo burn; a ligação de métodos e o filtro de `alwaysUnSent` podem dar propriedade vacuamente verdadeira; o harness Radicle posterior não é substituto da produção auditada. **Nenhuma equivalência CVL1→CVL2 demonstrada**. Todos os 155 casos estão documentados, só 1 foi testado em CVL2 nesta rodada, 154 permanecem não testados.

AGENTE-08 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.
