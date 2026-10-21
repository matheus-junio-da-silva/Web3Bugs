# AGENTE-05 — RODADA 8 / QA e controle de execução

**Data de referência:** 20/10/2026. [PR #40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), branch `research/cvl2-agente-05`, mantido **Draft sem merge**. HEAD inicial observada `5a50cd43a56add63d91e2476b3d0460e991cdacc`. Baseline imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; upstream PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.

## 1. Integridade de entrada e fontes realmente lidas

Antes de criar qualquer arquivo da R8, foram consultados integralmente pelo **conector GitHub** `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md` do baseline, além dos exemplos de contraste P1 complete/1/1 e incomplete/1/1 e `1.txt`. Os arquivos históricos definem `complete` como fechamento de dependências no snapshot, e mantêm `Result`, `Detection Outcome` e Bug Labels separados; `complete` **não** significa migração CVL2 ou a mesma cena formal.

Foram lidas as revisões mais recentes do coordenador no PR #40, o [painel R7 já integrado na main](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/docs/cvl2/coordination/ROUND7_DASHBOARD.md), a planilha `ROUND7_PROGRESS.csv`, o [incidente WSL](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_WSL_IO_INCIDENT.md) e a documentação oficial de [migração](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [mudanças](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html) e [reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html). A contrarrevisão da HEAD `e4527033b3c2b1a6aa638f6b7c351ee996d0ae79` do PR #38 foi **READ-ONLY**.

## 2. Contabilidade do AGENTE-05, com status e autor exatos

| Classe histórica acumulada entre P3/P6/P7/P19/P21 | Casos | Autoria/evidência | Reexecutado na R8? |
| --- | ---: | --- | --- |
| `COMPILE_OK` CVL2 restrito | **4** | **Coordenador**, P7/complete/37,65 *fragmentos originais* e P19/complete/1,2 *derivadas mathint* no PR #46 | **NÃO** |
| `COMPILE_ERROR` CVL2 parser/typechecker | **5** | **AGENTE-05 R5**, P7/complete/36,41,47,63,73, comando/exit 1 e logs `7/round5_logs/` | **NÃO** |
| `NOT_RUN` CVL2 acumulado | **139** | Ausência de compilação válida por property, não uma falha do parser | **NÃO** |
| `PREFLIGHT_AUTH_BLOCKED` | **0** | Nenhum preflight assim registrado nesta carteira | **NÃO** |
| `SEMANTIC_PROVEN` / `MIGRATED_COMPLETE` | **0** / **0** | Não houve equivalência ou projeto completamente migrado | **NÃO** |
| **Novos testes `certoraRun --compilation_steps_only` da R8** | **0** | Infraestrutura WSL não recuperada | — |

**NOT_RUN_INFRA_BLOCKED R8 = 148** em campo independente para ausência de teste **nesta rodada**, enquanto `139 NOT_RUN` histórico se refere ao **acumulado de todas as rodadas**. Não somar as duas grandezas nem classificar `SIGBUS`/EIO/EROFS como erro CVL2. A preparação lexical P7/47 abortada em R6 também não é execução de compilação.

**Global, de propriedade do coordenador, NÃO desta carteira:** painel R7 = 1.386 instâncias, 1.390 relações históricas, quatro `COMPILE_OK` limitados, 12 `COMPILE_ERROR` de parser e 1.370 propriedades sem teste, zero equivalências, zero projetos migrados.

## 3. QA executado em memória pelo conector GitHub

A geração da [matriz R8](ROUND8_MATRIX_148.csv) executou checagem efetiva por chaves contra [`results/spec/spec_buglabel.csv` do baseline](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/spec_buglabel.csv), [`ROUND7_MATRIX_148.csv`](ROUND7_MATRIX_148.csv) e cinco `properties.csv` do próprio agente:

- **148/148 chaves únicas**, por projeto P3=3, P6=32, P7=74, P19=37, P21=2, com **149 relações Bug Label** (múltiplos rótulos preservados).
- Confronto sem divergências de `Property`, `Target Contract`, `Result`, `Detection Outcome`, paths N.spec/fonte/linhas e `Bug Label(s)` entre a matriz anterior e o CSV canônico.
- **148 hashes SHA-256 registrados para `N.spec` conferidos aos hashes `extracted_spec_sha256` dos cinco índices anteriores**; **não** recalculados diretamente a partir dos bytes individuais dos 148 `N.spec` em R8.
- Cinco `COMPILE_ERROR` com exit `1` anterior e comandos/logs do manifesto R5; quatro `COMPILE_OK` anteriores mantidos com autoria do coordenador. **Nenhuma nova medição de compilação.**
- Para o diff textual proposto de P7/47, cada um dos seis prefixos `f.selector == <nome>(` apareceu uma só vez no original; a comparação antes/depois, **somente em memória**, confirmou o corpo da rule inalterado e exatamente seis prefixos `sig:`. Sem gravar o arquivo derivado nem executar CLI.
- [`ROUND8_EVIDENCE.md`](ROUND8_EVIDENCE.md) fornece a tabela `source_or_report_fact`/ `inference`/ `missing_proof`, SHAs, linhas e gates individuais. Não há logs/manifests CVL2 novos na R8, pois nenhuma compilação ocorreu.

## 4. Comandos obrigatórios na HEAD final — **não executados localmente**

O [ROUND6_WSL_IO_INCIDENT.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_WSL_IO_INCIDENT.md) registra `spawn EIO`, `SIGBUS`, `EROFS` no host `DESKTOP-5E26TVU` e proíbe comandos naquele filesystem antes de recuperação **comprovada pelo administrador**. **Nenhuma interação com o WSL nesta R8**, inclusive para saúde/versão/worktree, por falta desse gate.

| Comando exigido (diretório correto) | Estado na HEAD R8 | Limite |
| --- | --- | --- |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | **NOT_RUN_INFRA_BLOCKED** | Local WSL não íntegro |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_BLOCKED** | Local WSL não íntegro |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_BLOCKED** | Local WSL não íntegro |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NOT_RUN_INFRA_BLOCKED** | `git diff` local não executado |

**A verificar após a publicação do último arquivo R8:** `compare_commits` GitHub `BASE...HEAD` para detectar arquivos fora do escopo e leitura de whitespace dos três documentos, e o workflow remoto `validate` da HEAD para saber quais passos efetivamente constam. Essas operações remotas **não** são execução local dos quatro comandos; o `validate` tradicional só contém `check_contests_csv`, `check_contracts`, `check_git`, não `check_specs.py` ou `git diff --check BASE...HEAD`. Atualizar o **comentário do PR** com a HEAD/CI reais.

## 5. Condições explícitas para um diagnóstico CVL2 futuro

1. Administrador deve restaurar WSL, confirmar backup, filesystem e espaço/IO, testar scratch novo RW, Python/Git, comparações de worktree, SHA de todos inputs, solc 0.8.10 e CLI direto 8.19.0 **sem expor credenciais**.
2. Executar os quatro checks estruturais obrigatórios na **HEAD final** e registrar stdout/stderr e exit. A integridade de CI externo pode ser relatada separadamente.
3. Apenas após **autorização individual do coordenador para P7/47**, preservar original e gerar **uma única** variante scratch com seis `sig:`, sem mexer em `method f`, `filtered`, `f@withrevert`, `assert`, summaries, ghosts, hooks, casts, requires ou ABI.
4. Invocar somente `--compilation_steps_only`, com timeout e manifesto completo, e reportar `COMPILE_OK` apenas se o comando real voltar exit0 para target+arquivo exatos, ainda **sem alegar equivalência**. P7/73 dependeria de segundo gate independente.
5. Sem migração em lote, CVL1, Prover, PR derived, merge ou promoção de buckets pela compilação. P19/1,2 do PR #46 continuam `02_unresolved` por `RCPT=0`.

**Semáforo final: 🟠 evidência/semântica incompletas; 🔴 infraestrutura operacional bloqueada. AGENTE-05 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.**
