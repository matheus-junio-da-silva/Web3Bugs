# AGENTE-01 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS (P10)

**PR existente:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 — `research/cvl2-agente-01`, manter **DRAFT**, sem merge ou Fase 2. HEAD de partida confirmada `a9f881bf5cb6158b6614554cd4d0250f34ca340a`; baseline original imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Origem PropertyGPT de referência `687f654c679ed45ab127b7949e2a29c8f5e491b9`. A pesquisa Furucombo usa, como fonte antiga separada, `dinngo/furucombo-contract@c90dec1046e5e26edf70f985dd86381403912482`; nunca confundir estes commits.

**Revisão coordenador:** comentário mais recente do PR #39 `pullrequestreview-5590730811`. PR #47 foi **mesclado apenas como instrumentação de QA documental** no commit `6f640b76cfbde49a6d76bc708799e8c4d7fb3f30`; os registros `ROUND7_DASHBOARD.md`/`ROUND7_PROGRESS.csv` estão nesse commit em main. O PR #47 fechado não autoriza merge do PR #39. O painel mantém **1.386** instâncias com pesquisa, **4** compile-only CVL2 EXIT 0 restritos, **12** COMPILE_ERROR reais, **1.370** sem teste CVL2 válido, **zero** equivalências e **0/23** projetos formalmente migrados. Esses indicadores globais não são execuções próprias da R8.

### Política e consultas concluídas antes de escrever

Os quatro documentos imutáveis de catálogo foram lidos diretamente no commit baseline: `docs/spec_catalog.md` blob `7211e9899e406c304c4828b5d02d221b5aa52b3f`, `docs/spec_catalog_workflow.md` blob `aa6fd6413c3be6487d6508f0795a08655feb84d9`, `docs/spec_catalog_project_1.md` blob `fd5ed8777cd4e582e236490993f81e3285d6fb61`, `docs/standard.md` blob `df4eefcc202ca5d7c441623cee81d8fdd6ec0e9a`. Comparação P1: `results/spec/complete/1/3.spec` contém definitions/methods históricos; `incomplete/1/1.spec` e `1.txt` documentam `queue2` ausente. **`complete` só significa closure no snapshot**, não CVL2 COMPILADO.

