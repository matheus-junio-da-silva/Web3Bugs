# AGENTE-02 — Rodada 6 / Registro fiel de QA, bloqueios e verificação remota

**Data:** 2026-10-20. Branch exclusiva `research/cvl2-agente-02`, PR #37 DRAFT; baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; nenhuma alteração de arquivos originais, `results/spec`, `contracts`, rótulos ou resultados históricos.

## O que foi de fato executado nesta rodada

1. **Leitura integral** dos quatro documentos obrigatórios (hashes e contagem de linhas em `ROUND6_DIRECT_CLI_DIAGNOSTICS.md`) e comparação dos exemplos completos/incompletos P1. Consultadas documentação oficial CVL2, últimas revisões PR #37, painel PR #47 e PR #36.
2. **Checkout/worktree isolada**: `/home/mat/cvl2-agente02-round6`, criada sem reset da branch. A partir daí o host WSL apresentou `EROFS` em `/home/mat`, `Segmentation fault` ao copiar uma spec para `/tmp` e `Bus error` na chamada ao CLI direto (`--version`), exit 135. Esta **não é execução de uma N.spec**. Não existem logs de parser CVL2 produzidos localmente na R6.
3. **Contraprova independente do coordenador já existente**: P18/complete/3 e /23, ambos `COMPILE_ERROR` exit 1 pelo parser CVL2 (métodos sem `function`/`;`), com hashes/cópias e fonte no PR #47/P18_DIRECT_CLI_CONTRACHECK.md. São as **duas observações reais disponíveis**, porém nenhuma foi reproduzida nesta rodada devido à falha do host.
4. **Reconciliador independente em memória via GitHub connector** executado sobre o CSV **canônico** `results/spec/spec_buglabel.csv` e `round6_diagnostic_matrix.csv`: 181 relações P18, 181 chaves únicas, **181/181 Property/Target/Result/Detection Outcome idênticos, 0 mismatches**. Matriz com 181 chaves únicas, 157 `ABSENT_AT_AUDITED_COMMIT`, 24 `CONTENT_DIFFERS`, 2 `COMPILE_ERROR` de autoria do coordenador, 179 `NOT_RUN` e 181 `SEMANTIC_UNRESOLVED`. A comparação foi realizada **sem executar** o programa `check_specs.py`.
5. **Verificação dos três novos artefatos via API**: `round6_diagnostic_matrix.csv`, `ROUND6_DIRECT_CLI_DIAGNOSTICS.md` e `ROUND6_ROCKETJOE_READONLY.md` tiveram **zero linhas com trailing whitespace** na leitura integral. O GitHub Compare da branch contra o baseline mostrava **242 arquivos, zero fora de `Web3Bugs-certora/docs/cvl2/research/AGENTE-02/`** no momento desta conferência.
6. **GitHub Actions existente `validate` na HEAD `3e9204c47d283ec205fad10e0187cba4f1389efb`**: workflow run **39473661717**, job `integrity_validation` id **118803929776**, concluído **SUCCESS**. Etapas `check_contests_csv`, `check_contracts` e `check_git` concluídas com sucesso. O workflow **não** executa `check_specs.py`, **não** roda o comando solicitado de `git diff --check BASE...HEAD` e **não** compila CVL2.

## Comandos solicitados e estado verdadeiro

| Comando | Resultado nesta rodada |
| --- | --- |
| `python3 scripts/check_specs.py .` em `Web3Bugs-certora/` | **NÃO EXECUTADO LOCALMENTE** — Python/WSL atingiu `Bus error`; reconciliação alternativa 181/181 por conector (não substitui script) |
| `python3 scripts/check_contests_csv.py .` em `Web3Bugs-certora/` | **CI GITHUB ACTIONS: SUCCESS** (etapa do workflow `validate`); execução local não concluída |
| `python3 scripts/check_contracts.py .` em `Web3Bugs-certora/` | **CI GITHUB ACTIONS: SUCCESS**; execução local não concluída |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NÃO EXECUTADO NO HEAD FINAL LOCALMENTE** por `/home/mat` readonly; verificação substitutiva de trailing whitespace dos novos artefatos e escopo via API, não equivalentes ao comando |
| Certora CLI direto `--compilation_steps_only` em N.spec scratch | **NÃO EXECUTADO na R6**; comando de inspeção `--version` terminou com sinal de erro de host (exit 135), antes de copiar qualquer target |

**QA anterior não transportado:** na HEAD da R5 `9350a3f9` os três validadores e `git diff --check BASE...HEAD` haviam retornado exit 0. Esse fato histórico **não** autoriza afirmar que foram reexecutados na R6.

## Artefatos publicados e próximos gates

- `round6_diagnostic_matrix.csv`: 181 chaves, resultados históricos originais, SHA-1/SHA-256 de fonte global, SHA de recortes quando previamente registrado, auditoria de origem, compilação efetivamente observada, provenance do observador, risco de vacuidade, bloqueio e próximo gate.
- `ROUND6_DIRECT_CLI_DIAGNOSTICS.md`: pares P18/3,4,23,46,53; erros do parser vistos pelo coordenador e falha de host local com comandos/exits realmente observados, scope `public` e summaries, Timelock, Initializable e Governor.
- `ROUND6_ROCKETJOE_READONLY.md`: revisão cruzada 5/5 P24 e contraprovas/limitações de patch/harness, source IDs e SRI.
- `ROUND6_QA.md`: este relatório.

**Dependências para encerramento R6**: recuperar host de execução com filesystem gravável e binário Python funcional; rodar exatos quatro checks solicitados sobre HEAD atual; reproduzir 5 casos P18 em scratch sem token e com logs e hashes. Separadamente, provar proveniência do run auditado para eventual conversão `internal/external`, receiver ou summary; nenhum cast, `require` ou alteração de assert foi autorizado.

**Estado de qualidade: pesquisa documental avançou; execução local R6 bloqueada por falha de infraestrutura. Sem `COMPILE_OK`, sem `SEMANTIC_PROVEN`, sem `MIGRATED_COMPLETE`.**

**AGENTE-02 — RODADA 6.**
