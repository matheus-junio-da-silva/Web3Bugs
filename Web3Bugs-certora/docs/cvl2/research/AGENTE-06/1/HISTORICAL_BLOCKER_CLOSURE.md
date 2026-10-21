# P1 — Conclusao documentaria da segunda revisao

A segunda revisao do coordenador confirmou o inventario, mas nao autorizou Fase 2. historical_blocked descreve uma lacuna documental no corpus preservado, NAO impossibilidade tecnica, vulnerabilidade ou falha do Prover.

## Estados por causa
- historical_blocked_complexity_runner: 6 instancias.
- historical_blocked_mock_helper: 6 instancias.
- historical_blocked_queue2: 14 instancias.
- historical_run_unattributed: 44 instancias.

## Evidencia historica suficiente
- Audited Solidity commit: 303bd3e16c8d3465325389a72564126c3bacc4f9; o arquivo difere em pragma e comentario em algumas comparacoes. Commit nao prova replay de regras.
- Arquivados: PolygonBridge.spec, Optimism_ArbitrumBridge.spec, complexity.spec e erc20.spec. queue2 aparece no Optimism_ArbitrumBridge.spec (linha 128 em diante) e _mock(e) na linha 171; complexity.spec tem regras parametricas com chamadas e lastReverted.
- Ausentes do corpus recuperado: prova de ABI que inclua queue2/_mock e runner/target autenticado de complexity.spec. Validacao de origem Polygon difere de L2. Nao presumir um helper nem wildcard receiver.

## Fontes recuperaveis e condicao de reabertura
- Codigo e arquivos citados acima existem e podem subsidiar futura pesquisa; para superar historical_blocked exigem-se artifacts autenticados da auditoria (harness, executavel Specify, config, run, SHA ou ABI) que nao foram comprovados no corpus atual.
- Nao realizar buscas infinitas, nao fabricar contratos, mocks, getters ou variaveis, nao substituir versoes modernas.

## Estado de migracao
- original_status e Bug Labels inalterados. proposed_migration_bucket permanece UNRESOLVED_CANDIDATE para todos os casos. historical_closure_state e um eixo adicional e independente.
- Docs oficiais: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html.
- Sem compilation CVL1/CVL2, Prover ou alteracao de sources. Fase 2 nao autorizada.

## Links verificaveis para fontes preservadas (baseline fixado)

- [contracts/1/specs/Optimism_ArbitrumBridge.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/1/specs/Optimism_ArbitrumBridge.spec)
- [contracts/1/specs/complexity.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/1/specs/complexity.spec)
- [contracts/1/contracts/bridges/BridgeExecutorBase.sol](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/1/contracts/bridges/BridgeExecutorBase.sol)
- [reports/1.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/reports/1.md)
