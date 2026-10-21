# AGENTE-03 — RODADA 9 / QA e execução efetiva

**PR:** #36, branch research/cvl2-agente-03. **Baseline:** 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. **HEAD inicial:** cfaf119579ec3c1718bcd32b6e637c03ea4cd174. Worktree isolada R9 em /home/mat/cvl2-agente03-round9-20261020, criada por git worktree add --detach a partir da HEAD remota **sem reset, rebase ou alteração das worktrees R5/R6**. Um arquivo untracked da R6 não foi tocado. O fork Certora/rocket-joe-1@dba90f9 permaneceu clean.

## 1. Ambiente — de fato examinado (preflight)

Em 20/10/2026, comandos read-only responderam: Python 3.14.4, git 2.53.0, df com filesystem legível e espaço disponível, git HEAD R9 igual à branch remota, worktree R9 inicialmente limpa, git cat-file baseline válido. Os quatro guias históricos foram lidos integralmente e seus SHA256 exibidos; referências P1 complete/1 e incomplete/1 e catálogo foram inspecionadas. Esta observação de saúde é **local a esta rodada**; não garante ausência de EIO/SIGBUS/EROFS futura. Em caso de retorno desses erros, interromper testes.

## 2. Experimento R9 executado SOMENTE em scratch — não Certora, não solc

| Ação executada | Input/cwd e integridade | Resultado real |
| --- | --- | --- |
| verificar git HEAD/status do fork | /home/mat/cvl2-agente03-source-fork, dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10, clean | OK |
| copiar source do fork | cp -a fork/contracts/. para scratch/scene/ | executado; original x scratch LaunchEvent cmp **exit 0** |
| verificar blob do patch | certora/applyHarness.patch Git blob abfb1eae851307c9a3e7d17a7b3e913962952845, SHA256 e06f5a9d5503e82310ffccfab55214b9cb847d2146656f2558271e0777e27fdb | MATCH com R4/R8 |
| patch dry-run | CWD scratch/scene, **patch --dry-run --batch --fuzz=0 -p0 < fork/certora/applyHarness.patch**; stdout + stderr redirecionados a ROUND9_PATCH_FUZZ0_DRYRUN.log | **EXIT 0**, 23 linhas do log, nenhum aviso de fuzz, offset ou rejeição |
| aplicação real de patch | CWD scratch/scene, **patch --batch --fuzz=0 -p0 < fork/certora/applyHarness.patch**; log bruto ROUND9_PATCH_FUZZ0_APPLY.log | **EXIT 0**, 23 linhas, pós-LaunchEvent SHA256 e74bc68f15e5fb9a40974a8a723ded121dd0b68e7273cd0daf1672d1cf984d24 |
| verificar fork depois | git status --porcelain no checkout fork versionado | vazio |
| autenticar dependências OZ 4.4.2 | Python em scratch, tarballs existentes da R5; calcular SHA512 e comparar com Yarn lock do fork L672 e L677 | **2/2 SRI MATCH**, sha256 contracts f0f5e4bd..., upgradeable b6ea889c... |
| ler source Staking e hashes | git show ef2ef302:contracts/RocketJoeStaking.sol e git dba90f9, scripts/harness | checagem estática; sem solc e sem Prover |
| conferir conteúdo N164 e helper | N164 SHA256 852ef929..., full sanity.spec SHA256 b1631a0..., helper fork blob b12fec... | checagem estática, sem source N164 modificado |

**Falha de ferramenta separada:** a primeira tentativa do *script privado de leitura de lock* falhou com AssertionError por aspas nos campos Yarn integrity/version, **não executou solc, parser CVL2 ou Prover**. O parser de lock foi ajustado apenas na análise scratch e a segunda tentativa teve **2/2 SRI MATCH**, como acima. Nenhuma chamada de autenticação, nenhuma credencial exposta.

