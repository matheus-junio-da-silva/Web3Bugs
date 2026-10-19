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

## Correção de revisão cruzada (Fase 1)
- O índice `properties.csv` foi reconciliado por padrão individual; `P03` só foi mantido nas 16 declarações com literais de método tipados em código ativo, não comentários nem usos isolados de `f.selector`. IDs 122, 123, 124 e 126 tiveram o falso sinalizador P03 removido, preservando a prova histórica e o texto CVL.
- `P07` foi registrado para 90–100 quando a spec possui `using`; `P08` para atribuições aritméticas condicionais 70 e 94. Evidência A1/A2 ainda não prova necessidade de um cast particular.
- `recovery_manifest.csv` registra os hashes Git completos dos arquivos upstream recuperáveis no SHA auditado; recuperação de arquivo não prova replay do job.
- GitHub Compare API: 194 arquivos novos, todos sob o diretório autorizado; nenhuma mudança em fontes históricas. Checar novamente após este commit.


## Reexecucao de validacao no checkout isolado em 2026-10-19
CWD de todos os comandos Python: /home/mat/cvl2-agente02-revision/repo/Web3Bugs-certora
- python3 scripts/check_specs.py . => exit 0, Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . => exit 0, Check passed! results/contests.csv is consistent with reports.
- python3 scripts/check_contracts.py . => primeira tentativa exit 1 (sparse checkout omitia outros IDs; nao falha da fonte). Com sparse checkout ampliado para contracts/ de todos IDs, **segunda tentativa exit 0**: contracts consistent with reports.
- git diff --check: a registrar depois de staged diff; nenhuma compilacao nem Prover.
- O PDF de 13 paginas foi lido diretamente, digest registrado em pdf_page_review.md; nao inferir simbolos graficos.
- 181 dossies auditados pela ocurrencia textual; 7 DOCUMENTED e 12 INDIRECT anteriores rebaixados. Buckets: {'UNRESOLVED_CANDIDATE': 131, 'DOCUMENTED_CANDIDATE': 50}.
- A comparacao byte a byte identificou 12 specs ausentes e 4 homonimas diferentes no commit 109778c. Scripts/harnesses recuperados nao equivalem a proveniencia completa.
- O risco de selector fallback foi isolado em example 81; 15 propriedades tem assinatura tipada ativa, sem afirmar ABI em target.
- Relevancia dos before/after depende de confirmacao do target e dos parametros/retornos; os 50 documentados sao candidatos lexicais, nao equivalencia semantica.

## QA final do staged diff (2026-10-19)
- git diff --cached --check (cwd raiz repo) => exit 0; 197 arquivos stageados, 0 fora de docs/cvl2/research/AGENTE-02/18/.
- git diff --check (cwd raiz repo apos staging) => exit 0; sem changes unstaged.
- QA nao valida semantic equivalence, solc/CVL2/Prover, original harness, historical findings.
