# AGENTE-05 — Project 21 / Lido V2 — Fase 1

- Web3Bugs baseline: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; PropertyGPT baseline: `687f654c679ed45ab127b7949e2a29c8f5e491b9` (ambos confirmados em 2026-10-19).
- Histórico catalogado: **2 exemplos únicos, 0 complete, 2 incomplete**, apenas `specs/DSM.spec`; sem extrapolar os 18 checks de nomes diferentes no PDF.
- CVL original: `contracts/21/specs/DSM.spec`; SHA256 relatado no catálogo: `f166f8b394189b3a2396325e343a17550f53d46c2d22f407e93819fcc75cf57b`.
- PDF: `resources/21/Certora-Lido-V2-Audit-Report-04-23.pdf` (40 páginas, emissão 2023-04-27; SHA256 registrado no catálogo: `b8acbf2e980db873706a40ac1abefdbffa6ad3e6f649445f2000e93e905f9c5b`). O relatório não identifica resultados para estas duas declarações CVL.
- Commit exato da execução histórica: **não estabelecido**. O módulo de produção não substitui um harness ausente. Source snapshot não inclui `DepositSecurityModuleHarness`, `depositBufferedEtherHarness`, `getGuardianLength`, `../common/lib/ECDSA.sol`.

## Documentos

`properties.csv` contém as duas chaves `(21, incomplete, Example ID)`; `properties/incomplete/{1,2}.md` individualizam falsificações, dependências e riscos; `patterns/methods-and-semantics.md` contém regras CVL2 e respectivos limites; `evidence_register.csv` fornece URLs/evidências; `recovery_manifest.csv` distingue ausências não recuperadas; `QA_REPORT.md` reúne validações documentais.

**Limite estrito:** nenhuma spec, Solidity, script, snapshot ou catálogo histórico foi editado. Não houve compilação CVL2, execução de Prover ou teste CVL1. Todos os buckets são hipóteses provisórias.
