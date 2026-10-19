# P04 — invariant termination

**Authority:** A2-SEMI. Only invariants *not followed by* filtered/preserved blocks need an expression-final `;`. Do not insert a semicolon inside an existing filtered or preserved clause; read the entire declaration and its helpers, not only the property title. Syntax is not evidence that the invariant is inductive or sound. Historical result remains unchanged.

## Segunda auditoria de aplicabilidade (19 Oct 2026)
Evidencia lexical em uma spec inteira NAO e prova de uso da sintaxe ou summary por cada property. A secao individual Contrarrevisao de evidencias por propriedade mostra os metodos e literais no corpo, antes/depois hipotetico e a escolha internal/external nao resolvida; verificar A2-OPTIONAL, A2-REFERENCE e A2-RETURNS antes de implementar. O receiver _ nao foi aprovado para nenhum caso sem grafo de chamadas. Nao usar require_ para esconder contraprovas.
