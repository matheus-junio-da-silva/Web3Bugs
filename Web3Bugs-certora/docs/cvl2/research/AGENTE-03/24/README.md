# AGENTE-03 — Fase 1, pesquisa pré-migração CVL2: Project 24 Rocket Joe

- Baseline Web3Bugs/main `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` (confirmado). PropertyGPT/main `687f654c679ed45ab127b7949e2a29c8f5e491b9` (confirmado).
- Source: Project 24 Rocket Joe, 164 exemplos, **0 complete / 164 incomplete**, chaves únicas (24,incomplete,ID).
- Inventário por CVL original: LEHighLevel.spec: 10; LEInProgress.spec: 3; LEPreset.spec: 1; LEValidStates.spec: 35; LEVarTran.spec: 19; LaunchEvent.spec: 76; Staking.spec: 19; sanity.spec: 1. Oito arquivos fonte CVL, 15 Solidity e PDF histórico errado preservados no snapshot.
- Audited commit Rocket Joe: `ef2ef30248661b5509c52ab30af9bd0fc07f6657`. Os contratos arquivados LaunchEvent e RocketJoeStaking diferem do auditado.
- PDF Rocket Joe correto: [Certora_Formal_Verification_Report_Rocket_Joe.pdf](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/resources/24/Certora_Formal_Verification_Report_Rocket_Joe.pdf), SHA256 f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4 (hash documental da proveniência).
- O PDF OpenZeppelin incorreto em contracts/24/final-report-3.pdf NÃO fornece resultado Rocket Joe. **164 Result NOT_STATED** no catálogo; não reinstalar as antigas 53 atribuições VERIFIED.

## Arquivos desta entrega

- [properties.csv](properties.csv) — 164 identidades originais com status e evidência.
- [properties/incomplete/](properties/incomplete/) — 164 dossiês originais por ID.
- [patterns/](patterns/) — 10 análises CVL2 condicionais.
- [evidence_register.csv](evidence_register.csv) — 17 fontes e bases.
- [recovery_manifest.csv](recovery_manifest.csv) — 5 grupos de dependências.
- [QA_REPORT.md](QA_REPORT.md) — conferências de contagem, riscos e limitações.

## Estado

**164 UNRESOLVED_CANDIDATE (PROVISÓRIO)**. Import ../helpers/erc20.spec, Joe/Dummy harness, Certora .conf e sua identidade de versão não demonstrados. Os ajustes textuais de methods, selector, mathint, imports e invariants são apenas hipóteses fundamentadas, não prova de compilação.
A árvore do auditado tem 94 entradas sem specs/harness de Certora. Hardhat 0.8.6 e OpenZeppelin ^4.4.1 não definem a execução Prover.
O PDF correto foi analisado via proveniência pré-existente e página oficial; não foi reproduzida inspeção integral página a página nem execução formal nesta fase.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
