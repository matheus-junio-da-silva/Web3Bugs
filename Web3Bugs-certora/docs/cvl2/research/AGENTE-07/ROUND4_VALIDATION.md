# AGENTE-07 — Rodada 4 / execução e integridade

- **Worktree isolado:** `/home/mat/cvl2-agent07-round4-20261020`.
- **Commit de origem:** `78800bb132f9a40d7db4d5ae3e3bbb99c2c884c8`.
- **Baseline:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- **Escopo autorizado:** somente `Web3Bugs-certora/docs/cvl2/research/AGENTE-07/`.
- **Sem CVL2 compilation, Prover, CVL1 replay, modificações de originals/CSV histórico, merge ou auto-merge.**

## Comandos estruturais efetivamente executados no checkout AGENTE-07

Executados no root do Git worktree (`/home/mat/cvl2-agent07-round4-20261020`):

```sh
timeout 120 python3 Web3Bugs-certora/scripts/check_specs.py Web3Bugs-certora
timeout 120 python3 Web3Bugs-certora/scripts/check_contests_csv.py Web3Bugs-certora
timeout 120 python3 Web3Bugs-certora/scripts/check_contracts.py Web3Bugs-certora
git -c core.whitespace=cr-at-eol diff --cached --check
```

Resultados: os três validadores Python **exit 0**; `check_specs.py` confirma 1.386 exemplos e 1.390 relações; `check_contests_csv.py` e `check_contracts.py` passaram. O primeiro `diff --cached --check` detectou três trailing spaces de formatação Markdown na nota de revisão do PR #43; foram removidos os 6 bytes de whitespace sem alterar o sentido. Após novo `git add`, o **staged diff --check exit 0**.

## Matriz e conformidade

`ROUND4_MATRIX.csv` possui 156 linhas únicas, P9=61, P8=42, P20=37, P11=16, hashes N.spec recalculados 156/156; classificações de pesquisa 50 `DOCUMENTED_CANDIDATE` e 106 `UNRESOLVED_CANDIDATE`. Há zero afirmações de `COMPILE_OK` e zero de `SEMANTIC_SUPPORTED`.

As novas medições documentam leitura textual de ABI/sources e replay de script em **scratch**, não o runner Certora. Os novos achados não alteram `Results`, `Detection Outcome`, `require`, `assert`, `Solidity`, `N.spec`, `N.txt`, relatórios ou CSV do catálogo.

## Check do diff COMMITADO

Executar exatamente a partir do root Git depois do commit e push:

```sh
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

O resultado final desse comando será registrado também na conversa do PR #41 com a SHA publicada, sem confundir diff staged com diff COMMITADO.

## PR #43 independente

Ver `ROUND4_PR43_INDEPENDENT_AUDIT.md`: HEAD `8d5734a896119442f3d93f7a6f4b754e22fd344d`, `BASE...HEAD diff --check` exit 0, três validadores exit 0 e 196 arquivos apenas AGENTE-08, 155/155 unresolved.

**AGENTE-07 — RODADA 4**
