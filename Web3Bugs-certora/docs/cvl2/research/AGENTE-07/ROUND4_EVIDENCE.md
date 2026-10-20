# AGENTE-07 — Rodada 4: evidências técnicas e gates de CVL2

> Documento de pesquisa; nenhum Prover, CVL1, compilação CVL2 ou migração aplicada. Baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; HEAD inicial 78800bb132f9a40d7db4d5ae3e3bbb99c2c884c8.

## Cobertura e significado dos estados

- `ROUND4_MATRIX.csv` tem **156/156** chaves únicas: P9 61, P8 42, P20 37, P11 16; hashes de N.spec 156/156 revalidados.
- Bucket preexistente: **50 DOCUMENTED_CANDIDATE** (P9) e **106 UNRESOLVED_CANDIDATE**. Nenhum `COMPILE_OK`; nenhum `SEMANTIC_SUPPORTED`.
- `round4_p9_names_missing_phase2_plus_snapshot_harness` é apenas um teste textual de NOMES de funções em Sources e Harness, NÃO um ABI checker (herança, getters públicos, overloads e bindings não cobertos).
- Candidatura documentada não é contrato historicamente atestado nem candidata pronta para compilação; Result do relatório não é certificação de não-vacuidade.

## P9 — Celo Governance / duas revisões históricas

- Árvores GitHub recursivas completas dos commits auditados: 9d2ec0d9399a6959565062f57efa037d03fd4fbc (2637 entradas, truncated=false), a46ce55ebd3867fa69290bf3be040846d433525d (4086, truncated=false).
- No commit de fase 1, `packages/protocol/contracts/common/Accounts.sol` e `.../governance/LockedGold.sol` NÃO aparecem em qualquer caminho de nome correspondente na árvore; aparecem na fase 2. Isso impede atribuir essas properties à fase 1. Não implica que o projeto ou a história do arquivo nunca existiram.
- `Governance.sol`: phase1 blob `79bf02035380a650f343df00042ded0578568bfe`; phase2 `641c834fa6bbf677aa8cc743890142c0cacce08d`; snapshot `633b7d2d23c665a11fa9afd98351236b5c9fe3f8`. Diferenças substanciais de funções de votação, hotfix e proposta; execução e ABI não são intercambiáveis.
- `Reserve.sol`: existe em ambas as fases, mas não em `contracts/9/contracts/stability/Reserve.sol` do snapshot; `ReserveHarness.sol` tenta importar exatamente esse caminho. ID 61 permanece unresolved.
- As 50 candidaturas P9 foram correlacionadas individualmente com source group, target, hashes disponíveis e nomes explícitos de métodos no `ROUND4_MATRIX.csv`. A presença lexical da assinatura NÃO demonstra função ABI, getters autogerados, reversões ou receiver/summary aplicados; todos retêm ABI histórica **NOT_DEMONSTRATED**.
- Subgrupo de triagem documental mais simples para investigação *futura*: Accounts IDs 1–7; em todos os nomes de métodos declarados na extração há correspondência nominal no Accounts.sol fase 2 e/ou AccountsHarness snapshot. Ainda faltam ABI tipada, runner, constructor, inheritance closure, fase atribuída à rule e integridade da configuração. **Sem promoção ou compilação.**
- Governança e LockedGold usam harnesses locais cuja correspondência byte a byte com a fase auditada não foi comprovada. `applyHarness.sh` altera `Governance.sol`, `FixidityLib.sol` e `Proposals.sol`; por isso raw source de fase 1/2 não é cena compilada da prova.

## P8 — W1/W2/W3 e vacuidade

- **W1**: 22 instâncias (IDs 14–35), axioma universal `rayMul_g(1,0)=0` combinado com limite inferior `rayMul_g(1,0)>=1`. Inconsistência independente do Solidity.
- **W2/W3**: ID 1 com `mulDiv` e `rayDiv` universais sem proteção contra denominador zero; valoração zero força desigualdade estrita `0 < 0`.
- As demais 19 instâncias não incluem essas contradições específicas; isso não prova satisfatibilidade do modelo, segurança ou prova não vacuosa.
- Não modificados axiomas, `require`, `assert`, ghosts ou statements. A cobertura é texto extraído, não reconstrução de flags/harness do Prover original.

## P20 — BentoBox / aplicação isolada de patches

