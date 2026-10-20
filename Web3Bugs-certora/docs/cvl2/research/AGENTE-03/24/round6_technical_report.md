# AGENTE-03 — RODADA 6 / Rocket Joe P24 — relatório de evidência

**PR #36 (Draft), documentação apenas.** Todos os 164 exemplos permanecem historically incomplete e UNRESOLVED_CANDIDATE. `COMPILE_OK=0`; `COMPILE_ERROR=0`; `PREFLIGHT_AUTH_BLOCKED=0`; `NOT_RUN=164`; `SEMANTIC_PROVEN=0`; `MIGRATED_COMPLETE=0`. Arquivo `round6_evidence_matrix.csv`: 164 chaves distintas, nome, target, resultados canônicos e SHA individuais herdados dos registros da Rodada 5, cenário, comando e exit observados, bloqueio, risco/vacuity e gate.

## Preparação e fontes

Antes da pesquisa, a worktree isolada em `/home/mat/cvl2-agente03-round6-20261020` foi criada em HEAD `907303e8647bf9e390c481bc4180f736fb21814e`. Foram lidos os quatro guias obrigatórios (79, 487, 90, 270 linhas) e comparados `results/spec/complete/1/1.*` e `incomplete/1/1.*`: *complete* é fechamento de dependências no snapshot, nunca CVL2 validado. Revisão mais recente do PR #36: `#pullrequestreview-5589227193`, 164/164 e Fase 2 não autorizada. Painel do PR #47: `ROUND5_DASHBOARD.md` HEAD `5835165642875f52de43227cb20334bae66edb77`: 1.386 propriedades, 4 exits CVL2=0 de escopo limitado, 11 exits=1, 1.371 não testados, zero semânticas provadas.

