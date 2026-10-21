# AGENTE-02 — RODADA 5 / QUALIDADE CVL2 — análise de ABI e compile-only

Data: 2026-10-20. PR [#37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), branch `research/cvl2-agente-02`, baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; HEAD observada no início `2c32e08521a1a709cad9f86f4c9d2c7cb0954251`. Worktree isolada `/home/mat/cvl2-agente02-round5`. Nenhum original, resultado histórico, catálogo, rótulo, contracts ou N.spec modificado.

## Informação nova do coordenador e regra de prova

Lidas as revisões mais recentes dos PRs [#37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), [#36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36) e o painel [#47](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/47), fixado em `705641e9f8920da648c724ce4c3361f03b8ac821`. Os quatro documentos `spec_catalog.md`, `spec_catalog_workflow.md`, `spec_catalog_project_1.md`, `standard.md` foram relidos antes das mudanças. Documentação oficial: [Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html) e [Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html).

**157/181 exemplos têm `ABSENT_AT_AUDITED_COMMIT` e 24/181 `CONTENT_DIFFERS`** no campo `upstream_spec_identity` do registro anterior: a discrepância é **por instância catalogada**, não por contagem de arquivos de spec; os 16 arquivos originais têm 12 ausentes e quatro homônimos diferentes no commit `109778c`. A coincidência de blobs Solidity não comprova a identidade de specs, execução, summaries, método `f`, targets, flags ou ABI histórica.

A linha `COMPILE_OK` deve significar **CVL2 + target exatos realmente compilados com Certora**, e não apenas compilação Solidity `solc`. `SEMANTIC_PROVEN` requer comparação fundamentada do universo de contraexemplos; `MIGRATED_COMPLETE` requer conclusão de todas as propriedades, inexistente.

## Snapshot ABI real, somente em scratch

A árvore `contracts/18/contracts` foi copiada byte a byte para `/home/mat/cvl2-agente02-round5-scratch/snapshot-contracts`; cada root Solidity SHA-256 foi comparado com a origem no dataset. O `solc` invocado foi o binário **0.8.6+commit.11564f7e** via caminho de versão fixada, **sem alterar a seleção global**. Usou `--standard-json`, closure recursiva de imports relativos, sem placeholders, remappings, patch nem mock novo, `optimizer.enabled=false`. Entrada JSON tem SHA-256 registrado no CSV; saída integral preservada em GZIP e stderr textual por target, com SHA-256 do stdout *descomprimido*. Os erros das tentativas preliminares de preparar argumentos solc (`--include-path` não reconhecido, depois imports não encontrados) foram de configuração da invocação e não são `COMPILE_ERROR` CVL. A extração final usou Standard JSON e terminou sem erro Solidity nos quatro targets.

| Target exato | Exemplos | Imports no closure, inclusive root | Funções ABI compiladas | solc |
|---|---|---:|---:|---|
| `AccessControlMock` | complete/3, /4 | 7 | 9 | Exit 0 |
| `ERC1155Mock` | complete/23 | 9 | 13 | Exit 0 |
| `ERC1155BurnableMock` | complete/46 | 10 | 11 | Exit 0 |
| `ERC1155PausableMock` | complete/53 | 12 | 16 | Exit 0 |

As quatro ABIs também cobrem estruturalmente os targets das **50** candidaturas lexicais (2 AccessControl, 34 ERC1155Mock, 6 Burnable, 8 Pausable), mas **não demonstram que as 50 rules foram compiladas em CVL2**. CSV `round5_abi_extraction.csv` preserva as assinaturas canônicas, selectors, Git blob dos roots, hashes de closure/entrada/ABI, caminho/versão do compiler, comandos e logs integrais.

## Cinco pares originais: fontes, argumentos e risco semântico

| Exemplo | Fonte da rule e métodos no snapshot | ABI confirmada por solc 0.8.6 | Semântica ainda pendente |
|---|---|---|---|
| **complete/18/3** `grantRoleEffect` | `contracts/18/specs/AccessControl.spec:45–57`; `contracts/18/contracts/access/AccessControl.sol:84,144` | `grantRole(bytes32,address)`, `hasRole(bytes32,address)` | Ambos `public` Solidity: wrapper externo e corpo interno são métodos diferentes para CVL2; rule chama diretamente as funções, mas o runner histórico não está vinculado |
| **complete/18/4** `revokeRoleEffect` | `AccessControl.spec:62–74`; `AccessControl.sol:84,159` | `revokeRole(bytes32,address)`, `hasRole(bytes32,address)` | Mesmo dual-path, sem licença para escolher `internal` ou receiver via nome |
| **complete/18/23** `noTransferEffectOnApproval` | `ERC1155.spec:385–398`; `ERC1155.sol:110,117`; `ERC1155Mock.sol:7–12` | `safeTransferFrom(address,address,uint256,uint256,bytes)`, `isApprovedForAll(address,address)` | `safeTransferFrom` público e `isApprovedForAll` público; ABI externa existe, mas call-resolution e exact target/job continuam incertos |
| **complete/18/46** `onlyHolderOrApprovedCanReduceBalance` | `ERC1155Burnable.spec:8–20`; `ERC1155Burnable.sol:15–25`; `ERC1155BurnableMock.sol:7–18` | `balanceOf(address,uint256)`, `isApprovedForAll(address,address)`, `burn(address,uint256,uint256)` | Rule quantifica `method f`, universo depende da ABI exata. Burnable impõe autenticação em `burn`; `ERC1155Mock.sol:36–42` chama `_burn` sem essa guarda, logo **não são targets intercambiáveis** |
| **complete/18/53** `transferMethodsRevertWhenPaused` | `ERC1155Pausable.spec:24–37`; `ERC1155PausableMock.sol:8–28`; `Pausable.sol:64` | `paused()`, `safeTransferFrom(...,bytes)`, `safeBatchTransferFrom(...,bytes)` | Dois selectors tipados no filtro, ambos exigiriam `sig:` em CVL2; `pause/unpause` são `external`, `paused` é `public`; preservar universo de `f` e `lastReverted` |

Para cada N.spec foram conferidos bytes/SHA-256 entre `results/spec/complete/18/N.spec` e cópia scratch. As specs globais originais foram copiadas separadamente com mesmo hash. A **global tem métodos/rules adicionais** (AccessControl e ERC1155) e o `N.spec` uma closure recortada; não se pode extrapolar eventual compilação de N para a spec global ou vice-versa. O `method f` de Burnable/Pausable inclui métodos ABI que não precisam aparecer como declaração explícita no `methods` extraído.

## Diagnósticos Certora CVL2 — invocações reais, mas parser não alcançado

Foram efetuadas **nove invocações** com `timeout 45s certoraRun <scratch Solidity> --verify Target:<scratch spec> --solc <solc 0.8.6> --compilation_steps_only`: **cinco N.spec originais (3,4,23,46,53) e quatro specs globais distintas**. Por segurança, o ambiente passado ao processo não continha `CERTORAKEY` nem tokens; nenhuma credencial foi lida ou publicada.

**Todas as nove retornaram exit 1 antes do parser**, com mensagem do guard local de `CERTORAKEY` ausente. Isto registra nove **preflight attempts**, não nove compilações CVL. Todos os stdout/stderr completos, SHA-256 e comandos estão em `round5_logs/` e `round5_cvl_compile_attempts.csv`. Resultado fiel: **0 `COMPILE_OK`, 0 `COMPILE_ERROR` do parser, 0 `SEMANTIC_PROVEN`**. Não usar o rótulo `COMPILE_ERROR` para falha de autenticação ou ausência de ambiente. Não foi invocado Prover formal nem CVL1.

## Casos restantes: bloquear com causa, não parar no ERC1155

- **ERC20Votes/ERC20Wrapper/ERC721Votes:** getters de checkpoints, `_delegate`, `_recover`, wrappers e patches históricos; o nome de função não certifica exposição de ABI pós-munging.
- **Governor:** `GovernorBase.spec:5,26–29` usa `ERC20VotesHarness` e summaries `DISPATCHER(true)` para `getVotes`, `getPastTotalSupply`, `getPastVotes`. Em CVL2 o summary por padrão só atinge um receiver, enquanto CVL1 aplicava aos homônimos em múltiplos contratos; `_` expandiria de modo diferente sem prova de call graph. GovernorPreventLateQuorumHarness segue sem proveniência suficiente.
- **Initializable:** 26 instâncias distintas por dois targets flat/multinheritance, mas mesmos métodos CVL em `Initializable.spec:1–17`; sem artefatos dos dois harnesses, compilar um contrato homônimo diferente não preserva semântica.
- **Timelock:** `TimelockController.spec:14` define `schedule(address,uint256,bytes32,bytes32,bytes32,uint256)` contra `contracts/governance/TimelockController.sol:214–221`, cujo terceiro argumento é `bytes calldata`. `_checkRole(bytes32) => DISPATCHER(true)` na linha 17 também exige receiver/scope identificado. Nenhum cast ou correção de assinatura foi introduzido.
- **ERC1155Supply:** `exists_wrapper` depende de harness não comprovado; compilar `ERC1155Supply.sol` isoladamente não prova a ABI dessa wrapper.

## Matriz auditável e política de próximo gate

`round5_diagnostic_matrix.csv`: **181** IDs/keys únicos, 69 complete e 112 incomplete, 157 `ABSENT_AT_AUDITED_COMMIT`, 24 `CONTENT_DIFFERS`; **50 `DOCUMENTED_CANDIDATE` com `NOT_RUN`**, **131 `BLOCKED`**, **181 `SEMANTIC_UNRESOLVED`**. São colunas separadas para ABI `solc`, gate CVL, status semântico, evidência e próximo passo. Cinco P0 experimentais tiveram ABI externa do target confirmada no snapshot. As outras 45 lexicalmente candidatas compartilham os mesmos quatro targets compilados, mas continuam sem diagnóstico CVL. No restante das 131, a closure/harness do runner falta ou a spec diverge.

**Solicitação específica ao coordenador:** prover meio autorizado de executar `--compilation_steps_only` sem bloqueio pré-parser de autenticação, e sobretudo manifests por job associando **spec SHA, target/harness, solc, import closure, patch SHA e aplicação com fuzz=0, ABI compilada, linkings, call-resolution e summaries/receivers** à cena histórica. Só então avaliar um par por vez, eventualmente autorizando specs candidatas derivadas *em scratch* mediante diff semântico supervisionado. Compilação bem-sucedida sozinha não aprova equivalência.

**Decisão: 🟠 LARANJA — ABI do snapshot confirmada em 4 targets, sem execução CVL2 compilada e sem prova semântica. Pesquisa DRAFT, sem merge.**

**AGENTE-02 — RODADA 5 — QUALIDADE CVL2.**
