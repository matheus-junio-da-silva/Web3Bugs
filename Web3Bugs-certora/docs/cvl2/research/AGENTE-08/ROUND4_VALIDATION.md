# AGENTE-08 — Rodada 4 / verificacoes locais
Data: 2026-10-20. Checkout isolado em `/home/mat/cvl2-agente08-round4-20261020/repo`.
Baseline: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; HEAD inicial `8d5734a896119442f3d93f7a6f4b754e22fd344d`.

| Verificacao | Comando no diretório `Web3Bugs-certora` | Exit | Evidência |
|---|---|---:|---|
| Catalogo de specs | `timeout 160s python3 scripts/check_specs.py .` | 0 | 1386 exemplos, 1390 relações coerentes |
| Concursos | `timeout 160s python3 scripts/check_contests_csv.py .` | 0 | Check passed, contests vs reports |
| Contratos | `timeout 160s python3 scripts/check_contracts.py .` | 0 | Check passed, contracts vs reports |
| Matriz | CSV parse `ROUND4_MATRIX_155.csv` | 0 | 155 chaves únicas; P13=58, P23=46, P14=34, P5=17 |
| CVL2 `--compilation_steps_only` | Não executado | N/A | Ausência de ABI/cena/harness CVT e compiladores históricos correspondentes; registrar blocked, não inferir sucesso |
| Certora Prover / CVL1 | Não executados | N/A | Expressamente proibidos |

Testes externos restritos a scratch fora do checkout: cópia Opyn `applyHarnesses.sh` sob `timeout 20s`, quatro arquivos alterados somente no scratch; fonte P5 `applyHarness.patch` com `patch --dry-run --fuzz=0` seguido de `patch --batch --fuzz=0`, ambos sem conflitos, nenhum arquivo de produção alterado.
`certoraRun --version` apontou indisponibilidade da CERTORAKEY no wrapper do ambiente; não se acessou, expôs ou solicitou credenciais. Ferramentas `solc6.10`, `solc7.5`, `solc8.10` não presentes; `solc` presente reporta 0.8.7, portanto não é substituto silencioso.
A checagem de diff **commitado** será registrada no comentário de publicação, com SHA final, `git -c core.whitespace=cr-at-eol diff --check BASE...HEAD`, contagem de arquivos e lista de exceções de escopo. O próprio arquivo não é prova de execução futura.

A verificação dos scripts estruturais não equivale a compilação CVL2, equivalência semântica ou resultado do Prover.

## Complemento P5 — fechamento textual, somente scratch
Em checkout isolado de `aave-starknet-bridge@4c010c18`, dois tarballs Yarn foram baixados e validados `sha1sum -c`: `core-v3@1.16.2` OK, `protocol-v2@1.0.1` OK. As 11 seeds de `verifyBridge.sh` com `certora/munged/l1` do patch e `node_modules` extraído resultaram em 40 sources / 64 imports / 0 imports ausentes sob parser estático (regex, não solc). A evidência por arquivo SHA-256 está em `5/ROUND4_IMPORT_CLOSURE.csv`. Não foi feita compilação CVL, Prover ou instalação de packages no checkout de produção.
