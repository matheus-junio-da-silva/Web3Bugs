# P12 — Construtor, harness historico e scripts por familia (revisao 2)

**B1 auditado:** https://github.com/aave/protocol-v2/blob/750920303e33b66bc29862ea3b85206dda9ce786/contracts/protocol/tokenization/StableDebtToken.sol tem construtor de 5 argumentos, invocado pelo https://github.com/aave/protocol-v2/blob/750920303e33b66bc29862ea3b85206dda9ce786/specs/harness/StableDebtTokenHarness.sol. Git blob auditado `78401405f1b1587428a514cb7b864f2384b73897`.

**Snapshot Web3Bugs:** StableDebtToken.sol tem initialize(ILendingPool,address,IAaveIncentivesController,uint8,string,string,bytes), sem construtor de cinco argumentos. Getter getIncentivesController retorna interface IAaveIncentivesController e nao e virtual; harness snapshot retorna address, mudou imports e adicionou rayWadMul. Variantes sao historicamente diferentes e nao podem ser combinadas automaticamente.

**Scripts B1 de epoca, sem executar:** https://github.com/aave/protocol-v2/blob/750920303e33b66bc29862ea3b85206dda9ce786/runStableTokenCLI.sh chama StableDebtTokenHarness --solc solc6.8 --verify StableDebtTokenHarness:specs/StableDebtToken.spec --settings -assumeUnwindCond. https://github.com/aave/protocol-v2/blob/750920303e33b66bc29862ea3b85206dda9ce786/runUserConfigCLI.sh chama UserConfigurationHarness --settings -useBitVectorTheory. https://github.com/aave/protocol-v2/blob/750920303e33b66bc29862ea3b85206dda9ce786/runVariableTokenCLI.sh chama VariableDebtToken junto a LendingPoolHarnessForVariableDebtToken, link POOL e settings -assumeUnwindCond,-useNonLinearArithmetic. A fonte declara pragma 0.6.12, enquanto o script imprime solc6.8: alias/binario efetivo nao foi comprovado; nao fazer suposicoes de compilabilidade.

**Leitura documental B2:** PDF 25 paginas e N.md de 26 propriedades inspecionados. Os dados de familia e simplificacoes no PDF nao provam executabilidade deste snapshot nem associacao nominal inequivoca a cada rule.

**Buscas negativas:** nenhuma evidencia de runner CLI/solc, logs de cada regra ou versao do contrato initializer que tenha sido a mesma compilada no commit auditado. Nove incomplete permanecem UNRESOLVED_HISTORICAL_SOLIDITY. Dezessete complete sao lexicalmente DOCUMENTED, porem ABI/receiver/target e semantica nao demonstrados; nao ready.

**A1/A2:** https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html.
