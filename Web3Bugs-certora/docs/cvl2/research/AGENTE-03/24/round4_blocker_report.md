# AGENTE-03 — Rodada 4 / Rocket Joe P24

**Decisão:** 164/164 permanecem incomplete e UNRESOLVED_CANDIDATE. Nenhum target tem, até agora, ABI auditada e fechamento completo das dependências para diagnóstico CVL2 compile-only. Nenhum original de contracts, results/spec, CSV de catálogo ou PDF foi alterado.

## Separação das três origens

- **Relatório Certora Rocket Joe**: resources/24/Certora_Formal_Verification_Report_Rocket_Joe.pdf, SHA256 f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4. Fonte auditada indicada: lfj-gg/rocket-joe@ef2ef30248661b5509c52ab30af9bd0fc07f6657. Documento atesta as premissas e resultados impressos, mas não os blobs de harnesses, ABI, CLI/Prover nem execução exata.
- **Fork histórico Certora**: Certora/rocket-joe-1@dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10, PR upstream #168 fechado sem merge. O fork preserva os scripts, patch, helpers, harnesses e oito specs; não se atribui automaticamente esses bytes à execução do relatório.
- **Snapshot PropertyGPT/Web3Bugs**: contracts/24/spec/*.spec do baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. Os oito Git blobs CVL são idênticos aos de certora/spec/*.spec no fork. Essa igualdade não estabelece target instrumentado nem resultado verificado.

### Hashes concretos e correspondências

| Artefato | Git blob auditado | Git blob fork | Relação |
| --- | --- | --- | --- |
| contracts/LaunchEvent.sol | 2af4cfe5472decc22ab3dd361d0117893a61539e | 2656eb863a83ca2a53714eb0ed336f420f952dae | Divergentes |
| contracts/RocketJoeStaking.sol | 6f970060b271826b98c70f58131211454c3682a6 | ae45dd7493c87c9451118c687e1ce77db8668bc3 | Divergentes |
| contracts/RocketJoeFactory.sol | Vide historical_artifact_provenance.csv | ba2edbb458da... | Identidade de bytes apenas |
| contracts/RocketJoeToken.sol | Vide historical_artifact_provenance.csv | 08c481fb3d3b... | Identidade de bytes apenas |

**Os seguintes blobs só foram identificados no fork e NÃO na árvore do commit auditado:** certora/helpers/erc20.spec = b12fec167edd76a2f59a64bc80bc33a9eeb04f65; certora/harness/LaunchEventHarness.sol = 1b6a42c5e397d03c921d18217364c7e67878621a; certora/harness/RocketJoeStakingHarness.sol = 367bbcae7952ea7ad8a016969a1b428184a4b15c; certora/helpers/DummyERC20A.sol = 1230df5b6ffe79aaff1be710dac8e5c4e41373a9; DummyERC20B.sol = c50f16f79c5baf136776da31ef75ae07bb6f18b1; DummyERC20Impl.sol = ee8731ee5deb50929de78471e127f95e5e0ec7c; DummyWeth.sol = 3c0c997b0921b702e16185ddb2fe73b890731b08. Outros caminhos e SHA estão na matriz historical_artifact_provenance.csv: **55 objetos; 50 ausentes na árvore auditada, 3 contratos diferentes, 2 idênticos; nenhuma linha prova o run**.

## Matriz individual e causas dominantes

O novo **round4_example_blocker_matrix.csv** tem **164 linhas**, cobrindo IDs 1–164, propriedade e spec de origem, SHA das oito specs, fechamento CVL transitivo com SHA de cada arquivo importado, runner script e hash, todos roots Solidity por script com hash quando presente, imports externos ausentes, hash de target auditado/fork e decisão do gate por item.

| Causa dominante | Specs | Exemplos | Bloqueio positivo/negativo |
| --- | --- | ---: | --- |
| SPEC_WITHOUT_RECOVERED_RUNNER | LaunchEvent e LEPreset | 77 | Spec idêntica ao fork; não há script histórico específico comprovado |
| NO_RUNNER_OR_IMPORT_PROVEN | LEInProgress | 3 | Não declara import CVL nem runner; não presumir helper por analogia |
| OZ_EXTERNAL_BYTES_AND_ABI | LEHighLevel, LEValidStates, sanity | 46 | Scripts/cadeias CVL encontrados; dez referências externas OpenZeppelin por script sem materialização de pacote e ABI |
| OWNER_SOL_ROOT_ABSENT | LEVarTran | 19 | Script cita certora/harness/Owner.sol, ausente; OwnerA/B não o substituem; mais dez imports externos |
| STAKING_TWO_RUNNERS_DIFFERENT_TARGETS | Staking | 19 | Scripts verifyStaking.sh e stakingRule.sh usam targets diferentes; último cita certora/spec/staking.spec com case inexistente; seis imports externos |
| **TOTAL** | 8 specs | **164** | 0 elegíveis à compilação |

As categorias são **dominantes**, não mutuamente exclusivas. As 164 carecem de execução histórica reconstituída e ABI auditada. O verifyAll.sh do fork enumera **45 regras específicas**: dez LEHighLevel e 35 LEValidStates; o fork possui scripts associados a 84 exemplos, mas existência de script não prova execução.

### CVL import closure recuperada no fork (sem presumir Solidity closure)

- LEHighLevel → LEValidStates → LEPreset → sanity → helpers/erc20.spec
- LEVarTran → LEValidStates → LEPreset → sanity → helpers/erc20.spec
- LEValidStates → LEPreset → sanity → helpers/erc20.spec
- LaunchEvent → sanity → helpers/erc20.spec
- LEPreset → sanity → helpers/erc20.spec
- Staking → helpers/erc20.spec; sanity → helpers/erc20.spec
- LEInProgress: nenhuma importação declarada.

Todos os arquivos CVL dessas cadeias são encontrados no fork, mas não resolvem bibliotecas Solidity externas nem assinaturas CVL2 de methods/receivers. historical_import_closure.csv contém **192 ocorrências** estáticas distribuídas por seis scripts, e historical_run_config_matrix.csv seus roots, solc e linkings. Nenhum script foi executado.

### Patch original em cópias descartáveis — novo teste estrito

Origem: certora/applyHarness.patch (2.732 linhas), blob abfb1eae851307c9a3e7d17a7b3e913962952845, SHA256 e06f5a9d5503e82310ffccfab55214b9cb847d2146656f2558271e0777e27fdb.

- Cena fork (contratos dba90f9): patch --dry-run --batch --fuzz=0 -p0 → **exit 0**; aplicação no scratch → **exit 0**.
- Cena híbrida auditada (substitui LaunchEvent.sol e RocketJoeStaking.sol por blobs de ef2ef302): mesmo comando com --fuzz=0 → **exit 1**, Hunk #7 FAILED at 670.
- Cena híbrida com fuzz padrão → **exit 0**, porém Hunk #7 succeeded at 670 with fuzz 2.

Essa diferença é incompatibilidade textual estrita. Aceitação permissiva não prova equivalência de ABI ou semântica. Log completo: round4_patch_scene.log. Árvore original do fork manteve git status --porcelain vazio.

### Fechamento ABI e versões: bloqueios não contornáveis por mocks

O yarn.lock auditado prende OpenZeppelin **4.4.1**, e o yarn.lock do fork prende **4.4.2**; o intervalo ^4.4.1 no package.json não torna os blobs intercambiáveis. Não foram recuperados os node_modules da execução, configurações .conf, outputs de compilação, ABI compilada vinculada ao commit auditado, toolchain de solc comprovada nem Prover/CLI históricos. A identificação dos imports e do patch não substitui essas provas.

Documentação oficial CVL2: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html. Especialmente a mudança de receivers de summaries e annotations internal/external, além de casts/mathint e DISPATCHER, impedem presumir preservação de contraexemplos por conversão superficial. Nenhum cast, require ou assert foi introduzido.

## Próximos candidatos (pesquisa, nunca autorização para migração)

1. sanity (1): menor alvo com script e helper legíveis; buscar ABI e pacote exatos.
2. LEHighLevel (10) e LEValidStates (35): runners explícitos em verifyAll.sh; reconstruir pacote e ABI conforme commit auditado.
3. Staking (19): distinguir as duas cadeias de target/runner e recuperar closure 4.4.1.
4. LEVarTran (19): buscar Owner.sol real por hash, sem substituir por OwnerA/B.
5. LaunchEvent/LEPreset/LEInProgress (80): recuperar runners específicos comprováveis antes de associar CLI.

**Decisão:** compile-only NÃO EXECUTADO por falta do gate target+ABI+closure; Prover NÃO executado; CVL1 NÃO executado; PR permanece DRAFT e sem merge.

**AGENTE-03 — RODADA 4.**
