# AGENTE-02 — RODADA 10 / QA EXECUTADO, NÃO EXECUTADO E INCIDENTE EIO

**Data:** 2026-10-20. Branch exclusiva `research/cvl2-agente-02`, PR #37 **Draft**, HEAD inicial `7a2d339114814b6be669ed4c57b11c725dcb4ccf`. Baseline imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Não houve uso de credenciais, merge, Prover/CVL1 ou alterações históricas.

## Preflight WSL e motivo do encerramento do trabalho local

O WSL `DESKTOP-5E26TVU` (o mesmo de R9) foi examinado **antes do uso**, sem tocar nas worktrees de outros agentes. Comandos simples efetivamente responderam:

- Host `DESKTOP-5E26TVU`; montagem `/home/mat` apontou `/ rw,relatime,discard,errors=remount-ro,data=ordered`; espaço disponível reportado ~912 GiB.
- Diretório temporário único criado em `/tmp`, escrito/lido/removido com sucesso.
- Worktree exclusiva `/home/mat/cvl2-agente02-round9` em HEAD `7a2d339114814b6be669ed4c57b11c725dcb4ccf`, `git status --short` limpo. Checkout legado R5 também limpo, não alterado.
- Binários `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun` e `solc-0.8.6` existem e são executáveis; **não foram invocados para uma spec na R10**.
- `git ls-remote` confirmou `research/cvl2-agente-02` exatamente em `7a2d339...` antes de novos documentos.

**Falha material posteriormente observada:** a primeira chamada Python de revalidação dos dados falhou **na fase de importação**, antes de abrir qualquer gzip:

```text
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
...
  File "<frozen importlib._bootstrap_external>", line 951, in get_data
OSError: [Errno 5] Input/output error
```

A ferramenta reportou término do shell, mas não há **resultado de auditoria de hash Python**, nem stdout `LOG_AUDIT` ou `REVERT_INTEGRITY`. Por segurança, **nenhum outro comando foi enviado ao WSL após esse EIO**. Não há evidência de integridade continuada do filesystem, logo qualquer comando de compilação, patch, escrita ou QA local posterior estava proibido. O EIO **não** é erro CVL2.

## QA alternativo remoto EXECUTADO (GitHub connector)

**Fonte de dados:** arquivos efetivamente lidos por API GitHub da HEAD de R9 `7a2d339...`, sem mudar dados canônicos:
- `ROUND9_MATRIX_181.csv` Git blob `eec10d9ef4658049212f5b43f5c09759f7fb945b`;
- `ROUND9_ORIGINAL_ATTEMPTS.csv` `a566a932737c57ac7ef53dfc6c044ea5b2e64e41`;
- `ROUND9_DERIVED_ATTEMPTS.csv` `7d5665a1f0641032c2bbecca14dacf138e4dfac9`;
- `ROUND9_INPUT_MANIFEST.csv` `575d59c6180ebce57ccca31225dd2e2d589cb257`;
- `ROUND8_METHOD_RECEIVER_MATRIX.csv` `925b6027e46007bf9a89fbe0c8d29908b75d0348`;
- `results/spec/spec_buglabel.csv` do snapshot imutável.

A rotina em memória conferiu:
1. Exatamente **181** keys únicas P18 na matriz, **69 complete/112 incomplete** e os campos `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Spec` e `Bug Label` para cada key contra o CSV canônico. **Zero diferenças**.
2. **51 relações de metadados SHA e existência de path** entre as 3 execuções originais, 3 derivadas, 3 manifestos e os 12 logs gzip mais 3 patches publicados no GitHub. Resultado **MATCH** nas referências declaradas, sem conteúdo binário lido.
3. `ROUND10_LOG_REFERENCE_AUDIT.csv` contém **6 linhas de tentativas** com SHA bruto e SHA gzip separados, ambos transportados da R9, `r10_csv_cross_manifest=MATCH`, `r10_github_paths=EXIST_IN_PR`, **`r10_raw_gzip_rehash=NOT_DONE_EIO_AND_BINARY_CONNECTOR_LIMIT`** e **`r10_patch_reverse_reexecution=NOT_DONE_EIO`**. Nenhum resultado `sha256sum`, `gzip.decompress` ou `patch --reverse` foi artificialmente atribuído à R10.
4. `ROUND10_MATRIX_181.csv` gerada por chave com eixos **originais 5 COMPILE_ERROR / 176 NOT_RUN** e **derivados 3 COMPILE_OK / 178 NOT_RUN**, tendo **0 compilações novas** e **181 SEMANTIC_UNRESOLVED**. Mantidos 157 `ABSENT_AT_AUDITED_COMMIT` e 24 `CONTENT_DIFFERS`, sem interpretar como número de arquivos distintos.

**Limite do QA remoto:** igualdade de hashes **declarados** em duas matrizes não equivale a recalcular o hash dos bytes. O GitHub connector neste ambiente não entrega bytes de `.gz` como conteúdo UTF-8; a consulta `fetch_file` de um gzip retornou `UnicodeDecodeError`. A URL pública GitHub API dos binários também não pôde ser recuperada pelo buscador. Os 12 logs e 3 patches haviam sido efetivamente descomprimidos e verificados na **R9**, não na R10. Esse fato anterior é preservado, não repetido ficticiamente.

## Controles locais obrigatórios — NÃO EXECUTADOS na R10

| Comando oficial | Status real R10 |
| --- | --- |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | **NOT_RUN_INFRA_EIO** |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_EIO** |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_EIO** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NOT_RUN_INFRA_EIO** |
| `certoraRun --compilation_steps_only` em originais ou variantes novas | **NOT_RUN_INFRA_EIO** |
| `solc`, Prover CVL1, Prover completo, patch ou nova worktree | **NÃO EXECUTADOS** |

Os **três validadores e diff COMMITTED tiveram EXIT0 na R9 depois do push**, mas **esses resultados históricos não são portados para a HEAD R10**. O workflow GitHub `validate`, quando executado na HEAD final, é QA estrutural independente: sua passagem **não substituirá** os scripts locais nem provará semântica CVL2.

## QA documental final e riscos

- Foi feita leitura read-only da última revisão R9 do coordenador no PR #37 e do painel `ROUND9_DASHBOARD.md` da coordenação, sem somar eventos duplicados.
- Confirmados por consultas independentes os blocos auditados/fork de LaunchEvent, RocketJoeStaking e patch Rocket Joe. Cross-review PR #36 **somente leitura**.
- A matriz de 181 entradas preserva SHA do N.spec, target, resultados históricos, autoria da compilação, estado real anterior, fato de fonte, inferência, prova faltante e próxima ação. A compilação limitada das variantes R9 não prova igualdade do conjunto de chamadas da CVL1, não-vacuidade ou equivalência formal.
- **Próximo gate humano imediato:** restaurar saúde duradoura do WSL e executar novos checks locais **depois** de revisar a HEAD do PR. Então descomprimir/rehashar 12 logs brutos e 3 patches e provar novamente aplicação+reversão com `--fuzz=0` em scratch. Não executar automaticamente Prover/CVL1 ou implementar a migração.

**Status: BLOQUEIO INFRA EIO na R10; sem novas compilações; 0 `SEMANTIC_PROVEN`; PR #37 Draft.**

**AGENTE-02 — RODADA 10.**
