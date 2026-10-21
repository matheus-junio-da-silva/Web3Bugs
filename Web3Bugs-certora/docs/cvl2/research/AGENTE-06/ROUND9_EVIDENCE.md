# AGENTE-06 — RODADA 9 / EVIDÊNCIAS TÉCNICAS

**PR:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38 — Draft. HEAD inicial 6da9aac35f73a6b0a792807ee6000b7e8b7f077f. Baseline intocado 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. P1=70, P4=27, P17=41, P22=21.

**Método:** leitura prévia dos quatro documentos do catálogo, originais complete/1 e incomplete/1, comentários mais recentes dos PRs #38 e #48, documentos oficiais Certora CVL2 migration, changes, methods, ghosts, hooks, statements/reverts. CLI Certora CVL2 NÃO foi executada; todos os diagnósticos inéditos abaixo são exclusivamente compilações Solidity em scratch. Full-spec original, executor Prover e equivalência CVL1/CVL2 continuam NÃO demonstrados.

## P4 StakedToken: construção ABI em scratch íntegro

Fonte auditada upstream Certora/aave-stk-v1-5 no commit 4cf8837121a4351cc0e21703bb1df76036205114, checkout para /tmp/ag06-round9-p4-upstream. Copiados 36 arquivos de src byte-idênticos ao scratch e separados do diretório certora/munged. Makefile original contracts/4/certora/Makefile:3–16 usa src → munged via applyHarness.patch, SHA256 f77b4320ee1991fdb38c3557516717ab12ca8360a5b3d8804275f0adcd5258fc. Patch com --batch --fuzz=0, exit 0, zero rejects; munged gerado 37 arquivos (34 iguais, 2 modificados: contracts/StakedTokenV2.sol e contracts/StakedTokenV3.sol, 1 .gitignore novo). Nenhuma alteração no Git histórico. Manifesto integral [ROUND9_P4_SOURCE_MANIFEST.json](ROUND9_P4_SOURCE_MANIFEST.json).

O harness original StakedAaveV3Harness.sol:4–24 (blob 507903cb7b0134c44896ea0e577f46926c350344) importa de certora/munged; DummyERC20Impl.sol:1–5 (blob 139fc27ad9595e01c411bcf85f3aa7b3e5f9c6ef) importa da árvore src. Os dois IERC20.sol carregados possuem o MESMO SHA256 241d1d3c877f5143051fec983d744d82c5c48a9d447f9e1b1c395ccdddcf2958, embora os paths sejam distintos. Sem stubs, remappings inventados ou mudança de ABI.

Compilador apenas Solidity: solc-js 0.8.17+commit.8df45f5f.Emscripten.clang; soljson.js SHA256 04184dd4a976c37a64c8d6470e25983cfdbb09b10ff371da9178f50d6e132745. Standard JSON com as fontes exatas StakedAaveV3Harness.sol, DummyERC20Impl.sol, RewardVault.sol e resolução real de imports restrita ao scratch. Seleção ABI e methodIdentifiers, optimizer false; 29 arquivos efetivamente carregados. Execução com timeout 60s: EXIT **0**, **zero erros Solidity**, oito avisos. Resultado integral [ROUND9_P4_ABI_RESULT.json](ROUND9_P4_ABI_RESULT.json), SHA256 8e2c3d378ad69c7ec3b56f70a77e35c8861952372e509eca675a283d283abb38.

| Target fonte | Entradas ABI | Selectors |
| --- | ---: | ---: |
| StakedAaveV3Harness | 112 | 87 |
| DummyERC20Impl | 14 | 11 |
| RewardVault | 0 | 0 |

A ABI REAL obtida é da árvore upstream + patch e **não está autenticada como ABI usada no audit Certora**. Não prova execução histórica, summary, storage, revert, counterexamples nem CVL2. Runners do snapshot runAllProps.sh:1–14 e runPropertiesWithSummarization.sh:3–27 incluem RewardVault e três linkings; runInvariants.sh:2–24 omite RewardVault. P4 mantém 27 NOT_RUN CVL2.

## P22 Popsicle: ABI FullMath e erros Solidity independentes do CVL2

Copiados 54 arquivos .sol do snapshot contracts/22 para scratch sem modificação, com SHA256 em [ROUND9_P22_SOURCE_MANIFEST.json](ROUND9_P22_SOURCE_MANIFEST.json). Compilador solc-js **0.7.6+commit.7338295f.Emscripten.clang**.

**FullMathWrapper.sol:** compilação isolada com biblioteca FullMath.sol (2 imports contabilizados), **EXIT 0**, zero erros Solidity, sete warnings; a ABI apresenta somente:
- callMulDiv(uint256,uint256,uint256): selector 3b46282d;
- callMulDivRoundingUp(uint256,uint256,uint256): selector 9056f536.

Resultado integral [ROUND9_P22_FULLMATH_ABI.json](ROUND9_P22_FULLMATH_ABI.json), SHA256 82dcc919d361424bdea9a58ef0bca7eede8bab53dd4fe5f1c36628d1d5b04161. **Três exemplos FullMath catalogados continuam sem compilação CVL2**, pois faltam job específico e fonte de auditoria.

**PoolActionsWrapper.sol:** compilação Solidity isolada de 17 arquivos de closure, **EXIT 1**, dois TypeErrors originais:
- PoolActionsWrapper.sol:28:31: *Wrong argument count for function call: 7 arguments given but expected 6* (Solidity errorCode 6160).
- PoolActionsWrapper.sol:40:31: *Member burnExactLiquidity not found or not visible* na biblioteca PoolActions carregada (errorCode 9582).

