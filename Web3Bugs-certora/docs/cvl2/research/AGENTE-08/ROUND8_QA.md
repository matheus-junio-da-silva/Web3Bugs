# AGENTE-08 — RODADA 8 / QA, integridade e observações NÃO executadas

**PR [#43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43), DRAFT, branch `research/cvl2-agente-08`.** Commit inicial pinado `fe0c25ae89835616a8b36f86cb067c4ab6a5fcf1`, baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` imutável. A coordenação integrou apenas documentação/checadores do PR #47 à main, não autorizou implementação ou merge deste PR.

## Execuções de documentação/validação realmente realizadas pelo conector GitHub

- Leitura HEAD, PR DRAFT, reviews mais recentes de PR #43 e PR #39 e painel `ROUND7_DASHBOARD.md` já integrado à main. Leitura dos quatro documentos originais de metodologia do catálogo e de `complete/1/1.spec`, `incomplete/1/1.spec`, `incomplete/1/1.txt`.
- Em memória, foram parseados o `results/spec/spec_buglabel.csv` do baseline Git blob `97e20443586540034a4c0305ce1db19b0d2f8cb5` e `ROUND7_MATRIX_155.csv` existente. Para cada chave, exigiu-se consistência entre relações multilabel e compararam-se **Property, Target Contract, Result, Detection Outcome, Original Spec e Original Spec Lines**. Resultado **155/155 chaves únicas**, projetos P5 17/P13 58/P14 34/P23 46, **zero mismatches**. Os Bug Labels históricos foram copiados diretamente do CSV canônico (sem supor que `UNMAPPED` ou múltiplos labels sejam resultados Prover).
- A `ROUND8_MATRIX_155.csv` foi **gerada em memória**, com os seis campos canônicos, Bug Labels, `original_spec_sha256_from_R7` (hash preservado, **não recalculado** na R8), source factual, inferência, falta de prova, status e execução. **155 `NOT_RUN` CVL2**, 155 com bloqueio ambiental separado, 0 semânticas demonstradas.
- Via GitHub foram examinados: relatório `reports/23.md` (escopo `Splits.sol`, commit `6fe9d38`), tree da branch `Certora/drips-contracts@8d1db123` (**70 registros**) e tree da produção `6fe9d38` (**44 registros**) para localizar saída CVT — **sem pathname de output CVT gerado** nessas duas árvores, não prova de ausência universal. Recuperados `SplitsHarness`, `runSplits`, `runSplits2`, pin OZ; confrontadas seis specs e `src/Splits.sol` por Git blob com snapshot. Consultados sources/runner P5, linhas do Controller Opyn e scripts Notional. A cross-review PR #39 foi SOMENTE LEITURA.
- As publicações foram feitas **exclusivamente pela ação GitHub create_file**, na branch do agente, sem checkout/escrita no WSL nem commit ou PR paralelo. A checagem literal de linhas com trailing whitespace dos documentos Markdown precedeu upload e retornou zero. As verificações via conector são remotas/documentais, não garantem sucesso do comando `git diff --check` completo.

## Comandos bloqueados — não declarar exit 0

A coordenação mantém o dispositivo WSL DESKTOP-5E26TVU sem recuperação administrativa comprovada após falhas EIO, EROFS, SIGBUS. **Nenhum comando de processo foi executado no WSL na Rodada 8**. Não há compilação, log CLI ou hash de scratch novo.

| Comando/ação previsto | Realmente executado R8? | Status correto |
| --- | --- | --- |
| `python3 scripts/check_specs.py .` (dentro de `Web3Bugs-certora/`) | NÃO | **NOT_RUN_INFRA_BLOCKED** |
| `python3 scripts/check_contests_csv.py .` | NÃO | **NOT_RUN_INFRA_BLOCKED** |
| `python3 scripts/check_contracts.py .` | NÃO | **NOT_RUN_INFRA_BLOCKED** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | NÃO | **NOT_RUN_INFRA_BLOCKED** |
| `certoraRun --compilation_steps_only` para `incomplete/5/14.spec` | NÃO | **NOT_RUN_INFRA_BLOCKED** |
| `certoraRun --compilation_steps_only` para `incomplete/23/42.spec` | NÃO | **NOT_RUN_INFRA_BLOCKED** |
| `solc` ABI; `certoraRun --version`; Prover completo; CVL1; patches/solc in-place; worktree WSL | NÃO | **NOT_RUN** |

`COMPILE_OK=0`, `COMPILE_ERROR=0`, `NOT_RUN=155`, `PREFLIGHT_AUTH_BLOCKED=0` observado, `SEMANTIC_PROVEN=0`. Não imputar observações 4 OK + 12 erros CVL2 de outros agentes à carteira, nem reclassificar a compilação Solidity da R5 como CVL2. CI remoto `validate` poderá rodar automaticamente após os commits: **reportar conclusão real da HEAD final**, distinguindo de execução local de Python/whitespace.

## QA de commit e autorização de retomada

Após a HEAD final ser publicada, conferir:
1. HEAD remota ainda na **mesma** `research/cvl2-agente-08`, PR #43 **DRAFT**, sem merge;
2. `compare_commits(BASE...HEAD)` — todos os caminhos **somente** em `Web3Bugs-certora/docs/cvl2/research/AGENTE-08/`;
3. novamente a existência da `ROUND8_MATRIX_155.csv` com 155 chaves e `ROUND8_EVIDENCE.md`, `ROUND8_QA.md`; inspeção textual de whitespace nos documentos novos;
4. `validate` da HEAD final por API GitHub. Um `SUCCESS` prova apenas integridade estrutural nos passos do workflow, não os quatro comandos locais no WSL nem semântica CVL2.

**Intervenção humana obrigatória antes dos próximos experimentos**: o administrador deve confirmar backups, saúde do filesystem, scratch novo gravável, `git status` e worktree correta, versões CLI/solc e todos os hashes. Somente depois os quatro comandos de QA local podem ser executados, e apenas cenário **individual** autorizado pelo coordenador deve prosseguir para compile-only em scratch byte-idêntico, timeout, `cmp`/SHA256, stdout/stderr completos. Nenhuma autorização para correção de original, Prover, CVL1, ou merge de PR de implementação.

**Alerta operacional: VERMELHO (WSL precisa intervenção humana). Alerta semântico: LARANJA (155 unresolved; riscos vermelhos P5/P14/P23).**

AGENTE-08 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.
