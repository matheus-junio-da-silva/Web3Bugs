# P03 — typed selector literals

**Authority:** A2-SELECTOR. A CVL1 literal `schedule(address,uint256,bytes,bytes32,bytes32,uint256).selector` is a candidate for `sig:schedule(address,uint256,bytes,bytes32,bytes32,uint256).selector`. `f.selector` is NOT prefixed. Independently, Timelock's original `methods` lists `schedule(address,uint256,bytes32,bytes32,bytes32,uint256)`; Solidity uses `bytes` in that position: resolving the discrepancy needs historical harness/target investigation, not a mechanical parser adjustment.

Use property SRC18-### to confirm typed literal in its own body and inspect selector comparison for affected cases. If mismatch remains, UNRESOLVED_CANDIDATE.

## Segunda auditoria de aplicabilidade (19 Oct 2026)
Evidencia lexical em uma spec inteira NAO e prova de uso da sintaxe ou summary por cada property. A secao individual Contrarrevisao de evidencias por propriedade mostra os metodos e literais no corpo, antes/depois hipotetico e a escolha internal/external nao resolvida; verificar A2-OPTIONAL, A2-REFERENCE e A2-RETURNS antes de implementar. O receiver _ nao foi aprovado para nenhum caso sem grafo de chamadas. Nao usar require_ para esconder contraprovas.
