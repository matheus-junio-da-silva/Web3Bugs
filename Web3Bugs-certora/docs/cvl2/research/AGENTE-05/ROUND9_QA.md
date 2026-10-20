# AGENTE-05 — ROUND9_QA / execução real, inventário sem duplicações e limites

**Data:** 2026-10-20. PR [#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40) Draft, branch `research/cvl2-agente-05`. HEAD de partida conferida `d9e8e668a92dd468a5e676e1e6ef7d284affab78`. Baseline histórico `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Todos os commits da R9, inclusive correção de whitespace, ficaram exclusivamente em `Web3Bugs-certora/docs/cvl2/research/AGENTE-05/`; nenhuma spec original, contrato, label, resultado, relatório, assert, require, summary ou harness alterado. Nenhum Prover/CVL1 nem merge.

## Integridade de fontes — tarefas realmente executadas

1. Leitura via GitHub dos quatro documentos obrigatórios `spec_catalog.md`, `spec_catalog_workflow.md`, `spec_catalog_project_1.md`, `standard.md`, contraste P1 complete/1/1 e incomplete/1/1, documentação oficial [migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [statements](https://docs.certora.com/en/latest/docs/cvl/statements.html), relatório do [PR #48](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/48) e última revisão do coordenador em #40.
2. Geração de [ROUND9_MATRIX_148.csv](ROUND9_MATRIX_148.csv) por parser CSV independente sobre [ROUND8_MATRIX_148.csv](ROUND8_MATRIX_148.csv), `results/spec/spec_buglabel.csv` do baseline e `ROUND8_COMPILATION_ATTEMPTS.csv` da coordenação: **148/148 chaves únicas**, **149 relações** para P3=3, P6=32, P7=74, P19=37, P21=2; **0 divergências** em Property/Target/Result/Detection Outcome/labels. Hashes N.spec da maioria herdados e confrontados com ledger anterior, **não recalculados bytes de todos 148 nesta R9**; os cinco P7 originais focais foram conferidos no WSL e comparados com manifest R5.
3. Verificação da lista tentativa-caso, incluindo **18 tentativas globais em 16 chaves**, das quais **11 tentativas correspondem a nove propriedades da carteira**: seis exit0 (4 anteriores + 2 DERIVED_SIX_SIG_PREFIXES do coordenador em R8), cinco exit1 das originais P7, **intersecção de duas chaves** P7/47,73, e **139** chaves da carteira sem qualquer teste observado. A execução R9 do AGENTE-05 com Certora é **0**: nenhuma `certoraRun --compilation_steps_only`, nenhum parser fail novo, nenhum `PREFLIGHT_AUTH_BLOCKED`. `SEMANTIC_PROVEN=0`, projetos migrados=0.
4. **Auditoria independente real em WSL, somente leitura:** foram conferidos `sha256sum` de originais e variantes preservados em `/tmp/cvl2_coordinator_round8_20261020/{47,73}/specs/` contra o CSV do coordenador, e `exit_code.txt=0` de cada um. Os seis prefixos foram reproduzidos **só em memória** sobre arquivos originais: SHA256 do resultado e compare de sufixo da rule coincidiram com os dos pilotos. O stdout de P7/47 inclui warning de autofinder `Stack too deep` e fallback, com exit principal 0. **Releitura de `.abi` Solidity-only:** Stable 33 e Variable 30 funções, seis selectors ERC20-style presentes em ambas e revertendo no Solidity. Não inferir não-vacuidade ou equivalência.
5. **Propostas novas exclusivamente em memória:** P7/41 e P7/63 têm exatamente sete literais legados cada (seis no filtro e um `delegationWithSig` na assertion); hashes hipotéticos calculados e guardados documentalmente em [ROUND9_EVIDENCE.md](ROUND9_EVIDENCE.md); **nenhum arquivo candidato escrito ou executado por Certora**.
6. Contrarrevisão **somente leitura** PR #38 HEAD `6da9aac35f73a6b0a792807ee6000b7e8b7f077f`: P1 `queue2/_mock` temporal, P4 `src` versus `munged` e solc8.17, P17 Specify 2019 `.spclnk` divergentes, P22 wrappers/runner. Nenhuma edição na branch alheia.

## Saúde operacional e QA local realmente executado (sem confundir com Certora)

O coordenador havia observado recuperação temporária do WSL `DESKTOP-5E26TVU`; **R9 validou novamente** comandos simples `pwd`, `git --version`, `python3 --version`, `df -h` e clean status. Um worktree novo, **isolado e com status vazio**, foi criado em `/home/mat/cvl2-agente05-round9-20261020` a partir da **HEAD exata da branch remota**, sem reset, rebase nem tocar worktrees de outros agentes. A unidade retornou leitura e execução estáveis; `/tmp` local é scratch. Ao retornar EIO/SIGBUS/EROFS, a regra permanece suspender imediatamente.

Os seguintes **quatro comandos exatos** foram executados dentro do checkout desse worktree sobre a HEAD `e8becb4f7455dd5ae10694b87eeeb86949a6951b` (antes da inserção deste próprio arquivo de QA), com **EXIT 0**:

```bash
cd /home/mat/cvl2-agente05-round9-20261020/Web3Bugs-certora
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
cd ..
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

Outputs confirmados: `Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.`, `Check passed!` para contests/contracts e ausência de erros em `git diff --check`; `git status --porcelain` vazio. O primeiro check de whitespace realizado antes da correção **falhou legitimamente** em `ROUND9_EVIDENCE.md:46: trailing whitespace`; foi corrigido **somente esse espaço** em commit `e8becb4f7455dd5ae10694b87eeeb86949a6951b`, rechecado exit0. **Não ocultar falha inicial nem declarar que o check sempre passou.**

**Controle pós-commit deste arquivo:** os quatro comandos precisarão ser **reexecutados na HEAD final** depois de publicada esta QA; resultados exatos, escopo `BASE...HEAD` e GitHub Actions serão registrados no **comentário final do PR #40** com a SHA final. A confirmação deste arquivo por si não substitui o check depois do commit. O workflow GitHub `validate` é evidência separada de `check_contests_csv`, `check_contracts`, `check_git`, não Prover/CVL2 nem o `git diff --check` local.

## Bloqueios, semântica e próximos gates

**Duas candidaturas para revisão específica do coordenador:** (A) P7/41 StableDebtToken, (B) P7/63 VariableDebtToken, cada uma com **sete** prefixos `sig:` estritamente lexicais no N.spec (incluindo o selector dentro da assertion), `f(e,args)` sem `@withrevert` preservado, sem inserir premissa, sem derived publicado. Verificar snapshots, hashes, ABI, toolchain, recepção de métodos e global spec antes de autorizar *qualquer* `--compilation_steps_only`; os dois alvos não são intercambiáveis. Próximo gate posterior requer evidência de instanciação real de `method f`, não-vacuidade, semântica de revert e contraexemplos históricos.

**Alertas:** semântica **VERMELHA** (dispatch de `method f`, globals/ghosts/hooks, EIP712/nonce, P19 `RCPT=0` e divisor indefinido, P21 getter/harness ausente); infraestrutura **sob observação** após recuperação pontual, não garantia permanente. P19/1,2 continuam `02_unresolved` no PR #46 Draft. `00_unchanged` e `DOCUMENTED_CANDIDATE` não são provas.

**AGENTE-05 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.**
