# P22 — Conclusao documentaria da segunda revisao

A segunda revisao do coordenador confirmou o inventario, mas nao autorizou Fase 2. historical_blocked descreve uma lacuna documental no corpus preservado, NAO impossibilidade tecnica, vulnerabilidade ou falha do Prover.

## Estados por causa
- historical_blocked_free_symbol: 1 instancias.
- historical_blocked_private_getter: 1 instancias.
- historical_blocked_runner_scope: 6 instancias.
- historical_run_unattributed: 13 instancias.

## Evidencia historica suficiente
- verifyPopsicleV3Optimizer.sh usa --verify PopsicleV3Optimizer:spec/PopsicleV3Optimizer.spec com --rule $1, links token0, token1, pool simbolico, solc7.6 e loop_iter 1. Nao atesta execucao de FullMathWrapper, PoolActions e sanity.
- Seis blobs iguais entre snapshot e branch upstream commit 3cb9cb7279a3fb1790b55251a029bb3065606dc8; o commit e posterior a janela reportada e NAO identifica o audited commit.
- incomplete/4: totalSupply nao possui getter ABI. incomplete/5: to em require e um simbolo CVL nao declarado. Sao causas separadas registradas em N.txt.

## Fontes recuperaveis e condicao de reabertura
- Codigo e arquivos citados acima existem e podem subsidiar futura pesquisa; para superar historical_blocked exigem-se artifacts autenticados da auditoria (harness, executavel Specify, config, run, SHA ou ABI) que nao foram comprovados no corpus atual.
- Nao realizar buscas infinitas, nao fabricar contratos, mocks, getters ou variaveis, nao substituir versoes modernas.

## Estado de migracao
- original_status e Bug Labels inalterados. proposed_migration_bucket permanece UNRESOLVED_CANDIDATE para todos os casos. historical_closure_state e um eixo adicional e independente.
- Docs oficiais: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html.
- Sem compilation CVL1/CVL2, Prover ou alteracao de sources. Fase 2 nao autorizada.

## Links verificaveis para fontes preservadas (baseline fixado)

- [contracts/22/spec/scripts/verifyPopsicleV3Optimizer.sh](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/22/spec/scripts/verifyPopsicleV3Optimizer.sh)
- [contracts/22/spec/PoolActions.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/22/spec/PoolActions.spec)
- [results/spec/incomplete/22/4.txt](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/22/4.txt)
- [results/spec/incomplete/22/5.txt](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/22/5.txt)
