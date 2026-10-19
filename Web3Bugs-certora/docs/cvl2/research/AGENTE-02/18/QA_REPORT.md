# QA — AGENTE-02 P18 / fase 1

## Reconciliação efetivamente realizada
- Fonte: `spec_catalog_project_18_evidence.json` (181 entradas); matriz `spec_catalog_project_18_semantic_matrix.csv` (181); `spec_buglabel.csv` (181 linhas do Project 18, uma por exemplo neste projeto).
- Chaves únicas entre status/project/ID: 181; divergências entre `Property`, `Status`, `Target` nas três fontes: **0**.
- Conferência via GitHub Contents API na HEAD de entrada: `complete/18` 69 `N.spec` e 69 `N.md`; `incomplete/18` 112 `N.spec`, 112 `N.md`, 112 `N.txt`.
- A fonte contém 168 declarações ativas, mas foram mantidos 181 contextos; Initializable 26 linhas em 2 harness targets para 13 declarações.
- Os 181 arquivos de dossiê usam `contracts/18/specs/*.spec` original com ranges `evidence.json` sem editar fonte. Cada dossier referencia seu próprio `SRC18-###`, target e predicado.
- Contagens de estado no CSV de pesquisa: {"UNRESOLVED_CANDIDATE":112,"DOCUMENTED_CANDIDATE":57,"INDIRECT_CANDIDATE":12}; 69 complete/112 incomplete de origem, **não** compilados. Os 4 registros `VIOLATED` são históricos e escopados; marcadores gráficos de PDF e outcomes individuais não foram reproduzidos.

## Verificações documentais em execução
- Parsing RFC-style para CSV com vírgulas/aspas e guardas programáticas de duplicidade e correspondência de identidades entre três fontes: OK.
- Verificação dos ranges de código originais onde os dossiês foram criados: existência do nome de property no segmento informado; nenhum diff nos históricos.
- GitHub API comparou blobs de contratos `Governor.sol`, `ERC1155.sol` com commit 109778c: iguais. Quatro specs homônimas examinadas em `certora/specs/` upstream têm blobs diferentes: risco de provenance.
- CLI `python scripts/check_specs.py .`, `python scripts/check_contests_csv.py .`, `python scripts/check_contracts.py .`, `git diff --check`: **NÃO EXECUTADOS** (não houve worktree/terminal conectado; Remote Desktop Commander dispositivo offline; runtime de arquivos local indisponível). Sem registrar exit code fictício.
- `certoraRun`, `solc` e `python --version`: NÃO EXECUTADOS. Nenhuma credencial consultada.

## Questões bloqueantes / revisão independente
- Falta provar se cada property realmente usou o commit, target harness e summary histórico alegado; PDF não fornece trace por rule/target.
- Recuperação parcial de patch/harness/scripts Governor no 109778c não resolve ABI de todas as specs. Não introduzir compilação com a especificação fonte não coincidente sem decisão.
- Initializable flat/multi, Supply exists_wrapper, GovernorPreventLateQuorumHarness e getter checkpoint permanecem sem proveniência exata.
- Timelock schedule typagem inconsistente já no CVL original em relação ao Solidity; não resolver com troca textual silenciosa.
- Oficial Certora consultado em página `en/latest` no dia 2026-10-19, não versão SHA fixada. Revisão futura deve pin ou registrar versão da CLI antes de execução.
- Extrato textual de `reports/18.md` usado para mapear páginas. Nenhuma interpretação nova de símbolo gráfico PDF ou prova histórica inferida.
- P01/P02 são candidatos de documentação, mas a resolução de métodos, o alcance do receiver, `require`, `assert`, `filtered` e invariants só podem ser validados em eventual Fase 2 autorizada.

## Limites e política
Nenhuma fonte `.spec`, `.sol`, PDF, script, arquivo fora de `docs/cvl2/research/AGENTE-02/18/` foi editado. Sem CVL1 replay, migração in-place, compilar CVL2 ou Prover. PR permanecerá draft sem merge até revisão do coordenador.
