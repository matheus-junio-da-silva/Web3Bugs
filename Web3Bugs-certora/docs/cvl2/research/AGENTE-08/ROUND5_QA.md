# AGENTE-08 — Rodada 5 / QA, inventário e comandos
Execuções locais somente em checkout isolado `/home/mat/cvl2-agente08-round4-20261020/repo`. Baseline imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, HEAD de partida `96771fa27f90e56299bccc75a9729937ec4e77cc`, sem reset. Ambiente solc8.10 `/home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10`. Download da release oficial solc v0.6.10 em scratch, não instalada como substituição global.

## Comandos de compilação Solidity, experimentos realmente executados
P5 (scratch em `starknet-upstream`, commit `4c010c18`): `timeout 110s /home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10 --base-path . --include-path node_modules --allow-paths . --abi --bin -o SCRATCH/p5-solc/abi --overwrite certora/harness/{BridgeHarness,BridgeL2Harness,DummyERC20UnderlyingA_L1,DummyERC20UnderlyingB_L1,ATokenWithPoolA_L1,ATokenWithPoolB_L1,StaticATokenA_L2,StaticATokenB_L2,DummyERC20RewardToken,SymbolicLendingPoolL1,IncentivesControllerMock_L1}.sol`. As chaves entre chaves são notação abreviada na documentação; o comando efetivo expandiu 11 argumentos literais. Primeira tentativa exit 1 devido a symlink, segunda exit 0 após cópia física do mesmo diretório patchado dentro de `certora/munged/l1`. ABI 40, warnings no log integral.
P14 (scratch `opyn-transform`, versão `0.6.10+commit.00c0fcaf`): `timeout 70s SCRATCH/solc-0.6.10-static --base-path . --allow-paths . --abi --bin --overwrite -o SCRATCH/abi/<NAME> specs/harness/<NAME>.sol` aplicado a ControllerHarness, ControllerHarnessExtra, MarginVaultHarness; também Controller.sol pós-harness e Controller.sol original byte-idêntico noutro diretório scratch. Os cinco exit 0, warnings no log integral. Não executar scripts Certora de prova, Prover, CVL1, nem CVL2 compile-only.
Comandos de validação estrutural e diff **pós push** serão publicados no comentário de resposta da mesma PR, após execução. Validadores testam somente integridade, não semântica.

## Arquivos da rodada
- `ROUND5_MATRIX_155.csv`: uma linha para cada chave `(Project ID, Status, Example ID)`, SHA-256 da fonte `N.spec`, evidência e next gate.
- `ROUND5_SOLIDITY_ABI_REGISTER.csv`: 40 ABI P5 e 71 ABI P14 para targets/dependências compilados, com assinatura e hash.
- `ROUND5_SOLIDITY_FULL_COMPILER_LOGS.txt`: stdout+stderr íntegros de 7 invocações `solc` / 14 streams.
- `ROUND5_EVIDENCE_AND_GATES.md`: evidências por commit e linhas, distinção dos gates e revisão read-only PR #39.
Todos somente sob `docs/cvl2/research/AGENTE-08/`, sem mudanças nos diretórios históricos ou saídas `results/cvl2`.
