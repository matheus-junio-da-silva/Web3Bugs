# AGENTE-01 — RODADA 7 / Evidência e gates técnicos — P10 Furucombo

**Escopo exclusivo:** Projeto 10, 266 instâncias (2 complete, 264 incomplete). **PR existente:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39, branch `research/cvl2-agente-01`, Draft, sem merge. **HEAD de partida confirmada:** `58ca698ab8e1b81ee205a471d5d1cb98bb472ff9`; baseline `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` intocável.

Coordenação consultada: PR #39, revisão mais recente `pullrequestreview-5590007290`; PR #47, HEAD `948121599b546d61579dc9ecb8c316f9c088e78a`, documentos `ROUND6_DASHBOARD.md`, `ROUND6_PROGRESS.csv`, `ROUND6_COMPILATION_OBSERVATIONS.csv`, `ROUND6_WSL_IO_INCIDENT.md`. Há 1.386 instâncias globalmente, 4 compile-only exit 0 restritos, 12 COMPILE_ERROR reais, 1.370 sem execução CVL2 observada, **zero** equivalências. Esses valores **não são execuções deste agente**.

## 1. Integridade da pesquisa e semântica CVL2

Lidos os quatro documentos canônicos `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md` e `docs/standard.md`; referência P1: `complete/1/3` inclui `methods`, definição transitiva `stateVariableUpdate` e assertion histórica, enquanto `incomplete/1/1` explicita ausência de `queue2`. Complete/incomplete é **fechamento das dependências do recorte catalogado**, não compilação CVL2 e não prova. Os valores Result/Detection Outcome são históricos, independentes do estado atual da pesquisa.

