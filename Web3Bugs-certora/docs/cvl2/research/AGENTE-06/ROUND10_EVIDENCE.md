# AGENTE-06 — RODADA 10 / pesquisa técnica e limites de evidência

**Data:** 20/10/2026. **PR existente:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38 (Draft). **HEAD inicial confirmada:** c07432f9c81843be532eec5c4f792143aaabde59. Baseline imutável: 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. PropertyGPT: 687f654c679ed45ab127b7949e2a29c8f5e491b9. Carteira P1=70, P4=27, P17=41, P22=21, total 159 propriedades.

Antes de editar foram lidos na íntegra os quatro documentos obrigatórios docs/spec_catalog.md, docs/spec_catalog_workflow.md, docs/spec_catalog_project_1.md e docs/standard.md, exemplos complete/1/1.spec e incomplete/1/1.spec, revisão mais recente do coordenador no PR #38, painel R9 integrado no PR #49 e fontes dos quatro projetos. As fontes oficiais vigentes consultadas em 20/10/2026 foram [Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html) e [Statements/reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html). Esse guia CVL2 moderno não autentica retroativamente o motor Specify de 2019.

[ROUND10_MATRIX_159.csv](ROUND10_MATRIX_159.csv) contém uma linha por chave, Property, Target Contract, Result, Detection Outcome e todos os Bug Labels históricos, SHA-256 original atestado na R9, fatos de fonte separados de inferências e provas faltantes, indicação explícita de ABI e bytecode, risco e próximo gate. **159 NOT_RUN CVL2, zero COMPILE_OK, zero COMPILE_ERROR, zero equivalência e zero projetos migrados.** Globalmente, a coordenação R9 registrou 33 eventos para 20 propriedades distintas, 11 sucessos limitados, 21 erros CVL2, 1 erro de setup Solidity, interseção de 7 propriedades e 1.366 sem teste; nenhum evento foi reatribuído a este agente.

## P4 — ABI recompilada na R9; hash de bytecode ausente

