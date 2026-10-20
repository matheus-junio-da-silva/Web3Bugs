# AGENTE-01 — RODADA 7 / QA, escopo e bloqueio operacional

**PR:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 — branch `research/cvl2-agente-01`, Draft. **Baseline catalogado imutável:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. **HEAD de partida verificada:** `58ca698ab8e1b81ee205a471d5d1cb98bb472ff9`.

## Leituras e verificações de fato realizadas

1. Consultadas revisões e comentários MAIS RECENTES dos PRs #39 e #37 e painel PR #47 na HEAD `948121599b546d61579dc9ecb8c316f9c088e78a` com `ROUND6_DASHBOARD.md`, `ROUND6_PROGRESS.csv`, `ROUND6_COMPILATION_OBSERVATIONS.csv` e `ROUND6_WSL_IO_INCIDENT.md`. Confirmado bloqueio EIO/SIGBUS/EROFS e proibição de comandos de escrita/build no WSL.
2. Lidos os quatro documentos de catalogação e integridade `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md`; comparação dirigida de referência P1 complete/incomplete, distinguindo `queue2` faltante de erros de sintaxe.
3. **Reconciliador em memória pelo conector GitHub EXECUTADO**, usando `round6_progress_matrix.csv` da HEAD inicial e `results/spec/spec_buglabel.csv` canônico. Gerada a nova `ROUND7_MATRIX_266.csv` com **266 pares de status/ID P10 únicos**; confrontados por linha Project ID, Status, Example ID, Property, Target Contract, Result e Detection Outcome. **266 matches e zero divergências**. Cada linha mantém source SHA Git do N.spec/N.sol, alvo, driver e próximo gate. Não alterar catálogo original.
4. Inventário `ROUND7_SELECTOR_INVENTORY.csv` extraído da `semantic_candidate_gate_matrix.csv` original da Rodada 6, que já havia sido testada com parser de comentários em R5: **13 method literals ACTIVE_CODE e 15 COMMENT_ONLY**. Não houve parsing/recompilação de todos os N.spec nesta R7 e não se reivindica tal atividade.
5. Por GitHub, os imports dos dois seeds `contracts/Registry.sol` e `specs/harnesses/ProxyHarness.sol` foram visitados recursivamente nos dois repositórios pinned (commit Furucombo 2021 e tag OZ v3.3.0): **16 fontes Solidity únicas, 17 relações de import, zero destino faltante nesses grafos**. Esta contagem não inclui o fechamento de todos os demais arquivos adicionados por `proxy.sh` e `_runHandler.sh`; **nenhum ABI/bin ou compilação** resultou desta operação. Artefatos no `ROUND7_SOURCE_MANIFEST.csv`.
6. Auditoria de fonte `HMaker.sol`/`HandlerBase.sol`/`_runHandler.sh`/`hmaker.spec`, por blobs e linhas; transformação Perl descrita **sem executar script**, logo nenhuma ABI pós-modificação é reivindicada.
7. Auditoria READ-ONLY da nova entrega do AGENTE-02 PR #37 HEAD `2477787fe3f4cddb650cb4f1a08760bdbd1fde13`: P18/complete/3 e /23 e proposta de continuar /4,46,53. Resultados de parser para /3 e /23 são do **coordenador na rodada anterior**, não deste agente; preflights CERTORAKEY do AGENTE-02 separados, sem confundir com parser. Nenhum arquivo do AGENTE-02 editado.

## Execuções que NÃO aconteceram na Rodada 7

| Comando/atividade | Status R7 | Motivo e limitação |
| --- | --- | --- |
| `python3 scripts/check_specs.py .` em `Web3Bugs-certora` | **NOT_RUN_INFRA_BLOCKED** | WSL sem recuperação atestada; reconciliação por conector não substitui script |
| `python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_BLOCKED** | Mesmo bloqueio |
| `python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_BLOCKED** | Mesmo bloqueio |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NOT_RUN_INFRA_BLOCKED** | Nenhuma execução local na HEAD final |
| `certoraRun --compilation_steps_only` ou solc/Perl | **NOT_RUN_INFRA_BLOCKED** | Não iniciar scratch, versões ou executáveis no WSL defeituoso |
| Prover formal, CVL1, migração em lote e patch de originals | **PROIBIDO, NÃO EXECUTADO** | Gates inexistentes; preservação da semântica |

Não contar `SIGBUS`, `EIO`, `EROFS`, `CERTORAKEY`, `solc` isolado nem a visualização do CI como `COMPILE_ERROR` ou `COMPILE_OK`. **Os dois COMPILE_ERROR do P10 continuam exclusivamente R5/complete/33,34**, 264 NOT_RUN, zero equivalência. Há **266 NOT_RUN_INFRA_BLOCKED na coluna de tentativas locais R7**.

## Resultado de controles alternativos e verificação após publicar

- Escopo exclusivo permitido: `Web3Bugs-certora/docs/cvl2/research/AGENTE-01/`; publicações por GitHub Contents API diretamente na branch existente, sem ref force-update, reset, merge ou escrita no WSL.
- Verificações pela API do GitHub de chaves/matriz, escopo e estado Draft podem ser concluídas independentemente do host remoto. O workflow `validate`, quando concluído, verifica apenas integridade estrutural nas etapas que efetivamente executa. **Mesmo SUCCESS não substitui** os quatro comandos locais solicitados nem estabelece semântica CVL2.
- Nenhum log de compilação novo foi criado. Os dois logs históricos reais continuam em `round5/logs/` com manifestos e SHA; nenhum SHA de stdout/stderr inexistente foi inventado.
- Fonte e status experimental não foram alterados em `results/spec`, `contracts`, `reports`, `resources`, catálogo nem labels.

**Próximo gate operacional obrigatório:** administrador deve recuperar controladamente o volume/dispositivo WSL, preservar worktrees e logs, confirmar leitura/escrita em scratch novo, saúde de Python/Git/solc/CLI e sincronização não destrutiva de HEAD. Somente então executar, **na HEAD final publicada**, os três validadores e `git diff --check BASE...HEAD`; avaliar a saída real e informar exit codes autênticos.

**Alerta infra: VERMELHO. Alerta semântico: LARANJA.** Sem `SEMANTIC_PROVEN`, sem projeto migrado.

**AGENTE-01 — RODADA 7.**
