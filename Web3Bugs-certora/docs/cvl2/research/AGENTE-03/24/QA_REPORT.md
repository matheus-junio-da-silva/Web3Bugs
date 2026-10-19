# QA_REPORT — AGENTE-03 / Rocket Joe P24 / Fase 1

## Proveniência e escopo
- Web3Bugs main/base: 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; PropertyGPT base: 687f654c679ed45ab127b7949e2a29c8f5e491b9.
- PR #36, research/cvl2-agente-03, commit anterior 021bfdf2a1a2e0983002a5845565a6579e2aa286.
- Fork Certora/rocket-joe-1 em dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10 (2022-03-09), PR upstream #168 fechado sem merge.
- Versão auditada e publicada: ef2ef30248661b5509c52ab30af9bd0fc07f6657, ancestral do fork e diferente em LaunchEvent/Staking.
- Escopo exclusivo: 164 exemplos (0 complete, 164 incomplete); nenhuma spec, Solidity, recursos históricos ou script editado.

## Reconciliação individual
- properties.csv: 164 linhas; migration_applicability.csv: 164; source_provenance_matrix.csv: 164; 164 dossiês properties/incomplete/N.md.
- Identidade canônica (24,incomplete,Example ID) para os IDs 1-164; status original permanece incomplete, independentemente de recuperação de dependência.
- Oito specs originais comparadas byte a byte à árvore do fork Certora. Git blob SHA-1 individual registrado.
- P01=161, P02=79 casos candidatos, P03=161, P04=75, P05=27, P06=29, P07=26, P08=5, P10=3; P09 reservado exclusivamente a proveniência e não a patch CVL2.
- P02 indica ocorrência explícita de chamada relevante ou method f na closure de import, não prova da aplicação da summary nem necessidade obrigatória de alteração.
- Três casos LEInProgress não recebem automaticamente P01/P03; seu original não importa outras specs.

## PDF correto lido diretamente
- 21 páginas, SHA-256 f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4, bytes de resources/24 verificados diretamente.
- PDF página 1 fixa quatro contratos e commit ef2ef302; páginas 2-4 descrevem achados e interpretação; páginas 5-6, assumptions e limitações do LaunchEvent.
- Páginas 7-16 descrevem estados, transições e high-level LaunchEvent; páginas 16-21, Staking e ressalvas.
- PDF p6: loops de uma iteração, LaunchEvent inicializado, WAVAX, bibliotecas/joe-core assumidos e transferência AVAX harnessed que pode ocultar reentrância.
- PDF p21: setup initialized e emergencyWithdraw, além da regra temporal enfraquecida por timeouts.
- Casos #2/#5/#7 têm discrepância de precondição, postcondição ou identidade da regra; #147 usa >= no CVL e == no PDF; #150 mostra variável diferente.
- Casos #12/#13, #152/#154 exigem cuidado com quantificadores existenciais e vacuity; #163 exige distinção entre require após withrevert e assert; #164 assert false é sonda.
- Sem copiar indicadores gráficos de VERIFIED para o snapshot divergente. Ver pdf_formula_review.md, source_provenance_matrix.csv e os dossiês.

## Recuperação histórica e limites
- Recuperados helper erc20.spec, DummyERC20A/B/Impl, DummyWeth, OwnerA/B, LaunchEventHarness, RocketJoeStakingHarness, scripts, Makefile e applyHarness.patch com hashes do commit Certora.
- O patch de 2732 linhas contém payload traderjoe/JoePair, JoeFactory, JoeRouter02 e bibliotecas; NÃO aplicado ou recompilado.
- Scripts históricos apresentam --link, --solc_map solc8.6/6.12, --optimistic_loop e --loop_iter 1 para Staking.
- Busca negativa no fork: não há .conf rastreado; verifyLEVarTran.sh cita Owner.sol ausente e stakingRule.sh cita staking.spec em case diferente.
- No commit auditado anterior não consta certora/; a fonte Certora recuperada coincide com specs arquivadas, não estabelece execução do mesmo snapshot auditado.
- Remaining uncertainty: transitive vendor import closure e versão compilada, ferramentas/flags originais efetivamente utilizadas e equivalência de semântica observável ainda não demonstradas.

## Validadores reais
- Worktree isolada: /home/mat/cvl2-agente03-revision-20261019, cwd dos validadores: Web3Bugs-certora.
- python3 scripts/check_specs.py . => exit 0; Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . => exit 0; Check passed! contests.csv consistent with reports.
- python3 scripts/check_contracts.py . => exit 0; Check passed! contracts consistent with reports.
- git diff --check em cwd da worktree => primeira tentativa exit 2 por CRLF em CSV e linha vazia extra; normalização somente documental; segunda tentativa exit 0.
- git diff --cached --check e custom reconciliation serão executados antes do commit final e seu resultado será registrado no comentário do PR.

## Gate
- Todas as 164 continuam UNRESOLVED_CANDIDATE e nenhuma classificação histórica foi promovida.
- SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1. Sem merge; PR em DRAFT. Fase 2 somente com aprovação expressa.
