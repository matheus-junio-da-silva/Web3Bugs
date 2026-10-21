# AGENTE-04 — RODADA 10 — QA, integridade e bloqueio operacional

**Estado de partida confirmado via GitHub:** PR #42 Draft, `research/cvl2-agente-04`, HEAD `3dc12cdc7700d582ce3bcca25c537dfbc6de4e5a`, não mergeado. O PR #49 da coordenação já havia sido integrado como instrumentação documental/QA. No baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` o catálogo possui 1386 properties e 1390 relações Bug Label.

## Procedimentos EXECUTADOS nesta R10

1. **Leitura de normas**, via worktree existente e GitHub, ANTES das alterações: `docs/spec_catalog.md` (79 linhas), `docs/spec_catalog_workflow.md` (487), `docs/spec_catalog_project_1.md` (90), `docs/standard.md` (270); exemplos `results/spec/complete/1/1.spec` e `incomplete/1/1.spec`. Sem edição dos arquivos.
2. **Probe local WSL ANTES do problema:** `uname -s=Linux`, Python 3.14.4, Git 2.53.0, leitura/escrita teste em `/tmp/cvl2-ag04-r10-20261020/health`, `df -h /tmp` saudável, HEAD do worktree anterior igual a `3dc12cdc...`, `git status --porcelain` vazio, compiladores solc 0.8.10 e 0.6.12 disponíveis. Probe **EXIT 0**, mas isto NÃO garante saúde posterior.
3. **Falha subsequente REAL de infraestrutura:** tentativa de leitura do CVL global autenticado pelo WSL: `nl` retornou **`nl: could not read line: Input/output error` (EIO)** com EXIT 1. Por segurança, **nenhum outro comando enviado ao WSL após EIO**. Sem tentativa de reset/rebase/reinstalação/limpeza nem escrita em worktree de colega. A pesquisa continuou **somente via GitHub**.
4. **GitHub fonte/ABI:** SHA Git dos contratos audited GHO/P12/PoR e blobs, leitura do conteúdo FULL/N.spec, comparação em memória JS dos seis methods e regra P15/36 (idênticos); contagem auditada 5 active rules, 2 helper functions, 0 invariant/ghost/hook. PR #40/#46 revisados READ-ONLY.
5. **Reconciliação da matriz NOVA** `ROUND10_MATRIX_157.csv` em memória contra `ROUND9_MATRIX_157.csv` e CSV canônico `results/spec/spec_buglabel.csv`: **157 linhas, 157 chaves únicas** P15=116/P12=26/P2=15, zero diferenças em Property, Target Contract, Result, Detection Outcome, Bug Label(s) ou N.spec path. Hashes `N.spec` e source foram **herdados do ledger R9, não recalculados fisicamente nesta R10**. Campos de status distinguidos: original `COMPILE_ERROR` em três IDs (P12/23,25; P15/36); derivada `COMPILE_OK_LIMITED` só P15/36; **154 originais ainda NOT_RUN**. Nenhuma nova compilação, nenhum `PREFLIGHT_AUTH_BLOCKED`, nenhum resultado semântico provado.

## Compilação e validação local — execução versus bloqueio

| Atividade/comando | Estado R10 | Evidência/justificativa |
| --- | --- | --- |
| `certoraRun --compilation_steps_only`, qualquer ID | **NOT_RUN_INFRA_EIO** | Zero tentativas nesta R10, 33 eventos globais pertencem a rodadas anteriores |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | **NOT_RUN_INFRA_EIO** | Não iniciar após erro de I/O |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_EIO** | Idem |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_EIO** | Idem |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` no WSL | **NOT_RUN_INFRA_EIO** | Não inferir exit 0 de R9 ou CI R10 |
| GitHub validação textual de arquivos novos e escopo do PR | **Em memória pós-publicação** | Não substitui `git diff --check` real |
| GitHub Actions `validate` desta HEAD | **Verificação pós-publicação separada** | CI estrutural pode não incluir `check_specs.py` nem diff BASE...HEAD |

**R9 (histórico, não execução R10):** o trio de validadores e o diff literal passaram EXIT 0 na HEAD `3dc12cdc...`; 6 tentativas CVL2 em 3 propriedades originárias tiveram 4 erros de parser (3 originais únicos), 1 erro de setup Solidity e 1 compile-only derivado EXIT 0 P15/36. Não transportar esses exits para a HEAD R10.

**Segurança:** todos os novos arquivos desta rodada apenas sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-04/` pelo conector GitHub. Nenhuma modificação em `results/spec/`, `contracts/`, `reports/`, `resources/`, `results/cvl2/`, scripts originais, CSV histórico, Bug Labels ou PR de outro agente. PR segue Draft, sem merge. Nenhum Prover, CVL1, mocks, summaries, casts, `require`, `assert` ou Solidity alterados.

## Gate humano

Administrador deve comprovar recuperação persistente de EIO/EROFS/SIGBUS antes de qualquer novo processo WSL. Após isso validar filesystem/read-write, HEAD e worktree separada, versão CLI/solc, hashes e executar exatamente quatro comandos de QA na HEAD atual. Para eventual `--compilation_steps_only`, obter gate por propriedade, copiar byte-identicamente inputs em scratch e registrar SHA256 do original/variante, stdout, stderr, exit, HOME/token env removido e timeout. Não atribuir `SEMANTIC_PROVEN` à aceitação de parser.

**AGENTE-04 — RODADA 10**
