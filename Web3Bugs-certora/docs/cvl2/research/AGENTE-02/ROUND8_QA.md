# AGENTE-02 — RODADA 8 / QA de catálogo, integridade e portões

**Data:** 2026-10-20. PR [#37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37) **DRAFT**; branch existente `research/cvl2-agente-02`, HEAD inicial `4ceac5d5e988dba5b54c44d5678f486a6dabc5af`, baseline histórico `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Exclusivamente arquivos documentais sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-02/`.

## QA efetivamente realizado por GitHub (não é execução local dos scripts)

Por ferramentas GitHub foram lidos: quatro documentos exigidos e amostras P1, painel R7 integrado à `main`, última revisão PR #37, fontes oficiais da Certora, 181 linhas da matriz R7, manifesto dos 181 Git blobs de `N.spec`, o CSV histórico em **duas refs** (baseline e branch) e as matrizes R8. Confrontaram-se no runtime JavaScript do conector **todos os campos históricos comparáveis** de cada chave única. Os Git blobs remotos lidos no fim dessa checagem foram:

- `ROUND8_MATRIX_181.csv`: `c37339487afa28878fc74fea6e76a4bd21f34f99`.
- `ROUND8_METHOD_RECEIVER_MATRIX.csv`: `925b6027e46007bf9a89fbe0c8d29908b75d0348`.
- `ROUND8_EVIDENCE.md`: `1142286633339a390f964ef6f790a010e24a84f1`.
- `results/spec/spec_buglabel.csv`: `97e20443586540034a4c0305ce1db19b0d2f8cb5` **tanto na baseline quanto na branch**.

| Check do conector executado | Resultado |
| --- | ---: |
| Matriz R8: registros / colunas | **181 / 48**, todas as linhas com comprimento correto |
| Chaves `project_id,original_status,example_id` únicas | **181 / 181** |
| Catálogo P18, identidades únicas | **181** |
| Pareamento Property / Target / Result / Detection Outcome / path N.spec | **181/181, zero divergências** |
| Bug Labels históricos | **Preservados e reconciliados na geração da matriz** |
| Manifests individuais `N.spec` em R7 herdados | **181/181**, Git SHA-1, ref fixa `2477787fe3f4cddb650cb4f1a08760bdbd1fde13` herdada do manifesto R7 |
| R8 methods: registros / colunas | **18 / 18**, nenhuma coluna perdida |
| Colunas `source_or_report_fact` / `inference_semantic_risk` / `missing_proof` preenchidas | **181/181** |
| `complete` / `incomplete` | **69 / 112** |
| `DOCUMENTED_CANDIDATE` textual | **50**, sem aprovação formal |
| `ABSENT_AT_AUDITED_COMMIT` / `CONTENT_DIFFERS` | **157 / 24** |
| CVL2 P18 `COMPILE_ERROR` comprovados antes R8 | **2**, /3 e /23, executor **COORDENADOR** |
| CVL2 P18 `COMPILE_OK` / `NOT_RUN` | **0 / 179** |
| Novos testes CVL2 executados na R8 | **0** |
| `SEMANTIC_PROVEN` / projetos `MIGRATED_COMPLETE` | **0 / 0** |
| Trailing whitespace em R8 matriz, methods, evidências | **0 linhas** |
| Arquivos alterados no PR acumulado contra baseline antes deste QA | **250**, zero fora do diretório autorizado |

O confronto de N.spec usa **hashes Git SHA-1** individualmente apurados na R7 contra os originais em ref fixa; não afirma recalcular SHA-256 de 181 arquivos nesta rodada. Valores SHA-256 previamente aferidos permanecem na matriz quando disponíveis. A ABI solc0.8.6 dos mocks foi compilada **na R5**, com hashes/logs anexados naquela rodada; **nenhum solc foi executado nesta R8**. Os dois `COMPILE_ERROR` do parser foram observados **pelo coordenador na R5**, não são testes novos da R8.

## Comandos históricos pedidos — NÃO executados por infraestrutura

O administrador **não confirmou recuperação** do WSL DESKTOP-5E26TVU, afetado por `spawn EIO`, `EROFS` e `SIGBUS`. A revisão de coordenação R7 proíbe inclusive comandos triviais nesse host. **Nenhum comando remoto foi enviado ao WSL nesta R8**, nenhum scratch/worktree novo criado, nenhum token/credencial lido ou exposto.

| Comando em checkout íntegro | Status R8 |
| --- | --- |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NOT_RUN_INFRA_BLOCKED** |
| `certoraRun --compilation_steps_only` em P18/4,/46,/53 | **NOT_RUN_INFRA_BLOCKED** |

**CI `validate` do GitHub não substitui esses comandos executados localmente nem é compilação CVL2.** A CI poderá ser verificada separadamente na HEAD final, relatando seu resultado sem extrapolação. Os nove preflights `CERTORAKEY` da R5 não são `COMPILE_ERROR`; `--version`, `SIGBUS`, `EROFS`, `solc ABI` e checks estruturais não são parser CVL2.

## Próximos gates prioritários

1. **Ação humana obrigatória (VERMELHO):** recuperar/atestar WSL e preservar caches e worktrees, teste de leitura/escrita apenas após liberação do administrador. Registrar saúde, versões/hashes, HEAD, clean worktrees; rodar três validadores e o diff `BASE...HEAD` sem alterar originais.
2. **Experimento 1 para revisão do coordenador:** P18/complete/4, `AccessControlMock`, N.spec original, CLI direto Certora 8.19.0/solc 0.8.6, compile-only em scratch byte-idêntico com timeout e logs; depois comparação distinta com `AccessControl.spec` full. Sem variante implementada nem decisão auto sobre receiver.
3. **Experimento 2 para revisão do coordenador:** P18/complete/53, `ERC1155PausableMock`, N.spec original, mesmo protocolo. Somente depois avaliar *proposta documental* `sig:`/visibilidade e prova de não-vacuidade/reverts, sem tocar `require`, `assert`, hook ou summary. P18/46 fica na próxima fila por exigir domínio `method f` do runner.
4. **Ação semântica distinta (LARANJA):** recuperar spec/runner/ABI auditados, adjudicar `GovernorBase` PER_CALLEE_CONSTANT vs DISPATCHER, `Timelock.schedule(bytes32)` vs `bytes`, e closure de harnesses Initializable/Votes. Nenhum resultado pode receber `SEMANTIC_PROVEN` pela mera passagem no parser.

**NÃO houve Prover completo, teste CVL1, migração de implementação, mudança de labels ou merge. PR continua DRAFT.**

**AGENTE-02 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.**
