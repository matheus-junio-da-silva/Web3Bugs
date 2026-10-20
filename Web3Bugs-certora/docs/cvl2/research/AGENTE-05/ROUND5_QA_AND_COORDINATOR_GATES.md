# AGENTE-05 — RODADA 5 — QUALIDADE CVL2 | QA e critérios de gate

**Data:** 2026-10-20. **PR:** [#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), somente documentação, **Draft**. **Base histórica:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. **HEAD original da rodada:** `21adc9551d7bf6aa979486e34a11d1f26f4909f5`. **Workspace isolado:** `/home/mat/cvl2-agente05-round5-20261020`; branch local separada `research/cvl2-agente-05-round5`, destinada a push fast-forward no PR da branch `research/cvl2-agente-05`, sem reset.

## Ledger individual completo

[Matriz Round 5: `ROUND5_PROGRESS_148.csv`](ROUND5_PROGRESS_148.csv) tem **148 chaves únicas** `(Project ID, original status, Example ID)`, todas com property, target, estado histórico, result/outcome original, SHA-256 de N.spec, prioridade, fonte recuperada, evidência de execução, status semântico e próximo gate. A geração exigiu que **todos os 148 hashes** coincidissem com a matriz preexistente por projeto. Não edita `properties.csv` nem `results/spec/spec_buglabel.csv`.

| Projeto | Casos | Complete | Incomplete | Round 5 diagnósticos CVL2 | Evidência anterior mantida |
| --- | ---: | ---: | ---: | --- | --- |
| P7 AAVE V3 | 74 | 46 | 28 | **5 erros de compilação do fragmento** (complete 41,63,36,47,73) | **2 fragmentos com COMPILE_OK anterior** (37/65), mas specs integrais CVL1 falham em CVL2 |
| P19 OUSD | 37 | 2 | 35 | nenhum novo | **2 derivadas mathint compilaram anteriormente** (1/2), `02_unresolved` |
| P6 Static aToken | 32 | 0 | 32 | nenhum | bloqueio da revisão auditada |
| P3 Rescue | 3 | 0 | 3 | nenhum | submódulo recuperado, runner ainda não autenticado |
| P21 Lido DSM | 2 | 0 | 2 | nenhum | harness e getter ausentes |
| **Total** | **148** | **48** | **100** | **5 COMPILE_ERROR novos** | **4 COMPILE_OK limitados anteriores** |

Distribuição por evidência de compilação: **5 `SNAPSHOT_FRAGMENT_CVL2_COMPILE_ERROR` realmente executados nesta rodada**; **2 `SNAPSHOT_FRAGMENT_CVL2_COMPILE_OK_PRIOR_ROUND`**; **2 `DERIVED_MATHINT_CVL2_COMPILE_OK_PRIOR_ROUND`**; **139 `NOT_TESTED`**. **0 `SEMANTIC_PROVEN`**, **0 `MIGRATED_COMPLETE`**, **0 reprodução do job histórico 2022/2023**. Pesquisa preexistente, não bucket final: **12 `DOCUMENTED_CANDIDATE` / 5 `UNCHANGED_CANDIDATE` / 131 `UNRESOLVED_CANDIDATE`**. A presença de novos erros CVL2 não altera as categorias históricas e não deve ser copiada para `Result`.

## Artefatos e evidência cruzada

- [P7 — cinco exemplos, ABI, método paramétrico e hashes/logs](7/ROUND5_ABI_METHOD_DOMAIN_AND_COMPILE.md) e `7/round5_logs/`: cinco `stdout.log.gz` + cinco `stderr.log.gz` completos, arquivos ABI Solidity-only de StableDebtToken e VariableDebtToken, `ROUND5_COMMAND_MANIFEST.json` com comandos/timeout/hashes/cwd/exit.
- [P3/P6/P19/P21 — fontes, recuperação e busca negativa](ROUND5_EXTERNAL_RECOVERY_AND_BLOCKERS.md): P3 gitlink e árvore de submódulo; P19 tarballs OpenZeppelin autenticados por SHA-512; P6 PDFs com diferentes commits; P21 comentário concreto permitindo `quorum > guardians.length`.
- [Cross-review do PR #38 somente leitura](ROUND5_PR38_READONLY_SPECIFY_QUEUE2_REVIEW.md): P17/8,9,39 e P1 `queue2`, sem atualização da branch alheia.

## Testes efetivamente executados durante a pesquisa

1. **Cinco** invocações do Certora CLI 8.19.0 em scratch, somente `--compilation_steps_only`, subprocess timeout 65s, target Solidity 0.8.10, cópias byte-idênticas, exit 1 por `sig:` ausente. Nenhum Prover, CVL1 ou formal verify foi chamado. Logs disponíveis.
2. **Duas** extrações de ABI Solidity-only com solc 0.8.10, ambos exit 0, 33 e 30 funções respectivamente; seis selectors disallowed existentes, todos com revert deliberado.
3. **Git histórico em scratch:** pin `lib/solidity-utils@49f2bd...` recuperado; clone `HEAD^{tree}=36cb441...`; interface IERC20 presente.
4. **Dois** downloads npm `pack --ignore-scripts` em scratch, sha512 exatos do `yarn.lock`; 38+8 imports OZ diretos disponíveis.
5. **Leitura somente da branch PR #38** (HEAD `e075395...`): inspeção P17/8,9,39, queue2 e `git diff --check BASE...remote branch` exit 0, sem editar branch.

Os **três validadores oficiais do catálogo e o diff do PR #40 devem ser executados novamente após commit e push**, conforme solicitação da rodada. Seus códigos de saída pós-push serão registrados no comentário de entrega GitHub, não inferidos dos testes de compilação nem de status de CI.

## Decisões que dependem do coordenador

| Gate | Evidência necessária | Enquanto ausente |
| --- | --- | --- |
| P7/41,63,36,47,73 | aprovação individual para testar transformação `sig:` em cópia scratch, com ABI/receptor dos `methods` globais, `method f` e regra de vacuity documentados | manter `DOCUMENTED_CANDIDATE`/UNRESOLVED por semântica; **não** gerar CVL2 derivado |
| P7/37,65 | job de auditoria correspondente, EIP712/initialization, cena, hooks/summaries e checagem de reachability | fragment-only `COMPILE_OK`; **não** `00_unchanged` final |
| P7/3 | implementação exata `SimpleERC20`, `handleAction` receiver/links e hook Sstore | contextual blocked |
| P19/3–37 | closure transitiva e árvore efetivamente compilada após `applyHarnesses.sh`, sem mexer na original; flags e target de cada rule | dados OZ são fonte recuperada, não migration |
| P19/1–2 | documentação semântica CVL1 real para `divPrecisely`, inclusive `RCPT=0` | **`02_unresolved`**, não repetir piloto |
| P3/1–3 | harnesses, remappings, scripts, linked tokens, solc_map e commits do run por rule | gitlink recuperado mas incompletes preservados |
| P6/1–32 | origem/commit completos de `ac92951` e `51d46b1`, hash do PDF e runner aplicável | histórico conflituoso, sem compile-only |
| P21/1–2 | `DepositSecurityModuleHarness`, getter real `getGuardianLength` e prova do report por rule | não sintetizar getter nem reinterpretar assertion |
| AGENTE-06 PR #38 | Specify 2019 runtime/aliases; helper `queue2`/`_mock` e jobs por rule | cross-review mantém unresolved, read-only |

**ALERTA DA RODADA 5: LARANJA.** Há avanço verificável de ABI e recuperação de fontes, mas cinco falhas sintáticas novas, zero equivalências CVL1→CVL2 e dependências globais/históricas não fechadas. Nenhum merge, Prover ou mudança de semântica autorizados.

**Assinatura: AGENTE-05 — RODADA 5 — QUALIDADE CVL2.**

**Integridade adicional dos logs:** para evitar warnings de `blank-at-eof` sem modificar bytes emitidos pelo CLI, todos os stdout/stderr originais foram comprimidos em `gzip` determinístico (`mtime=0`). Cada descompressão foi comparada byte-a-byte à fonte original; hashes SHA-256 **comprimido e descomprimido** estão no manifesto. `gzip -dc <arquivo>.log.gz` reproduz integralmente o log bruto.
