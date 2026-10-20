# AGENTE-03 — RODADA 7 / EVIDÊNCIAS ROCKET JOE — P24

**Escopo:** exclusivamente Rocket Joe P24, 164 instâncias `incomplete`. PR [#36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36) **DRAFT**; baseline imutável `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Esta rodada foi **somente leitura de fontes GitHub + escrita documental via conector GitHub**. Proibição de qualquer uso do WSL comprometido mantida. **Resultado P24: 164 NOT_RUN / NOT_RUN_INFRA_BLOCKED, 0 COMPILE_OK, 0 COMPILE_ERROR, 0 PREFLIGHT_AUTH_BLOCKED, 0 SEMANTIC_PROVEN, 0 MIGRATED_COMPLETE.**

## 1. Hierarquia de fontes e identidades

| Fonte | Identificador, arquivo/linhas | Evidência positiva | Limite |
| --- | --- | --- | --- |
| Auditada | [lfj-gg/rocket-joe@ef2ef30248661b5509c52ab30af9bd0fc07f6657](https://github.com/lfj-gg/rocket-joe/tree/ef2ef30248661b5509c52ab30af9bd0fc07f6657); `contracts/LaunchEvent.sol:599,673–679`, blob `2af4cfe5472decc22ab3dd361d0117893a61539e` | Guarda e retorno issuer no commit atribuído ao relatório | Não há harness/patch/runner da execução nesse commit |
| Fork histórico posterior | [Certora/rocket-joe-1@dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10](https://github.com/Certora/rocket-joe-1/tree/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10); `contracts/LaunchEvent.sol:599,673–679`, blob `2656eb863a83ca2a53714eb0ed336f420f952dae` | Guarda com subtração; script, patches e harnesses rastreáveis | NÃO é identidade do Prover/target auditado |
| Patch | [`certora/applyHarness.patch:96–104`](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/applyHarness.patch#L96-L104); blob `abfb1eae851307c9a3e7d17a7b3e913962952845` | Hunk #7 pressupõe a guarda do fork e marca função `virtual` | `fuzz 2` no híbrido auditado **não** prova correspondência |
| Override | [`certora/harness/LaunchEventHarness.sol:114–116`](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/harness/LaunchEventHarness.sol#L114-L116); blob `1b6a42c5e397d03c921d18217364c7e67878621a` | Substitui `_safeTransferAVAX` com `IReceiver(_to).receiveETH{value: _value}()` | A execução sob o harness pode **não avaliar** a guarda base; risco distinto, sem replay |

**Verificação nova de identidade CVL por GitHub:** oito arquivos `Web3Bugs-certora/contracts/24/spec/*.spec` são byte-idênticos aos `certora/spec/*.spec` do fork, com mesmo blob Git: LEHighLevel `0f212bba0969fcc2f8b5caf8e9c1160b91fe7c7b`; LEInProgress `087da98c6029d1092d6f779a60a6a9b3438e4d74`; LEPreset `9403d0ee77f7e006c05dfa6e3d15f02d057aa02a`; LEValidStates `6d4d0814942113fa3cf0e633d0c2147895769a20`; LEVarTran `9f117b7bb61971cc3acbfafa26ca34be66290d83`; LaunchEvent `e1c229367ea7b872d738df4a40fbbdc91c3e5cf2`; Staking `2fd60f3d0e46ec0954abc0ebba31801bd01b5e17`; sanity `452a10f1268de27b5dd8e263cd27c5044c98daaf`. **A identidade de specs completas não prova identidade do Solidity ou da ABI e os 164 extratos `N.spec` não são a full-spec original.**

## 2. Guarda: comparação formal sobre domínio permitido, sem prova de alcançabilidade

Sejam `b=address(this).balance`, `r=avaxReserve` e `v=_value` como `uint256` (todos em `[0,2^256−1]`). Em `LaunchEvent.sol:675`:

- **Auditado A:** `b >= r`. Não utiliza `v` no guard.
- **Fork B:** avalia `b - v >= r` em Solidity 0.8.x. **Se `v > b`, a subtração aritmética causa revert antes do `require`;** quando definida (`b>=v`), a condição é equivalente, em inteiros matemáticos, a `b >= v + r`.
- Logo a região que satisfaz B está **contida** na que satisfaz A, pois `v>=0`: `B => A` (comparação de guardas de sucesso, não de contratos). Para `v=0`, as condições são idênticas. **Não há equivalência universal:** em `b=100`, `r=80`, `v=30`, A é verdadeira, B é falsa (70 não é ≥80). Este testemunho é matemático e cabe no domínio `uint256`, mas **não prova estado alcançável, pré-condições de chamadas, reentrância, resultado do Prover ou vulnerabilidade explorável**.
- Fonte também diverge em `LaunchEvent.sol:599`: quando `pair==0`, o auditado retorna `tokenIncentiveIssuerRefund`, enquanto o fork retorna `0`. Dois pontos de divergência no mesmo arquivo, não apenas Hunk #7.
- `LaunchEvent.sol:387–397,503–507,565–568` inclui usos de `_safeTransferAVAX`; a configuração de harness substitui o corpo em `LaunchEventHarness.sol:114–116`. **Uma comparação do guard isolado não estabelece igualdade das trajetórias instrumentadas**.

### Staking: reordenação antes de chamada externa

| Contrato exato | Blob / linhas | Ordem observada |
| --- | --- | --- |
| Auditada `RocketJoeStaking.sol` | `6f970060b271826b98c70f58131211454c3682a6`, `withdraw:143–149` | `user.amount -= _amount`; `user.rewardDebt = ...`; `_safeRJoeTransfer(...)`; **`totalJoeStaked -= _amount`**; `joe.safeTransfer(...)` |
| Fork `RocketJoeStaking.sol` | `ae45dd7493c87c9451118c687e1ce77db8668bc3`, `withdraw:143–150` | `user.amount -= _amount`; **`totalJoeStaked -= _amount`**; `user.rewardDebt = ...`; `_safeRJoeTransfer(...)`; `joe.safeTransfer(...)` |

Esta é uma diferença de ordem de efeitos e do estado intermediário potencialmente observável em chamadas, **não prova de reentrância alcançável**. O `RocketJoeStakingHarness` do fork (blob `367bbcae7952ea7ad8a016969a1b428184a4b15c`) importa `../munged/RocketJoeStaking.sol`, expõe getters e inicializa via construtor; nenhuma identidade com target do relatório foi encontrada.

## 3. Revisão de caminhos e dependências

| Driver do fork | Arquivo/linhas e blob Git | Teste de identidade e bloqueio |
| --- | --- | --- |
| `sanity.sh` | [1–26](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/scripts/sanity.sh#L1-L26), blob `a3f398159145e62b757ecf234f3200295566d9f2` | Executa `make -C certora munged`, target `LaunchEventHarness:certora/spec/sanity.spec`, links explícitos, `--solc_map` contendo `solc8.6` e `solc6.12`, `--method "depositAVAX()"`. Esses flags são evidência **do fork**, não run PDF |
| `verifyStaking.sh` | [15–25](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/scripts/verifyStaking.sh#L15-L25), blob `c45f10b2694a08b337059fbad4b0d11e474b7c54` | **Target `RocketJoeStakingHarness`**, `certora/spec/Staking.spec` existente, `--solc solc8.6`, `--link joe=DummyERC20Impl, rJoe=RocketJoeToken` |
| `stakingRule.sh` | [11–29](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/scripts/stakingRule.sh#L11-L29), blob `766a9f0adc54ea447f80c14d70c0466b6c7bdae9` | Target **`RocketJoeStaking`** (não harness); `certora/spec/staking.spec` (minúsculo) retornou **404** no commit, mas `certora/spec/Staking.spec` existe (blob `2fd60f3d0e46ec0954abc0ebba31801bd01b5e17`); também usa `msg=$2` após testar somente `$1` |
| `verifyLEVarTran.sh` | [1–24](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/scripts/verifyLEVarTran.sh#L1-L24), blob `5f71d4e2089bb1bfb78ec812a3458c3fecff71a8` | Pede `certora/harness/Owner.sol` + `--solc_map Owner=solc8.6`: arquivo consultado no commit fixo retornou **404**. `OwnerA.sol` (blob `64b711337368121e166f756897742f5ea49dd966`) e `OwnerB.sol` (blob `d6e4047332ad00db845dc808f9e6d9f43b37f9c9`) existem, mas **não são o mesmo arquivo ou target** |

As consultas específicas a `certora/specs/Staking.spec`, `certora/specs/staking.spec`, `certora/specs/sanity.spec` retornaram 404. **Isto não é prova de que nenhum outro commit ou repositório histórico contenha tais arquivos.** Os 12 registros de `round6_import_closure.csv` já documentam resolução **textual** da cena do fork: para `sanity.sh`, 10 roots, 47 arquivos Solidity, 59 arestas, zero caminhos ausentes nas versões OZ 4.4.1 e 4.4.2 pesquisadas; para `verifyStaking.sh`, 3 roots, 15 arquivos, 19 arestas, zero ausências nesse grafo; `verifyLEVarTran.sh` permanece sem `Owner.sol`. Um fechamento textual não comprova ABI, linkagem histórica, compilação `solc` nem CVL2.

## 4. ÚNICO cenário futuro de compile-only — **FORK-ONLY**, sem replay

**Candidato exclusivamente P24/incomplete/164 `sanity`** (N.spec SHA256 `852ef92957b7d31e844ae41c7e7c4307056e2bb53d6446a4073c8846870070c9`, valor aferido e herdado de R6; full CVL `sanity.spec` blob `452a10f1268de27b5dd8e263cd27c5044c98daaf`). A regra envolve `rule sanity(method f)` e `assert false`, útil para sondar executabilidade/vacuidade mas não verificar um requisito de segurança por si.

**Plano condicionado, NÃO EXECUTADO:** após recuperação do WSL e autorização do coordenador, criar scratch isolado, fixar fork `dba90f9`; copiar sem mudança o N164 original para scratch e provar SHA256 e `cmp`; usar patch original apenas nesse scratch, exigir `--fuzz=0`; validar hashes de `munged`, OZ 4.4.2 do lock do **fork** e todo grafo; conferir versão/hash dos binários `solc 0.8.6/0.6.12`, `--link`, `--solc_map` e comportamento de `--method depositAVAX()` do `sanity.sh` versus a quantificação `method f`. **Apenas após fixar ABI e receiver:** invocar diretamente Certora CLI com `--compilation_steps_only`, sem Prover, sem credenciais, timeout ~60s, log stdout/stderr/exit e todos os hashes. Não rodar `make`/script original sobre a árvore preservada. **Mesmo eventual exit 0 seria COMPILE_OK apenas desse N164 e scene fork, nunca VERIFICATION SUCCESS ou equivalência CVL1→CVL2.** Não criar `results/cvl2` sem gate individual.

**Fora da fila de compilação atual:** Staking (19) tem drivers/targets concorrentes e mudanças de ordem no Solidity; LEVarTran (19) pede Owner.sol ausente; 77 specs sem runner dedicado, 3 LEInProgress sem runner; 46 com histórico da ABI/prover pendente. Nenhuma migração, mudança de signature, cast, `require`, `assert`, hook, ghost ou summary foi feita.

## 5. Contrarrevisão independente **READ-ONLY** PR #42, HEAD `3cd8f72c35d94b4a48cb6155628cba4bea378c67`

| Verificação | Fontes verificadas | Conclusão conservadora |
| --- | --- | --- |
| P12/complete/23 `setBorrowing`, /25 `setUsingAsCollateral` | `round5/P12_TARGET_ABI_AND_DIAGNOSTICS.md`, `round6/ROUND6_REVIEW.md` | Na ABI snapshot, wrappers públicos não têm `address user`; no auditado, métodos possuem `address user`. Essa variável não cria necessariamente mapa de storage diferente, mas muda selectors e domínio de quantificação. N.spec byte-original teve CVL2 **EXIT 1** por `methods` sem `function;`; `solc ABI EXIT 0` do snapshot **não** é COMPILE_OK CVL2. O full-spec P12 tem 7 methods, 4 invariants e 4 rules; cada extrato 23/25 tem 2 methods e 1 rule. |
| P15/incomplete/36 `limitOnDiscountRate` | `round6/ROUND6_REVIEW.md`, `round6/P15_36_CVL2_COMPILE_LOG.txt` | **EXIT 1 real** de typechecker local (Certora 8.19.0) por seis methods sem `function` e `;` nas linhas 7–12; não é erro de auth. O runner verifica `GhoDiscountRateStrategyHarness`, diferente da target nominal. GHO patch altera `require` e visibilidade; full-spec inclui 5 rules e 2 helpers adicionais. **Não afirmar que corrigir parser comprovará equivalência ou non-vacuity.** |

O PR #42 permanece Draft; nenhuma branch, artifact ou resultado desse agente foi modificado. **Riscos gerais da documentação oficial:** summaries só aplicam ao contrato selecionado por default em CVL2; usar wildcard/receiver e `envfree` pode alterar o universo; axiomas/ghosts/hooks e `@withrevert` exigem comparação dos contextos completos. [Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html).

## 6. Pedidos explícitos ao coordenador

1. **Intervenção humana** sobre WSL: aplicar gate de `ROUND6_WSL_IO_INCIDENT.md`; nenhuma escrita, teste ou compilação em WSL até comprovar saúde do filesystem, worktrees e binários.
2. Adjudicar a identidade da cena auditada versus fork; recuperar `Owner.sol` e runner/casing Staking em commits comprovados, sem stub/renomear originais; decidir diferença das guardas e do `withdraw`.
3. Caso deseje **único diagnóstico fork-only N164**, autorizar individualmente target `LaunchEventHarness`, patch `fuzz=0`, inputs, solc/ABI e tratamento de `--method` antes de qualquer compilação.
4. Depois de recuperado WSL, exigir os três validadores históricos e `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD`, registrar cwd, stdout/stderr, exit e HEAD **da execução efetiva**. CI estrutural GitHub **não substitui** essas etapas.

**Alerta: LARANJA (bloqueios históricos) + VERMELHO operacional (WSL). AGENTE-03 — RODADA 7.**
