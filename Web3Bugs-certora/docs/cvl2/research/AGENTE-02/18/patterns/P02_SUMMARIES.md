# P02 — summaries and receiver drift

**Authority:** A2-SUMMARY, A2-CVL-METHODS. CVL1 same-signature summary was global; CVL2 defaults to `currentContract`. Conditional candidate only: `function _.f(...) external => NONDET;` *if and only if* the original summary was global and return type/expect rules are resolved. An explicit defining contract may be necessary for inherited methods. Changing from DISPATCHER to NONDET, replacing a ghost, or adding `require` would be semantic changes, not grammar fixes.

Particularly investigate Governor/RulesInProgress and any multi-contract harness. Log ABI, full call-resolution universe, and original receiver coverage before any implementation. Source evidence SRC18-###; syntax A2-SUMMARY. Semantics unproven.

## Segunda auditoria de aplicabilidade (19 Oct 2026)
Evidencia lexical em uma spec inteira NAO e prova de uso da sintaxe ou summary por cada property. A secao individual Contrarrevisao de evidencias por propriedade mostra os metodos e literais no corpo, antes/depois hipotetico e a escolha internal/external nao resolvida; verificar A2-OPTIONAL, A2-REFERENCE e A2-RETURNS antes de implementar. O receiver _ nao foi aprovado para nenhum caso sem grafo de chamadas. Nao usar require_ para esconder contraprovas.
