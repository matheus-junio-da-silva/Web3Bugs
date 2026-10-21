# P14 — registro de buscas delimitadas, 2026-10-19
## Fontes verificadas
1. contracts/14/specs/scripts/applyHarnesses.sh lido sem execucao: perl substitutions em Controller.sol, MarginPool.sol, MarginCalculatorInterface, ERC20Upgradeable; altera observabilidade e modelo de prova.
2. contracts/14/specs/scripts/runOrderOfOperations.sh (linha 1) explicita ControllerHarness, libs/mocks, links e solc6.10.
3. contracts/14/specs/scripts/runNoBankruptcy.sh (linha 1) usa ControllerHarnessExtra, OtokenHarnesses, links e executavel nomeado solc (sem versao exata nesse comando).
4. contracts/14/specs/scripts/runMarginVault.sh (linha 1) usa MarginVaultHarness e executavel solc (tambem sem versao do binario).
5. 34 N.spec e 34 N.md, relatorio OpynGammaDec2020.pdf (pp. 5-15), sem executavel/ABI historico em cache da verificacao.
## Estado
Nao se fez mutacao, solc, compilacao CVL ou replay. Scripts fornecem condicoes de reproduzibilidade plausiveis, nao um attestation do input que gerou o PDF. Buscar novamente apenas se surgir checksum do codigo pos-script, ambiente de auditor ou execucao gravada. Nao interpretar placeholders external|internal/RECEIVER como sintaxe CVL2 valida.
