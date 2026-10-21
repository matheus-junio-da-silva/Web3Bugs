# AGENTE-08 — RODADA 10 / Registro de QA, execução e incidente EROFS

**PR existente:** [#43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43), `research/cvl2-agente-08` Draft. **HEAD observada antes de alterar:** `cb9a7838e558909f5c4766abb086c6bd23284abf`. Baseline catalogado imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; upstream PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.

## Saúde da infraestrutura — realmente observada

No **WSL DESKTOP-5E26TVU** foi executado preflight básico **antes** de criar a variante: `date -Is`, `uname -sr`, `df -h /home/mat /tmp`, `git rev-parse HEAD`, `git status --porcelain` no checkout **exclusivo** `/home/mat/cvl2-agente08-round9-20261020/repo`. HEAD correspondeu a `cb9a7838e558909f5c4766abb086c6bd23284abf`, branch AGENTE-08 e status limpo. Arquivos originais eram legíveis. Quatro documentos `docs/spec_catalog.md` (79 linhas), `docs/spec_catalog_workflow.md` (487), `docs/spec_catalog_project_1.md` (90), `docs/standard.md` (270) foram lidos integralmente com `cat` e comparados os precedentes P1 `complete/1/1.spec` e `incomplete/1/1.spec` (sha256 originais documentados na saída do preflight).

No scratch novo e exclusivo `/home/mat/cvl2-agente08-round10-20261020/scratch/`, `mkdir`, `printf` e `cmp` inicialmente **passaram**. CLI `certora-cli 8.19.0` e `solc 0.8.10+commit.fc410830.Linux.g++` disponíveis. SHA256 do original P5/14 conferiu: `0c0e05b80677a46deccfe1494e205cf09b966efab14785e6206c37a0a92e2031`. O arquivo de stdout original R9, no scratch antigo, foi relido e sua integridade SHA256 **`cbf24143137931fcd317c00fd3c175e440fcbf5a16b9efc945ce21f49e4269f8`** confirmada.

### Interrupção real observada durante preflight da variante

Foi criada com sucesso, em scratch fora do repositório, **uma** variante lexical temporária (`ROUND10_P5_LEXICAL_PROPOSAL.md` contém diff e hashes). SHA256 derivado **`f246fe4490c92102fdc1fd91634bf4f7506f3a6c42e9124ae7d37aa61530c804`** e `cmp` do N.spec original confirmados ANTES da falha. Tentou-se configurar um comando `certoraRun` com 11 seeds, 10 links, `--solc` versionado, `--compilation_steps_only`, `HOME`/cache novos, ambiente `env -i` e `timeout -k 5s 70s`. **O shell retornou `Read-only file system` ao tentar gravar `logs/command_exact.txt`, `logs/start_time.txt`, `logs/stdout.txt`, `logs/stderr.txt`, `exit_code.txt`.** A falha de redirecionamento impediu iniciar `certoraRun` (nenhum stdout/stderr de Certora derivado foi criado). O shell posteriormente imprimiu `DERIVED_CVL2_EXIT=1`, mas essa variável refletiu **o erro de redirecionamento no shell**, **NÃO** um processo Certora executado. Consequentemente:

- **`round10_derived_compile_status=NOT_RUN`**;
- **`round10_derived_preflight=EROFS_LOG_REDIRECTION_PREVENTED_CERTORA_PROCESS_START`**;
- **`round10_compiler_exit_code=N/A_NO_COMPILER_LAUNCHED`**;
- nenhuma interpretação de `COMPILE_ERROR` baseada nesse exit 1;
- **nenhum novo solc, Prover, CVL1 ou Certora CLI de compilação foi executado na R10**; o `--version` foi apenas conferência de toolchain.

**Interrompi todos os comandos no WSL imediatamente após EROFS.** Não houve `wsl --shutdown`, remount, reset, rebase, limpeza destrutiva, escrita no checkout alheio ou nova tentativa de build. A disponibilidade temporária no primeiro preflight NÃO garante a saúde permanente do dispositivo.

## Contagem executada vs histórico — por exemplo, sem dupla contagem

| Medida AGENTE-08 | R10 nova execução | Histórico acumulado desta carteira |
| --- | ---: | ---: |
| Propriedades documentadas | 155 | 155 |
| Tentativas **originais realmente iniciadas em Certora** | **0** | **1** (P5/incomplete/14, R9) |
| Tentativas **derivadas realmente iniciadas em Certora** | **0** | **0** |
| `COMPILE_OK` CVL2 | 0 | 0 |
| `COMPILE_ERROR` parser/typechecker CVL2 | **0 novo** | **1** (P5/incomplete/14, R9 exit1) |
| Propriedades `NOT_RUN` CVL2 | 154 historicamente | **154** |
| Derivadas em `NOT_RUN` com pré-flight EROFS | **1** | **1** |
| Equivalências CVL1→CVL2 demonstradas | 0 | **0** |

**Não** adicionar a tentativa EROFS aos 33 compile-only de 20 propriedades distintas do painel de coordenação R9. A R10 não criou novo `COMPILE_OK` nem nova property distinta testada. O original R9 tinha [stdout Base64 byte-exato](ROUND9_P5_N14_stdout.log.b64), status parser `COMPILE_ERROR` real, SHA original conferido; isso permanece sem reexecução.

## Validações documentais efetivamente realizadas via GitHub API (não WSL)

- Nova matriz `ROUND10_MATRIX_155.csv` foi parseada **em memória** a partir de `ROUND9_MATRIX_155.csv` publicado e reconciliada às relações de `results/spec/spec_buglabel.csv` no baseline Git SHA `97e20443586540034a4c0305ce1db19b0d2f8cb5`. **155 chaves `(project_id,original_status,example_id)`, 0 duplicatas e 0 divergências** em Property, Target, Result, Detection Outcome, Original Spec, Original Spec Lines e Bug Label; P5=17, P13=58, P14=34, P23=46. N.spec sha256 das outras 154 chaves foi preservado das matrizes anteriores; **não** alegar rehash local de 155 N.spec.
- **P14 source auditada via GitHub API**: `MarginCalculator.sol` Git blob `4987c09fba9e98d297e1b6efecfeb0e91967f4b1`; branch de all-empty condicionado a guards de `_checkIsValidVault`, `_isMarginableLong` e `_isMarginableCollateral` foi lida nas linhas detalhadas em [ROUND10_EVIDENCE.md](ROUND10_EVIDENCE.md).
- **P23**: duas árvores Git recursivas (70 + 44 objetos, `truncated=false`) inspecionadas em buscas delimitadas por `CVT`, `generated`, `wrapper`, `output`; nenhum output CVT gerado nos pathnames públicos dessas árvores. Não estender a conclusão a outros commits/cache/job privado.
- **Cross-review** PR #39 da HEAD `fc668ccdfa825266952b9daca9cc08432ad8ccf6`: documentação original e último review consultados SOMENTE LEITURA; P10/33 derived `COMPILE_ERROR` `lastHasThrown` não declarado, P10/34 derived `COMPILE_OK` limitado com `require false` preservado. Nenhuma escrita no PR alheio.

### QA local após commits desta rodada — NÃO EXECUTADO devido ao incidente

Os comandos exigidos, **não executados nesta rodada** após EROFS, são:

```bash
cd Web3Bugs-certora
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
cd ..
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

Cada um permanece `NOT_RUN_INFRA_BLOCKED` em **R10**; os resultados **EXIT 0 de R9 na HEAD anterior** não podem ser falsamente transportados para os commits desta rodada. O GitHub Actions `validate` que rodar no commit final é **CI estrutural remoto**, não substitui os comandos locais ou Prover. `compare_commits` permite verificação remota de escopo e o conector GitHub permite conferir whitespace textual das três entregas, mas isso tampouco executa o `git diff --check` pedido. Após publicação da HEAD final, revisar CI, diffs, Draft e arquivos; não afirmar exit local inexistente.

**Intervenção humana bloqueante:** o administrador deve restaurar e comprovar filesystem gravável de modo estável, sem alterar histórico ou branches, antes de reexecutar qualquer diagnóstico ou os quatro checks locais. Em seguida o coordenador decidirá **por propriedade** se a tentativa P5/14 scratch derivada pode prosseguir. PR permanece DRAFT, 155 dossiers de pesquisa, **0 equivalências**.

**AGENTE-08 — RODADA 10.**
