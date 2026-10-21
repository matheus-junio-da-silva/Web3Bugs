# AGENTE-06 — P22 Popsicle V3 Optimizer / Fase 1 (inventário inicial)

Baselines verificados em 2026-10-19: Web3Bugs 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3, PropertyGPT 687f654c679ed45ab127b7949e2a29c8f5e491b9. O commit do código efetivamente auditado é NÃO_CONFIRMADO.

| Status histórico | Exemplos únicos | Relações Bug Label |
|---|---:|---:|
| complete | 19 | 19 |
| incomplete | 2 | 2 |
| Total | 21 | 21 |

A chave é (Project ID, Status, Example ID), não property name. Risco específico: Archived runner selects only PopsicleV3Optimizer.spec with solc7.6 and links. PoolActionsWrapper totalSupply is private, not an external getter.

**AVISO DE ESCOPO:** esta entrega é o inventário documental rastreável, não a pesquisa semântica integral. Cada property está explicitamente marcada INCOMPLETE_RESEARCH, sem recomendações de alteração textual não suportadas.

Arquivos: properties.csv, properties/, patterns/, evidence_register.csv, recovery_manifest.csv, QA_REPORT.md.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## Atualização 2026-10-19 / escopo real da Fase 1

A triagem inicial foi ampliada por leitura documental dos N.spec, N.md, N.sol e N.txt e de PDF preservado onde disponível. A cobertura de leitura é 21/21; **cobertura de equivalência ou verificação da rule não é 100%**. Nenhuma conversão foi aprovada, nenhuma execução CVL2 foi realizada. Veja QA_REPORT.md, evidence_register.csv, recovery_manifest.csv e PDF_SOURCE_ANALYSIS.md quando disponível.