Output integral [ROUND9_P22_POOL_ERRORS.json](ROUND9_P22_POOL_ERRORS.json), SHA256 307c2ab2cfd8d1c02afea265e76baafa8eaeb3246b6e835df5c1838ea85eb828. A tentativa exploratória conjunta FullMath+PoolActions também falhou nesses mesmos dois erros, sem emitir ABI do FullMath, o que motivou os diagnósticos separados. PoolActionsWrapper.sol:13 declara totalSupply sem public: não gera getter totalSupply() requerido por incomplete/22/4; incomplete/22/5 mantém identificador to livre. **Esses dois erros são Solidity, não COMPILE_ERROR CVL2.** Nenhuma assinatura ou source original foi corrigida.

Outras famílias P22: 13 Optimizer com runner verifyPopsicleV3Optimizer.sh:1–12 selecionando Optimizer.spec via --rule $1 (argumento efetivo desconhecido) e 2 sanity sem runner documentado. Os seis Git blobs iguais ao commit posterior 3cb9cb7279a3fb1790b55251a029bb3065606dc8 de 04/11/2021 não provam a execução da auditoria até 25/10/2021. Total P22 21 NOT_RUN CVL2.

Os **três replays de diagnóstico** capturados com comando, exit real, stdout, stderr e hash estão em [ROUND9_COMPILATION_DIAGNOSTIC_LOG.json](ROUND9_COMPILATION_DIAGNOSTIC_LOG.json): P4 EXIT 0; P22 PoolActions EXIT 1; P22 FullMath EXIT 0. Houve antes quatro explorações Solidity (P4 0, P22 conjunta 1, FullMath 0 e PoolActions 1), total **7 invocações de solc-js** para **quatro cenários de source**, 0 invocações do Certora.

## P1: comparação direta junho versus setembro

GitHub API releu os cinco arquivos contracts/bridges nas refs junho 303bd3e16c8d3465325389a72564126c3bacc4f9 e setembro 93c39de7065a7dc3bb08cddf7dadb466f9a393b8. [ROUND9_P1_JUNE_SEPT_BLOBS.csv](ROUND9_P1_JUNE_SEPT_BLOBS.csv) guarda os cinco SHA1 por versão: L2BridgeExecutor, PolygonBridgeExecutor, OptimismBridgeExecutor e ArbitrumBridgeExecutor são quatro blobs **idênticos**. BridgeExecutorBase difere **somente no comentário da linha 32**. A equivalência do source Solidity de produção NÃO autentica runners/harnesses/ABI/execução de junho. Setembro contém queue2 com cinco arrays fixos de 2 (em vez de queue dinâmica), guards de rede e links distintos para _mock, solc8.10, argumentos --rules e --send_only, porém **nenhum job auditado de junho comprovado**. Família original: 14 queue2, 6 _mock, 6 complexity, 44 sem associação de job individual. P1 70 NOT_RUN CVL2.

## P17 Specify 2019: domínio/state/calls ainda sem prova

Reabertas original P17/complete/8 (borrowFresh, linhas 19–116), /9 (repayBorrowFresh, linhas 19–148) e /39 (transferFrom, linhas 21–153). Em /8: env e0/e1/e2 havoc, sinvoke getters pré, static_require result == invoke borrowFreshPub, lastReverted, sinvoke pós e asserts condicionais. Em /9: condições distintas payer/borrower/other, UINT_MAX e realRepayAmount, reverts. Em /39: e0/e1a/e1b/e2, havoc locals doApprove e approvedAmount, *sinvoke approve* opcional antes de invoke transferFrom, allowancePre/allowancePost e reverts. Um env NÃO é snapshot storage provado; sintaxe sinvoke no motor 2019 NÃO prova que approve seja leitura sem efeito.

MintRedeemBorrowRepay.spclnk Git blob ca6350e7ac992af6f9b8037787d834fef591da76 mapeia CErc20Certora a specs borrowAndRepayFresh com state 6→789,18→456,19→321. EIP20.spclnk Git blob cb89e560789d881139449b687342449e1f35d25f associa eip20.cvl e possui state 6→789,18→456, sem alias 19. **Diferença de aliases é fato**, impacto sobre storage/reverts é inferência pendente. Falta runtime Specify original, ABI vinculada e full job. Não converter por troca textual, não criar require/cast/summary ou snapshot novo. P17 41 NOT_RUN CVL2.

## Próximos dois gates para coordenação

1. **P4 StakedAaveV3Harness/allProps (ABI agora reproduzida)**: recuperar o bundle original de auditoria (ABI, bytecode, source hash, solc, deploy/links, versões e runner) e comparar contra este ABI scratch. Apenas com proveniência comprovada e autorização por propriedade considerar Certora --compilation_steps_only limitado. O sucesso solc 0.8.17 de R9 não é esse gate.
2. **P22 FullMathWrapper (3 casos)**: recuperar o runner e a biblioteca da janela de auditoria 2021, com alvo FullMathWrapper e --rule real; então avaliação individual de CVL2 em scratch se houver autorização. O PoolActionsWrapper está bloqueado por **duas incompatibilidades Solidity no snapshot** e não deve ser corrigido automaticamente.

**Contrarrevisão somente leitura PR #41:** [ROUND9_PR41_READONLY_REVIEW.md](ROUND9_PR41_READONLY_REVIEW.md), W1/W2/W3 comprovam contradição matemática sob axiomas globais assumidos, não que prova histórica foi vacuous.

**Semântica:** 159 documentados, **0 tentativas Certora CVL2**, **0 COMPILE_OK/0 COMPILE_ERROR CVL2**, **159 NOT_RUN**, **0 equivalências**, **0 projetos migrados**. Erros Solidity de PoolActions não contam como parser CVL2.

AGENTE-06 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.
