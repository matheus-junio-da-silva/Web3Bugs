# AGENTE-03 — RODADA 10 / Livro de execução e QA

**PR #36 DRAFT, início HEAD 8e4ff5b31406a07f09cbe22aa031f6a4519b701d.** Baseline imutável 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. Alterações via GitHub restritas à pasta docs/cvl2/research/AGENTE-03; worktree R10 fora das demais, sem reset, rebase ou merge.

## Executado no WSL antes do incidente

- Saúde inicial: Python 3.14.4, Git 2.53.0, filesystem com espaço, worktree antiga R9 limpa, fork Certora/rocket-joe-1 em dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10 limpo, solc 0.8.6+commit.11564f7e, solc 0.6.12+commit.27d51765, certora-cli 8.19.0. **Resultado preflight OK naquele momento, não garantia futura**.
- Ler integralmente quatro documentos originais docs/spec_catalog.md, spec_catalog_workflow.md, spec_catalog_project_1.md, standard.md e confrontar complete/1/1.spec vs incomplete/1/1.spec. Documentação oficial consultada: [CVL2 migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html) (inclui alerta de transformação não automática), [changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html). Métodos CVL2 exigem function, external/internal e ; e mudanças de summaries/receivers são semânticas, não cosméticas.
- Criar worktree isolada /home/mat/cvl2-agente03-round10-20261020 (detached) na HEAD inicial, clean. Montar scratch FORK_ONLY /home/mat/cvl2-agente03-round10-scratch com cópias da cena patchada R9 e dos harness/helpers originais; referenciar pacotes OZ 4.4.2 via symlinks no scratch. Nenhuma escrita em fork source ou dados originais.
- Verificar SHA256 de dois sources munged da R9: LaunchEvent.sol e74bc68f15e5fb9a40974a8a723ded121dd0b68e7273cd0daf1672d1cf984d24; RocketJoeStaking.sol af436d7d252e77224165211863d37160db0adf18484726fb46fe91492628e077. Harnesses staged: LaunchEventHarness.sol bbc1acc2e54480c6db2dd1f8c90ffbd34e9a285873ec6a66533cd41cf431e80e; RocketJoeStakingHarness.sol 26cf0d7e67f5369c4d33a4a91d3b55c0c61c58992dc00d58255317528e898f17.
- **Uma tentativa de extrair ABI Solidity (não CVL2)**: alvo certora/harness/RocketJoeStakingHarness.sol, solc 0.8.6, flags --base-path . --include-path node_modules --abi --bin -o scratch/abi/staking --overwrite, timeout 60. Exit **1**, stderr **unrecognised option '--include-path'**. **0 ABI geradas.** O erro antecedeu a análise de Solidity; classificar **SOLC_CLI_OPTION_SETUP_ERROR**, não erro de parser Solidity, muito menos CVL2.
- Próximo comando de inspeção de pacotes OZ scratch retornou literalmente **Input/output error (os error 5)**. Interrompida toda atividade WSL imediatamente; **sem tentativa de corrigir flags, repetir compilação ou usar outros tools naquele filesystem**.
- O erro inicial não implicou uso de credenciais; **nenhum CERTORAKEY lido**, nenhuma execução Certora/Prover/CVL1, nenhuma modificação de require/assert/hooks/ghost/receiver/summary/casts.

**Nota dos logs:** stdout/stderr da tentativa solc foram redirecionados a scratch logs/solc_staking_stdout.log e solc_staking_stderr.log. Devido ao EIO posterior, **não foram relidos/copiados** para o repositório. O exit e stderr listados acima vieram da saída do comando remoto já observada antes do incidente. Não anexar log inventado.

## Executado fora do WSL após incidente

- Consultas GitHub confirmaram o PR #36 Draft, HEAD inicial e comentários de revisão; PR #49 e painel ROUND9_DASHBOARD com 33 eventos em 20 propriedades globais, sem contar esses eventos como execução P24.
- [ROUND10_MATRIX_164.csv](ROUND10_MATRIX_164.csv) criada em memória por reconciliação completa de CSV R9 e canônico original: **164/164 chaves distintas**, 32 campos, campos Property/Target/Bug Label/Result/Detection Outcome/Original Spec preservados sem divergências. N.spec SHA256 **herdados da R9** (quando foram realmente recalculados), não recalculados na R10.
- [ROUND10_SOURCE_ROOTS.csv](ROUND10_SOURCE_ROOTS.csv) gerado com Git blob/URLs fixos para raízes fork; quatro paths TraderJoe identificados como arquivos **introduzidos pelo patch** (seções com diff -ruN), não fontes rastreadas; Owner.sol e spec minúscula Staking não foram inventados.
- Cross-review READ-ONLY PR #42 HEAD 3dc12cdc7700d582ce3bcca25c537dfbc6de4e5a, P15/36 derivada CVL2 compilation-only exit0 do AG04 com remapping; original exit1 parser, candidato sem mapping exit1 setup Solidity. Riscos P12 ABI address user e P2 receiver Chainlink externos. Nenhum arquivo/branch AG04 alterado.
- Web oficial Certora CVL2 consultada em 20/10/2026 pelas URLs explícitas: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html, https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html, https://docs.certora.com/en/latest/docs/cvl/methods.html.

## NÃO EXECUTADO na R10 / estado de bloqueio

| Comando ou atividade | Estado | Por quê |
| --- | --- | --- |
| python3 scripts/check_specs.py . na raiz Web3Bugs-certora | **NOT_RUN_INFRA_EIO** | Interrupção ao observar EIO, após criação dos documentos pela API |
| python3 scripts/check_contests_csv.py . | **NOT_RUN_INFRA_EIO** | Idem |
| python3 scripts/check_contracts.py . | **NOT_RUN_INFRA_EIO** | Idem |
| git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD | **NOT_RUN_INFRA_EIO** | Não usar WSL com erro de I/O |
| Solidity ABI bem-sucedida dos dois harnesses | **NOT_PRODUCED** | Flag CLI inválida no primeiro e EIO posterior |
| certoraRun --compilation_steps_only P24 original ou derivada | **NOT_RUN** | Não há ABI comprovada, nem gate individual, nem ambiente íntegro |
| CVL1, Prover, Fase 2, merge, results/cvl2 | **NOT_RUN** | Não autorizados |

**P24 R10 contagem individual:** 164 original properties históricas incomplete, 0 originals testados em CVL2, 0 derived testados em CVL2, 0 COMPILE_OK, 0 COMPILE_ERROR CVL2, 0 PREFLIGHT_AUTH_BLOCKED, **164 NOT_RUN**, 0 SEMANTIC_PROVEN, 0 MIGRATED_COMPLETE. Houve **uma tentativa de setup solc** na cena Staking, **não** uma tentativa por cada uma das 19 properties da família.

**Próximas ações humanas:** administrador confirmar recuperação EIO e integridade de scratch/checkout; coordenador autorizar gate N164 ou classificar scene fork-only ainda incompleta. Prioridade subsequente: reconstruir ABI de RocketJoeStakingHarness/LaunchEventHarness somente com flags solc realmente suportadas, novos hashes/logs e closure estática completa. Estado operacional **VERMELHO EIO**; técnico **LARANJA**.

**AGENTE-03 — RODADA 10.**