Documentação primária: [Certora CVL2 migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [CVL2 changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [statements e reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html). Para provenance de `stack_slot`, essencial consultar a documentação **historicamente compatível** [Solidity 0.6.12 / Inline Assembly / Access to External Variables](https://docs.soliditylang.org/en/v0.6.12/assembly.html#access-to-external-variables-functions-and-libraries), e [Solidity 0.6.0 function overriding](https://docs.soliditylang.org/en/v0.6.0/contracts.html#function-overriding), sem transplantar regras da versão Solidity 0.8 para 0.6.

---

## 1. P10/complete/33 e /34: methods e riscos reais

| Fonte fixada e localização | SHA-1 Git blob | source_or_report_fact |
| --- | --- | --- |
| [`dinngo/furucombo-contract@c90dec1/specs/libParam.spec:1–31`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L31) | `096f9f704226a7aa77c3d0da3862644db5051eb3` | GLOBAL contém bloco methods envfree + `noThrow` + `noRevert` |
| [`specs/harnesses/LibParamHarness.sol:10–19`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L10-L19) | `e31683f3b63a95d3522f897748d0d13159388a15` | Cinco wrappers externos |
| [`contracts/lib/LibParam.sol:17–59`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/lib/LibParam.sol#L17-L59) | `740e8a5ccae25d5e041c9736545c13de7cd3867f` | Biblioteca interna `pure`; `getParams` tem três condições `require` adicionais |
| [`specs/scripts/libParam.sh:1–4`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/libParam.sh#L1-L4) | `3344316e9569c8292df6d47725126dfa3173c605` | target `LibParamHarness`, global `libParam.spec`, `-b=64,-smt_bitVectorTheory=true`, **sem Perl** |
| `results/spec/complete/10/33.spec` | `e55057a90f641156538f732c0fe172c28cd86dad` | N.spec traz methods mais `noThrow`, mas não a regra `noRevert` |
| `results/spec/complete/10/34.spec` | `3e180d5f3a046f2e63192cd1a464cadff5b8775a` | N.spec traz `noRevert`, **sem methods** da GLOBAL |

**Interface de fonte, NÃO ABI compilada do job:**

| method | wrapper no harness e linha | Mutabilidade declarada wrapper | Biblioteca homônima | Receiver CVL hipotético |
| --- | --- | --- | --- | --- |
| `isStatic(bytes32) returns bool` | `external`, L10 | sem `view`/`pure`/payable — `nonpayable` | `LibParam.isStatic` é `internal pure` | `LibParamHarness` (target único fixado) |
| `getNumOfReferences(bytes32) returns uint256` | `external`, L14–22 | `nonpayable` | cálculo local do harness, não getter library exportado | `LibParamHarness` |
| `getParams(bytes32)` sem `returns` no harness | `external`, L13 | `nonpayable` | `LibParam.getParams` `internal pure` retorna `uint256[] memory` duas vezes | `LibParamHarness`, literal `sig:getParams(bytes32).selector` hipotético |

**Cuidado semântico:** `envfree` não é summary e a Certora exige checks de independência do ambiente ao anotá-lo; `external` decorre do wrapper de fonte, mas não prova identidade com a cena original do Prover. `using LibParam for bytes32` não transforma os métodos de biblioteca internos em externos da ABI. `method f` pode abranger outros métodos do harness; ausência de filtro não autoriza restringir f. `@withrevert` e `lastHasThrown`/`lastReverted` não devem ser reescritos para evitar contraexemplos.

A hipótese mínima **DOCUMENTAL, sem execução** está em [`ROUND8_MINIMAL_DIFF_PROPOSAL.md`](ROUND8_MINIMAL_DIFF_PROPOSAL.md): para `33.spec`, aplicar somente `function`, `external`, receiver explícito e `;` aos dois métodos e `sig:` ao literal ativo; para `34.spec`, somente `sig:`. Isso é uma **candidatura gramatical**, não prova de ABI, de compilação ou de equivalência.

O ramo `if f.selector == getParams(bytes32).selector` de `noRevert` contém `require false;`, **preservado**. Portanto essa parte está excluída do domínio admissível; `assert !lastReverted` aplica-se ao ramo `else`, não prova que `getParams` não reverte. `noThrow` mantém os guards sobre `x` e `assert !lastHasThrown`; os requires adicionais da biblioteca `getParams` deixam aberto o risco de revert e de vacuity do conjunto de modelos.

**Observação real herdada da R5:** `complete/33` e `/34` foram executados pelo AGENTE-01 com Certora CLI 8.19.0 e solc 0.6.12, `--compilation_steps_only` sobre recortes ORIGINAIS byte-idênticos, exit **1** (methods antigos e selector sem `sig:`). Logs e SHA preservados em `10/round5/diagnostics.csv` e `10/round5/logs/`. **Nenhum teste adicional executado R8.**

---

## 2. Registry / Proxy / ProxyHarness — revisão de `stack_slot` e closure ampliada

Há **29 incomplete**: Registry `incomplete/1–11` (11), Proxy `/12` (1) e ProxyHarness `/13–29` (17). O N.txt original de `incomplete/15` (blob `81003ae05dfcae6910f0be3eb9721f8e882dea91`) e `/16` (blob `ef90a99d55a1f64012920aa788d9690726d6329`) registra o `stack_slot` como declaração ausente. **A classificação `incomplete` é um fato histórico e NÃO foi alterada**.

**Nova distinção de sintaxe confirmada pela documentação oficial:** no Solidity **v0.6.12**, uma variável de storage chamada `x` disponibiliza a identificação de slot `x_slot` dentro de inline assembly ([docs v0.6.12, Access to External Variables](https://docs.soliditylang.org/en/v0.6.12/assembly.html#access-to-external-variables-functions-and-libraries)). A declaração [`Storage.sol:8`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/Storage.sol#L8) é `bytes32[] public stack;`; `Proxy` herda `Storage` ([`Proxy.sol:14`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/Proxy.sol#L14)), e `ProxyHarness` herda `Proxy` ([`ProxyHarness.sol:6`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/ProxyHarness.sol#L6)). `ProxyHarness.getStackLengthSlot()` contém `assembly { x := stack_slot }` ([L14–19](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/ProxyHarness.sol#L13-L20)).

**Conclusão qualificada (INFERENCE, não compiled proof):** `stack_slot` provavelmente corresponde ao *nome gerado pelo compilador* para o slot da variável herdada `stack`, e não precisa de declaração literal em `Storage.sol`. O impedimento anteriormente descrito apenas como "símbolo faltante" deve ser rebaixado documentalmente a `ASSEMBLY_0_6_STORAGE_SLOT_SYNTAX_SUPPORTED__SCENE_NOT_COMPILED`. **Não** inferir que o target inteiro compila, o valor numérico final do slot, nem substituir por `stack.slot` da sintaxe Solidity posterior. O N.txt imutável fica registrado como classificação original, não como diagnóstico novo.

**Outro gate não resolvido, potencialmente mais bloqueante:** [`ProxyHarness.sol:41,57,68,78`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/ProxyHarness.sol#L41-L95) marca `_parse`, `_trim`, `_exec`, `_execs` como `override`. As funções correspondentes da base [`Proxy.sol:116,164,201,233`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/Proxy.sol#L116-L237) não exibem `virtual`. A documentação [Solidity 0.6 Function Overriding](https://docs.soliditylang.org/en/v0.6.0/contracts.html#function-overriding) exige `virtual` na base. **Possível incompatibilidade de herança a ser testada via solc**; não é um COMPILE_ERROR observado. Além disso, o harness usa tipos de arrays `bytes32[2]` nos overrides de `_parse/_trim` contra `bytes32[256]` da base, com risco adicional de assinaturas incompatíveis.

**Fechamento apenas textual de source/SHAs:**
- Na R7, `Registry.sol` e `ProxyHarness.sol` como raízes fecharam **16** arquivos Solidity distintos (hashes em `10/ROUND7_SOURCE_MANIFEST.csv`) com dependências `@openzeppelin/contracts/*` da tag `OpenZeppelin/openzeppelin-contracts@6be5ffe54fc8982b7c1d0f45d4cb7bbd313107cd` (v3.3.0).
- Nesta R8, foram adicionados **quatro arquivos distintos** para os seeds **efetivamente nomeados** em `specs/scripts/proxy.sh`: `DummyERC20A.sol` blob `b47441c13741ad73edcb835cfc296bb3a6b31cfc`, `DummyERC20B.sol` `5c9dc6bc6508dac4a8c2c4407008fce5d48e90e7`, `Summary.sol` `1e91873ab8cdab1e81e36ebfd0cdb471797bb7ad` e `DummyERC20Impl.sol` `991a0806ccc929d1217f9734525f272a48db8b3a`. `A/B` importam `DummyERC20Impl.sol`, `Summary` importa `A` e `DummyERC20Impl` não tem import Solidity no blob examinado.
- Dessa forma há **20 fontes Solidity únicas na união dos seeds de `proxy.sh`**, com imports textuais resolvidos nos commits citados; a closure de source é uma **INFERENCE fundamentada em imports**, não ABI executada nem prova de resolução de todos os contratos pós-patch ou dos flags do job original.
- Runner Registry: [`registry.sh`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/registry.sh) (blob `bdc1dbeb52619db0e3b80432082221b467e74946`), target `Registry`, sem Perl. Runner Proxy: [`proxy.sh`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/proxy.sh) (blob `653607e3a26ee35581cf04eae93d33de55e81071`), cinco seeds e flags `-assumeUnwindCond,-b=2`. Runner `privProxy.sh` para `Proxy` (blob `0df5e2a0ebcf4cf369b5d32fed8303aa5c811905`) é outro contexto. Não misturar cenas distintas nem inventar remapping.

**Missing proof:** compilador/versão com hash verificado para todos os seeds, `solc --storage-layout`/ABI da cena exata, herança/array overrides, vínculo com o runner CVL GLOBAL e o conjunto de summaries/havocs. Nenhuma execução solc ou CVL2 na R8.

---

## 3. Handler HMaker e duas outras famílias de incompletos com hashes

### HMaker — 11 N.spec

IDs `incomplete/{31,37,38,39,40,129,130,131,132,133,134}`. [`runHMakerSpecific.sh`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/runHMakerSpecific.sh) blob `e2e559577cfe523f8e0932d4f6ff08733c1327b8` chama `_runHandler.sh HMaker maker ./specs/hmaker.spec 3`; `_runHandler.sh` blob `b603b618b4e85782cc63b9b97101a928c350636b`; fonte [`HMaker.sol`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/handlers/maker/HMaker.sol) blob `71bdc74f488d12cb058ebabff777c4fd3481bb79`, `HandlerBase.sol` blob `a8bb5407eefacc1186272b6063913054232bb6da`, `hmaker.spec` blob `5ca9e440cf8d7265d44ad9b7b959021e667c0acd`.

**source_or_report_fact:** [`_runHandler.sh:38–66`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L38-L66) marca `_revertMsg` na base `virtual` e injeta no handler que tem match textual `is HandlerBase {` getters `getSlot/getStackLengthSlot/getStackLength/ethBalance` **external** e `getSender/getCubeCounter/isHandler` **public** sem `view`. Também injeta override `_revertMsg` cujo corpo chama `revert()`, diferentemente da mensagem composta da base. [L67–73](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L67-L73) troca import `SafeERC20.sol`→`ERC20.sol`, tokens `safeA`→`a`, `safeT`→`t` e alguns `constant`. [`hmaker.spec:1–55`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/hmaker.spec#L1-L55) usa `using`, `DISPATCHER(true)`, `NONDET`, receiver `summaryInstance`, assinatura sighash legada `0x12345678`; a função `arbitrary(f)` aparece nas linhas 62–69.

**Inference / missing_proof:** no `HMaker.sol:9` há match literal de herança direta, portanto o script **seria aplicável ao input**; isso não demonstra o output real do Perl histórico, o pacote OZ exato após substituição, ABI ou o Prover. A mudança de revert message pode afetar semântica e contraexemplos. Não simular patch nem aplicar a `N.spec`; **0 ABI gerada na R8**.

### HBalancer — 11 N.spec, recuperação documental importante

IDs: `incomplete/30,65,66,67,68,171,172,173,174,175,176`. **N.txt baseline** de `incomplete/30` blob `7bdcaa9d1947328cb50757a797da921cc5976e48` e `/65` blob `acf42a3a950d08f445e34629065b746686d53a06` documentam que a fonte do handler falta no snapshot PropertyGPT. **Isso continua verdadeiro para o snapshot**.

**Fonte adicional efetivamente recuperada:** [`dinngo/furucombo-contract@c90dec1/contracts/handlers/balancer/HBalancer.sol`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/handlers/balancer/HBalancer.sol) blob `f1d09c9f4c4c55d1ec5f3f28f60a1f6068c2e797`, com imports de `HandlerBase`, `IDSProxy`, `IBPool`, `SafeERC20` e `SafeMath`. Runner [`runHBalancerSpecific.sh`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/runHBalancerSpecific.sh) blob `0fc1a099520afe9ec045d1be6247cc56c4d5defa` chama `_runHandler.sh HBalancer balancer ./specs/hbalancer.spec` **sem quarto argumento**, portanto o script utiliza seu `B=2` default, diferente de HMaker B=3. `hbalancer.spec` blob `61e07d4fea18476da2db8e268d49658fe5aa9a8f`; interface `IBPool.sol` blob `ed2707d80a675467b0697d3304a4ac37687980d4`.

**Adjudicação:** `SOURCE_RECOVERED_IN_AUDITED_2021_REPOSITORY` reduz o bloqueio de *disponibilidade de fonte*, mas **não reclassifica os 11 `incomplete` originais**, nem comprova que o código desse commit foi efetivamente usado no job auditado. A matriz antiga `perl_getter_scope_matrix.csv` citava `HandlerBase.sol` como `source` de HBalancer por falta no snapshot; a pesquisa R8 identifica a fonte adicional, não edita o registro anterior. Pendem script pós-Perl, versão/ABI, remappings e correspondência de artefatos com a spec GLOBAL.

### HSCompound — 11 N.spec, efeito concreto da renomeação

IDs: `incomplete/32,49–52,147–152`. [`HSCompound.sol`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/handlers/compound/HSCompound.sol) blob `b0c34faa33d62e213eb043085bbb63ab9d46b29a`, declara `claimComp(address dsProxy)` e herda diretamente `HandlerBase`. Runner `runHSCompoundSpecific.sh` blob `541c96d9ac356b727cd1428e9cf4e875bfac355a` aponta para `_runHandler.sh HSCompound compound ./specs/hscompound.spec 3`; GLOBAL `hscompound.spec` blob `98c8742bdc65f0178ebea1815c6fbe98d04afa75`. O Perl possui substituição específica `function claimComp(`→`function unique_claimComp(` em HSCompound (e HComptroller).

**Fonte/relatório:** `incomplete/32.txt` blob `ea13b230955ea70ebd961ec185828a1e0dfdc5f7` registra imports que faltavam no snapshot e transformations não aplicadas; `incomplete/49.txt` blob `15ce1d4cb4210ed61530c819b0a615cb396d8004` registra a mesma classe de blocker. A renomeação pode afetar selector de função/calls e universo `method f`; **não assumir equivalência**. Fonte 2021 tem imports `SafeERC20.sol` em caminho antigo; o snapshot registra caminho diferente. Pendem inputs binários, output pós-Perl e seleção do receiver/summary.

### Sanity / incomplete/35

`incomplete/35.txt` blob `75e9ce0bf80e2bcb03e69293c0e39d49d4ccff5f` permanece sem target/runner atribuível. O N.spec contém `sinvoke` legado e `assert false`; escolher target aleatoriamente produziria comportamento artificial. Nenhuma execução.

As fontes e hashes adicionais HBalancer, HSCompound e seeds Proxy foram versionadas em [`ROUND8_CLOSURE_DELTA.csv`](ROUND8_CLOSURE_DELTA.csv) — 14 entradas. Os `N.txt` são citados como fatos originais, sem qualquer correção in-place.

---

## 4. Cross-review do AGENTE-02 / PR #37, SOMENTE LEITURA

Lida a HEAD [`4ceac5d5e988dba5b54c44d5678f486a6dabc5af`](https://github.com/matheus-junio-da-silva/Web3Bugs/commit/4ceac5d5e988dba5b54c44d5678f486a6dabc5af), PR #37 Draft. O `AGENTE-02/ROUND7_EVIDENCE.md` e `ROUND7_MATRIX_181.csv` mostram:

| P18 | Evidência de fonte e limites |
| --- | --- |
| `complete/3` `grantRoleEffect`, target `AccessControlMock` | `grantRole` e `hasRole` são `public`; N.spec 2 entradas `methods`, GLOBAL `AccessControl.spec` contém outras regras e métodos. O coordenador, **não** o AGENTE-01, fez `--compilation_steps_only` no fragmento original: EXIT 1 por falta de `function`/`;`. Seleção `internal` vs `external` ainda não homologada. |
| `complete/23` `noTransferEffectOnApproval`, target `ERC1155Mock` | N.spec 2 métodos, GLOBAL `ERC1155.spec` 12. `isApprovedForAll`/`safeTransferFrom` públicos; em `safeTransferFrom` implementação `bytes memory`, interface `bytes calldata`. O coordenador obteve também EXIT 1 por `methods` histórico; nenhuma equivalência ou escolha de receiver. |
| Proposta do AGENTE-02 para `complete/4,46,53` | `/4` AccessControl com `revokeRole` público; `/46` Burnable/Mock têm métodos `burn` com permissões distintas; `/53` dois selectors tipados, `require paused()` e `@withrevert`. **NOT_RUN** de parser para os três; só hipóteses lexicais. |

A fonte de ambos os erros reais P18/3 e /23 é `docs/cvl2/coordination/P18_DIRECT_CLI_CONTRACHECK.md` na coordenação, executor **coordenador**, CLI 8.19.0/solc0.8.6, dois N.spec byte-idênticos. Os nove `PREFLIGHT_AUTH_BLOCKED` do AGENTE-02 em testes antigos não são compilação. O AGENTE-02 tampouco reexecutou parser na R7. A branch do AGENTE-02 **não** foi alterada.

**Julgamento de revisão:** não há prova de escopo dos summaries de GLOBAL, relação internal/external do método público nem igualdade entre ABI do snapshot e contrato do job auditado. Exigir evidência do Prover/job/target e semântica do f-domain; um source ABI compilado via solc não sana o CVL2 parser nem demonstra equivalência.

---

## 5. Matriz de progresso, QA, gaps e próximos gates

Arquivo [`ROUND8_MATRIX_266.csv`](ROUND8_MATRIX_266.csv): uma linha por `(project_id,original_status,example_id)`, **266 linhas, sem exceções**, Bug Label, Property, Target, Result, Detection Outcome e originais `Spec`/linha intocados. Para cada chave: Git blob SHA do `N.spec` e `N.sol`; blob do `N.txt` onde lido, fonte/commit, runner, última execução realmente observada (responsável, rodada, exit/log), execução R8 separada, risco de vacuidade, `source_or_report_fact`, `inference`, `missing_proof` e próximo gate. O CSV foi reconciliado via **GitHub connector**, não por scripts Python locais.

| Métrica exclusiva P10 | Resultado real |
| --- | ---: |
| Casos com documentação/matriz de pesquisa | **266 / 266** |
| Compilações `--compilation_steps_only` executadas **na R8** | **0** |
| `COMPILE_OK` atribuíveis ao P10 | **0** |
| `COMPILE_ERROR` reais atribuíveis ao P10 | **2**, **executados apenas na R5** |
| Casos sem compilação CVL2 atribuível | **264** |
| R8 `NOT_RUN_INFRA_BLOCKED` | **266** |
| `SEMANTIC_PROVEN` | **0** |
| P10 integralmente migrado | **NÃO** |

**Riscos vermelhos:** (i) alterar universo `method f`/receiver `envfree` e concluir vacuamente; (ii) remover `require false` /34 ou tratar ramo excluído como provado; (iii) aceitar ProxyHarness sem verificar herança/override/tipos/ABI; (iv) aplicar o Perl HMaker/HSCompound/ HBalancer ao snapshot original ou fingir que alterou só ABI; (v) confundir fonte HBalancer 2021 recuperada com o job original; (vi) classificar EIO, falta de tokens, `solc --abi` ou CI como CVL2 comprovado.

**Duas experiências prioritárias para revisão do coordenador, NÃO EXECUTADAS:**
1. `E1` — P10/complete/33: CLI/solc0.6.12 fixados e hashes/cmp, apenas scratch e diff lexical mínimo do `methods` + `sig:`; confrontar fragmento com `libParam.spec` GLOBAL em execuções distintas, preservar `envfree`/`lastHasThrown` e domínio de f.
2. `E2` — P10/complete/34: somente `sig:` em scratch com controle original, **`require false;` intocável**, `lastReverted` inalterado, distinguir cenário GLOBAL vs N.spec e demonstrar não-vacuidade antes de qualquer conclusão. **Gate separado** do 33.

Teste adicional de dependências aguardando infraestrutura: compilação Solidity 0.6.12 da cena Proxy completa para testar `stack_slot`, `virtual/override` e arrays; Perl pós-script HMaker/HBalancer/HSCompound com SHA de árvore de entrada/saída e ABI, sempre sem tocar originais. Não promover `00_unchanged`, `01_documented`, `COMPILE_OK` ou `SEMANTIC_PROVEN` apenas por sugestão lexical.

**Bloqueio operacional:** WSL `DESKTOP-5E26TVU` sem recuperação humana atestada (spawn EIO/SIGBUS/EROFS); **nenhuma operação, script, scratch, solc ou CLI foi executado nele nesta rodada**. Três validadores históricos e `git -c core.whitespace=cr-at-eol diff --check BASE...HEAD` são `NOT_RUN_INFRA_BLOCKED`, registrados no [`ROUND8_QA.md`](ROUND8_QA.md). GitHub CI de integridade (caso concluído) não substitui esses comandos nem Prover.

**AGENTE-01 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.**
