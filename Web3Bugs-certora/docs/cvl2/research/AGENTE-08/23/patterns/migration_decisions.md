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

## Famílias Radicle — casos a revisar individualmente
- **P23/1–12:** DripsHubHarness ausente; **P23/13–18:** UpdateReceiverStatesHarness ausente; não misturar schemas.
- **P23/19–23:** ReserveHarness e DummyERC20s ausentes; **P23/24:** SlotTester e `getPausedSlot`/`get_storageSlot` ausentes, não substituir por campos no DripsHub.
- **P23/25–41:** Splits.sol com métodos internos e wrappers CVT gerados; só as propriedades identificadas no PDF receberam históricos VERIFIED/VIOLATED. P23/36 é VIOLATED/FINDING por arredondamento; P23/38 teve timeout (NOT_STATED/INCONCLUSIVE).
- **P23/42–46:** Splits2.spec é distinta, não herda os resultados de nomes homônimos em Splits.spec.
- O commit [6fe9d38](https://github.com/Certora/drips-contracts/commit/6fe9d38a30765df6aa3e4078634a37aeabbceef1) mostra produção e testes, sem comprovar conteúdo/ABI do harness de verificação original.

<!-- AGENTE08-R2 -->
## Contrarrevisão P23: provedores de CVT não encontrados
O PDF de seis páginas (sobretudo páginas 3-5) restringe a verificação formal a Splits.sol. A árvore do commit oficial Certora/drips-contracts@6fe9d38a30765df6aa3e4078634a37aeabbceef1 contém produção e testes, mas não os CVT wrappers esperados; isso não prova inexistência em servidores ou artefatos gerados históricos. DripsHubHarness (#1-12), UpdateReceiverStatesHarness (#13-18), ReserveHarness/mocks (#19-23), SlotTester/getters (#24) e wrappers Splits/Splits2 (#25-46) permanecem não recuperados. #36 VIOLATED/FINDING por arredondamento, #38 NOT_STATED/INCONCLUSIVE por timeout e #39-41 VERIFIED apenas nas suas instâncias Splits.spec. O limite de unrolling (2) e receiver weights (até 1000000) não foram ampliados.
