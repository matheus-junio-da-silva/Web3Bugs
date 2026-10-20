# AGENTE-02 — RODADA 6 / Diagnóstico CVL2 direto e limite operacional

Data: 2026-10-20. [PR #37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), branch `research/cvl2-agente-02`, baseline **imutável** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. HEAD de partida verificada `9350a3f9a1ffd5861358a3b085adfa2bd48a8e6b`. Worktree isolada **criada** em `/home/mat/cvl2-agente02-round6`. Nenhuma alteração dos originais, nenhuma migração, Prover, CVL1 ou merge.

## Pré-requisitos e fontes lidos antes da pesquisa

Os quatro arquivos obrigatórios foram percorridos integralmente no checkout: `docs/spec_catalog.md` (79 linhas, SHA256 `83a28f78a4d33e421e80bebe04973eeb03d0fefc2ac290509d7dd22a701623c3`), `docs/spec_catalog_workflow.md` (487, `aa504e32ac26eff34c492374b9b71f246091a03f0fda541bce548bc8ce298c5b`), `docs/spec_catalog_project_1.md` (90, `750622fb5b1ddf461f35b3bc8332a01bcba7cc5827fea9b76d1451746b1a2e69`) e `docs/standard.md` (270, `455ee45d19a0a582e5dcbd2a14e2ec9c90cbfcbca88f598498957f518ce1a99d`). Conferidos os exemplos `results/spec/complete/1/{1,3}.spec` e `results/spec/incomplete/1/{1,29}.spec`: respectivamente recorte de methods/summary, dependências e selector, helper `queue2` ausente, e sonda `assert false`; `complete` não é prova de migração CVL2.

Revisão de coordenação mais recente do [PR #37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), [painel Round 5](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/5835165642875f52de43227cb20334bae66edb77/Web3Bugs-certora/docs/cvl2/coordination/ROUND5_DASHBOARD.md), [P18_DIRECT_CLI_CONTRACHECK.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/5835165642875f52de43227cb20334bae66edb77/Web3Bugs-certora/docs/cvl2/coordination/P18_DIRECT_CLI_CONTRACHECK.md) e revisão do [PR #36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36) consultados. Documentação oficial atual: [migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html) e [specification syntax](https://docs.certora.com/en/latest/docs/cvl/index.html).

## Resultado disponível de CVL2: distinguir o proprietário da execução

| Property | Fonte N.spec SHA-256 original | Target | Prova de parser real | Rodada 6 local |
| --- | --- | --- | --- | --- |
| `complete/18/3` `grantRoleEffect` | `5ca7758775888bd0f8275e7f00a41b3dd8056668bc647bb7478010b1dff702c2` | AccessControlMock | **Coordenador**, CLI 8.19.0, solc0.8.6, `--compilation_steps_only`, **EXIT 1**, exige `function` e `;` em methods; duas entradas nas linhas N.spec 8–9 | **NÃO REEXECUTADO** por falha do dispositivo |
| `complete/18/23` `noTransferEffectOnApproval` | `3c2ac679b19f75c7777d3221c858337529a4646a18bcb194bf6a812d64ba16c9` | ERC1155Mock | **Coordenador**, CLI 8.19.0, solc0.8.6, `--compilation_steps_only`, **EXIT 1**, exige `function` e `;` em methods; N.spec linhas 8–9 | **NÃO REEXECUTADO** por falha do dispositivo |
| `complete/18/4` `revokeRoleEffect` | SHA de recorte não reavaliado nesta rodada (SHA da spec global e caminhos na matriz) | AccessControlMock | **NOT_RUN**; sem parser CVL2 observado para este ID | **NÃO EXECUTADO** |
| `complete/18/46` `onlyHolderOrApprovedCanReduceBalance` | SHA de recorte não reavaliado nesta rodada | ERC1155BurnableMock | **NOT_RUN**; `method f` depende de selector-universe | **NÃO EXECUTADO** |
| `complete/18/53` `transferMethodsRevertWhenPaused` | SHA de recorte não reavaliado nesta rodada | ERC1155PausableMock | **NOT_RUN**; filtro dois selectors `sig:`, reverts e domínio `method f` | **NÃO EXECUTADO** |

Os dois **COMPILE_ERROR** de P18 são apenas observações do coordenador no documento P18_DIRECT_CLI_CONTRACHECK, não saídas reproduzidas pelo AGENTE-02. A trilha do coordenador contém hashes/cópias idênticos e comandos:

```text
certoraRun contracts/mocks/AccessControlMock.sol:AccessControlMock --verify AccessControlMock:specs/property.spec --compilation_steps_only --solc solc-0.8.6
certoraRun contracts/mocks/ERC1155Mock.sol:ERC1155Mock --verify ERC1155Mock:specs/property.spec --compilation_steps_only --solc solc-0.8.6
```

P18/3 e /23 **não** são `COMPILE_OK`, tampouco representam evidência de equivalência CVL1→CVL2. Os **nove preflights da Rodada 5** com `CERTORAKEY` são observações ambientais distintas; cinco incidiam nos N.spec e quatro nas specs globais. `PREFLIGHT_AUTH_BLOCKED` não é `COMPILE_ERROR`; nenhum dos nove foi contado novamente como compilação CVL. O estado individual atual e os resultados históricos intactos constam de `round6_diagnostic_matrix.csv`.

## Diagnóstico operacional efetivamente executado na Rodada 6

Verifiquei `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun` como executável e `certora-cli` **8.19.0** por consulta ao venv. Criei a worktree na HEAD `9350a3f9` e li os arquivos de entrada. Em seguida ocorreu falha de I/O no host, **anterior a qualquer cópia de source para o scratch e a qualquer compilação CVL2 desta rodada**:

```text
Desktop Commander write_file("/home/mat/cvl2-agente02-round6_probe.py")
  -> EROFS: read-only file system

$ printf ok >/tmp/cvl2-02-check && cat /tmp/cvl2-02-check
  -> ok
$ printf ok >/home/mat/cvl2-agente02-round6-check
  -> /bin/bash: ... Read-only file system

$ cp /home/mat/cvl2-agente02-round6/Web3Bugs-certora/results/spec/complete/18/3.spec /tmp/r6-3.spec
  -> Segmentation fault; cópia inexistente

$ cd /tmp; timeout --kill-after=2s 8s /home/mat/certora-ac-audit/certora_venv/bin/certoraRun --version
  -> Bus error; EXIT=135
```

A chamada `certoraRun --version` acima **não é um teste de spec**; `EXIT=135` é falha do processo do host, não parser CVL2. A tentativa inicial de executar Python escrevendo em `/tmp` também resultou em `Bus error`. Portanto seria incorreto produzir logs de compilação fictícios para /4, /46, /53 ou marcar `COMPILE_ERROR` na matriz. Nenhuma credencial/`.env` foi lida ou publicada. Os dados documentais foram publicados pela API de conteúdos do GitHub, usando exclusivamente `docs/cvl2/research/AGENTE-02/18/`, após constatação de que o host estava em somente leitura.

## ABI, semântica e famílias a avançar

As quatro ABIs do snapshot **já compiladas em Rodada 5** com `solc 0.8.6` (AccessControlMock, ERC1155Mock, BurnableMock e PausableMock; closures 7/9/10/12; ABI funções 9/13/11/16) continuam evidência somente Solidity, não CVL2. Arquivo `round5_abi_extraction.csv` contém SHA e stdout originais. A revisão `source_comparison.csv` identificou **157 instâncias com ABSENT_AT_AUDITED_COMMIT** e **24 CONTENT_DIFFERS**, referindo-se a 12 fontes de spec ausentes e quatro divergentes no commit OpenZeppelin `109778c17c7020618ea4e035efb9f0f9b82d43ca`. A tabela da Rodada 6 guarda SHA-1 Git + SHA-256 da **spec global do snapshot para todas as 181 chaves**, e N.spec SHA-256 somente onde a Rodada 5 já o havia registrado, sem extrapolar SHA global para recorte N.spec.

| Rule-alvo ou família | Localização auditável | Impedimento semântico específico |
| --- | --- | --- |
| P18/3,4 AccessControlMock | `contracts/18/specs/AccessControl.spec:45–74`; `contracts/18/contracts/access/AccessControl.sol:84,144,159` | `grantRole`, `revokeRole` e `hasRole` são `public` Solidity; CVL2 separa rotas `internal` e `external`; ABIs não demonstram chamada interna/receiver original |
| P18/23 ERC1155Mock | `contracts/18/specs/ERC1155.spec:385–398`; `ERC1155.sol:110,117` | `safeTransferFrom`/getter públicos; target e call graph antigos não certificados |
| P18/46 Burnable | `ERC1155Burnable.spec:8–20`; `ERC1155Burnable.sol:15–25`; `ERC1155Mock.sol:36–42` | `Burnable.burn` exige owner/approval, enquanto `ERC1155Mock.burn` chama `_burn`; trocar targets altera comportamento; `method f` requer universo e não-vacuity |
| P18/53 Pausable | `ERC1155Pausable.spec:24–37`; `ERC1155PausableMock.sol:8–28`; `Pausable.sol:64` | Filtro dois selectors (`sig:` em CVL2), `paused()` público, `pause/unpause` externos, `@withrevert` e `lastReverted` devem permanecer |
| Timelock | `contracts/18/specs/TimelockController.spec:14,17`; `contracts/18/contracts/governance/TimelockController.sol:214–221` | Spec declara `schedule(...,bytes32,...)` enquanto Solidity exige `bytes calldata`; `_checkRole` tem `DISPATCHER(true)`; **não alterar assinatura, casts ou receiver sem provenance** |
| Governor | `contracts/18/specs/GovernorBase.spec:5,26–29` | `DISPATCHER(true)` em `getVotes`, `getPastVotes`, `getPastTotalSupply`; CVL1 versus CVL2 exige demonstrar scope/receiver; harness histórico não comprovado |
| Initializable | `contracts/18/specs/Initializable.spec:1–17` | 26 instâncias para cenas flat e multiple inheritance distintas, nenhum harness histórico identificado |
| ERC20/721 Votes e ERC1155Supply | `contracts/18/specs/{ERC20Votes,ERC721Votes,ERC1155Supply}.spec` | Getters e checkpoints patchados ou `exists_wrapper` ausentes; não inferir ABI histórica de classe homônima |

A mudança lexical `function` + `;` é documentada pela Certora, mas a anotação `internal/external`, receiver, tratamento de reverts, storage hooks e ghosts pode afetar o universo de contraexemplos. Não se fez variante sintática de scratch nem modificação de qualquer `require`, `assert`, cast, summary, hook ou ghost.

## Matriz R6 e próximos gates

O novo `round6_diagnostic_matrix.csv` preserva **181 chaves únicas**, 69 complete/112 incomplete, **50 DOCUMENTED_CANDIDATE puramente lexical** e 131 UNRESOLVED_CANDIDATE. Observações CVL2 (fontes explicitadas): 2 `COMPILE_ERROR` **do coordenador**, 179 `NOT_RUN`, 0 `COMPILE_OK`, 181 `SEMANTIC_UNRESOLVED`. O campo `round6_local_execution` marca todos como **não reexecutados neste host defeituoso**. Esta matriz não transforma os nove preflights R5 em `COMPILE_ERROR`.

**Gate dependente do coordenador:** restaurar WSL gravável e CLI executável sem `Bus error`; repetir /3, /23, /4, /46, /53 em scratch com originais byte-idênticos, `timeout 60s`, stdout/stderr/SHA e versões. Para promoção semântica, obter manifests da cena auditada: commit da spec, target/harness, flags, compilador, linkings, patch, call graph, scopes de summaries, conjunto `method f` e comparação de contraexemplos. Enquanto isso, manter PR Draft, zero implementação e zero migração completa.

**Estado: LARANJA para pesquisa, VERMELHO operacional para novas execuções locais. Nenhuma alegação de passagem no Prover.**

**AGENTE-02 — RODADA 6.**
