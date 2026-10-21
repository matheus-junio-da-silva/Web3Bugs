# Upstream checks — AGENTE-07 / Project 9 — Celo Governance

Fase 1 documental, 2026-10-19. Consultas GET feitas via conexão GitHub; nunca executado Prover/compilador.

| Evidência | Repositório | Commit | Resultado | Referência |
|---|---|---|---|---|
| Phase-1 PDF commit | celo-org/celo-monorepo | 9d2ec0d9399a6959565062f57efa037d03fd4fbc | GitHub commit API: OK | https://github.com/celo-org/celo-monorepo/commit/9d2ec0d9399a6959565062f57efa037d03fd4fbc |
| Phase-2 PDF commit | celo-org/celo-monorepo | a46ce55ebd3867fa69290bf3be040846d433525d | GitHub commit API: OK | https://github.com/celo-org/celo-monorepo/commit/a46ce55ebd3867fa69290bf3be040846d433525d |

## Limites e impacto
Ainda não ocorreu comparação byte a byte dos arquivos originais CVL/Solidity/scripts com os commits das duas fases. Ter SHA localizado não atribui individualmente um Result a cada rule.

**Não há blob SHA comprovadamente correspondente ao código e import closure do Prover histórico para todos os casos.** Os dossiers mantêm `UNRESOLVED_CANDIDATE` onde falta essa correspondência.

## Historical dependency follow-up — 2026-10-19
Two distinct upstream Celo audits were referenced by the PDF. GitHub-retrieved Governance.sol blob SHA-1 at packages/protocol/contracts/governance/Governance.sol:
- Phase 1 SHA 9d2ec0d9399a6959565062f57efa037d03fd4fbc: 79bf02035380a650f343df00042ded0578568bfe.
- Phase 2 SHA a46ce55ebd3867fa69290bf3be040846d433525d: 641c834fa6bbf677aa8cc743890142c0cacce08d.
- Local snapshot contracts/9/contracts/governance/Governance.sol: 633b7d2d23c665a11fa9afd98351236b5c9fe3f8. These are THREE different Git blobs: neither upstream stage Governance.sol is byte-identical to the local snapshot.
- packages/protocol/package.json phase 1 depends on openzeppelin-solidity ^2.2.0/truffle 5.0.19, while phase 2 lists openzeppelin-solidity ^2.5.0/truffle 5.0.20. Do not treat ABI/remapping/compiled harness as identical.
- Source snapshot includes specs/harnesses and scripts/applyHarness.sh and target-specific scripts. The original runner flags (including governance.sh optimistic_loop), ABI, cross-contract hooks, and compiler must be compared to the *appropriate phase* per property, rather than inferred from mere presence of a commit.
- The three properties extracted from governance_old_rules.spec (IDs 48,49,50) remain selected in the supplied dataset. Do not drop them based on the word old.
- Each dossier now has full original extraction / pattern lines and a local cryptographic fingerprint; none prove the original remote phase run identity.
Links: https://github.com/celo-org/celo-monorepo/blob/9d2ec0d9399a6959565062f57efa037d03fd4fbc/packages/protocol/contracts/governance/Governance.sol ; https://github.com/celo-org/celo-monorepo/blob/a46ce55ebd3867fa69290bf3be040846d433525d/packages/protocol/contracts/governance/Governance.sol
Local harness/script SHA-256s (evidence for snapshot identity only):
- contracts/9/specs/scripts/accounts.sh: a32805dc888be96f3a3392c8b156d8ae358853693a6aac859242c9fe6a87981a
- contracts/9/specs/scripts/accountsPrivileged.sh: 554cd1845e1a6e4fbec8c95d603748fa74cdd4765bb3640313dcb97b76104553
- contracts/9/specs/scripts/applyHarness.sh: 8fdd045733ed6c7d3fbde8200e3035504880f9ff6c27db68b5ad3fbbba61cb61
- contracts/9/specs/scripts/governance.sh: 074de65d93f5e856c2294dba71cdf0a13e121768ba34db76ddd45f749f0dba0c
- contracts/9/specs/scripts/governancePrivileged.sh: e6d998c0cf46a6c91c5d882153be44f22cd2066abca24c4d02aa3e2dbd02fe52
- contracts/9/specs/scripts/lockedgold.sh: 2c038b1cc430839758e629cd49e8bf6a237e33232a43621b89071b43a1a8e3b6
- contracts/9/specs/scripts/reserve.sh: e945582f12b6d726bb5b3471694ef48f48b51ca14a1e6b472d733a41c7a35a17
- contracts/9/specs/harnesses/AccountsHarness.sol: c694eb437de8b14ec014a5eaeb71a8632400bfd7b623f824ce8f1fa7a3ef8d8b
- contracts/9/specs/harnesses/GoldTokenHarness.sol: 400d6dfce1453680e1bddd9ce08904add705be374d27a8ca84f8dacc67f15305
- contracts/9/specs/harnesses/GovernanceHarness.sol: 060a64e652603693abf88952cf0c17990426298131869d165a326567f374315c
- contracts/9/specs/harnesses/IRegistryExtended.sol: fba96c1262a815d86e4e9bf3ffe143eec7e243cf2509dedc3e8d057577ff4069
- contracts/9/specs/harnesses/LockedGoldHarness.sol: fd8710781e769cd3d6533eb79d9d37c037bbdae2d7a234f8cfc8fe29d3d6b961
- contracts/9/specs/harnesses/RegistryHarness.sol: d30ac9c0b9d01e3e6c97f6ee1cced17da7118dfff4e9bf5db614b5423f8cc2c0
- contracts/9/specs/harnesses/ReserveHarness.sol: a9cba58d1155f30ff29969e0854fcce055a7c9aa6ac27dd39a98035d45680c10
