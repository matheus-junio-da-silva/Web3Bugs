# Upstream checks — AGENTE-07 / Project 11 — Keep Fully Backed Bonding

Fase 1 documental, 2026-10-19. Consultas GET feitas via conexão GitHub; nunca executado Prover/compilador.

| Evidência | Repositório | Commit | Resultado | Referência |
|---|---|---|---|---|
| Audit PDF commit in keep-ecdsa | keep-network/keep-ecdsa | 658b02f237e25c370feaba80a7a3b13824190c4 | GitHub API 422: No commit found for SHA no repositório consultado | https://github.com/keep-network/keep-ecdsa |
| Historical source-branch commit | keep-network/keep-ecdsa | a5cd1713621d94868765d1570fae373f4a497521 | GitHub commit API: OK | https://github.com/keep-network/keep-ecdsa/commit/a5cd1713621d94868765d1570fae373f4a497521 |

## Limites e impacto
A conclusão 46/46 blobs iguais ao branch histórico consta do catálogo preexistente. Esse compromisso foi obtido ~um mês após o período 2-16/11/2020 do relatório e não foi usado para substituir a SHA auditada. Não procurar tokens nem usar credenciais.

**Não há blob SHA comprovadamente correspondente ao código e import closure do Prover histórico para todos os casos.** Os dossiers mantêm `UNRESOLVED_CANDIDATE` onde falta essa correspondência.
