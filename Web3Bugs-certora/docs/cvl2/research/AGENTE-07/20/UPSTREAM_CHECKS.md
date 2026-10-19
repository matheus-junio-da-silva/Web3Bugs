# Upstream checks — AGENTE-07 / Project 20 — Sushi BentoBox

Fase 1 documental, 2026-10-19. Consultas GET feitas via conexão GitHub; nunca executado Prover/compilador.

| Evidência | Repositório | Commit | Resultado | Referência |
|---|---|---|---|---|
| BentoBox report-reviewed commit | sushiswap/bentobox | 0c68f2aa38cd600b5959197416fe090baa6a2a3f | GitHub commit API: OK | https://github.com/sushiswap/bentobox/commit/0c68f2aa38cd600b5959197416fe090baa6a2a3f |

## Limites e impacto
A existência do commit oficial não estabelece identidade do import @boringcrypto, configs/harness/SymbolicStrategy ou dos scripts historicamente reescritos; não substituir flattened sources por pacotes modernos.

**Não há blob SHA comprovadamente correspondente ao código e import closure do Prover histórico para todos os casos.** Os dossiers mantêm `UNRESOLVED_CANDIDATE` onde falta essa correspondência.

## Historical dependency follow-up — 2026-10-19
B1 official historical package at reviewed BentoBox commit 0c68f2aa38cd600b5959197416fe090baa6a2a3f:
- package.json depends on @boringcrypto/boring-solidity at boringcrypto/BoringSolidity#39fdd3b.
- yarn.lock resolves the precise commit 39fdd3b4c78be0380edc95fde98d198f4bac5b41 (declares package version 1.1.0), fetched from the Git object in public historical fork bartjellema/BoringSolidity at that *same* commit.
- Blob SHA-1 and SHA-256 below confirm the repository source bytes, but not that the archived Prover invocation used the unmodified npm tarball or harness.
- contracts/libraries/BoringERC20.sol Git blob 718d53a1eb79fd8c8ed3e42205220a05120b81ef SHA-256 bd2f1c315b5f066197dfd73d50db3710798fda225965022e12ca02489a7e3edc
- contracts/libraries/BoringMath.sol Git blob 0b94f91d5f650f61ce01506d24530d58a3de8745 SHA-256 50e475020a0930368e9321d112e898eaebfff79a790112540bf5d2e81a961958
- contracts/libraries/BoringRebase.sol Git blob dd27d7dba9e35fb99e4600b7ddf03f38d9e435a6 SHA-256 44603c739d81652a86181839b531d05cfe95b8f806f2528a1897bcb60d0203ac
- contracts/BoringBatchable.sol Git blob 048191cfb493a818e0ac48e67a0bebed473ad74e SHA-256 50e7f052569a27ad2d8edb0a8dd8995c078446b98a1804233326e8701d42016a
- contracts/BoringFactory.sol Git blob 301c657e2dcc6588c3783efe08f3f27548057f57 SHA-256 9626b37e827528cba6ac7d5b9e298824cead5868440b7bfe76da683909f0aed9
- contracts/interfaces/IERC20.sol Git blob 45b78549916632ae2fe6c80f9f3dbc8c266ed39a SHA-256 19c258f65935f39a0aca7086414331699d0da313c2dbb7f019a04046c33ffcbd
- Local spec/scripts/applyHarnesses.sh mutates BentoBox, CompoundStrategy, and BoringBatchable, BoringFactory and IERC20 files in node_modules IN PLACE. Virtualization, transfer interface, safeTransfer renaming, try/catch rewriting and external call replacement affect call/exception models; the unmodified original is not necessarily the compiled verification target.
- MAX_INT is defined in local spec/compoundStrategy.spec:60 and spec/strategy.spec:43. The separate spec/compoundStrategyAdditional.spec:65 calls MAX_INT but does not define it: must reconstruct actual spec inclusion/config or mark unresolved; presence in a sibling file alone does not close the symbol.
- Imported BoringMath/Rebase/ERC20 files at pinned SHA are recovered as source candidates; full historical runner solc_map/remappings, modified node_modules output and call-resolution remain UNPROVEN. Do not silently substitute newer BoringSolidity.
Links: https://github.com/sushiswap/bentobox/blob/0c68f2aa38cd600b5959197416fe090baa6a2a3f/package.json ; https://github.com/sushiswap/bentobox/blob/0c68f2aa38cd600b5959197416fe090baa6a2a3f/yarn.lock ; https://github.com/bartjellema/BoringSolidity/tree/39fdd3b4c78be0380edc95fde98d198f4bac5b41
