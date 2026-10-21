# P13 — registro de buscas delimitadas, 2026-10-19
## Fontes verificadas
1. Snapshot Web3Bugs, contracts/13/certora/verify.sh: solc7.5, Brownie OpenZeppelin 3.4.0, compound-finance e interfaces. Evidencia somente paths declarados, nao package hash.
2. Snapshot contracts/13/certora/scripts/applyHarness.sh: patch de Constants.sol internal constant para public constant. Scripts disponiveis: runAccountPortfolio, runSettlement, runValuation, runActiveCurrencies, runPortfolio, runDateTime, runLiquidityCurve, runAccountContext, runGovenanceOwner, runSanity, verify.sh; configs .conf ActiveCurrencies, SetAccountContext, GovernanceOwner.
3. Comando: find contracts/13/certora -maxdepth 4 -type f | grep -E '(\.sh|\.conf)$'. Resultado: nenhum runBalances.sh na lista. Ausencia nesta arvore apenas.
4. GitHub code search, escopo experimental repository_name=notional-finance/notional, consultas Balances.spec e AccountPortfolioHarness: zero resultados indexados. O escopo pode ser incompleto/incorreto; nao concluir que a origem inexiste.
5. PDF Notional1Nov2021.pdf e docs/spec_catalog_project_13.md versus results/spec/spec_buglabel.csv: 7 VERIFIED descritos em texto antigo contra 5 no indice atual. #32/#34 NOT_STATED no indice.
## Estado
Busca delimitada do snapshot e consultas publicas acima encerrada sem nova fonte de hashes/ABI. A versao exata da instalacao Brownie, harness ABI historica e alvo para dez regras Balances ainda podem existir em artefatos de mantenedores nao disponiveis. Bloqueio e insuficiencia documental, NAO impossibilidade tecnica. Sem inserir novas especificacoes.
