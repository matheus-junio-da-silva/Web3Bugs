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

## Famílias Opyn — casos a revisar individualmente
- **P14/1, `orderOfOperations`:** apenas o ramo condicionado por ordem do selector compara collateral pós-duas ordens de operação; o outro ramo termina em `assert true`. Não fortalecer regra para comutatividade universal e não extrapolar relatório Property 18.
- **P14/2–14:** MarginVaultHarness; distinguir latest-code VERIFIED de findings históricos nas variantes inverse/additive.
- **P14/15–19:** cinco casos especializados NoBankruptcy usam ControllerHarnessExtra; PDF apresenta solvência geral sem resultado separado por caso.
- **P14/20:** Whitelist target e summaries de privilégio demandam conferência de receiver.
- **P14/21–34:** ControllerHarness com scripts, mocks, links e `applyHarnesses.sh` que pode mutar contratos antes da execução; snapshot sem alterações não é necessariamente input histórico do Prover.
- Os 34 estados originais `complete` significam apenas fechamento documental das dependências; nenhum foi compilado nesta fase.