**Não executar:** scripts históricos originais (invocam make -C certora munged e certoraRun); solc ABI; certoraRun --compilation_steps_only; variantes N164 com function, receivers, casts, require/assert; Prover; CVL1. **0 compilações Solidity, 0 compilações CVL2 e 0 resultados de parser desta rodada.** Patch é apenas uma cena Solidity de fork, **não um resultado de property**.

## 3. Matriz, catálogos e hashes — executado R9

Matriz nova **ROUND9_MATRIX_164.csv**, 164 registros distintos (P24,incomplete,IDs 1..164), **63 campos**. Arquivo gerado por script somente scratch que leu cada N.spec real da worktree e o catálogo original, verificou:
- **164/164 SHA256 N.spec recalculados** e idênticos ao ledger anterior; SHA256 da matriz **84f782ff9646d6cf8a1eaabfc832f7b4d2e45bcbfff2539c5d214f391ca26158**.
- **164/164 Git blobs N.spec** idênticos ao baseline histórico; **164/164** blobs full CVL de snapshot iguais ao fork fixado e aos campos do ledger antigo (oito arquivos únicos). Isso não equivale a ABI auditada.
- **Zero diferenças** nos campos Property, Target Contract, Result, Detection Outcome, Bug Label e Original Spec por chave (24,incomplete,N) versus results/spec/spec_buglabel.csv; CSV canônico e dois contracts de P24 verificados idênticos ao baseline.
- Distribuição: LEHighLevel 10, LEInProgress 3, LEPreset 1, LEValidStates 35, LEVarTran 19, LaunchEvent 76, Staking 19, sanity 1. **164 Result NOT_STATED**; **161 Detection Outcome NOT_STATED**, **3 INCONCLUSIVE**.
- Cada linha tem source hash, estado de execução CVL2 **NOT_RUN**, autoria **NONE**, execução/exit **não aplicáveis**, fonte/fato, inferência, prova ausente, riscos semânticos e gate individual. Apenas N164 carrega referência ao patch **de cena**, explicitamente não à compilação da property.

## 4. Três validadores históricos — pré-commit executados

Logs em **ROUND9_VALIDATION_PRECOMMIT.log**, cwd raiz Web3Bugs-certora, timeout 120 por processo:
- python3 scripts/check_specs.py . → **EXIT 0**, 1386 exemplos e 1390 relações consistentes.
- python3 scripts/check_contests_csv.py . → **EXIT 0**.
- python3 scripts/check_contracts.py . → **EXIT 0**.

**Obrigação pós-commit:** executar novamente os três validadores na worktree com a HEAD commitada e, da raiz Git, **git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD**. Não atribuir um exit antes de executá-los; publicar SHA e logs efetivos no comentário do PR #36. Validar paths do diff inteiro, staging whitespace e ausência de arquivos fora de docs/cvl2/research/AGENTE-03. CI GitHub Actions é independente, **não** Prover nem prova CVL2.

## 5. Auditoria cruzada READ-ONLY e estados finais

PR #42, HEAD lida 06dca368f5f2324da45f156dd9bc206745f11af0, Draft: P12/23,25 (diferença ABI address user; erros CVL2 methods exit 1 **anteriores**) e P15/36 (GhoDiscountRateStrategyHarness e seis methods, exit 1 **anterior**); proposta methods de AG04 R8 segue **documental**. Nenhuma execução R9 nem alteração na branch AG04.

**Contadores próprios R9:** 164 documentados, **0 CVL2 original ou derivado executado**, **0 COMPILE_OK**, **0 COMPILE_ERROR**, **164 NOT_RUN**, **0 SEMANTIC_PROVEN**, **0 MIGRATED_COMPLETE**. Único diagnóstico novo: **1 cena patch Solidity FORK_ONLY, exit0 dry-run e exit0 aplicação**, sem compilação. Não somar estes dois comandos como duas propriedades.

**Alerta:** AMARELO operacional (preflight estável na R9, monitorar EIO/SIGBUS); LARANJA histórico/semântico (runner, ABI e equivalência não provados). **AGENTE-03 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.**