Fontes oficiais de CVL2 consultadas:
- [CVL2 migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html): métodos exigem `function`, `;`, `internal/external` e avaliação de receiver; `envfree` é anotação de interface e **não** summary por si só. No CVL2, `envfree` omite ambiente nas chamadas CVL e exige check adicional da independência de ambiente. Um receiver sem prefixo denota `currentContract`, não todos os contratos, e `_.` não é substituto automático.
- [statements](https://docs.certora.com/en/latest/docs/cvl/statements.html) e [methods / summaries](https://docs.certora.com/en/latest/docs/cvl/methods.html): `require` exclui modelos com guarda falsa; `@withrevert`, quantificação por `method f`, alcance de chamadas internas/externas e summaries devem ser preservados. O CLI/typechecker não demonstra equivalência de contraexemplos.
- [ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), documentação de invariants: propriedades de estado podem depender de storage/ghost revert/havoc; não inserir, remover ou reescrever regras desses tipos com base na ausência delas em um fragmento.

O WSL `DESKTOP-5E26TVU` teve EIO/SIGBUS/EROFS e **não possui recuperação atestada**. Por instrução expressa da coordenação, nesta rodada **nenhum comando foi enviado ao WSL**, nenhum clone ou scratch criado, nenhum compilador/prover/perl/patch executado. Todas as inspeções e commits foram feitos por conector GitHub; evidências históricas vêm de objetos já pinados, não de um novo build.

## 2. LibParam: spec GLOBAL versus N.spec 33–34

Commit da fonte auditada: `dinngo/furucombo-contract@c90dec1046e5e26edf70f985dd86381403912482`.

| Objeto / linhas | Git blob SHA-1 | Evidência |
| --- | --- | --- |
| [`specs/libParam.spec` L1–31](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L31) | `096f9f704226a7aa77c3d0da3862644db5051eb3` | Mesma GLOBAL contém `methods`, `noThrow`, `noRevert` |
| [`specs/harnesses/LibParamHarness.sol` L1–22](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L1-L22) | `e31683f3b63a95d3522f897748d0d13159388a15` | Cinco wrappers `external`, incluindo `getParams` (sem return externo) |
| [`contracts/lib/LibParam.sol` L13–61](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/lib/LibParam.sol#L13-L61) | `740e8a5ccae25d5e041c9736545c13de7cd3867f` | Biblioteca `internal pure`; `getParams` tem requires adicionais |
| [`specs/scripts/libParam.sh` L1–4](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/libParam.sh#L1-L4) | `3344316e9569c8292df6d47725126dfa3173c605` | `certoraRun ... --verify LibParamHarness:specs/libParam.spec`, `-b=64,-smt_bitVectorTheory=true`, **sem Perl** |
| `results/spec/complete/10/33.spec` | `e55057a90f641156538f732c0fe172c28cd86dad` | Registra `methods` mais `noThrow` |
| `results/spec/complete/10/34.spec` | `3e180d5f3a046f2e63192cd1a464cadff5b8775a` | Recorte `noRevert` **não copia** `methods`; não é a GLOBAL |

O grafo de importação direto é exatamente `LibParamHarness.sol -> ../../contracts/lib/LibParam.sol`. Não entra no Perl de handlers nem alcança OpenZeppelin por imports Solidity; isso não demonstra execução/versão Certora histórica. Os métodos `isStatic(bytes32)` e `getNumOfReferences(bytes32)` são **external no harness**, não equivalentes às rotas `internal pure` da biblioteca. O `getParams(bytes32)` externo é `void` (não retorna as duas arrays da biblioteca internal) e preserva os requires do código `LibParam.getParams`.

**Hipóteses DOCUMENTAIS mínimas, sem patch executado:**

```cvl
methods {
    function LibParamHarness.isStatic(bytes32) external returns (bool) envfree;
    function LibParamHarness.getNumOfReferences(bytes32) external returns (uint256) envfree;
}
```

O receiver específico `LibParamHarness` evita introduzir um wildcard; a própria regra CVL2 permite também receiver implícito `currentContract` **na cena que fixa esse contrato como target**, mas a substituição não é autorizada sem revisão de call resolution. `envfree` foi preservado textualmente e continua a requerer avaliação estática; nenhuma `=>`/summary existia nessas duas entradas. Não propor `optional` ou casts para fazer o caso passar.

Nos dois arquivos, `getParams(bytes32).selector` é código ativo; proposta exclusivamente lexical `sig:getParams(bytes32).selector`. Uma sugestão `sig:` **não é bucket 00_unchanged, 01_documented, COMPILE_OK ou SEMANTIC_PROVEN**.

**`complete/33` / `noThrow`:** GLOBAL L6–19, N.spec L9–22. Os guards `e.msg.value == 0`, `!isStatic(x)`, `getNumOfReferences(x)>0`, a chamada `getParams@withrevert(e,x)` versus `f@withrevert(e,arg)` e `assert !lastHasThrown` delimitam a regra. A implementação `getParams` na biblioteca tem `require(n>0)`, `require(i<n)` e `require(i==n)`; os guards CVL acima não provam, sem execução, todas essas condições. Não substituir `lastHasThrown` por `lastReverted` em silêncio, não estreitar `method f`.

**`complete/34` / `noRevert`:** GLOBAL L21–31, N.spec L4–14. `require false;` no ramo `getParams` é parte do original e **exclui esse ramo**. A assertion `!lastReverted` após `f@withrevert` no `else` **não prova** a não-reversão de `getParams`. Adicionar o `methods` da GLOBAL ao N.spec 34 para compilar seria alterar o recorte e precisa de gate; não fazê-lo automaticamente. A assertion é booleana, não há razão constatada para cast aritmético.

**Registros de compilação (R5, não R7):** CLI 8.19.0, `solc 0.6.12`, `--compilation_steps_only`, duas N.spec originais byte-idênticas, **EXIT 1** por bloco methods antigo no 33 e selector tipado sem `sig:` no 34; logs reais disponíveis em `round5/logs/33_compile_only.log`, `34_compile_only.log`, e bytes originais em `.log.b64`. Não há uma nova compilação R7 ou variantes temporárias executadas.

## 3. Inventário exato: 13 selectors ativos, 15 comentados

O inventário documental `ROUND7_SELECTOR_INVENTORY.csv` foi reconciliado às 993 ocorrências da `semantic_candidate_gate_matrix.csv` já auditada por linha na R5, sem reescrever os `N.spec`. Identificam-se:

| Família | Código ativo | IDs do catálogo P10 |
| --- | ---: | --- |
| LibParamHarness | 2 | complete/33 L13; complete/34 L8 |
| Registry | 8 | incomplete/1 (dois L26), /2 L28, /3 (dois L26), /4 L28, /9 L22, /10 L22 |
| ProxyHarness via Proxy | 3 | incomplete/23 L21; /24 L24 e L25 |
| **Total** | **13** |  |

Os 14 tokens de `incomplete/11–12` estão em comentários, assim como `certorafallback_0().selector` em `incomplete/23:21`. **15 COMMENT_ONLY, zero transformações**. Em `incomplete/23:21`, `proxy.batchExec(address[],bytes32[],bytes[]).selector` segue **ativo** na mesma linha; o fallback comentado não exige `sig:` nem pode ser usado para reconstruir um método removido. Não alterar `assert`/filtro ou aplicar cast numa comparação de selector.

Os oito selectors Registry têm assinatura de função `external` na fonte auditada 2021 (`register`, `unregister`, `registerCaller`, `unregisterCaller`, `unban`, `unhalt`), mas **não há ABI da cena Certora reproduzida**. No Proxy, `batchExec` e `execs` são `external` em `contracts/Proxy.sol` e o target `ProxyHarness` é herdado; não extrapolar a visibilidade para calls internas/receivers ou para a ABI de job. Todas as 13 ocorrências são **candidatas gramaticais**, não migrações aprovadas.

## 4. Registry / Proxy / ProxyHarness: fonte, compilação e ABI em níveis diferentes

**Fechamento textual por imports recursivos via GitHub:** foram recuperados **16 arquivos Solidity únicos** ao partir de `contracts/Registry.sol` e `specs/harnesses/ProxyHarness.sol` no commit auditado, redirecionando somente os imports `@openzeppelin/contracts/*` para a tag `OpenZeppelin/openzeppelin-contracts@6be5ffe54fc8982b7c1d0f45d4cb7bbd313107cd` (OZ 3.3.0). **0 imports textuais sem destino nesses dois grafos.** O arquivo `ROUND7_SOURCE_MANIFEST.csv` apresenta os Git blob SHA-1 desses 16 arquivos e 10 artefatos adicionais.

Exemplos diretos: [`Registry.sol` L3–7](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/Registry.sol#L3-L7) importa `Ownable.sol` da OZ e `IRegistry.sol`; Ownable importa `GSN/Context.sol`. [`Proxy.sol` L4–10](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/Proxy.sol#L4-L10) alcança OZ `SafeERC20`, `Address`, `IERC20`, `SafeMath`, mais `IProxy`, `IRegistry`, `Config`, `Storage`, `LibParam`, `LibCache` e `LibStack`.

**Este é fechamento de SOURCE TEXTUAL do seed, não ABI ou prova de compilação.** Não certifica o tarball npm distribuído em 2021, remappings/solc/linking, nem todos os seeds do `proxy.sh`: [`proxy.sh` L7–11](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/proxy.sh#L7-L11) inclui `Registry.sol`, `DummyERC20A/B.sol`, `Summary.sol`, `ProxyHarness.sol`, `--verify ProxyHarness:specs/proxy.spec` e `-assumeUnwindCond,-b=2`. [`registry.sh` L1–3](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/registry.sh#L1-L3) usa `Registry:specs/registry.spec`. Não são a mesma cena.

**Bloqueio concreto por source:** `specs/harnesses/ProxyHarness.sol:16–20` contém `assembly { x := stack_slot }`, enquanto `contracts/Storage.sol` declara `bytes32[] public stack` e não uma declaração literal `stack_slot` no trecho examinado. Não afirmar que o identificador falha na compilação: a resolução precisa ser testada com `solc 0.6.12` na cena exata. Além disso, `ProxyHarness.sol` marca como `override` as funções `_parse`, `_trim`, `_exec`, `_execs`; as declarações correspondentes em `Proxy.sol:116,164,201,233` não exibem o qualificador `virtual` nos source blobs inspecionados. Isso constitui **suspeita específica de incompatibilidade de override**, não COMPILE_ERROR até compilação efetiva. Não reescrever bases/harness ou presumir patch não recuperado.

**Atribuição por ID:** Registry = incomplete/1–11 (11); Proxy = incomplete/12 (1); ProxyHarness = incomplete/13–29 (17); total 29. `incomplete/15–16` permanecem bloqueados por `stack_slot` e cena. Estado de todos: NOT_RUN CVL2, nunca promovidos por um import closure lexical.

## 5. Família Perl selecionada — HMaker (11 exemplos)

**Seeds de 2021:** `runHMakerSpecific.sh` [L1](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/runHMakerSpecific.sh#L1) -> `_runHandler.sh HMaker maker ./specs/hmaker.spec 3`; `_runHandler.sh` blob `b603b618b4e85782cc63b9b97101a928c350636b`. Inputs: `contracts/handlers/maker/HMaker.sol` blob `71bdc74f488d12cb058ebabff777c4fd3481bb79`; `contracts/handlers/HandlerBase.sol` blob `a8bb5407eefacc1186272b6063913054232bb6da`; spec GLOBAL `specs/hmaker.spec` blob `5ca9e440cf8d7265d44ad9b7b959021e667c0acd`.

| Ponto / linhas históricos | Transformação prevista pelo SCRIPT, **não executada na R7** | Efeito que exigiria confirmação |
| --- | --- | --- |
| [`_runHandler.sh:38`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L38) | regex adiciona `virtual` ao `_revertMsg(string,string)` do `HandlerBase.sol` | Herança/override, declaração correspondente e comportamento após transformação |
| [`_runHandler.sh:39–65`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L39-L65) | em match literal `is HandlerBase {`, injeta `getSlot`, `getStackLengthSlot`, `getStackLength` external, `getSender/getCubeCounter/isHandler` public (sem `view` neste script) e override de `_revertMsg` | HMaker linha 9 contém match direto; não assumir ABI, nem universalizar para herança indireta; o override faz `revert()`, mudando a lógica da mensagem de revert |
| [`_runHandler.sh:67–73`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L67-L73) | `SafeERC20.sol` -> `ERC20.sol`, `safeA` -> `a`, `safeT` -> `t`, remove `constant` de certos endereços | Em [`HMaker.sol:7,104,128...`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/handlers/maker/HMaker.sol#L7-L128), os matches incidem em import/uso de safeApprove e declarações; podem afetar import resolution e comportamento |
| [`_runHandler.sh:75–102`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L75-L102) | transformação global de outros handlers/interfaces, mesmo numa execução da família HMaker | Não presumir que o patch afeta apenas HMaker nem alegar resultado de ABI pós-Perl |
| [`_runHandler.sh:104–108`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L104-L108) | `certoraRun HMaker.sol Registry.sol DummyERC20A/B.sol ProxyHarness.sol Summary.sol --verify HMaker:specs/hmaker.spec --settings -assumeUnwindCond,-b=3,-ciMode=true` | Dependências, remappings, compilador e ABI de **todos** os seeds ausentes de execução reprodutível; 0 run novo |

A [`specs/hmaker.spec` L1–55](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/hmaker.spec#L1-L55) possui `using Registry/DummyERC20A/ProxyHarness/Summary`, methods `envfree`, summaries `DISPATCHER(true)` de registry, tokens e DeFi, `NONDET`, e entrada sighash `0x12345678 => NONDET` que é legado CVL1. `arbitrary(f)` e função auxiliar aparecem nas linhas 62 e 69; não é seguro reaproveitar apenas uma assertion fragmentária. Para CVL2, o receiver padrão muda o alcance da summary; `DISPATCHER` e getters injetados podem alterar a cena e a vacuidade. **Não foi gerado output transformado nem ABI binária; a transformação é inferida das expressões Perl recuperadas, não de execução.**

**IDs HMaker no catálogo:** incomplete/31, /37–40, /129–134 (11). Ordem para próximo gate: capturar input hashes; após recuperação do host, aplicar Perl **somente numa scratch byte-preservada**, comparar diff e hashes de TODOS os arquivos tocados; validar import closure, solc exato e ABI antes de qualquer `--compilation_steps_only` individual, sempre sem Prover. Nenhuma propriedade é promovida por esse plano.

## 6. Contrarrevisão READ-ONLY — PR #37 / P18/3 e P18/23 + proposta recente

PR #37 HEAD consultada: `2477787fe3f4cddb650cb4f1a08760bdbd1fde13` (Draft). Lidos `ROUND6_DIRECT_CLI_DIAGNOSTICS.md`, `ROUND6_QA.md` e a matriz `round6_diagnostic_matrix.csv` da outra branch, além de `P18_DIRECT_CLI_CONTRACHECK.md` do coordenador. **Nenhum arquivo de AGENTE-02 modificado.**

- **P18/complete/3** `grantRoleEffect` / `AccessControlMock`: `grantRole` e `hasRole` são `public` no source; as chamadas diretas da rule não definem automaticamente se `internal` ou `external` era coberto por eventual summary. No fragmento, `methods` não possui `=>` (nenhuma summary a inventar). A spec exata não foi localizada no commit Solidity auditado. O coordenador observou **COMPILE_ERROR real EXIT 1**, `methods` exigem `function` e `;`.
- **P18/complete/23** `noTransferEffectOnApproval` / `ERC1155Mock`: `isApprovedForAll` e `safeTransferFrom` são `public` em Solidity. O último tem `bytes memory` no caminho de implementação e `bytes calldata` na interface externa, exigindo escolha contextual, não uma anotação automática de `internal/external`. O coordenador também observou **COMPILE_ERROR EXIT 1** pelo methods legado.
- **Nova proposta do AGENTE-02, R6:** preparar P18/4,46,53 com ABI Solidity de snapshot e CLI direto somente após recuperar o filesystem. Esses IDs continuam **NOT_RUN** de parser CVL2; quatro ABIs Solidity não demonstram equivalência. Os nove testes anteriores do wrapper bloqueados por token são `PREFLIGHT_AUTH_BLOCKED`, não `COMPILE_ERROR`. A revisão do PR #37 e o painel PR #47 corroboram autoria e limites das duas contraprovas do coordenador.

**Avaliação:** não há aprovação independente para transformar os 50 `DOCUMENTED_CANDIDATE` lexicais do P18; ABI public/internal/external, receivers, call graph, full spec, solc/job auditado e vacuity continuam bloqueios. Esta auditoria não reproduziu nem contou como próprio qualquer teste P18.

## 7. Estados, QA e próximos gates

Arquivo obrigatório `ROUND7_MATRIX_266.csv`: exatamente uma linha por `(project_id,original_status,example_id)` no P10; propriedades/targets/Result/Detection Outcome do CSV canônico, hash N.spec/N.sol, commit e target histórico, cenário, último resultado experimental e **execução R7 em coluna separada**. A matriz foi comparada **em memória pelo conector GitHub** ao `results/spec/spec_buglabel.csv` baseline: 266/266 chaves únicas, **0 divergências** nos quatro campos canônicos. As 13 ocorrências ativas do inventário foram cruzadas com os registros documentais de método literal.

| Métrica P10 | Valor | Evidência real |
| --- | ---: | --- |
| `COMPILE_ERROR` CVL2 anterior | **2** | R5 `complete/33,34`, logs e SHA publicados; nenhum novo R7 |
| `NOT_RUN` sem parser observado | **264** | Matriz individual |
| `COMPILE_OK` | **0** | Nenhum |
| `PREFLIGHT_AUTH_BLOCKED` P10 | **0** | Não confundir WSL SIGBUS com auth |
| `SEMANTIC_PROVEN` | **0** | Nenhum |
| `ROUND7_LOCAL_EXECUTION` | **266 NOT_RUN_INFRA_BLOCKED** | Host WSL em EIO/SIGBUS/EROFS; sem tentativa nesta rodada |
| Projetos finalizados P10 | **0** | Sem Fase 2 |

Os três validadores históricos e `git -c core.whitespace=cr-at-eol diff --check BASE...HEAD` ficam **NOT_RUN_INFRA_BLOCKED** nesta rodada: o CI GitHub (quando confirmar) é independente e não substitui checks locais. Não gerar logs novos inexistentes. O registro de QA final está em `ROUND7_QA.md`.

**Gates para intervenção humana:**
1. Administrador confirmar recuperação controlada do WSL sem executar reset/destruir worktrees, validar filesystem, Python/Git, solc/CLI, hashes e HEAD; depois executar os quatro checks da HEAD final.
2. Coordenador liberar individualmente uma variante temporária P10/33 e outra P10/34 em scratch com compiler 0.6.12 pinado, log completo e source cmp/SHA. Em 34 `require false` é inegociável. Mesmo `COMPILE_OK` futuro não prova equivalência.
3. Registrar outputs **reais** de Proxy/Registry com seeds e dependências adicionais, e investigar `stack_slot` + `override`/base `virtual` no solc histórico, sem patch in-place.
4. Rodar pipeline HMaker/Perl só em scratch íntegra, com diff por arquivo e ABI compilada de todos os inputs. Adjudicar CVL2 summaries/`DISPATCHER`/receiver e universo de `method f`, sem esconder contraexemplos.
5. Reconciliar testes/call graphs e prova de equivalência por property; manter PR Draft, nenhuma migração em lote e nenhum Prover/CVL1 por iniciativa do agente.

**AGENTE-01 — RODADA 7.**
