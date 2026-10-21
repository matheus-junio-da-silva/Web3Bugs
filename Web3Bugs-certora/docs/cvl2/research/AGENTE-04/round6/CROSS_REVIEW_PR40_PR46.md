# AGENTE-04 — RODADA 6 — Auditoria cruzada somente leitura PR #40 / #46

Revisadas HEADs Draft: PR #40 (AGENTE-05) f9a9c7d8167a532b9f2b534bc38e1e9f57c035d7 e PR #46 (P19 mathint) 62754c10e3e9dc23d122aad3333eac2ec60f817d. Nenhuma edição, comentário ou merge nesses PRs.

**P7 / PR #40:** P7/complete/36,41,47,63,73 retornaram compilation-only EXIT 1 no CVL2 por selectors sem sig:. Os métodos disAllowedFunctions presentes na ABI revertem OPERATION_NOT_SUPPORTED; a existência de seis métodos na seleção residual da ABI não demonstra que a regra seja satisfatível nem que não haja vacuity. P7/37,65 compilaram apenas como fragmentos, enquanto o CVL integral falhou por methods/hooks/ghosts e outros constructos. O commit auditado de 2022 é diferente do snapshot e não tem as mesmas rules. Nenhum claim de equivalência indevido foi observado no relatório conservador do AGENTE-05.

**P19 / PR #46:** as duas cópias derivadas de divPrecisely(uint,uint) para divPrecisely(mathint,mathint) compilaram no experimento anterior, mas RCPT=0 continua permitido; a segunda divisão da spec torna-se divisão matemática por zero. Coerções intermediárias CVL1 (RC*1e18) e comportamento de mathint/0 entre versões não foram comprovados. A inclusão estrita entre conjuntos de falhas das **duas assertions** no subdomínio RCPT>0 não prova equivalência de cada assertion entre CVL1 e CVL2. Conservar ambas 02_unresolved, sem requerer RCPT>0, casts restritivos ou retocar asserts.

Conclusão: 4 compilações globais anteriores de escopo limitado não demonstraram SEMANTIC_PROVEN. Sem Prover, CVL1 ou alterações nas branches alheias.

**AGENTE-04 — RODADA 6**
