# P08 — mathint and bounds

**Authority:** A1-CAST, A2-MATH. CVL2 arithmetic yields mathint. Where the actual property assigns arithmetic to bounded integers or calls Solidity with arithmetic, review type conversions. `assert_uintX` reports out-of-range counterexample, while `require_uintX` discards them; choose neither without proof of the intended specification. Document original range constraints and equivalent behavior before any candidate patch.

## Segunda auditoria de aplicabilidade (19 Oct 2026)
Evidencia lexical em uma spec inteira NAO e prova de uso da sintaxe ou summary por cada property. A secao individual Contrarrevisao de evidencias por propriedade mostra os metodos e literais no corpo, antes/depois hipotetico e a escolha internal/external nao resolvida; verificar A2-OPTIONAL, A2-REFERENCE e A2-RETURNS antes de implementar. O receiver _ nao foi aprovado para nenhum caso sem grafo de chamadas. Nao usar require_ para esconder contraprovas.
