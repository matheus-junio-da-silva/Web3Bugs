# AGENTE-03 — Rodada 5 / contrarrevisão independente somente leitura PR #42

**Fonte:** PR https://github.com/matheus-junio-da-silva/Web3Bugs/pull/42, branch research/cvl2-agente-04, HEAD dc5f710cd1ef02ded3cb37dd0bb01362406d8e33, comparada contra baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. Leitura via git show FETCH_HEAD após fetch; **sem checkout de escrita nem alteração dessa branch**.

## Documentos revisados

- Web3Bugs-certora/docs/cvl2/research/AGENTE-04/ROUND4_REVIEW.md, seções P12/P2/P15, resumo de candidates e QA.
- AGENTE-04/12/HISTORICAL_HARNESS_COMPARISON.md; projetos 12/2/15, properties.csv e ROUND4_PROGRESS.csv segundo PR anterior; comentários mais recentes de coordenação PR #42 e PR #47.
- Dados na HEAD anterior de P2 source_commit_audited e P12 fonte recuperada foram vistos também na contrarrevisão da Rodada 4; esta rodada toma por base a HEAD dc5f710c.

## Resultados separados por fonte, harness, target e compilador

| Projeto | Relato de PR #42 e referência | Adjudicação somente leitura |
| --- | --- | --- |
| P12 / StableDebtToken incomplete/1–9 | Documento P12 menciona source auditada aave/protocol-v2@750920303e33b66bc29862ea3b85206dda9ce786, StableDebtToken.sol de construtor 5 args, runner runStableTokenCLI.sh, target StableDebtTokenHarness, --solc solc6.8 | Snapshot guarda variante initializer/getter diferente. Flags de script não autenticam versão/binário de compiler nem ABI do snapshot. **Não misturar harness auditado com Solidity da extração.** |
| P12 / UserConfiguration complete/19–26 | ROUND4_REVIEW.md identifica a remoção de address user de methods e harness no snapshot versus auditado. Prioridades 23 e 25 são **lexicais** | Nome igual de property ou target não preserva domínio do argumento; compile-only só sob rótulo snapshot versus auditado com target e ABI fixos, nunca equivalente por default. |
| P12 / VariableDebtToken complete/10–18 | ROUND4_REVIEW.md: 2/9 corpos parecem coincidir por tokens após remover espaços/comentários; 7/9 diferem; receiver/link POOL pendente | A escolha de harness, compiler e símbolo resolvido pode modificar efeito; não atribuir COMPILE_OK. |
| P2 / Proof of Reserve | Fonte Solidity auditada Certora/aave-proof-of-reserve@12296ce4c6f9bde6663e1baa02cf19f179c1048b e quatro contratos centrais coincidentes. No CVL de Aggregator, latestRoundData() => NONDET sem receiver auditável, e Executor usa PORaggregatorDummy/configuratorDummy ausentes | Source Solidity idêntica não prova summary do oráculo, ABI externa ou mocks. O uso de _.latestRoundData em CVL2 seria decisão semântica, não mera correção lexical. |
| P15 / GHO | aave/gho-core@ce49fb0c94cfebf0159222ceb288e4f9a55d305f. Tarballs autenticados do package-lock, Makefile e patch que modifica GhoToken.sol, solc8.10 citado nos scripts | SRI de pacote não prova node_modules usados nem SHA de munged na execução; patch injeta mudanças de visibilidade e require e compromete igualdade de ABI/semântica. Não promover os 116 casos. |

**Invariantes conferidos:** 157 instâncias em PR #42, 18 DOCUMENTED_CANDIDATE continuam apenas hipóteses (17 P12, 1 P2), 139 unresolved; diferença entre resultados de relatório e estado compilável é reconhecida. PR #42 mantém DRAFT; diff de 214 caminhos somente em AGENTE-04 conforme documentação e checkout remoto. Nenhuma alteração feita.

**Alerta cruzado:** os runners P12 são particularmente sensíveis a diferença entre script textual --solc solc6.8 e pragmas/compilador realmente executado; e o harness UserConfiguration remove address user no snapshot. A mesma disciplina é aplicada em P24, onde o patch LaunchEvent e o override impedem tratar fork como auditado.

**AGENTE-03 — RODADA 5 — QUALIDADE CVL2 (read-only).**
