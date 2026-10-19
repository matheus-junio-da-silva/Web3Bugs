# AGENTE-03 — Project 24 Rocket Joe: pesquisa pré-migração CVL2

**164 exemplos originais: 0 complete, 164 incomplete. Fase 1 somente documental; nenhuma execução de verificação.**

## Revisão do coordenador

O review no PR #36 devolveu a pesquisa para investigar PDF, harness, scripts e aplicabilidade individual. Este commit responde com 164 dossiês revisados e matrizes adicionais.

## Descoberta histórica confirmada

- Fonte das regras e helpers: https://github.com/Certora/rocket-joe-1/blob/dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10/certora/spec/LEHighLevel.spec (Certora/rocket-joe-1 @ dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10), PR histórico https://github.com/lfj-gg/rocket-joe/pull/168 fechado sem merge.
- **Oito .spec byte a byte idênticas** ao snapshot PropertyGPT/Web3Bugs.
- Helper original erc20.spec, DummyERC20A/B/Impl, DummyWeth, LaunchEventHarness, RocketJoeStakingHarness, OwnerA/B e patch recuperados com blobs Git precisos; recovery_manifest.csv distingue recuperado de falta de prova de execução.
- Scripts originais --link, solc8.6/solc6.12, --optimistic_loop, --loop_iter 1, flags e targets foram localizados. Não havia .conf no fork; alguns scripts têm paths divergentes; patch de 2732 linhas inclui fontes traderjoe mas NÃO foi aplicado.
- Audited commit ef2ef30248661b5509c52ab30af9bd0fc07f6657 é ancestral do fork, porém LaunchEvent e RocketJoeStaking possuem mudanças comportamentais; ver source_provenance_matrix.csv.

## Relatório correto

21 páginas diretamente examinadas, SHA256 f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4. PDF incorreto OpenZeppelin permanece intacto. Ver pdf_formula_review.md, páginas 1-21 e diferenças pontuais 2/5/7/147/150 etc. Não transferir resultados do PDF de outra revisão.

## Entregas

- properties.csv — índice 164 instâncias, separando status original de recuperação histórica.
- source_provenance_matrix.csv — 164 confrontos source/fork/target/audit/PDF.
- migration_applicability.csv — 164 verificações específicas dos padrões P01-P10, incluindo ausência de ocorrência.
- properties/incomplete/N.md — 164 dossiês atualizados, com CVL literal, hash, evidência, PDF e condicionais CVL2.
- evidence_register.csv — A1/A2/B1/C2 com fonte, versão, scope.
- recovery_manifest.csv — arquivos rastreados e bloqueios residuais.
- patterns/ — padrões corrigidos; P09 retirado da lista de patches CVL2.
- pdf_formula_review.md — verificação direta p1-p21.
- QA_REPORT.md — validações e pendências.

**Todas as 164 permanecem UNRESOLVED_CANDIDATE PROVISÓRIAS, apesar da recuperação parcial de fontes históricas. SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
