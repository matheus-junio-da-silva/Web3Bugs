# AGENTE-06 / P17 / E-A2-HAVOC

Tier A2: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html
Section: Havocing local variables, consultado 2026-10-19 (latest não pinado).

Only havoc ghosts/ghost functions in CVL2; locals need fresh variables after review.

Este é um padrão para investigar, NÃO uma classificação de mudança de todos os exemplos. Atribuir somente após leitura literal da propriedade, ABI, dependências e controle de vacuity. Alternativa conservadora: manter UNRESOLVED_CANDIDATE.
