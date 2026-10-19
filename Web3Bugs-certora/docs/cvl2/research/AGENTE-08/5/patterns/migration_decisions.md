# AGENTE-08 — Regras e riscos CVL1 → CVL2 (somente hipóteses)

**Fase 1: este documento não substitui os dossiês por exemplo.** Referência A1: [Migration Guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), seções Step 2–4, e [Changes Introduced in CVL 2](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), seções Superficial syntax / Methods / Integer types / Removed features. A2: [Methods Block](https://docs.certora.com/en/latest/docs/cvl/methods.html). Páginas consultadas em 2026-10-19; versões executadas: nenhuma.

## E-METHODS — assinatura, despacho e receptor
- CVL1 pode conter `methods { foo(uint256) returns uint256 envfree }`. Em CVL2, o formato candidato é `function foo(uint256) external returns(uint256) envfree;` **somente depois de confirmar no Solidity se a chamada é external, internal ou pública compilada nas duas modalidades**.
- Summaries CVL1 alcançavam todas as implementações da assinatura; CVL2 presume `currentContract`. A forma wildcard `function _.foo(uint256) external => NONDET;` pode ser necessária para manter escopo global, mas não deve ser usada sem correspondência comprovada. Contratos secundários `using ... as ...` exigem resolução específica.
- Risco: restringir o receiver pode tornar a regra vacuamente verdadeira, expandir summaries pode mascarar efeitos ou criar falsos contraexemplos. Alternativa conservadora: manter uma anotação de compatibilidade pendente e não produzir spec compilável na Fase 1.

## E-INV — chamadas, reverts e seleção de métodos
- Documentação A1 Step 2: `sinvoke f(...)` tem candidato `f(...)`; `invoke f(...)` tem candidato `f@withrevert(...)`. Não alterar a posição de `lastReverted`, guards ou storage inicial. Fonte precisa está no N.spec citado por cada dossiê.
- Se houver literal `f.selector == fn(uint).selector`, a documentação A1 exige `sig:fn(uint).selector` **para o literal**, não para `f.selector` (E-SELECTOR). A presença de `.selector` sozinha não prova incompatibilidade.
- Risco: passar a explorar caminhos com reverts antes ignorados ou vice-versa. Alternativa: esperar comparação formal de paths na fase posterior.

## E-SEMICOLON — declarações históricas
- CVL2 requer terminador `;` nos `import`, `using` e `use`. `invariant` com `filtered`/`preserved` pode dispensar semicolon conforme seção oficial. Não adicionar `;` cegamente após comentários ou blocos.

## E-MATH — tipos/quantificadores
- CVL2 diferencia `mathint` e inteiros de largura fixa. `assert_` pode gerar contraexemplo, `require_` pode eliminar casos e mascarar bugs (guia A1 Step 3). Nunca propor `require_` como atalho automático; recast só com argumento explícito, domínio e bounds preservados.

## Condição para fase posterior
Para cada transformação, reabrir o N.spec, sua original source range e N.txt; verificar harness ABI, scripts/flags e original Result; comparar mesmo alcance, preconditions, ghosts/hooks, quantificadores, storage e possíveis contraexemplos. Sem reconstrução do modelo original, marcar UNRESOLVED_CANDIDATE, mesmo se sintaxe parecer simples.

## Famílias AAVE StarkNet — casos a revisar individualmente
- **P5 todos os 17:** o source `BridgeHarness`, `BridgeL2Harness`, SymbolicLendingPool, mocks e `erc20.spec` são ausentes no snapshot PropertyGPT, mas há blobs identificados no [commit 4c010c18](https://github.com/aave-starknet-project/aave-starknet-bridge/commit/4c010c18b08703e4f367db1e0c642c76c25e551b), registrados no recovery_manifest.csv. Isso comprova origem de arquivos, não fechamento de imports nem cena equivalente.
- **`erc20.spec`** declara métodos ERC20 com `DISPATCHER(true)`; `withdrawMessageStatus` e `bridgeRewardsMessageStatus` pertencem ao BridgeHarness. Não transferir summaries entre esses arquivos.
- **Regras duplicadas `depositWithdrawReversed` e `integrityOfDepositExpanded`**: resultados agregados do relatório não identificam qual instance de spec é destinatária; preservar NOT_STATED onde registrado.
- **Bridge.sol mais recente** no snapshot diverge do verificado (balanceOf versus scaledBalanceOf, approve versus safeApprove). A migração CVL2 não deve usar a implementação errada como alvo.
- **Índices ray, mocks de L2, `--optimistic_loop`, `--loop_iter 3`, solc8.10, links de alvo** precisam ser preservados ao comparar semântica. O comentário de script sobre 2 iterações diverge do flag executável; valor histórico comprovado é 3.

<!-- AGENTE08-R2 -->
## Contrarrevisão P5: scripts, remappings e ABI
No commit 4c010c18b08703e4f367db1e0c642c76c25e551b, erc20.spec blob b12fec167edd76a2f59a64bc80bc33a9eeb04f65 contém somente methods ERC20 DISPATCHER(true). Os getters withdrawMessageStatus/bridgeRewardsMessageStatus aparecem no BridgeHarness.sol blob 850d5a63fa375ee6f9754c8377990d5d48c09c07, não no erc20.spec.
Os scripts verifyBridge.sh e verifyBridgeConstIndex.sh fixam BridgeHarness e seus mocks, nove links, solc8.10, optimistic_loop, loop_iter 3 e settings -mediumTimeout=700,-depth=12. Comentário de texto diz 2 iterações; comando executável usa 3. Não há argumento packages/path explícito nos scripts; imports indiretos continuam exigindo fechamento. Makefile target munged copia contratos e aplica applyHarness.patch (blob f806c1e6957b164a0a8419fa6f5c8015de5dd95c), inclusive alterações virtual em Bridge.sol. O snapshot contém Bridge.sol de revisão posterior, e os 17 exemplos seguem incomplete. A recuperação dos blobs não prova ABI transitiva nem equivalência de prova.
