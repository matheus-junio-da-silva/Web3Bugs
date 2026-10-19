# P13 — Notional Finance V2: consolidacao de prova historica e bloqueios

## Comprovado

- Inventario de 58 propriedades historicas e result/outcome originais reconciliados ao CSV imutavel.
- 48 alvos nomeados/inferidos sem import closure; dez Balances.spec (#8-17) sem target comprovado.
- Script verify.sh fixa solc7.5, pacote Brownie OpenZeppelin@3.4.0-solc-0.7, Compound e interfaces; applyHarness.sh torna Constants.sol observavel.
- Resultado historico e metadados NAO significam prova CVL2 nem equivalencia:
  - CATALOG_NOT_STATED_DOC_7_VS_5_CONFLICT: 2
  - HISTORICAL_VERIFIED_CATALOG_ONLY: 5
  - NOT_STATED_NO_ATTRIBUTABLE_PROOF: 51

## Recuperavel condicionalmente

Cada linha em historical_status.csv identifica um artefato ou acao humana plausivel. Nomes e versoes sugeridos por script nao comprovam fontes realmente compiladas, snapshot do audito ou ABI. O recovery_manifest.csv retém caminhos, blobs e incertezas por dependencia.

## Bloqueado pela evidencia atual

- Dependencias historicas e hashes de pacotes nao recuperados. Divergencia 7 VERIFIED nos docs antigos contra 5 no CSV vigente (#32/#34 NOT_STATED).
- Totais por lacuna:
  - TARGET_NOT_EVIDENCED: 10
  - TRANSITIVE_IMPORT_AND_HARNESS_MISSING: 48

## Limite da busca e decisao

- Ver RECOVERY_SEARCH_LOG.md com consultas e escopo exato, inclusive resultados negativos. Foi encerrada apenas a busca nas fontes enumeradas, NAO a possibilidade de arquivos privados, artefatos gerados, runs Certora ou outras revisoes nao indexadas.
- Persistem 58 UNRESOLVED_CANDIDATE. Nao aplicar CVL2, nao usar placeholders de metodo como codigo, nao alterar assertions, requires/assumes, storage, paths de revert, quantificadores nem universe of methods.
- Eventual fase de implementacao exige instrucao explicita do coordenador e evidencias da ABI/scene. Ate la, fechar investigacao documental como BLOCKED_PENDING_HUMAN_EVIDENCE.
- Referencias: README.md, QA_REPORT.md, evidence_register.csv, recovery_manifest.csv e as paginas originais em resources/13/; CVL2 A1 https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html.