**Fato prévio verificável:** [ROUND9_P4_ABI_RESULT.json](ROUND9_P4_ABI_RESULT.json), SHA-256 de arquivo 8e2c3d378ad69c7ec3b56f70a77e35c8861952372e509eca675a283d283abb38, registra compilador solc-js **0.8.17+commit.8df45f5f.Emscripten.clang**, SHA do soljson 04184dd4a976c37a64c8d6470e25983cfdbb09b10ff371da9178f50d6e132745, commit upstream [Certora/aave-stk-v1-5@4cf8837121a4351cc0e21703bb1df76036205114](https://github.com/Certora/aave-stk-v1-5/commit/4cf8837121a4351cc0e21703bb1df76036205114), 29 entradas de compilação Solidity e saída com zero erros na R9. A fonte auditada upstream foi copiada byte-idêntica (36 arquivos src), o patch histórico SHA256 f77b4320ee1991fdb38c3557516717ab12ca8360a5b3d8804275f0adcd5258fc aplicado com fuzz 0 exit0 exclusivamente em scratch gerou 37 itens munged.

| Contrato da cena scratch R9 | Entradas ABI | Seletores | Identidade do job auditado |
| --- | ---: | ---: | --- |
| StakedAaveV3Harness | 112 | 87 | NÃO COMPROVADA |
| DummyERC20Impl | 14 | 11 | NÃO COMPROVADA |
| RewardVault | 0 | 0 | NÃO COMPROVADA |

As duas cópias IERC20 dos caminhos src e munged têm mesmo SHA-256 241d1d3c877f5143051fec983d744d82c5c48a9d447f9e1b1c395ccdddcf2958 na entrada R9, apesar dos caminhos/imports distintos. A ABI vazia RewardVault não exclui a possibilidade de funcionar como alvo de link, pois o runner original lista o endereço como target.

**Comparação real com runners preservados, não com jobs executados:**
- [runAllProps.sh:1–14](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/4/certora/scripts/runAllProps.sh#L1-L14), Git blob bc56cf825918d906ec627a8ac592bc1097de30ee, lista os **mesmos três contratos nomeados**, solc8.17, verify StakedAaveV3Harness:certora/specs/allProps.spec, loops e os três links STAKED_TOKEN, REWARD_TOKEN, REWARDS_VAULT; aceita argumento --rules parametrizado. NÃO disponibiliza ABI, hashes de deployed bytecode, calldata, log nem o selector efetivamente verificado.
- [runPropertiesWithSummarization.sh:3–30](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/4/certora/scripts/runPropertiesWithSummarization.sh#L3-L30) usa os mesmos três targets mas OUTRA spec, summarizationsCollector.spec, que pode ter chamadas resumidas de outro modo.
- [runInvariants.sh:3–24](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/4/certora/scripts/runInvariants.sh#L3-L24) seleciona apenas StakedAaveV3Harness e DummyERC20Impl com dois links, e invariants.spec.
- [Makefile:3–16](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/4/certora/Makefile#L3-L16) copia src para munged e aplica o patch; não autentica runtime do Prover.

**Bloqueio incontornável desta R10:** a inspeção do artefato integral R9 revelou que a compilação foi configurada com outputSelection **somente abi e evm.methodIdentifiers**. Não existe evm.bytecode, deployedBytecode ou objeto binário nos contract_abis; **hash de bytecode = NÃO DISPONÍVEL, não foi calculado**. Comparar o SHA de arquivo JSON com o hash de bytecode seria falso. Também não foi recuperado o ABI/bytecode efetivamente usado por um job de auditoria. Não houve solc R10. P4: 27 NOT_RUN CVL2.

## P22 — closure textual demonstrada de FullMath e ABI somente Solidity

Os bytes textuais lidos por GitHub da [spec global FullMathWrapper.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/22/spec/FullMathWrapper.spec), blob 4add6fed2e9c62788e35b067d626662e3b90bb23, foram comparados, linha por linha, com três N.spec originais **sem alterar código**:

| Property original | Intervalo da spec global | Intervalo N.spec, retirados os 3 comentários catalográficos | Resultado |
| --- | --- | --- | --- |
| complete/22/1 integrityOfMulDivNoOverflow | 2–19 | 4–21 | **18/18 linhas exatamente iguais** |
| complete/22/2 integrityOfMulDiv | 22–38 | 4–20 | **17/17 linhas exatamente iguais** |
| complete/22/3 checkMulDivRoundingUp | 60–72 | 4–16 | **13/13 linhas exatamente iguais** |

**Regra prioritária escolhida: complete/22/1.** O corpo global conserva guard denominator > 0 e a*b <= max_uint256, env e, chamada callMulDiv(e,a,b,denominator), resultado e assert de igualdade a a*b/denominator. A aritmética moderna CVL2 pode introduzir distinções uint256/mathint e de divisão/revert, portanto matching textual é fechamento de provenance, NÃO prova de domínio equivalente. **complete/22/2 possui guard de denominator apenas em comentário no original**; inserir require seria restrição semântica proibida. A terceira regra verifica a divisão com arredondamento.

**Métodos e targets:** o arquivo FullMathWrapper.spec global **NÃO tem bloco methods**. [FullMathWrapper.sol:5–19](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/22/spec/harness/FullMathWrapper.sol#L5-L19) define os dois wrappers que delegam à biblioteca. [ROUND9_P22_FULLMATH_ABI.json](ROUND9_P22_FULLMATH_ABI.json), SHA256 82dcc919d361424bdea9a58ef0bca7eede8bab53dd4fe5f1c36628d1d5b04161, contém ABI Solidity solc0.7.6 com seletores callMulDiv(uint256,uint256,uint256)=3b46282d e callMulDivRoundingUp(uint256,uint256,uint256)=9056f536. **Não executou CVL2**. O único [runner arquivado verifyPopsicleV3Optimizer.sh:1–12](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/22/spec/scripts/verifyPopsicleV3Optimizer.sh#L1-L12), blob 9b25cf5a8aa340593a125c1eb8ebfaaa6e87f731, seleciona **PopsicleV3Optimizer:spec/PopsicleV3Optimizer.spec**, não FullMathWrapper.spec. Seu parâmetro --rule $1 não documenta a execução FullMath. Não fabricar runner, methods nem receiver.

**Os dois erros Solidity PoolActionsWrapper foram analisados separadamente:**
1. [PoolActionsWrapper.sol:28:31](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/22/spec/harness/PoolActionsWrapper.sol#L28), errorCode **6160**: sete argumentos enviados a burnLiquidityShare; biblioteca carregada espera seis.
2. [PoolActionsWrapper.sol:40:31](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/22/spec/harness/PoolActionsWrapper.sol#L40), errorCode **9582**: burnExactLiquidity inexistente ou não visível no PoolActions compilado. R9 EXIT 1 **exclusivamente Solidity**, resultado SHA256 307c2ab2cfd8d1c02afea265e76baafa8eaeb3246b6e835df5c1838ea85eb828. Nenhuma ABI do wrapper PoolActions foi emitida. Sua declaração totalSupply sem public não gera getter, e incomplete/22/5 usa identificador to livre. Nada foi alterado. Restam 13 regras Optimizer e 2 sanity sem execução nesta carteira. **P22: 21 NOT_RUN CVL2, 3 corpos FullMath textualmente reconciliados**.

## P1 — cinco blobs produção junho versus setembro, sem job retroativo

Fonte oficial: [junho 303bd3e16c8d3465325389a72564126c3bacc4f9](https://github.com/aave/governance-crosschain-bridges/commit/303bd3e16c8d3465325389a72564126c3bacc4f9), relatado junho 05–26/2022; [setembro 93c39de7065a7dc3bb08cddf7dadb466f9a393b8](https://github.com/aave/governance-crosschain-bridges/commit/93c39de7065a7dc3bb08cddf7dadb466f9a393b8). **BridgeExecutorBase.sol** junho Git blob e825e5f201365b39288bd8bad2ac5b6886d219ab, setembro blob 4bb4ba518c4b2fa0112c30f7b6b55e302f655bef: apenas comentário **linha 32** mudou. Blobs **idênticos** em ambas refs: L2BridgeExecutor.sol 0b587c4c5e6960b6accabfaad79b281c081cdbe6, PolygonBridgeExecutor.sol 644f1f6d93b0552bda196b9ef776bce2b8a09bdf, OptimismBridgeExecutor.sol 3f6117314f84009616392bd077d94968fd6713ed, ArbitrumBridgeExecutor.sol 09e54ca1f168d5396951d809632e1eb1111769ba. [Matriz pinada de 5 blobs](ROUND9_P1_JUNE_SEPT_BLOBS.csv).

**Fato distinto:** harnesses de setembro introduzem queue2 com cinco arrays fixos [2] onde contrato produção expõe queue com arrays dinâmicos; mocks e links Polygon/Optimism/Arbitrum diferem; solc8.10 e scripts com --rules são receitas e não comprovam jobs do PDF em junho. A ausência de certora/ no commit junho consultado não prova ausência de arquivos privados naquela data, apenas delimita o Git público. 14 queue2, 6 mocks, 6 complexity e 44 sem job individual. P1 70 NOT_RUN CVL2.

## P17 — Specify 2019, três regras e mapas state não intercambiáveis

- [complete/17/8](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/17/8.spec#L19-L117): borrowFresh usa havoc de e0/e1/e2, static_require de ordenação de block.number, sinvoke de getters antes/depois, static_require result == invoke borrowFreshPub, lastReverted e assertions condicionais.
- [complete/17/9](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/17/9.spec#L19-L148): repayBorrowFresh separa payer/borrower/other, UINT_MAX e realRepayAmount, reverts e pre/post balances.
- [complete/17/39](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/17/39.spec#L21-L153): transferFrom possui e0/e1a/e1b/e2, havoc local doApprove e approvedAmount, sinvoke approve opcional, allowancePre/allowancePost, invoke transferFrom e lastReverted. O efeito de sinvoke approve sobre storage não é estabelecido por sintaxe moderna.

**Configuração fonte não equivalência:** MintRedeemBorrowRepay.spclnk blob ca6350e7ac992af6f9b8037787d834fef591da76 associa CErc20Certora a aliases state **6→789,18→456,19→321**; EIP20.spclnk blob cb89e560789d881139449b687342449e1f35d25f associa eip20.cvl e aliases **6→789,18→456** apenas. Não unir essas cenas, nem confundir env de transação com snapshot storage. Guia CVL2 recomenda transformações lexicais de invoke, sinvoke e static_*, mas não prova storage/reverts do engine Specify 2019. P17 41 NOT_RUN CVL2.

## Infraestrutura e próximos dois experimentos

**Preflight da R10 falhou parcialmente:** Desktop Commander via WSL reportou dispositivo online; pwd, python3 --version (3.14.4), git --version (2.53.0) retornaram. Entretanto git rev-parse HEAD e git status da worktree R9 produziram literalmente **fatal: error reading /home/mat/agente06-round9-20261020/.git**; df -h, cat .git e alguns ls passaram a retornar saída vazia ou sem dados confiáveis. Isso NÃO demonstra errno EIO/EROFS/SIGBUS determinado nem parser CVL2 falho. Por segurança **nenhuma escrita/comando de compilação/worktree/reset/repair subsequente** foi feita naquele WSL. R10 executada somente em memória via conector GitHub (leitura/checagem/comits documentais).

**Gate 1 P4:** após administrador restaurar e verificar o WSL, comparar fonte+ABI R9 com o bundle **do job auditado**, compiler, config e hashes. Quando houver cena e aprovação, adicionar apenas em scratch output bytecode/deployedBytecode ao mesmo compilador e capturar SHA sem editar originales; então decidir CVL2 compile-only por property.

**Gate 2 P22:** recuperar run FullMathWrapper histórico (target+global spec+solc+library+--rule exata); em cenário único aprovado, testar completa versus N.spec isolada com hashes e parser CVL2, sem inserir require ou methods para ocultar diferença.

**Estado:** documentação 159/159, três closures textuais FullMath, zero tentativas de CVL2 originais ou derivadas na R10, zero COMPILE_OK, zero COMPILE_ERROR, 159 NOT_RUN, zero equivalências, zero projetos concluídos. Read-only peer audit PR #41 em [ROUND10_PR41_READONLY_REVIEW.md](ROUND10_PR41_READONLY_REVIEW.md). QA no [ROUND10_QA.md](ROUND10_QA.md). PR #38 mantém-se Draft sem merge.

**AGENTE-06 — RODADA 10.**
