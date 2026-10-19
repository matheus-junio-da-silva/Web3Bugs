# P23 — Radicle Drips: consolidacao de prova historica e bloqueios

## Comprovado

- Inventario de 46 propriedades historicas e result/outcome originais reconciliados ao CSV imutavel.
- DripsHub #1-12; DripsHubBackup #13-18; Reserve #19-23; SlotTester #24; Splits #25-41; Splits2 #42-46.
- PDF reportado limita o resultado a Splits.sol; commit 6fe9d38a30765df6aa3e4078634a37aeabbceef1 identifica codigo de producao, nao os wrappers CVT.
- Resultado historico e metadados NAO significam prova CVL2 nem equivalencia:
  - HISTORICAL_VERIFIED_CATALOG_ONLY: 15
  - HISTORICAL_VIOLATED_CATALOG_ONLY: 1
  - NOT_STATED_NO_ATTRIBUTABLE_PROOF: 29
  - REPORT_TIMEOUT_INCONCLUSIVE: 1

## Recuperavel condicionalmente

Cada linha em historical_status.csv identifica um artefato ou acao humana plausivel. Nomes e versoes sugeridos por script nao comprovam fontes realmente compiladas, snapshot do audito ou ABI. O recovery_manifest.csv retém caminhos, blobs e incertezas por dependencia.

## Bloqueado pela evidencia atual

- Ausentes DripsHubHarness, UpdateReceiverStatesHarness, ReserveHarness, SlotTester e wrappers CVT. #36 VIOLATED/FINDING; #38 timeout NOT_STATED/INCONCLUSIVE. Splits2 nao herda Splits.
- Totais por lacuna:
  - DRIPSHUB_HARNESS_ABSENT: 12
  - RESERVE_HARNESS_MOCKS_ABSENT: 5
  - SLOTTESTER_TARGET_ABSENT: 1
  - SPLITS2_CVT_WRAPPERS_ABSENT: 5
  - SPLITS_CVT_WRAPPERS_ABSENT: 17
  - UPDATE_HARNESS_ABSENT: 6

## Limite da busca e decisao

- Ver RECOVERY_SEARCH_LOG.md com consultas e escopo exato, inclusive resultados negativos. Foi encerrada apenas a busca nas fontes enumeradas, NAO a possibilidade de arquivos privados, artefatos gerados, runs Certora ou outras revisoes nao indexadas.
- Persistem 46 UNRESOLVED_CANDIDATE. Nao aplicar CVL2, nao usar placeholders de metodo como codigo, nao alterar assertions, requires/assumes, storage, paths de revert, quantificadores nem universe of methods.
- Eventual fase de implementacao exige instrucao explicita do coordenador e evidencias da ABI/scene. Ate la, fechar investigacao documental como BLOCKED_PENDING_HUMAN_EVIDENCE.
- Referencias: README.md, QA_REPORT.md, evidence_register.csv, recovery_manifest.csv e as paginas originais em resources/23/; CVL2 A1 https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html.
