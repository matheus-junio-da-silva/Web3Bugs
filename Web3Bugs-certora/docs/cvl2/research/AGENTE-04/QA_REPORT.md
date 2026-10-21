# AGENTE-04 — cross-project QA and handover (2026-10-19)

- Baseline Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- All 3 `properties.csv` parsed as quoted CSV. **157 distinct canonical keys**: Project 2 (1 complete, 14 incomplete), Project 12 (17 complete, 9 incomplete), Project 15 (0 complete, 116 incomplete). Total: **18 complete / 139 incomplete**.
- GitHub compare from baseline to draft branch, checked at commit `925c1e8edf68128a123380d8f485e46fc571ed49`: 24 commits ahead, 206 changed files, all inside `Web3Bugs-certora/docs/cvl2/research/AGENTE-04/`. Exactly **157** new individual dossier paths, all referenced by their corresponding `properties.csv`. No changes to historical `.spec`, `.sol`, contracts snapshot, catalogs, CSV original, scripts or reports.
- The GitHub compare scope test is distinct from execution of `git diff --check`; CLI/solc/Prover were **not** executed.
- The Project 15 pinned baseline includes semantic adjudication that shifted one `balance_after_burn` historic result to NOT_STATED; do not overwrite it with older catalog markdown values.
- Cross-project assumptions not treated as proven: recovery of historical hidden harnesses, blob-identity of external dependencies, original Prover configs, quantified reachability, preserved/invariant induction, receiver scope of summaries, no-loss-of-counterexamples under casts, report per-rule attribution.
- Research files may contain candidate patterns whose precise applicability remains provisional; links/evidence and individual CVL snippets are checkpoints for coordinator review, not automated migration instructions.
- No attempt was made to create Fase 2 code, alter source history or merge.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**

## Contrarrevisao 2026-10-19
Cobertura 157/157 (P15 116, P12 26, P2 15). Commits auditados 15:ce49fb0c94cfebf0159222ceb288e4f9a55d305f, 12:750920303e33b66bc29862ea3b85206dda9ce786, 2:12296ce4c6f9bde6663e1baa02cf19f179c1048b. PDF 13+25+6 paginas examinados; novos B1 registros, scripts de epoca, lock npm, diferenca de constructor V2 e ausencia de helpers Por identificados sem reconstrucoes. Sem CVL1, CVL2, Prover e sem alterar specs/Solidity. Status de fonte e ferramenta ainda incompleto; PR continua Draft.


## Validação estrutural em WSL após contrarrevisão — execução efetiva

A afirmação antiga de que o desktop estava indisponível e de que os validadores não tinham sido executados descreve SOMENTE a primeira entrega; está **superada** pela retomada de 2026-10-19. Device remoto DESKTOP-5E26TVU online; checkout isolado em /tmp/cvl2-agent04-20261019/repo (não interfere nos demais agentes).

Diretório de execução dos três validadores: /tmp/cvl2-agent04-20261019/repo/Web3Bugs-certora
- python3 scripts/check_specs.py . — exit 0; saída: Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . — exit 0; saída: Check passed! results/contests.csv consistent with reports.
- python3 scripts/check_contracts.py . — exit 0; saída: Check passed! contracts consistent with reports.

Diretório de execução Git: /tmp/cvl2-agent04-20261019/repo
- git diff --check — após normalizar exclusivamente docs/cvl2/research/AGENTE-04, exit 0. O diff inicial contra base detectou whitespace nos dossiês originais; foi sanado APENAS em documentos.
- O comando git diff --check origin/main...HEAD falhou com exit 128 por clone --single-branch sem ref origin/main. Não é resultado negativo do dataset. Para comparação final usar explicitamente o commit base 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 e o novo SHA, cujo exit deve ser registrado após publicação.

Nota sobre QA: o uso de 1386/1390 é a contagem da main congelada; os índices adicionais de pesquisa (157 chaves) não alteram o catálogo. Nenhuma execução de certoraRun, solc, CVL1, CVL2 ou Prover. Os status históricos continuam intocados.

## Segunda revisao independente - gate Fase 2
157/157 com campos separados de sintaxe, ABI pendente, dependencia historica, risco semantico e phase2 readiness. Todos UNRESOLVED, inclusive os 18 DOCUMENTED_CANDIDATE (17 P12 e 1 P2). Estudos: [GHO](15/HISTORICAL_PACKAGE_CLOSURE.md); [AAVE V2](12/HISTORICAL_HARNESS_COMPARISON.md); [Proof of Reserve](2/HISTORICAL_ABI_SEARCH.md). Buscas negativas encerradas nas fontes examinadas sem inventar runtime. Sem Fase 2, sem mudar codigo original.
