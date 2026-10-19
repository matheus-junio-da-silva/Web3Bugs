# Upstream checks — AGENTE-07 / Project 11 — Keep Fully Backed Bonding

Fase 1 documental, 2026-10-19. Consultas GET feitas via conexão GitHub; nunca executado Prover/compilador.

| Evidência | Repositório | Commit | Resultado | Referência |
|---|---|---|---|---|
| Audit PDF commit in keep-ecdsa | keep-network/keep-ecdsa | 658b02f237e25c370feaba80a7a3b13824190c4 | GitHub API 422: No commit found for SHA no repositório consultado | https://github.com/keep-network/keep-ecdsa |
| Historical source-branch commit | keep-network/keep-ecdsa | a5cd1713621d94868765d1570fae373f4a497521 | GitHub commit API: OK | https://github.com/keep-network/keep-ecdsa/commit/a5cd1713621d94868765d1570fae373f4a497521 |

## Limites e impacto
A conclusão 46/46 blobs iguais ao branch histórico consta do catálogo preexistente. Esse compromisso foi obtido ~um mês após o período 2-16/11/2020 do relatório e não foi usado para substituir a SHA auditada. Não procurar tokens nem usar credenciais.

**Não há blob SHA comprovadamente correspondente ao código e import closure do Prover histórico para todos os casos.** Os dossiers mantêm `UNRESOLVED_CANDIDATE` onde falta essa correspondência.

## Historical dependency follow-up — 2026-10-19
Branch a5cd1713621d94868765d1570fae373f4a497521 in keep-network/keep-ecdsa, path solidity/package.json, states keep-core >1.5.0-pre <1.5.0-rc; sortition-pools >1.2.0-pre <1.2.0-rc; openzeppelin-solidity 2.3.0. Exact branch solidity/package-lock.json SHA-256: 565f154194c6ab4d122112b57913f6c2ee748afd93ab7d6b9e030c17d455e277 (1100930 bytes).
Lock resolves direct packages as follows, and the npm tgz contents were downloaded on 2026-10-19 and SHA-512 checked against lock integrity:
- @keep-network/keep-core 1.5.0-pre.0; URL https://registry.npmjs.org/@keep-network/keep-core/-/keep-core-1.5.0-pre.0.tgz; sha512 SRI sha512-A1tY5TBD0y4q/XbYtOtTlgwzGP/4Lwhm5/fiQd/HJW5xh7m97UkfIOwdn49fJIo/Q3xsBqHASfvm0Fb0b0Zk/w==; verified=True; archive SHA-256 41b278473f2f8d35c28afe99710c8ec48f49b6540a0708f54dfec3bcf1e4cee2.
- @keep-network/sortition-pools 1.2.0-pre.3; URL https://registry.npmjs.org/@keep-network/sortition-pools/-/sortition-pools-1.2.0-pre.3.tgz; sha512 SRI sha512-MlhhegYQ/bG/vA9IT8Vxgn+ojvluC0YENF+Ic3xJNP6Ir/MEWH6gC7rDeaILzOJdqSVV5/8I53aTbYSRwzHoSg==; verified=True; archive SHA-256 ce939202e2f35f8624250e3d7671660ac500e0ed57a20e4cf4a730e21e7573c0.
- openzeppelin-solidity 2.3.0; URL https://registry.npmjs.org/openzeppelin-solidity/-/openzeppelin-solidity-2.3.0.tgz; sha512 SRI sha512-QYeiPLvB1oSbDt6lDQvvpx7k8ODczvE474hb2kLXZBPKMsxKT1WxTCHBYrCU7kS7hfAku4DcJ0jqOyL+jvjwQw==; verified=True; archive SHA-256 230c85042d682e45deb2797e64a47f04e27e9d4e3486b9806df1e38994d1a7a9.

All 22 distinct DIRECT external import paths in snapshot contracts/11/**/*.sol map to corresponding files in these downloaded archives (22/22 present); per-file SHA-256 hashes follow in direct_dependency_paths.csv. This is a useful closure of direct imports, NOT closure of packages own transitive imports or their nested versions: @keep-network/keep-core has a nested openzeppelin-solidity 2.4.0 dependency in lock while top-level is 2.3.0. Compiler resolution needs verification.
The 2020 PDF audit SHA 658b02f237e25c370feaba80a7a3b13824190c4 was not located in consulted keep-ecdsa commit history. Source branch a5cd... is a DIFFERENT identity and should never replace the audit SHA. Even byte-identical local contract snapshot to the source branch (as catalogued elsewhere) cannot prove the complete audit model. No package installation or compilation performed.
Links: https://github.com/keep-network/keep-ecdsa/blob/a5cd1713621d94868765d1570fae373f4a497521/solidity/package.json ; https://github.com/keep-network/keep-ecdsa/blob/a5cd1713621d94868765d1570fae373f4a497521/solidity/package-lock.json
