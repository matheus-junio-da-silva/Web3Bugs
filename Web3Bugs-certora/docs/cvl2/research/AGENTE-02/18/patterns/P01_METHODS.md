# P01 — methods declarations and visibility

**Authority:** A1-METHODS, A2-METHODS, A2-CVL-METHODS. Historical CVL1 entries of `methods` lack compulsory `function`, `internal/external` and `;`. **Candidate only:** e.g. `grantRole(bytes32,address)` → `function grantRole(bytes32,address) external;` **iff** contract ABI exposes matching external method, without unretained harness; `_checkRole(bytes32)` may instead be internal and not ABI callable. Inspect source-line and concrete method. Never presume the example alone demonstrates a valid translation.

Review each property's `SRC18-###`, target, ABI, inherited definition and any envfree getter. The extra annotation can alter which calls are summarized. No CVL2 compilation; alternative is to leave unresolved, not guess visibility.

## Segunda auditoria de aplicabilidade (19 Oct 2026)
Evidencia lexical em uma spec inteira NAO e prova de uso da sintaxe ou summary por cada property. A secao individual Contrarrevisao de evidencias por propriedade mostra os metodos e literais no corpo, antes/depois hipotetico e a escolha internal/external nao resolvida; verificar A2-OPTIONAL, A2-REFERENCE e A2-RETURNS antes de implementar. O receiver _ nao foi aprovado para nenhum caso sem grafo de chamadas. Nao usar require_ para esconder contraprovas.
