# AGENTE-07 — Rodada 5 / relatório técnico CVL2

Baseline imutável: 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; PropertyGPT 687f654c679ed45ab127b7949e2a29c8f5e491b9. HEAD de partida 96257f027dddefdbc231dd136416020535ad0ecb.

Pesquisa e QA realizados em worktree isolado /home/mat/cvl2-agent07-round5-20261020. Diagnósticos e toolchain externos só em /home/mat/cvl2-agent07-round5-scratch; originais imutáveis.

**Cobertura:** ROUND5_MATRIX_156.csv contém 156/156 chaves individuais: P9 61, P8 42, P20 37, P11 16; 156 hashes N.spec verificados. Buckets mantidos: 50 DOCUMENTED_CANDIDATE (somente P9) e 106 UNRESOLVED_CANDIDATE. Zero COMPILE_OK CVL2, zero SEMANTIC_PROVEN, zero MIGRATED_COMPLETE. Não foi executado certoraRun --compilation_steps_only, Prover ou CVL1: nenhum candidato reuniu cena histórica, target, ABI e configuração comprovados. A compilação Solidity pura abaixo é um diagnóstico de ABI e não CVL2.

## P8 — 22/22 W1, 1/1 W2/W3 e 19 outros

Revisão independente do documento docs/cvl2/coordination/P8_AXIOM_CONSISTENCY_REVIEW.md do PR #47 HEAD 705641e9f8920da648c724ce4c3361f03b8ac821. Leitura textual integral de todos os 22 arquivos N.spec (IDs 14–35) com SHA-256 original e verificação de que ambas as condições estão no mesmo bloco ghost rayMul_g. 22/22 positivos; resultado e linha concreta individuais em ROUND5_P8_AXIOM_42.csv.

- W1 IDs 14–35: para x=1 e y=0, a condição universal força rayMul_g(1,0)=0 e rayMul_g(1,0)>=1. Contradição de aritmética inteira usual, independente de Solidity. Fontes: contracts/8/specs/fees_LEQ_ATokenBal.spec:26–33; lastVaultBal_LEQ_ATokenBalThis.spec:20–27; positiveSupply_imply_positiveAssets.spec:29–36 e os N.spec extraídos.
- W2 ID 1: contracts/8/specs/accrueYieldCheck.spec:11–21, em x=y=denominator=0, rounding=1, a desigualdade estrita exige 0<0.
- W3 ID 1: accrueYieldCheck.spec:29–31, em x=y=0, o termo 0/2 é definido mas o axioma exige 0<0.
- Outros 19 IDs: não identificadas *essas* contradições específicas; nenhum certificado de modelo satisfatível.

Isso é inconsistência na fórmula do modelo CVL extraído, NÃO prova de vacuidade na execução histórica do Prover. Sem mudar require/assert/ghost/hook, retirar axiomas, inserir guard de denominador, executar Prover ou prova de satisfatibilidade Certora sem gate formal do coordenador. **ALERTA VERMELHO — P8 axiomas.**

## P9 — ABI efetiva e contraste phase2/snapshot, IDs 1–7

Phase 2 Accounts original de celo-org/celo-monorepo@a46ce55ebd3867fa69290bf3be040846d433525d, caminho packages/protocol/contracts/common/Accounts.sol, Git blob SHA-1 5605111fb14c0be21f22ea9dd6980b2d75ad2127, SHA256 84defa1cb859957cb8bb435ab21ea01820c6d9676923245c5559f64e8a87d12f. A fonte compilada em scratch foi confirmada por hash. solc-js 0.5.13+commit.5b0b510c (soljson SHA256 89b634fb1c6010ea3c45fe9fc2365601c3d38289ecc7ae02807a0433bc198ba1); openzeppelin-solidity 2.5.0 usado como candidato, **NÃO atestado como tarball exato da auditoria**. Standard-json com 24 fontes recursivas: exit 0, erros zero, 53 ABI entries (40 funções). Input SHA256 58d199e1ba3eb1150ac6ed9462926e706876eb4144c02cd8de8ae85e9ea07261. ABI e log JSON publicados em ROUND5_P9_PHASE2_ACCOUNTS_ABI.json.

Tentativa distinta de compilar AccountsHarness do snapshot com mesmo solc: três ParserErrors devido a imports ausentes de lib/mento-core/contracts/interfaces/IExchange.sol, IReserve.sol e IStableToken.sol, em contracts/9/contracts/common/UsingRegistry.sol:20–22. Nenhuma ABI do harness foi produzida. Erros completos: ROUND5_P9_SNAPSHOT_SOLC_ERRORS.json. NÃO preencher essas dependências com stubs.

| ID | Resultado concreto do ABI phase2 | Bloqueio residual |
|---|---|---|
| 1 | isAccount e getWalletAddress disponíveis | _getAttestationSigner, _getVoteSigner e _getValidatorSigner só no source do harness snapshot; ABI não recompilada |
| 2 | isAccount disponível | _getAuthorizedBy só no harness snapshot |
| 3 | isAccount disponível | _getAuthorizedBy e três helpers de signer só no harness |
| 4 | isAccount disponível | _getDefaultSigner e _getAuthorizedBy só no harness |
| 5 | authorizeVoteSigner e authorizeValidatorSigner constam de ABI; isAccount consta | _getAuthorizedBy e runner/semântica histórica pendentes |
| 6 | authorizeSignerWithSignature **AUSENTE** na ABI compilada phase2 | Chamada literal não pode ser vinculada automaticamente à phase2 |
| 7 | Função _getAuthorizedBy só no harness snapshot | ABI e universo de method f pendentes |

