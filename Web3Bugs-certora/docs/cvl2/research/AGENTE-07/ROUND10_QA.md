# AGENTE-07 — Rodada 10 / QA: trabalho executado, EIO e gates pendentes

**PR existente:** [#41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), Draft, `research/cvl2-agente-07`. HEAD de partida atestada `3fcbf9d64af93ef9453abbbb7bee09a8c0dba0f5`. Baseline original `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` não alterado.

## 1. Pré-requisitos executados antes da falha

**Execuções locais reais no WSL DESKTOP-5E26TVU, antes de EIO:** `pwd`, `python3 --version` = Python **3.14.4**, `git --version` = **2.53.0**, `df -h /home/mat` = volume **/dev/sdd, 913G livres**, `git status --porcelain` vazio e `git rev-parse HEAD` = `3fcbf9d64af93ef9453abbbb7bee09a8c0dba0f5`. Binário `certoraRun` encontrado em `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun`; **existência não é versão nem execução de compilação nesta R10**. Fetch de HEAD remoto idêntico; criada worktree isolada `/home/mat/cvl2-agent07-round10-20261020`, branch local auxiliar `research/cvl2-agente-07-round10`, sem tocar worktrees de outros agentes. A recuperação ambiental era real nesses comandos, porém apenas temporária.

**Leituras em worktree:** quatro documentos canônicos integralmente lidos com hashlib SHA-256, `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md`, e amostras P1 `complete/1/{1,10,11}.spec` e `incomplete/1/{1,10,11}.spec`. P1 possui 36 complete e 34 incomplete. Históricos e método preservados sem edição.

**Pesquisa Celo executada antes da falha:** REST GitHub pública do arquivo `packages/protocol/contracts/common/Accounts.sol` mostrou **55 commits** na consulta ao path (2019–2026). Conteúdo Git `GET /repos/celo-org/celo-monorepo/git/blobs/ac93720967e0ca762e9f9ff66da34ff558b5e4f9` retornou **HTTP 200**, 44.178 bytes, comprovando que o blob do snapshot existe nesse repo. **16** arquivos do histórico amostrados por `contents/...Accounts.sol?ref=<SHA>` e nenhum tinha o blob exato; a consulta foi **parcial**, não varredura completa. A tentativa de ampliar a amostra **NÃO executou Python**, pois o runtime falhou na inicialização.

## 2. Incidente operacional R10 — EIO real, fora do parser CVL2

Após checagens iniciais sem falhas, a chamada remota que iniciaria nova busca de commits retornou:

```text
Fatal Python error: Failed to import encodings module
Python runtime state: core initialized
OSError: [Errno 5] Input/output error: '/usr/lib/python3.14'
```

**Ação realizada:** interromper imediatamente o uso do WSL conforme instrução. **Não** reiniciar WSL, executar `git reset`, `rm`, patch, qualquer compilador, teste, escrita ou outro processo na máquina. A análise restante e os commits de documentação R10 foram feitos **via conector GitHub**, que é independente do disco com EIO. Nenhuma tentativa abortada por esse erro deve ser chamada `COMPILE_ERROR` CVL2, `PREFLIGHT_AUTH_BLOCKED`, ou execução do Prover.

## 3. Matriz original e reconciliação efetivamente realizadas via API

`ROUND10_MATRIX_156.csv` foi gerado *em memória* do `ROUND9_MATRIX_156.csv` (Git blob `03db82bd2ae6a6277374deba094d04329bf4c649`) e do `results/spec/spec_buglabel.csv` do baseline (Git blob `97e20443586540034a4c0305ce1db19b0d2f8cb5`). O parser CSV preserva aspas, quebras, linhas e `Original Spec`. Comparação independente no momento da geração para TODAS as linhas e relações existentes:

- **156 chaves distintas** `(project_id, original_status, example_id)`: P9 61, P8 42, P20 37, P11 16, **zero duplicação**;
- **zero mismatch** `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Original Spec`, `Original Spec Lines`, Bug Label;
- 47 colunas por linha, `source_or_report_fact` vs `inference` vs `missing_proof` e **`original_compile_status` = `derived_compile_status` = `NOT_RUN`**. `semantic_equivalence=NOT_PROVEN`, `infra_preflight` separado; `round10_stdout_stderr=NONE_NO_COMPILE`;
- SHA-256 dos **156** `N.spec` e source completos provêm do **recálculo físico R9**, validado então no filesystem limpo; **NÃO foram recalculados fisicamente na R10 após EIO**. Os objetos Git obtidos por API são SHA-1 de blob e não equivalem a SHA-256 de build.

**Limite:** a reconciliação documental via API não substitui os scripts históricos executados em checkout saudável. `complete/incomplete`, `VERIFIED/VIOLATED` históricos e labels não foram reclassificados.

## 4. Comandos obrigatórios — não executados nesta rodada por EIO

| Comando | Execução nesta R10 | Status |
|---|---|---|
| `cd Web3Bugs-certora && python scripts/check_specs.py .` | **NÃO** | `NOT_RUN_INFRA_BLOCKED`; sem exit code |
| `cd Web3Bugs-certora && python scripts/check_contests_csv.py .` | **NÃO** | `NOT_RUN_INFRA_BLOCKED`; sem exit code |
| `cd Web3Bugs-certora && python scripts/check_contracts.py .` | **NÃO** | `NOT_RUN_INFRA_BLOCKED`; sem exit code |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NÃO** | `NOT_RUN_INFRA_BLOCKED`; sem exit code |
| `solc`, `certoraRun --compilation_steps_only`, Prover, teste CVL1, `--version` | **NÃO** | `NOT_RUN` |

As verificações com exit 0 da R9 foram realizadas naquela rodada, não reutilizadas como QA local da R10. Após recuperação **validada por administrador**, repetir saúde de leitura/escrita temporária, git status/HEAD/hashes e todos os quatro comandos a partir de checkout íntegro, coletando stdout/stderr/exit.

## 5. Contagem sem duplicidade e decisão de gates

| Indicador próprio AGENTE-07 R10 | Contagem |
|---|---:|
| Propriedades documentadas | **156** |
| Tentativas CVL2 originais realmente executadas na R10 | **0** |
| Tentativas CVL2 derivadas realmente executadas na R10 | **0** |
| `COMPILE_OK` nesta carteira | **0** |
| `COMPILE_ERROR` parser/typechecker nesta carteira | **0** |
| `NOT_RUN` nesta carteira | **156** |
| Equivalências CVL1→CVL2 demonstradas | **0** |
| Projetos totalmente migrados | **0** |

**Globais no dashboard Round9:** 33 tentativas sobre 20 propriedades (11 OK, 21 parser errors, 1 setup error, 7 propriedades com original errado e derivado OK), 1.366 propriedades sem teste CVL2. **Nenhuma das tentativas é atribuída a este agente**. ABI Solidity prévia e executável solc ainda não baixado não são compilações CVL2.

**Propostas de decisão do coordenador:** (1) P9/complete/6: localizar superproject que refere o blob `ac937...`, gitlink Mento/ABI completa do `AccountsHarness`, solc e fases auditadas; (2) P11/incomplete/1: recuperar **somente após autorização e recuperação WSL** o binário oficial `solc-linux-amd64-v0.5.17+commit.d19bba13`, comparando SHA-256 esperado `c35ce7a4d3ffa5747c178b1e24c8541b2e5d8a82c1db3719eb4433a1f19e16f3`, preparar três seeds e struct/link do runner, e solicitar aprovação de um compile-only scratch isolado. Gate distinto de consistência P8 W1/W2/W3, sem Prover nem assumptions.

## 6. Revisão cruzada read-only e CI

PR #43 observado em `cb9a7838e558909f5c4766abb086c6bd23284abf`; documentação Round9: **P5/incomplete/14** erro genuíno CVL2 EXIT 1 do AGENTE-08, **não** compilação desta carteira; P23 Radicle branch Certora 2023 com SplitsHarness distinto de produção 2022 e sem CVT autenticado. Sem edição em PR #43.

**CI GitHub:** consultar workflow da **HEAD final da R10** depois do último commit. `validate: success` é gate estrutural independente de EIO do WSL, não equivalência. A comparação GitHub com a HEAD inicial deve listar somente os documentos R10 em `AGENTE-07/`. Registrar o status remoto no comentário formal do PR, sem antecipar sucesso.

**AGENTE-07 — RODADA 10**
