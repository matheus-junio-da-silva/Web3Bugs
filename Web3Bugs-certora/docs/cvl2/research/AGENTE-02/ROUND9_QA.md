# AGENTE-02 — RODADA 9 / QA REAL, LOGS E LIMITAÇÕES

**Data:** 2026-10-20. PR [#37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37) existente, **Draft**, branch `research/cvl2-agente-02`. Baseline histórico `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, HEAD inicial `f13481755eeac310aac7f930022faa522c7b8fce`; **nenhum merge/reset/rebase de branch alheia**. Worktree de teste exclusiva `/home/mat/cvl2-agente02-round9`.

## 1. Infraestrutura: pré-condições EXECUTADAS

Antes de modificar documentação ou executar Certora, teste de leitura dos dados e `git status` limpo no checkout legado; montagem `/home/mat` reportou `rw`; tentativa de escrita/leitura/deleção isolada em `/tmp` teve exit 0. HEAD da branch remota confirmada igual a HEAD inicial; worktree R9 criada na ref exata, originalmente limpa. CLI `certora-cli 8.19.0` (`certoraRun` SHA256 `93f025f5262f816a57a877159dd03333e234c9d0da3912c2b9636115a2884576`) e `solc 0.8.6+commit.11564f7e` (SHA256 `abd5c4f3f262bc3ed7951b968c63f98e83f66d9a5c3568ab306eac49250aec3e`) verificados no WSL recuperado. Nenhum EIO/SIGBUS/EROFS ocorreu nesta rodada; isto não garante recuperação permanente de outras worktrees.

## 2. Diagnósticos Certora NOVOS realmente EXECUTADOS

**Três N.spec byte-idênticos originais** e **três variantes lexicais scratch**, total **6 invocações** `certoraRun --compilation_steps_only`, timeout **60s**, target único por caso. Sandbox em `/tmp/agente02-round9-original-only/` e `/tmp/agente02-round9-derived-lexical-only/`, `HOME`/cache exclusivos e environment allowlist sem `CERTORAKEY`, tokens ou credenciais. Comandos e versões por caso em `ROUND9_ORIGINAL_ATTEMPTS.csv` e `ROUND9_DERIVED_ATTEMPTS.csv`. **Nenhum Prover completo, CVL1, API de submissão, edição de source original, alteração de flags históricas ou resultado Bug Label.**

| Caso P18 complete | Original byte-idêntico | Scratch derivado | Natureza da conclusão |
| --- | --- | --- | --- |
| 4 | **EXIT 1 `COMPILE_ERROR`** parser `methods` | **EXIT 0 `COMPILE_OK`** | Só fragmento `AccessControlMock`, não full spec |
| 46 | **EXIT 1 `COMPILE_ERROR`** parser `methods` | **EXIT 0 `COMPILE_OK`** | Só fragmento `ERC1155BurnableMock`, não prova `method f` não-vacuoso |
| 53 | **EXIT 1 `COMPILE_ERROR`** parser `methods` e selector CVL1 | **EXIT 0 `COMPILE_OK`** | Só fragmento `ERC1155PausableMock`; `sig:` preserva texto de selector, não prova mesmo domínio |

**Logs realmente capturados:** `ROUND9_DIAGNOSTIC_LOGS/` contém **12 arquivos `.log.gz`** (stdout e stderr de cada uma das 6 chamadas, inclusive stderr vazio quando foi o caso), gzip **sem perda**. Cada linha de `ROUND9_ORIGINAL_ATTEMPTS.csv` ou `ROUND9_DERIVED_ATTEMPTS.csv` identifica caminho, SHA256 do conteúdo **bruto** e SHA256 do arquivo **gzip**, além de comando, SHA do CLI/solc, target, N.spec original/derivado, duração e exit code. A checagem Python efetivamente executada fez `gzip.decompress` e confirmou SHA256 do conteúdo bruto em **12/12** logs; confirmou também 3 arquivos `ROUND9_PROPOSED_DIFF_*.patch.gz` contra hashes dos patches brutos. A compressão preserva espaços/linhas vazias originais e evita falsear logs para satisfazer `git diff --check`.

**Inputs efetivamente conferidos:** três N.spec originais foram comparados byte a byte às cópias; as três transformações passaram `reverse_apply` para recuperar a string original exata. **Todas as cópias das árvores Solidity**, tanto originais quanto derivadas, conferem hash agregado de arquivos relativos `5cfae28c8b447b77e752241eaa158efa17f09264a07a5a20fb3ff43ab01b2bb7`, registrado em `ROUND9_INPUT_MANIFEST.csv` juntamente com hashes individuais. A flag `--solc` foi fixada no binário 0.8.6 absoluto; nenhum fallback foi indicado nos seis logs. Reversibilidade da proposta **não** equivale a equivalência CVL1→CVL2.

## 3. Validação estrutural pós-primeiro commit — EXECUTADA

Primeiro commit documental R9: **`636434bbc965a135ca8a321ca8cc837b4abefffa`**. Após ele, de `Web3Bugs-certora/`:

```text
$ python3 scripts/check_specs.py .
Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
exit=0

$ python3 scripts/check_contests_csv.py .
Check passed! ./results/contests.csv is consistant with ./reports
exit=0

$ python3 scripts/check_contracts.py .
Check passed! ./contracts is consistant with ./reports
exit=0
```

Da raiz Git pós-primeiro commit:

```bash
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

Resultado **EXIT 0**. Antes desse commit, o check detectou que stdout bruto continha linhas vazias finais e os patches exibiam espaços literais preservados da source CVL. **Não foram corrigidos os bytes das evidências**; em vez disso, foram arquivados em gzip sem perda e os hashes/decompressões foram checados. Após compactação, `git diff --cached --check` passou sem inconsistências.

## 4. Reconciliação matricial independente — EXECUTADA

- `ROUND9_MATRIX_181.csv`: **181 chaves únicas** `(project_id,original_status,example_id)`, **64 colunas**, **69 complete / 112 incomplete**, sempre com Property/Target/Result/Detection Outcome/Bug Labels preservados e comparados ao `results/spec/spec_buglabel.csv` canônico **sem alterá-lo**.
- Originais: **5 `COMPILE_ERROR`**, sendo /3 e /23 resultados do coordenador na R5 e **/4, /46, /53 R9**; **176 `NOT_RUN`**. **Zero originais `COMPILE_OK`.**
- Derivados: **3 `COMPILE_OK` limitados** (/4,/46,/53), **178 `NOT_RUN`**; não somados aos 5 erros como propriedades distintas.
- **0 `SEMANTIC_PROVEN`**, **0 `MIGRATED_COMPLETE`**. Os **nove preflights R5 barrados por `CERTORAKEY`** são classificados à parte.
- Auditoria individual pós-commit de integridade da matriz e comparador com CSV histórico passou **181/181**; checagem de hashes/descompressão 12/12 logs + 3/3 patches e árvores Solidity dos 3 pares passou. A matriz distingue fatos, inferências e provas faltantes; arquivos R8 preservados.

## 5. Limites, checks da HEAD final e próximos gates

A execução diagnóstica em fragmentos derivados é **somente compilação local CVL2**. Sem Prover completo, sem replay das specs globais, sem demonstração de resultados dos relatórios originais, sem adjudicação do receiver de todas as chamadas Solidity, sem prova de não-vacuidade de `method f` ou de `require paused()` e sem comparação histórica dos contraexemplos. O upstream auditado ainda apresenta 157 instâncias sem spec correspondente e 24 com spec homônima divergente; nenhum dos três pilotos resolve isso.

**Para a HEAD documental final:** após commit deste QA, repetir três validadores e `git diff --check BASE...HEAD`; depois do push verificar ref remota, PR Draft e CI GitHub. Relatar esses resultados no comentário final do PR. O workflow estrutural não substitui Certora nem Prover.

**Duas experiências futuras que exigem gate específico do coordenador:** P18/complete/3 (`grantRoleEffect`) e /23 (`noTransferEffectOnApproval`) **somente em candidatos scratch**, sem repetir seus erros CVL2 originais anteriores por contagem. Fixar target/ABI/call-resolution, verificar contexts globais, capturar logs e SHA256, jamais alterar `require`, `assert`, `ghost`, `hook`, cast, summary ou contratos para passar teste.

**AGENTE-02 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.**
