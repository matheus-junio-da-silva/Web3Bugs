# P05 — invariants, ghosts, quantification and filtering

**Authority:** A2-INVARIANTS, A2-MATH. Invariants may employ `filtered`, `preserved`, `requireInvariant`, hooks, and quantified expressions. Maintain method universe and induction base/step; filters can eliminate obligations and unjustified preserved conditions can yield misleading success. Quantified math cast behavior is restricted; never introduce `require_` to suppress counterexamples. Only attach P05 where the *individual* original CVL interval contains relevant constructs. No proof of the original soundness claimed.

## Segunda auditoria de aplicabilidade (19 Oct 2026)
Evidencia lexical em uma spec inteira NAO e prova de uso da sintaxe ou summary por cada property. A secao individual Contrarrevisao de evidencias por propriedade mostra os metodos e literais no corpo, antes/depois hipotetico e a escolha internal/external nao resolvida; verificar A2-OPTIONAL, A2-REFERENCE e A2-RETURNS antes de implementar. O receiver _ nao foi aprovado para nenhum caso sem grafo de chamadas. Nao usar require_ para esconder contraprovas.
