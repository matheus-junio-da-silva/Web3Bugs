# P14 — Opyn Gamma: consolidacao de prova historica e bloqueios

## Comprovado

- Inventario de 34 propriedades historicas e result/outcome originais reconciliados ao CSV imutavel.
- 34 originais complete documentalmente, todos unresolved para CVL2; 31 promocoes DOCUMENTED retiradas.
- applyHarnesses.sh modifica Controller/MarginPool; runOrderOfOperations.sh usa solc6.10, mas runNoBankruptcy.sh e runMarginVault.sh usam executavel solc sem versao explicita nesses scripts.
- Resultado historico e metadados NAO significam prova CVL2 nem equivalencia:
  - HISTORICAL_VERIFIED_CATALOG_ONLY: 19
  - NOT_STATED_NO_ATTRIBUTABLE_PROOF: 15

## Recuperavel condicionalmente

Cada linha em historical_status.csv identifica um artefato ou acao humana plausivel. Nomes e versoes sugeridos por script nao comprovam fontes realmente compiladas, snapshot do audito ou ABI. O recovery_manifest.csv retém caminhos, blobs e incertezas por dependencia.

## Bloqueado pela evidencia atual

- ABI final, receiver, internal/external, summaries e universe-of-methods nao comprovados; placeholders nao sao sintaxe pronta. #1 assert true condicional, #19 caso especial e #25 sinvoke/assert false intocados.
- Totais por lacuna:
  - CONTROLLER_ABI_RECEIVER_SUMMARY: 13
  - WHITELIST_PRIVILEGED_SELECTOR_SCENE: 1
  - MARGINVAULT_ABI_AND_SOLC: 13
  - NOBANKRUPTCY_ABI_AND_LINKS: 5
  - ORDER_OF_OPERATIONS_ABI_AND_SELECTOR: 1
  - SETTLEVAULT_REVERT_PATH: 1

## Limite da busca e decisao

- Ver RECOVERY_SEARCH_LOG.md com consultas e escopo exato, inclusive resultados negativos. Foi encerrada apenas a busca nas fontes enumeradas, NAO a possibilidade de arquivos privados, artefatos gerados, runs Certora ou outras revisoes nao indexadas.
- Persistem 34 UNRESOLVED_CANDIDATE. Nao aplicar CVL2, nao usar placeholders de metodo como codigo, nao alterar assertions, requires/assumes, storage, paths de revert, quantificadores nem universe of methods.
- Eventual fase de implementacao exige instrucao explicita do coordenador e evidencias da ABI/scene. Ate la, fechar investigacao documental como BLOCKED_PENDING_HUMAN_EVIDENCE.
- Referencias: README.md, QA_REPORT.md, evidence_register.csv, recovery_manifest.csv e as paginas originais em resources/14/; CVL2 A1 https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html.
