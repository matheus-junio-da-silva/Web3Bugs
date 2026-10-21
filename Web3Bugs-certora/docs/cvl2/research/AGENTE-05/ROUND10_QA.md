# AGENTE-05 — ROUND10_QA: reconciliação completa, incidentes e checks não executados

**Referência:** 20/10/2026. Branch `research/cvl2-agente-05`, [PR #40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40) Draft, sem merge. HEAD inicial confirmada `46c3f11261340aa4cf105a2c5921664ad12f014d`. Baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` (inalterável). Nenhum artefato de `results/spec/`, `contracts/`, `reports/`, `resources/`, `spec_buglabel.csv` ou de outra pasta de agente modificado; novos documentos R10 só na própria pasta. Nenhuma tentativa de merge, Prover/CVL1 ou migração em lote.

## QA realmente executado em memória via conector GitHub

- Antes das criações, leitura das quatro fontes obrigatórias `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md` na baseline, além de P1 `complete/1/1.spec` e `incomplete/1/1.spec`; fontes oficiais [CVL2 migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [CVL2 changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [rules](https://docs.certora.com/en/latest/docs/cvl/rules.html), [ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [statements/reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html). A documentação oficial **atual** não atesta o mesmo motor, ABI ou linguagem da auditoria CVL1 histórica.
- A construção de [ROUND10_MATRIX_148.csv](ROUND10_MATRIX_148.csv) leu a [matriz R9](ROUND9_MATRIX_148.csv), [`results/spec/spec_buglabel.csv` da baseline](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/spec_buglabel.csv) e [`ROUND9_ATTEMPT_EVENTS.csv` do coordenador](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/docs/cvl2/coordination/ROUND9_ATTEMPT_EVENTS.csv) com **33 eventos globais**, SHA Git blob `3e3aeeaa5e1b6f0f559dfcb1a95fb7192ac8e0cc`.
- O parser da matriz reconcilia **exatas 148 chaves canônicas únicas** (P7=74/P19=37/P6=32/P3=3/P21=2); **149 relações históricas** de Bug Label, preservando múltiplos labels. Para cada chave foram confrontados `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Original Spec`, `Original Spec Lines`, `N.spec path`, `Bug Label(s)`, com zero divergências. A coluna `N_spec_sha256_prior` conserva atestação anterior, **NÃO** constitui novo rehash criptográfico dos 148 N.spec na R10 devido a EROFS/SIGBUS.
- **11 eventos pré-R10 / 9 IDs distintos** da carteira no ledger: 6 `COMPILE_OK` limitados, 5 `COMPILE_ERROR` parser e **2 IDs na interseção** P7/47,73 (original EXIT1, derivado EXIT0). **139 IDs nunca tiveram teste CVL2**. Isto não significa 6+5=11 propriedades. A origem de cada evento e respectivos hashes quando existentes foram preservados. Campo da execução **R10 = `NOT_RUN` em 148/148**; `semantic_equivalence=NOT_PROVEN` e `project_migrated_complete=NO` em 148/148.
- Revisão cruzada do PR #38 **read-only**, HEAD `c07432f9c81843be532eec5c4f792143aaabde59`, lendo o R9 desse agente. P4 Staked ABI Solidity compilada, P22 FullMath Solidity compilada, P22 PoolActions falhou **Solidity**, e P1/P17 ainda com scene histórica ausente. Não registrar esses eventos como CVL2. Nenhuma escrita na branch do AGENTE-06.

## Incidente crítico do WSL observado nesta própria R10

Em `DESKTOP-5E26TVU`, o comando inicial de saúde executado pelo Remote Desktop Commander terminou **EXIT 0** e informou `git version 2.53.0`, `Python 3.14.4`, `/dev/sdd` com espaço, `/tmp` acessível, os checkouts AGENTE-05 R9 e R6 **sem modificações**, ferramentas Certora e solc0.8.10 existentes. A criação posterior de worktree própria foi tentada em `/home/mat/cvl2-agente05-round10-20261020`, partindo exclusivamente da branch AGENTE-05; o `git fetch` confirmou HEAD remota `46c3f11261340aa4cf105a2c5921664ad12f014d`. **Mas** durante `git worktree add`, retornou:

```text
FETCH_HEAD=46c3f11261340aa4cf105a2c5921664ad12f014d
error: reset died of signal 7
warning: unable to unlink '/home/mat/cvl2-agente05-round4-20261020/.git/worktrees/cvl2-agente05-round10-20261020/locked': Read-only file system
process exit code: 135
```

**Classificação exata:** `INFRA_SIGBUS_EXIT135_AND_EROFS`, tentativa de preparação de checkout. **Não** é `COMPILE_ERROR` CVL2, `PREFLIGHT_AUTH_BLOCKED` nem sintaxe inválida da spec. A saúde anterior à criação não prova saúde posterior. **Interrompi imediatamente** toda interação WSL; não executar reset/rebase, worktree prune/repair, limpeza, instalação, recompile nem outro comando naquele volume. Administrador deve examinar filesystem, backups e preservar estado/lock do Git antes de nova autorização; não presumir que checkout R10 foi criado corretamente.

## Checks históricos exigidos — estado real da Rodada 10

| Comando obrigatório | Resultado R10 | Justificativa |
| --- | --- | --- |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | **NOT_RUN_INFRA_BLOCKED** | WSL perdeu integridade antes da criação do worktree R10; não executar contra árvore potencialmente instável |
| `python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_BLOCKED** | Idem |
| `python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_BLOCKED** | Idem |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NOT_RUN_INFRA_BLOCKED** | Mesmo bloqueio, HEAD R10 não está disponível em checkout local confiável |
| `certoraRun --compilation_steps_only` para P7/41,63,47 ou 73 | **NOT_RUN** | Falta gate sintático individual e WSL está bloqueado; **nenhuma execução Certora R10** |

Os quatro comandos **tiveram EXIT 0 sobre a HEAD final da R9**, `46c3f112...`, na rodada anterior, fato preservado. **Não** aplicar esse EXIT 0 à HEAD R10. A validação em memória das chaves e o GitHub Actions `validate` remoto, se positivos, são alternativas parciais **não equivalentes** aos quatro checks locais. Reavaliar quando a máquina for restaurada e worktree atestada estável.

## QA remota pós-publicação e gates

Após os três commits novos R10, o comentário de entrega no PR #40 deve identificar (a) `compare_commits BASE...HEAD` com ausência de arquivos fora da pasta permitida, (b) ausência de whitespace em `ROUND10_MATRIX_148.csv`, `ROUND10_EVIDENCE.md`, `ROUND10_QA.md`, (c) novo parse das 148 linhas de dados/chaves e (d) status real do GitHub Actions da HEAD final. Essas verificações remotas, **se executadas**, serão registradas no comentário do PR, sem converter `validate SUCCESS` em compilação CVL2.

**Próximos gates humanos:** recuperar WSL/metadata Git e refazer QA local completo; revisar individualmente P7/47 e /73 method f, receiver e não-vacuidade com CVL global; então decidir separadamente sobre P7/41 e /63 sete `sig:` scratch, target+ABI, solc 0.8.10/CLI8.19, timeout, hashes/cmp e logs, sem mudar assertions nem `@withrevert`. P19/1,2 no PR #46 seguem `02_unresolved` por RCPT=0. Outros bloqueios P3/P6/P19/P21 registrados no [ROUND10_EVIDENCE](ROUND10_EVIDENCE.md).

**Alerta VERMELHO operacional e VERMELHO semântico; sem CVL1, Prover, merge ou promoção de bucket.**

**AGENTE-05 — RODADA 10.**