- Commit BoringSolidity travado em yarn.lock: `39fdd3b4c78be0380edc95fde98d198f4bac5b41`. Seis fontes base recuperadas de fork conservando o mesmo Git commit; nenhuma troca por biblioteca contemporânea.
- `bash spec/scripts/applyHarnesses.sh` executado **somente** sobre scratch `/home/mat/cvl2-agent07-round4-evidence/p20_replay`, com 58 arquivos Solidity incluindo 6 arquivos importados; **exit 0**, stderr vazio.
- Exatamente 5 arquivos Solidity sofreram mudanças: `contracts/BentoBox.sol`, `contracts/strategies/CompoundStrategy.sol`, `node_modules/@boringcrypto/boring-solidity/contracts/BoringBatchable.sol`, `.../BoringFactory.sol`, `.../interfaces/IERC20.sol`.
- Implicações: renomeação safeTransfer, alterações virtual, troca try/catch por chamada direta, redirecionamento `to.call` para `Nothing.nop` e duas declarações extras de transferência em interface modificam a cena e comportamentos. Reproduzir patches ≠ compilação/identidade do modelo da auditoria.
- `compoundStrategyAdditional.spec:65` chama `MAX_INT()` sem defini-lo nessa unidade; a definição em `compoundStrategy.spec:60` e `strategy.spec:43` é de arquivos irmãos, sem mecanismo de import comprovado.

### SHA-256 dos cinco arquivos afetados em scratch

- `contracts/BentoBox.sol`: antes `44b11475772f14d021551aa3160b91b4593e2185bea6c1f0320c58dac27e889b`; depois `52147b23189da42eaef195910e0bcef4c411cca1846cd97ae1eac7fbdb4c8037`.
- `contracts/strategies/CompoundStrategy.sol`: antes `deb2c4e0fd3abfafed8d266e2a5b4808c13418c2b6697e64f3b2fbe21e5686fe`; depois `f094092781de2d8489f50bcda5c5f2bc2fa03fab0ae2258f86f70b69002a0303`.
- `node_modules/@boringcrypto/boring-solidity/contracts/BoringBatchable.sol`: antes `50e7f052569a27ad2d8edb0a8dd8995c078446b98a1804233326e8701d42016a`; depois `e58d7894bf9ad1ba03fbd5d5f6eae99788dc3fa4b756805f90573a57e9915ee8`.
- `node_modules/@boringcrypto/boring-solidity/contracts/BoringFactory.sol`: antes `9626b37e827528cba6ac7d5b9e298824cead5868440b7bfe76da683909f0aed9`; depois `746571a0ae9b64d94dff35e7476b2431a500de388a6bd3b139fe6ba627e9f981`.
- `node_modules/@boringcrypto/boring-solidity/contracts/interfaces/IERC20.sol`: antes `19c258f65935f39a0aca7086414331699d0da313c2dbb7f019a04046c33ffcbd`; depois `bc44a916c8e924e6723aaccbaa8e4ba2ad470947463b008324c280d9c546dd39`.

## P11 — Keep ECDSA / import closure do lock histórico

- `keep-ecdsa@a5cd1713621d94868765d1570fae373f4a497521/solidity/package-lock.json` (não confundido com SHA auditada `658b02f237e25c370feaba80a7a3b13824190c4`).
- Download histórico de **6 arquivos tgz** (6/6 SRI SHA-512 coincidentes com lock): `@keep-network/keep-core@1.5.0-pre.0`, `@keep-network/sortition-pools@1.2.0-pre.3`, `openzeppelin-solidity@2.3.0`, `@openzeppelin/contracts@2.5.1`, `@openzeppelin/upgrades@2.7.2`, e `openzeppelin-solidity@2.4.0` aninhado sob keep-core.
- Análise de `import` Solidity por resolução relativa e de pacote (preservando versão nested): 45 arquivos Solidity locais, **104 nós alcançados / 204 imports percorridos / 0 paths ausentes**, incluindo versões distintas OZ.
- Resultado = **textual transitive import closure da árvore catalogada**. Não demonstra compilação Solidity com solc histórico, compiler remapping/ABI completa, links, bibliotecas geradas ou equivalência com o commit da auditoria não localizado. Sem promoção das 16 properties.

## Fontes oficiais e upstream

- CVL2 migration: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html
- CVL2 changes: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html
- Celo phase1: https://github.com/celo-org/celo-monorepo/commit/9d2ec0d9399a6959565062f57efa037d03fd4fbc
- Celo phase2: https://github.com/celo-org/celo-monorepo/commit/a46ce55ebd3867fa69290bf3be040846d433525d
- BoringSolidity historical fork commit: https://github.com/bartjellema/BoringSolidity/tree/39fdd3b4c78be0380edc95fde98d198f4bac5b41
- Keep historical lock: https://github.com/keep-network/keep-ecdsa/blob/a5cd1713621d94868765d1570fae373f4a497521/solidity/package-lock.json

## Gate

**Sem CVL1, Prover, recompilação CVL2, merge ou modificação de `contracts/`, `results/`, `reports/`, `resources/`.** Sem candidatos com simultânea prova de contrato auditado, import closure compilada, runner histórico e identidade de ABI/receiver; portanto `--compilation_steps_only` não foi executado: nenhuma afirmação COMPILE_OK sem ambiente completo. Próximo: obter artefatos do runner/solc, hashes da árvore efetiva e relação report→fase (P9), cena e flags de execução (P8), replay do runner de BentoBox (P20), audit hash e config Keep (P11). Se ausentes nas fontes consultadas, manter bloqueado, não alegar irrecuperável universal.