Referências oficiais: [CVL2 Migration Guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [CVL2 Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [Statements/reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html). O receiver de summary, anotações internal/external, ghost state e `lastReverted` exigem análise de domínio e não simples tradução lexical.

## Hunk 7 — linhas, bytes e risco

| Evidência | Linhas / commit | Comportamento |
| --- | --- | --- |
| Solidity auditado | `lfj-gg/rocket-joe@ef2ef30248661b5509c52ab30af9bd0fc07f6657:contracts/LaunchEvent.sol:673–679`, blob Git `2af4cfe5472decc22ab3dd361d0117893a61539e` | Guarda `address(this).balance >= avaxReserve` |
| Fork posterior | `Certora/rocket-joe-1@dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10:contracts/LaunchEvent.sol:673–679`, blob `2656eb863a83ca2a53714eb0ed336f420f952dae` | Guarda `address(this).balance - _value >= avaxReserve` |
| Patch original | `certora/applyHarness.patch:96–104`, blob `abfb1eae851307c9a3e7d17a7b3e913962952845` | Hunk #7 pressupõe condição do fork e injeta `virtual` |
| Harness do fork | `certora/harness/LaunchEventHarness.sol:114–116`, blob `1b6a42c5e397d03c921d18217364c7e67878621a` | Override com `IReceiver(_to).receiveETH{value: _value}()` no lugar de low-level call/guard |

A alteração da guarda aparece no commit histórico `8c01a06`, datado 2022-02-04, posterior ao auditado (2022-02-03). Busca de `git log --all -- certora/applyHarness.patch` localizou patches históricos em `c308ba7` (2022-03-09) e `50e53fb` (2022-03-12); a cópia `c308ba7` já espera a guarda subtrativa. A árvore do commit auditado não contém `certora/`, `.conf`, helper ou patch. **Não foi identificado patch/harness fixado com identidade de bytes e aplicação --fuzz=0 ao commit auditado**; ausência nas árvores examinadas não prova inexistência histórica fora delas.

Reexecução somente no scratch `/home/mat/cvl2-agente03-round6-scratch/scene-fork/`: `patch --batch --fuzz=0 --dry-run -p0` exit **0**; aplicação do patch original com `--fuzz=0` exit **0**, sem alterar o fork versionado. A cena híbrida da Rodada 4 falhou em `--fuzz=0` e aceitou `fuzz 2`, inadequado para provar equivalência. A guarda auditada e do fork apresentam fórmulas distintas; o exemplo aritmético hipotético `balance=100,reserve=80,value=30` as distingue, **não** demonstra alcançabilidade ou contraexemplo Prover.

## Import closure não OZ e compilação

Novo escaneamento **estático** dos 6 scripts, usando `certora/munged` do patch aplicado em scratch, os helpers do fork e os pacotes OZ 4.4.1/4.4.2 autenticados por SRI na Rodada 5:
- `verifyLEHighLevel.sh` / `verifyLEValidStates.sh`: 12 roots, 49 arquivos Solidity distintos, 61 arestas de import, 0 caminhos ausentes em ambas as versões.
- `verifyLEVarTran.sh`: 11 roots, 47 arquivos, 59 arestas, **1 root ausente**: `certora/harness/Owner.sol`, não substituir por OwnerA/B.
- `verifyStaking.sh`: 3 roots, 15 arquivos, 19 arestas, 0 caminhos ausentes.
- `stakingRule.sh`: 3 roots, 14 arquivos, 18 arestas, 0 imports Solidity ausentes, **mas** `--verify RocketJoeStaking:certora/spec/staking.spec` usa casing sem `staking.spec` presente.
- `sanity.sh`: 10 roots, 47 arquivos, 59 arestas, 0 caminhos ausentes.

**Limite:** resolução de paths textual da cena do fork não é compilation/ABI nem valida driver contra auditado. Tratar `solc 0.8.6` / `0.6.12` como versões de binários identificados localmente, não identidade de binários históricos. Não afirmar que `node_modules` efetivos do Prover foram recuperados. Source SHA CVL original das oito specs permanece byte-idêntico entre fork e snapshot, mas targets Solidity LaunchEvent e Staking divergem.

**N164 sanity:** closure textual do fork é candidata; o N.spec original SHA256 `852ef92957b7d31e844ae41c7e7c4307056e2bb53d6446a4073c8846870070c9` não foi alterado. Não se executou `certoraRun --compilation_steps_only`, pois o filesystem remoto passou a retornar **EIO** ao ler `sanity.sh`, e Python/solc apresentaram **Bus error / EIO**. Isso **não é `COMPILE_ERROR` nem `PREFLIGHT_AUTH_BLOCKED`**, e nenhuma autenticação Certora foi tentada. O CLI direto instalado foi identificado antes da falha: `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun`, `certora-cli 8.19.0`. Não houve Prover/CVL1, alteração de require/assert/ghost/hook/cast/summary, nem implantação derivada.

## N.txt, status e riscos por ID

A Rodada 5 havia conferido integralmente 164 N.txt: 161 com helper erc20 ausente **no snapshot**, 3 LEInProgress sem tal import; catálogo canônico P24 contém `164 Result=NOT_STATED` e `Detection Outcome=161 NOT_STATED + 3 INCONCLUSIVE`. A matriz R6 conserva os campos exatos do índice R5 com seus SHA para cada ID, acrescentando status de execução real e próximas dependências. As categorias dominantes continuam 77 sem runner, 3 LEInProgress, 46 com ABI externa não demonstrada, 19 Owner.sol ausente, 19 Staking divergente. Atenção específica aos IDs 2/5/7/147/150 (fórmulas no PDF), 12/13/152/154 (existenciais/vacuity), 163 (`require` pós `@withrevert`, não `assert`) e 164 (`assert false` diagnóstico). Não transportar VERIFIED do PDF.

## Auditoria cruzada somente leitura PR #42

Examinada HEAD `dd957753ac06d6e899d44cb7caf952de8e3e0916`, comentários, `round5/P12_TARGET_ABI_AND_DIAGNOSTICS.md` e `round5/P15_PACKAGE_IMPORT_CLOSURE.md`, sem editar arquivos ou branch alheia. P12/23 e P12/25 usaram N.spec byte-idênticos e solc 0.6.12 de snapshot com ABI exit 0, porém CVL2 CLI exit 1 por gramática legada de methods; a auditoria tem argumento `address user` que o snapshot remove. P15 atestou 3 bundles npm e ABI solc 0.8.10 de harness/patch, **não compilação CVL2**; patch munged altera require e visibilidade. P2 ainda não tem receiver externo e wrappers históricos comprovados. Nenhuma promoção de COMPILE_OK ou equivalência.

## QA, impedimento e gate do coordenador

**Executado:** leitura e hashes existentes das oito specs, linha/corpo do guard, busca histórica de commit e patch, patch fork fuzz0 em scratch (exit 0), matrizes estáticas locais executadas antes do erro de filesystem. **Não executado:** Certora CLI, solc, Prover, CVL1, validadores pós-commit Python e `git diff --check` após publicação. Tentativas de preflight do ambiente, sem executar CVL2: leitura de `sanity.sh` retornou EIO; `python3 --version` retornou Bus error. Não atribuir sucesso a comandos não executados. Publicação documental via conector GitHub após falha remota; requer **QA independente em ambiente funcional antes de considerar PR validado**.

**Gate solicitado:** coordenador deve decidir target histórico/harness, disponibilizar um patch que encaixe estritamente na fonte auditada ou adjudicar a divergência; resolver Owner.sol e runner staking/casing, vincular solc/linking/ABI/verifier; e autorizar explicitamente experimento `fork-only` N164 em ambiente estável. Sem qualquer saída em `results/cvl2`, PR #36 Draft sem merge. **Alerta LARANJA com QA pós-commit PENDENTE por EIO.**

**AGENTE-03 — RODADA 6.**