Ver ROUND5_P9_ACCOUNTS_ABI_1_7.csv: assinaturas, presença em phase2, existência apenas textual no harness, SHA original e linhas. A fase 1 histórica não contém Accounts ou LockedGold na árvore recursiva verificada anteriormente; não inferir getters públicos não compilados, contratos de outra fase, summaries ou receiver. O contrato base compilado NÃO representa AccountsHarness históricamente executado. **ALERTA LARANJA — P9 ABI.**

## P20 — hash do source auditado contra scratch patch

A Rodada 4 reproduziu applyHarnesses.sh somente em scratch (exit 0, 5 Solidity modificados entre 58). Nesta rodada cinco arquivos foram comparados com fontes upstream por SHA-256. Tabela ROUND5_P20_PATCH_SHA.csv.

- BentoBox.sol no snapshot antes do patch: 44b11475772f14d021551aa3160b91b4593e2185bea6c1f0320c58dac27e889b; upstream bentobox@0c68f2aa38cd600b5959197416fe090baa6a2a3f: 3df36160d3aaab5f5f328fb3fc2c426b702682d4a92340e6a2f64e0db496d669; scratch pós-patch: 52147b23189da42eaef195910e0bcef4c411cca1846cd97ae1eac7fbdb4c8037. **Três versões distintas.**
- CompoundStrategy.sol em contracts/strategies/ não foi localizado no commit de BentoBox consultado (HTTP 404). É negativa para aquele caminho/commit, NÃO prova de irrecuperabilidade geral.
- Três bibliotecas BoringSolidity antes do patch (BoringBatchable, BoringFactory, IERC20) tiveram SHA igual ao commit pinado 39fdd3b4c78be0380edc95fde98d198f4bac5b41; hashes após patch são diferentes.
- compoundStrategyAdditional.spec:65 chama MAX_INT sem definição local/import comprovado; definição existe APENAS nos siblings compoundStrategy.spec:60 e strategy.spec:43. Não importar ou definir por intuição.
- Patch altera try/catch, interfaces, virtualização e calls: sem autenticação da cena/runner e ABI, nenhum compile-only. **ALERTA LARANJA — P20.**

## P11 — verificação transitiva repetida

Reexecutado o script de import closure com versões travadas no lock keep-ecdsa@a5cd1713621d94868765d1570fae373f4a497521: 6/6 archives tiveram SRI SHA-512 verificado, incluindo OpenZeppelin 2.3.0 e 2.4.0 nested, @openzeppelin/contracts 2.5.1 e @openzeppelin/upgrades 2.7.2. 45 Solidity locais, 104 nós alcançados e 204 imports, **zero paths ausentes**. Isso fecha a closure TEXTUAL daquele lock, não o compilador nem a auditoria original com SHA 658b02f237e25c370feaba80a7a3b13824190c4, ainda sem reconciliação. **ALERTA AMARELO para import textual, LARANJA para migração.**

## Fontes documentadas por ocorrência

| Ocorrência | Fonte e linha | Evidência |
|---|---|---|
| W1 / P8 14–35 | P8 specs fees_LEQ_ATokenBal:26–33; lastVaultBal_LEQ_ATokenBalThis:20–27; positiveSupply_imply_positiveAssets:29–36 | ROUND5_P8_AXIOM_42.csv (linha de cada N.spec) |
| W2/W3 / P8 1 | accrueYieldCheck.spec:11–21, 29–31; N.spec:24–45 | ROUND5_P8_AXIOM_42.csv |
| P9 Accounts phase2 | packages/protocol/contracts/common/Accounts.sol@a46ce55 / Git blob 5605111 | ROUND5_P9_PHASE2_ACCOUNTS_ABI.json |
| P9 AccountsHarness | contracts/9/specs/harnesses/AccountsHarness.sol:5–57; UsingRegistry.sol:20–22 | ROUND5_P9_ACCOUNTS_ABI_1_7.csv, ROUND5_P9_SNAPSHOT_SOLC_ERRORS.json |
| P20 patch, MAX_INT | contracts/20/spec/scripts/applyHarnesses.sh; compoundStrategyAdditional.spec:65; compoundStrategy.spec:60; strategy.spec:43 | ROUND5_P20_PATCH_SHA.csv |
| P11 packages | keep-ecdsa/solidity/package-lock.json@a5cd171, contracts/11/**/*.sol | ROUND4_EVIDENCE.md e rerun desta rodada |
| CVL2 migração | https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html | Não adotar conversão automática; internal/external, receiver/summary, cast e revert requerem prova de equivalência |

**Gate humano:** versionar modelo e sanity W1/W2/W3, obter logs originais/ABI/harness Celo e import mento-core, confirmar fonte de BentoBox e MAX_INT; atestar commit/auditor run Keep. **Sem Prover, CVL1, CVL2 compile, equivalência ou migração concluída.**

AGENTE-07 — RODADA 5 — QUALIDADE CVL2
