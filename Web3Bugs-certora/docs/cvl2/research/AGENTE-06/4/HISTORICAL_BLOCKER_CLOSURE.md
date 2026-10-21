# P4 — Conclusao documentaria da segunda revisao

A segunda revisao do coordenador confirmou o inventario, mas nao autorizou Fase 2. historical_blocked descreve uma lacuna documental no corpus preservado, NAO impossibilidade tecnica, vulnerabilidade ou falha do Prover.

## Estados por causa
- historical_blocked_generated_munged: 27 instancias.

## Evidencia historica suficiente
- StakedAaveV3Harness importa ../munged/contracts/StakedAaveV3.sol e ../munged/interfaces/IERC20.sol. No snapshot munged tem apenas .gitignore.
- Makefile copia ../src para munged e aplica applyHarness.patch; patch altera StakedTokenV2/V3; runInvariants.sh tem links STAKED_TOKEN/REWARD_TOKEN, solc8.17, optimistic_loop, loop_iter 3.
- Commit auditado de source Solidity: 4cf8837121a4351cc0e21703bb1df76036205114. Src recuperavel no upstream, mas nao provado byte-identico a munged gerado do run; 27 originais incomplete preservados.

## Fontes recuperaveis e condicao de reabertura
- Codigo e arquivos citados acima existem e podem subsidiar futura pesquisa; para superar historical_blocked exigem-se artifacts autenticados da auditoria (harness, executavel Specify, config, run, SHA ou ABI) que nao foram comprovados no corpus atual.
- Nao realizar buscas infinitas, nao fabricar contratos, mocks, getters ou variaveis, nao substituir versoes modernas.

## Estado de migracao
- original_status e Bug Labels inalterados. proposed_migration_bucket permanece UNRESOLVED_CANDIDATE para todos os casos. historical_closure_state e um eixo adicional e independente.
- Docs oficiais: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html.
- Sem compilation CVL1/CVL2, Prover ou alteracao de sources. Fase 2 nao autorizada.

## Links verificaveis para fontes preservadas (baseline fixado)

- [contracts/4/certora/Makefile](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/4/certora/Makefile)
- [contracts/4/certora/applyHarness.patch](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/4/certora/applyHarness.patch)
- [contracts/4/certora/harness/StakedAaveV3Harness.sol](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/4/certora/harness/StakedAaveV3Harness.sol)
- [contracts/4/certora/scripts/runInvariants.sh](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/4/certora/scripts/runInvariants.sh)
