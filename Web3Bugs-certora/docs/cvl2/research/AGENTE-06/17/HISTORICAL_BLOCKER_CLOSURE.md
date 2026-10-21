# P17 — Conclusao documentaria da segunda revisao

A segunda revisao do coordenador confirmou o inventario, mas nao autorizou Fase 2. historical_blocked descreve uma lacuna documental no corpus preservado, NAO impossibilidade tecnica, vulnerabilidade ou falha do Prover.

## Estados por causa
- historical_blocked_specify_semantics: 41 instancias.

## Evidencia historica suficiente
- Commit auditado de source Solidity: f385d71983ae5c5799faae9b2dfea43e5cf75262. Exemplos .cvl sao Specify 2019 com .spclnk JSON de contratos auxiliares, NAO CVL1 convencional.
- complete/8 borrowFresh usa env e0/e1/e2 com havoc, snapshots pre/post via sinvoke, static_require envolvendo invoke borrowFreshPub(e1,...), lastReverted e static_assert com equivalencias bidirecionais.
- A documentacao oficial CVL1 para CVL2 explica sintaxe, mas nao comprova equivalencia de env/static_require/havoc/revert no motor Specify de 2019. Sem gramaticas/versionamento do motor e jobs antigos, nao propor conversao como validada.

## Fontes recuperaveis e condicao de reabertura
- Codigo e arquivos citados acima existem e podem subsidiar futura pesquisa; para superar historical_blocked exigem-se artifacts autenticados da auditoria (harness, executavel Specify, config, run, SHA ou ABI) que nao foram comprovados no corpus atual.
- Nao realizar buscas infinitas, nao fabricar contratos, mocks, getters ou variaveis, nao substituir versoes modernas.

## Estado de migracao
- original_status e Bug Labels inalterados. proposed_migration_bucket permanece UNRESOLVED_CANDIDATE para todos os casos. historical_closure_state e um eixo adicional e independente.
- Docs oficiais: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html.
- Sem compilation CVL1/CVL2, Prover ou alteracao de sources. Fase 2 nao autorizada.

## Links verificaveis para fontes preservadas (baseline fixado)

- [contracts/17/spec/formal/borrowAndRepayFresh.cvl](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/17/spec/formal/borrowAndRepayFresh.cvl)
- [contracts/17/spec/formal/MintRedeemBorrowRepay.spclnk](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/17/spec/formal/MintRedeemBorrowRepay.spclnk)
- [results/spec/complete/17/8.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/17/8.spec)
- [reports/17.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/reports/17.md)
