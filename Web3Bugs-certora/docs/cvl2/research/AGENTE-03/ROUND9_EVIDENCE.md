# AGENTE-03 — RODADA 9 / Evidências P24 Rocket Joe

**PR:** [#36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36), branch research/cvl2-agente-03, Draft. **Baseline histórica:** 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. **HEAD inicial:** cfaf119579ec3c1718bcd32b6e637c03ea4cd174. **Escopo:** P24, 164 exemplos incomplete, nenhuma propriedade migrada.

**Resultado da R9:** UM diagnóstico de aplicação de patch Solidity, classificado estritamente como **FORK_ONLY**, com dry-run fuzz=0 **exit 0** e aplicação em cópia temporária fuzz=0 **exit 0**. **Zero compilações Solidity solc, zero Certora CVL2, zero Prover, zero CVL1, zero equivalências demonstradas.** O patch é cenário de source, não execução por property.

## 1. Proveniência com commits e hashes — três cenas distintas

| Cena e objeto | Commit/blob ou SHA256 | Evidência verificável | Limite |
| --- | --- | --- | --- |
| **AUDITED** LaunchEvent.sol | lfj-gg/rocket-joe@ef2ef30248661b5509c52ab30af9bd0fc07f6657, contracts/LaunchEvent.sol, Git blob 2af4cfe5472decc22ab3dd361d0117893a61539e, L599 e L673–679 | L675 guarda balance >= avaxReserve; L599 retorna tokenIncentiveIssuerRefund quando pair == 0 | Não fornece harness/runner/ABI da execução do PDF |
| **FORK_ONLY** LaunchEvent.sol | Certora/rocket-joe-1@dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10, contracts/LaunchEvent.sol, Git blob 2656eb863a83ca2a53714eb0ed336f420f952dae, SHA256 1c70e9642a1e392d48ec4e54aa3ba591e678f26d60ac4580dfae0cd0b579bf7f | L675 guarda balance - _value >= avaxReserve; L599 retorna 0 | Fork posterior não representa source auditado |
| Patch **do fork** | certora/applyHarness.patch, blob abfb1eae851307c9a3e7d17a7b3e913962952845, SHA256 e06f5a9d5503e82310ffccfab55214b9cb847d2146656f2558271e0777e27fdb, L96–104 | Hunk 7 acrescenta virtual à assinatura interna e preserva expressamente a guarda subtrativa do fork | Não encaixa strict fuzz0 em híbrido auditado (evidência R4, não reexecutada R9) |
| Harness **do fork** | certora/harness/LaunchEventHarness.sol L114–116, blob 1b6a42c5e397d03c921d18217364c7e67878621a | Override substitui corpo com IReceiver(_to).receiveETH{value: _value}() | Não é harness comprovadamente usado no PDF |
| R9 scratch LaunchEvent.sol pós-patch | SHA256 e74bc68f15e5fb9a40974a8a723ded121dd0b68e7273cd0daf1672d1cf984d24 | L673 virtual internal; L675 guarda do fork mantida | Alterado **somente na cópia temporária**, não implementa CVL2 |
| R9 scratch RocketJoeStaking.sol pós-patch | SHA256 af436d7d252e77224165211863d37160db0adf18484726fb46fe91492628e077 | Aplicação textual do patch do fork | ABI/semântica de auditoria não foi compilada nem provada |

**Links de source:** [audited LaunchEvent L673–679](https://github.com/lfj-gg/rocket-joe/blob/ef2ef30248661b5509c52ab30af9bd0fc07f6657/contracts/LaunchEvent.sol#L673-L679); [fork LaunchEvent](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/contracts/LaunchEvent.sol#L673-L679); [patch Hunk 7](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/applyHarness.patch#L96-L104); [override](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/harness/LaunchEventHarness.sol#L114-L116).

### Diagnóstico novo executado R9 — somente scratch

O preflight no WSL DESKTOP-5E26TVU passou: Python 3.14.4, git 2.53.0, filesystem legível, checkout P24 R9 limpo na HEAD inicial. Fork source dba90f9 e limpo (git status --porcelain vazio). Scratch exclusivo: /home/mat/cvl2-agente03-round9-scratch/scene; **não usar nem referenciar este caminho como runner histórico**.

1. Copiado **apenas** o diretório contracts do fork para scratch com cp -a, e cmp LaunchEvent.sol original x scratch retornou exit 0; SHA256 dos dois arquivos idêntico 1c70e9642a1e392d48ec4e54aa3ba591e678f26d60ac4580dfae0cd0b579bf7f.
2. Na raiz scratch/scene: comando executado **patch --dry-run --batch --fuzz=0 -p0 < certora/applyHarness.patch** com stdout/stderr no arquivo ROUND9_PATCH_FUZZ0_DRYRUN.log: **exit 0**.
3. Na mesma raiz scratch/scene: comando executado **patch --batch --fuzz=0 -p0 < certora/applyHarness.patch** com stdout/stderr no ROUND9_PATCH_FUZZ0_APPLY.log: **exit 0**.
4. Ambos os logs contêm 23 linhas de arquivos processados, **zero ocorrências** de fuzz, offset, FAILED ou rejeição na busca estática. SHA256 do pós-patch LaunchEvent e Staking acima; fork versionado permaneceu com git status --porcelain vazio. Não se rodou script histórico in-place, Makefile, solc nem certoraRun.

**Comparação semântica:** para inteiros uint256 b=balance, r=reserve, v=value, guarda auditada b>=r versus guarda fork b-v>=r, com subtração checked. No domínio onde a subtração do fork é definida e B é verdadeira, B implica A; A não implica B (b=100,r=80,v=30). O override do harness nem necessariamente executa a guarda base. Esta é uma **diferença real de source**, não um contraexemplo alcançável formalmente e tampouco replay do relatório.

## 2. Lock OpenZeppelin autenticado na R9, sem substituir pacotes entre cenas

| Pacote | Commit/lock e linha | Versão | SHA256 do tarball | Verificação desta rodada |
| --- | --- | --- | --- | --- |
| @openzeppelin/contracts | fork dba90f9:yarn.lock L677, blob 2e5fe995f869eb0f386229a55ef5ef4765d00ccb | 4.4.2 | f0f5e4bd0cd7a9aa55c70bc815b80ea4c4b96af08ba4e184e95b86d4c83828d6 | SRI SHA512 do tarball R5 **MATCH** no lock do fork |
| @openzeppelin/contracts-upgradeable | fork dba90f9:yarn.lock L672 | 4.4.2 | b6ea889c4ebf697b584db6823035d90c72e3457d4aa4d6b8147ee7e84bbd6a89 | SRI SHA512 **MATCH** |
| Auditoria ef2ef302:yarn.lock, blob 49939a552262aef9fb0aab38f66b594011a99973 | Fonte histórica diferente | 4.4.1 | ver round5_oz_package_provenance.csv | Evidência R5, **não** reinterpretada como pacotes do fork ou runtime real |

A R9 recalculou localmente SHA512 contra duas cópias dos **tarballs 4.4.2 já recuperados na R5** e reconfirmou os locks; não baixou novos pacotes nem instalou nada na árvore versionada. Isso não prova qual node_modules a auditoria utilizou.

## 3. Propriedade individual candidata e closure

**P24/incomplete/164, sanity.** N.spec byte-original em results/spec/incomplete/24/164.spec (SHA256 **852ef92957b7d31e844ae41c7e7c4307056e2bb53d6446a4073c8846870070c9**, confirmado novamente na R9), 28 linhas com metadados/declarações CVL1, métodos e regra ativa; **import "../helpers/erc20.spec" ausente no snapshot**, disponível no fork em certora/helpers/erc20.spec (blob **b12fec167edd76a2f59a64bc80bc33a9eeb04f65**). Full CVL fork certora/spec/sanity.spec (Git blob **452a10f1268de27b5dd8e263cd27c5044c98daaf**, SHA256 **b1631a0289c2ac48030ef60c31b5cd3083b21141cb3636bc100ea9bb315c9f67**, 23 linhas). Ambos importam o helper. Byte-identidade **N.spec ≠ full-spec**; não promover status do recorte.

**Runner fork específico:** [certora/scripts/sanity.sh:L3–26](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/scripts/sanity.sh#L3-L26), blob **a3f398159145e62b757ecf234f3200295566d9f2**. Enumerados 10 roots Solidity, links LaunchEventHarness pair/factory/router/rJoe/rocketJoeFactory/WAVAX e RocketJoeFactory eventImplementation/rJoe; target **LaunchEventHarness:certora/spec/sanity.spec**, --solc_map (JoeLibrary/JoeRouter02/JoePair/JoeFactory solc6.12, demais solc8.6), --optimistic_loop e --method "depositAVAX()". A linha 1 chama make -C certora munged **in-place** — NÃO executada na R9. Resultado estático histórico R6: 10 roots, 47 fontes Solidity, 59 import edges, zero caminhos faltantes **na cena do fork patchada**; ainda faltam compilação solc e ABI efetiva, verificação de links/receivers e compatibilidade de filtro --method com o method f da regra.

**Decisão:** N164 é um candidato **DOCUMENTED_CANDIDATE_FORK_ONLY**, sem COMPILE_OK. Após gate nominal do coordenador, só então cópias de N164, helper e os roots do fork sob diretório temporário com SHA256/cmp, solc 0.8.6/0.6.12 identificados, direct CLI + timeout ~60s + --compilation_steps_only; manter todas as premissas/asserts/ghosts/hooks/summaries; não invocar script legado, Prover ou CVL1. Mesmo exit 0 não reproduziria o run do PDF. A regra usa assert false e método quantificado, com risco de vacuity.

## 4. Staking: progresso independente e blockers

**Audited** RocketJoeStaking.sol blob 6f970060b271826b98c70f58131211454c3682a6, [withdraw L137–149](https://github.com/lfj-gg/rocket-joe/blob/ef2ef30248661b5509c52ab30af9bd0fc07f6657/contracts/RocketJoeStaking.sol#L137-L149). Decrementa totalJoeStaked **depois** de user.rewardDebt e **depois** de _safeRJoeTransfer. **Fork** blob ae45dd7493c87c9451118c687e1ce77db8668bc3, [withdraw L137–150](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/contracts/RocketJoeStaking.sol#L137-L150), decrementa totalJoeStaked **antes** da atualização do rewardDebt e da chamada externa. O helper [L199–205](https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/contracts/RocketJoeStaking.sol#L199-L205) consulta saldo rJoe e chama IERC20Upgradeable(...).safeTransfer; logo há call externa potencial antes/depois do decremento. **Não** prova reentrância alcançável, exploit, ou diferença observada pelo Prover.

**Dois drivers contraditórios no mesmo fork:** verifyStaking.sh (blob c45f10b2694a08b337059fbad4b0d11e474b7c54, L15–25) verifica RocketJoeStakingHarness:certora/spec/Staking.spec, usa solc8.6, links joe/rJoe; stakingRule.sh (blob 766a9f0adc54ea447f80c14d70c0466b6c7bdae9, L11–27) verifica RocketJoeStaking:certora/spec/staking.spec, **path minúsculo ausente** no commit fixo. spec correta Staking.spec blob 2fd60f3d0e46ec0954abc0ebba31801bd01b5e17. Harness fork blob 367bbcae7952ea7ad8a016969a1b428184a4b15c herda munged RocketJoeStaking e introduz getters/construtor. Não renomear original nem assumir qual driver foi o auditado.

**LEVarTran Owner.sol:** verifyLEVarTran.sh (blob 5f71d4e2089bb1bfb78ec812a3458c3fecff71a8, L6) usa certora/harness/Owner.sol ausente na árvore do fork; OwnerA/OwnerB possuem blobs próprios e não são substitutos. Uma ausência em dba90f9 não prova inexistência universal. Famílias sem runner dedicado (LaunchEvent 76, LEPreset 1, LEInProgress 3) permanecem bloqueadas.

## 5. Contrarrevisão somente leitura PR #42 (AGENTE-04)

Revisadas a HEAD **06dca368f5f2324da45f156dd9bc206745f11af0** e suas publicações R8 sem modificar branch/arquivos desse agente:

- P12/complete/23 e /25: wrapper auditado protocol-v2@750920303e33b66bc29862ea3b85206dda9ce786 possui address user adicional, snapshot remove esse parâmetro; mesmo quando não usado no corpo, assinatura, selectors e domínio quantificado divergem. **COMPILE_ERROR CVL2 exit 1 históricos R5**, grammar methods, não reproduzidos nesta rodada.
- P15/incomplete/36: target do script realmente **GhoDiscountRateStrategyHarness**, não a target nominal; seis methods externos sustentados por ABI Solidity histórica, envfree ainda requer check. Patch GHO modifica GhoToken/IGhoToken/.gitignore, **não** strategy/harness dessa cena específica; não extrapolar para 115 exemplos. **COMPILE_ERROR CVL2 exit 1 histórico R6** de methods sem function/;, não reproduzido; proposta R8 lexical é **somente documental**.
- P2: latestRoundData pertence a feed externa Chainlink e deve preservar receiver, não currentContract por reflexo; não é assunto de implementação P24. Nenhuma alteração na branch PR #42.

## 6. Próximos experimentos para o coordenador — ordem

1. **P24/164 sanity — fork-only CVL2 compile-only condicional**, apenas se for comprovada ABI closure completa e autorizada execução do N.spec byte-original, com staging isolado, log/exit/timeouts e solc fixados. Não replay histórico.
2. **P24/Staking — comparação ABI/driver e efeitos de chamada externa somente em leitura**, até resolver identidade do runner/casing antes de propor teste individual CVL2. Owner.sol/LEVarTran é pesquisa histórica subsequente, não fabricar stub.

**Nenhum resultado VERIFIED/VIOLATED do PDF foi transportado ao snapshot, nenhum Bug Label ou Result/Detection Outcome alterado. Estado P24: 164 NOT_RUN, 0 COMPILE_OK, 0 COMPILE_ERROR, 0 SEMANTIC_PROVEN, 0 MIGRATED_COMPLETE.**

**AGENTE-03 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.**
