# P07 — multicontract using aliases

**Authority:** A1-USING, A2-METHODS. Check `using ERC20VotesHarness as erc20votes`-type declarations against concrete targets, import propagation and method receiver semantics. The guide says a multicontract using declaration is not imported in CVL2. Only repeat/rename alias where the source actually depends on it; use contract names for user-defined types. No new aliases introduced in Fase 1.

## Segunda auditoria de aplicabilidade (19 Oct 2026)
Evidencia lexical em uma spec inteira NAO e prova de uso da sintaxe ou summary por cada property. A secao individual Contrarrevisao de evidencias por propriedade mostra os metodos e literais no corpo, antes/depois hipotetico e a escolha internal/external nao resolvida; verificar A2-OPTIONAL, A2-REFERENCE e A2-RETURNS antes de implementar. O receiver _ nao foi aprovado para nenhum caso sem grafo de chamadas. Nao usar require_ para esconder contraprovas.
