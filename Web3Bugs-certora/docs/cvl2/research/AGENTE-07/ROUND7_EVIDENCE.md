# AGENTE-07 — RODADA 7 / Evidências e gates CVL2

**Escopo exclusivo:** P8 (42), P9 (61), P11 (16), P20 (37), total 156 instâncias; [PR #41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), DRAFT. Baseline imutável `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. HEAD inicial conferida: `104f6deef80ac95ab5fec75c3e5ebb01f075f6fe`. Painel R6 [PR #47](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/47) HEAD `948121599b546d61579dc9ecb8c316f9c088e78a`; revisão coordenador [#5590012874](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41#pullrequestreview-5590012874).

**Leituras obrigatórias:** `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md` (integrais), `results/spec/complete/1` e `incomplete/1` como precedentes de integridade histórica. `complete` significa dependências de fragmento resolvidas no snapshot — NÃO CVL2 ou run reproduzido. Fonte normativa: [CVL2 Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [CVL2 Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Invariants](https://docs.certora.com/en/latest/docs/cvl/invariants.html), [Methods/Summaries](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Statements/Havoc](https://docs.certora.com/en/latest/docs/cvl/statements.html).

## Escopo dos resultados: zero compilações deste agente

`ROUND7_MATRIX_156.csv` contém 156 chaves únicas `(project_id,original_status,example_id)`, cada qual com Property, Target, Result, Detection Outcome do CSV original, SHA-256 de `N.spec` já atestado anteriormente, origem/versão, cenário e estado efetivo. **156 NOT_RUN CVL2, 0 COMPILE_OK, 0 COMPILE_ERROR, 0 PREFLIGHT_AUTH_BLOCKED, 0 equivalências, 0 projetos migrados.** `INFRA_EIO` é motivo externo separado e **não** um parser error. As 4 compilações limitadas e 12 erros CVL2 do painel global pertencem a outros projetos. Nenhum `certoraRun`, solc, shell, build ou Prover executado nesta rodada: WSL segue `INFRA_BLOCKED`.

## P8 — protocolo documental de consistência, alcance e scheduling (VERMELHO)

**Identidade literal dos três testemunhos documentados na R5:**

- **W1 / 22 IDs P8/incomplete/14–35:** ghost global `rayMul_g(uint256,uint256)`, `axiom forall uint256 x. forall uint256 y.` contendo `((x==0||y==0) => rayMul_g(x,y)==0)` e `x <= rayMul_g(x,y) && rayMul_g(x,y) <= 2*x`. Substituir `x=1,y=0` força simultaneamente `rayMul_g(1,0)=0` e `rayMul_g(1,0)>=1`, sem modelo aritmético convencional. Os 22 hashes e linhas dos **22 blocos efetivamente extraídos** constam de `ROUND5_P8_AXIOM_42.csv`; blocos de origem em `contracts/8/specs/fees_LEQ_ATokenBal.spec:26–33`, `lastVaultBal_LEQ_ATokenBalThis.spec:20–27` e `positiveSupply_imply_positiveAssets.spec:29–36`.
- **W2 / P8/incomplete/1:** `accrueYieldCheck.spec:11–21`, `mulDiv_g` universal, em `x=0,y=0,denominator=0,rounding=1`, obriga `0<0`, independentemente do resultado do ghost.
- **W3 / P8/incomplete/1:** `accrueYieldCheck.spec:29–31`, `rayDiv_g` universal em `x=y=0`, novamente `0<0`. O termo `y/2` é `0/2`, **não** divisão por zero.
- **Outros 19 P8**: IDs `2–13,36–42` não contêm especificamente os três testemunhos conhecidos; isto NÃO certifica consistência dos demais ghosts, axiomas, hooks, interações e premises.

**Distinções lógicas obrigatórias:**

1. **Quantificador:** a contradição acima é matematicamente válida para a fórmula universal W1/W2/W3 *se* o axioma inteiro entra no conjunto de premissas de um modelo. Não depende de selecionar um parâmetro da rule, overflow Solidity ou do codepath de determinada função.
2. **Scheduling/alcance:** a [documentação de Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html) afirma que axiomas de ghost são assumidos quando o ghost é utilizado. Não basta a declaração textual: analisar cada uso direto da ghost, os `methods` com summaries `=> rayMul_g(...) / rayDiv_g(...)`, invocações dos métodos resumidos, hooks e possíveis `havoc`. A identidade do runner histórico, opções, scopes do Prover e ativação efetiva **não foram reconstituídas**; logo, NÃO atribuir vacuidade ao `VERIFIED` original.
3. **`init_state` versus axiom global:** W1/W2/W3 são `axiom` globais, **não** `init_state axiom`. Ghosts auxiliares de soma encontrados nas specs P8 podem usar `init_state axiom`. Segundo [Invariants](https://docs.certora.com/en/latest/docs/cvl/invariants.html) e [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), o `init_state` aplica-se ao passo base do invariante, não automaticamente a cada rule nem ao passo preservado. Não transportar essas suposições entre contextos.
4. **Hooks, reverts e quantificação de métodos:** comparar os hooks Sload/Sstore, `havoc assuming`, `requireInvariant`, filtros `method f`, resumidores e tratamento de chamadas revertidas por ID. Ausência de uma chamada resumida em um caminho pode alterar alcance; não presumir que um path específico invoca o ghost.
5. **Gate proposto, NÃO executado:** produzir mapa por ID de (declaração → usos → summaries/hook → rule/invariant → etapa base/preservada), com linhas/hashes; requer do coordenador versão original do CLI, runner/flags, harness, imported specs e evidência de `--verify`. Somente após aprovação **por cenário** discutir teste de satisfatibilidade de modelo **em derivados scratch**, preservando as premissas originais. Sem executar Prover, alterar ghost/guard/`require`/assert ou concluir equivalência.

A matriz separa claramente W1 (22), W2_W3 (1) e P8_OTHER (19) e retém risco semântico/vacuidade até prova histórica.

## P9 — Celo/Mento: progresso em fontes com commit e blobs, sem stubs (LARANJA)

**Evidência positiva NOVA, estritamente de source, não do run:**

| Origem exata | Caminho | Git blob SHA-1 | Interpretação |
|---|---|---|---|
| [celo-org/mento-core@4ceb4f0ed3e24163617e9da2b5bfc4c5a2b722b8](https://github.com/celo-org/mento-core/tree/4ceb4f0ed3e24163617e9da2b5bfc4c5a2b722b8) | `contracts/interfaces/IExchange.sol` | `968158a26512cb4bcf479af85cb11d9c4f301b88` | Interface original concreta candidata, Solidity ^0.5.13 |
| mesma revisão | `contracts/interfaces/IReserve.sol` | `2fc72df0a4937bfabd2fc76de624a2d8763f4c4b` | Interface original concreta candidata |
| mesma revisão | `contracts/interfaces/IStableToken.sol` | `b62d7fe7169cb591f704242ee9bfa904ef90d58d` | Interface original concreta candidata |
| mesma revisão | `contracts/common/UsingRegistry.sol` | `e3bca1e6bb2ffe86dd656fb7b79de429d69ab690` | Importa `../interfaces/...` dentro do repo Mento: **não** é o UsingRegistry do snapshot Celo |
| [celo-monorepo@a46ce55ebd3867fa69290bf3be040846d433525d](https://github.com/celo-org/celo-monorepo/tree/a46ce55ebd3867fa69290bf3be040846d433525d) | `packages/protocol/contracts/common/UsingRegistry.sol` | `cee300411c82433085cc8429ab4018f376fd5aed` | Importa **`../stability/interfaces`**, não Mento |
| [celo-monorepo@10c3f192a1d78611d12c3d4132319462549eaf25](https://github.com/celo-org/celo-monorepo/blob/10c3f192a1d78611d12c3d4132319462549eaf25/.gitmodules) | `.gitmodules` | `7690307ca10d76705c7633ffafcea77ac96b00d6` | Declara submódulo `packages/protocol/lib/mento-core` apontando a `https://github.com/celo-org/mento-core` (revisão **posterior, não runner auditado**) |

**Problema específico:** snapshot `contracts/9/contracts/common/UsingRegistry.sol:20–22` importa `../../lib/mento-core/contracts/interfaces/{IExchange,IReserve,IStableToken}.sol`, resolvendo para `contracts/9/lib/mento-core/... `; esse diretório não está no snapshot. **Os três arquivos agora têm candidatos públicos com SHA verificável**, mas ainda NÃO foi localizada a SHA **do gitlink usado na cena histórica do AccountsHarness**. Não há evidência de que `4ceb4f0...` seja o submódulo daquela auditoria. Substituir arquivos, introduzir stubs ou forçar imports da phase2 geraria uma terceira cena potencialmente diferente.

**Condição para ABI sem stubs:** obter um commit do *superproject* que contenha o gitlink exato `lib/mento-core` (e demais gitlinks), seus package lock/remappings, versão de solc e versão byte-idêntica do `AccountsHarness`. Só então verificar `gitlink → blobs das três interfaces → import closure completa → compile-only Solidity em scratch → ABI do AccountsHarness`. Sem todos os elementos a pergunta “AccountsHarness pode compilar com ABI autêntica?” permanece **NÃO DEMONSTRADA**. Na R5 somente o **Accounts.sol phase2 isolado** compilou via `solc-js 0.5.13` com 40 funções; o harness snapshot teve **três ParserErrors de Solidity**, não CVL2. **P9/6** chama `authorizeSignerWithSignature` ausente dessa ABI phase2, exigindo associação a fase/target distintos. Phase1 `9d2ec0d9399a6959565062f57efa037d03fd4fbc` não forneceu `Accounts.sol` na árvore recursiva anteriormente consultada; não atribuir as 61 rules indiscriminadamente à mesma fase.

## P20 — BentoBox: cinco patches por família de properties (LARANJA)

Fonte literal [`contracts/20/spec/scripts/applyHarnesses.sh`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/20/spec/scripts/applyHarnesses.sh), Git blob `ac0ecabd863f02b60d065f1d79e0be47f388feb4`. A replay em scratch da R4 alterou **cinco** Solidity, dos quais **três** pertencem ao commit pinado BoringSolidity `39fdd3b4c78be0380edc95fde98d198f4bac5b41`, com hashes pré-patch conferidos em `ROUND5_P20_PATCH_SHA.csv`. Não houve replay novo nesta R7.

| Arquivo transformado | Operação literal do script | Potencial efeito sobre cena/propriedade |
|---|---|---|
| `contracts/BentoBox.sol` | substitui `safeT` por `t`; altera `virtual` em funções/constructor | dispatch, binding de bibliotecas e caminho de código do target BentoBoxHarness |
| `contracts/strategies/CompoundStrategy.sol` | `safeT→t`, remove `try/catch` de `cToken.redeem` e `redeemUnderlying`; redireciona `to.call{value:value}(data)` para `Nothing(to).nop{value:value}(data)` | muda alcance de reverts, semântica de chamada/callee e sucesso em `exit@withrevert` |
| `node_modules/@boringcrypto/boring-solidity/contracts/BoringBatchable.sol` | virtualiza `external payable returns` | resolução/instrumentação de método herdado |
| `.../contracts/BoringFactory.sol` | virtualiza `public payable` | resolução/instrumentação de método herdado |
| `.../contracts/interfaces/IERC20.sol` | acrescenta `transfer` e `transferFrom` | interface/ABI disponível após patch difere do original |

**Mapping individual por fonte original, replicado por ID na nova matriz:** `bentobox.spec` (8, BentoBoxHarness), `bentoBoxCompoundStrategy.spec` (8, BentoBoxHarness), `compoundStrategy.spec` (6, CompoundStrategyHarness), `compoundStrategyAdditional.spec` (1, CompoundStrategyHarness), `rebase.spec` (8, RebaseWrapper), `strategy.spec` (3 SymbolicStrategy + 3 SushiStrategyHarness). Classificar exposição **potencial** por target e import, não afirmar que o patch alterou todo traço desses 37 exemplos. O wrapper de Rebase não tem efeito de patch comprovado pela classificação textual; registrar como `PATCH_REACHABILITY_UNCONFIRMED`, não `PATCHED` por indução.

**`MAX_INT()` é caso isolado P20/CompoundStrategyAdditional:** `contracts/20/spec/compoundStrategyAdditional.spec:65` chama o símbolo sem definição/import comprovado. Há definições em `compoundStrategy.spec:60` e `strategy.spec:43`, arquivos irmãos que não são automaticamente compartilhados. Ausência de include precisa de runner/concatenação auditada. Em especial, remover `try/catch` ou adicionar uma summary que force sucesso pode excluir contraprovas, logo nenhuma conversão permitida sem gate.

## P11 — Keep: runner e ghost initial-state/hook (LARANJA para migração)

Fonte original [`contracts/11/specs/fullyBackedBonding.spec`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/11/specs/fullyBackedBonding.spec), Git blob `5241b30db6e5781033c5ff422926477aa2bcb60a`. **16/16** N.spec fragmentados desse documento, target catalogado `FullyBackedBondingHarness`. A spec contém `ghost allLockedBond()` e `ghost allUnbonded()` com `init_state axiom ...==0`, hooks de `Sload` e `Sstore`, `havoc ... assuming`, quantificação sobre selectors `method f`, invariants e paths `invoke/lastReverted`. Uma ABI Solidity sozinha não reconstitui a semântica desses ghosts/hook e reverts. A distinção base-step/preservation e invocations é obrigatória também para P11.

**Proveniência verificável mas insuficiente:** commit de branch de trabalho [keep-network/keep-ecdsa@a5cd1713621d94868765d1570fae373f4a497521](https://github.com/keep-network/keep-ecdsa/commit/a5cd1713621d94868765d1570fae373f4a497521) existe e possui mudanças em spec (`cleanup to the spec`); seu `solidity/package-lock.json` suporta **6/6 tarballs SRI SHA512**, closure textual de **45 Solidity locais, 104 nós e 204 imports** sem caminhos faltantes (R4/R5, não reexecutado em R7). Já a SHA indicada na auditoria `658b02f237e25c370feaba80a7a3b13824190c4` retornou **GitHub commit lookup HTTP 422 “No commit found for SHA”** em `keep-network/keep-ecdsa`, busca negativa estritamente desse repo/ref. Não é prova de inexistência em fork, SHA diferente ou objetos não publicados. Pesquisas indexadas de `certoraRun`/runner não recuperaram `--verify FullyBackedBondingHarness` e linkings autenticados. `init_state()` como declaração CVL em `methods` não garante ligação com construtor Prover.

**Gate humano P11:** obter commit/URL do fork auditado, checksum do runner `--verify`, contratos reais e seus `--link`, versão solc/CLI, configurações de invariants/hook e reconciliação do SHA do relatório. Não simular targets nem alterar selectors/reverts.

## Contrarrevisão cruzada independente READ-ONLY — PR #43

HEAD observada `748a8e345061961faf977f78cf9bcce7739e8385`, PR [#43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43) DRAFT; revisão mais recente [#5590013542](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43#pullrequestreview-5590013542). Consulta **somente via conector GitHub**, sem tocar na branch AGENTE-08.

- **P5 StarkNet:** `ROUND6_FINDINGS.md` escolhe `incomplete/5/14.spec`, `alwaysUnSent` SHA256 `0c0e05b80677a46deccfe1494e205cf09b966efab14785e6206c37a0a92e2031` e target BridgeHarness. Dois getters do harness vistos em ABI solc0.8.10; 11 inputs, links, `--loop_iter 3` do launcher histórico. Sem montagem de cena auditada nem teste CVL2: tentativa de scratch falhou **EROFS**, não parser.
- **P14 Opyn:** Controller upstream/patchado compilou apenas Solidity solc0.6.10 na R5, 39→42 funções externas (+3 getters), com mudanças em `getExcessCollateral`, `settleVault` e `_runActions` que alteram branches e potenciais reverts. Os `assert true;` de `complete/14/1.spec:10` e `sinvoke ...; assert false;` de `complete/14/25.spec:31–32` permanecem originais; nenhuma reescrita de suas asserções é autorizada. **34/34 unresolved P14 e 17/17 unresolved P5**.
- Nenhuma promoção `COMPILE_OK` CVL2 nem equivalência a partir da ABI solc ou do patch em scratch. Esta revisão verifica afirmações documentais e fontes específicas; não replica 155 compilações/provas, nem executa patch.

## Intervenções e semáforo

**P8 VERMELHO** — requer aprovação por cenário para estudo de alcance e consistência matemática versus uso efetivo, com logs/versionamento Prover. **P9 LARANJA** — demonstrar gitlink exato Mento + ABI do AccountsHarness/phase2. **P20 LARANJA** — reconstruir cena de cinco patches e composição MAX_INT sem modificar universo de reverts. **P11 LARANJA** — recuperar runner/linkings e SHA da auditoria; closure do lock apenas textual. **QA/WSL VERMELHO operacional** — `ROUND6_WSL_IO_INCIDENT.md` proíbe escritas/compilações locais antes da recuperação administrada.

**NÃO EXECUTADOS nesta Rodada 7:** `certoraRun --compilation_steps_only`, Prover, CVL1, Solidity compile, npm, scripts históricos, três validadores locais e `git diff --check` CLI. Commitar apenas documentação por GitHub. A execução do GitHub Actions é evidência separada de integridade, nunca de CVL2.

**AGENTE-07 — RODADA 7**
