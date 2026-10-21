# P5 — AAVE StarkNet Bridge: consolidacao de prova historica e bloqueios

## Comprovado

- Inventario de 17 propriedades historicas e result/outcome originais reconciliados ao CSV imutavel.
- 17 properties originalmente incomplete; fonte upstream 4c010c18b08703e4f367db1e0c642c76c25e551b.
- Blobs de erc20.spec, BridgeHarness, BridgeL2Harness, mocks, scripts, Makefile e applyHarness.patch identificados; solc8.10, loop_iter 3, links entre contratos.
- Resultado historico e metadados NAO significam prova CVL2 nem equivalencia:
  - HISTORICAL_VERIFIED_CATALOG_ONLY: 6
  - HISTORICAL_VIOLATED_CATALOG_ONLY: 4
  - NOT_STATED_NO_ATTRIBUTABLE_PROOF: 7

## Recuperavel condicionalmente

Cada linha em historical_status.csv identifica um artefato ou acao humana plausivel. Nomes e versoes sugeridos por script nao comprovam fontes realmente compiladas, snapshot do audito ou ABI. O recovery_manifest.csv retém caminhos, blobs e incertezas por dependencia.

## Bloqueado pela evidencia atual

- Import closure, arvore munged apos patch, compilador/hashes e comparacao Bridge.sol snapshot posterior versus revisao auditada pendentes. erc20.spec nao define getters BridgeHarness.
- Totais por lacuna:
  - BRIDGE_IMPORT_CLOSURE_AND_VERSION_DRIFT: 17

## Limite da busca e decisao

- Ver RECOVERY_SEARCH_LOG.md com consultas e escopo exato, inclusive resultados negativos. Foi encerrada apenas a busca nas fontes enumeradas, NAO a possibilidade de arquivos privados, artefatos gerados, runs Certora ou outras revisoes nao indexadas.
- Persistem 17 UNRESOLVED_CANDIDATE. Nao aplicar CVL2, nao usar placeholders de metodo como codigo, nao alterar assertions, requires/assumes, storage, paths de revert, quantificadores nem universe of methods.
- Eventual fase de implementacao exige instrucao explicita do coordenador e evidencias da ABI/scene. Ate la, fechar investigacao documental como BLOCKED_PENDING_HUMAN_EVIDENCE.
- Referencias: README.md, QA_REPORT.md, evidence_register.csv, recovery_manifest.csv e as paginas originais em resources/5/; CVL2 A1 https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html.
