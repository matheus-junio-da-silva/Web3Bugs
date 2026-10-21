# Auditoria cruzada AGENTE-05: PR #40 e PR #46 — SOMENTE LEITURA

Realizada somente após as prioridades P12, P15 e P2, usando comentários recentes do GitHub, documentação do PR e painel coordenador #47. Nenhuma alteração, comentário, execução remota ou push nas branches alheias.

## PR #40 — HEAD 21adc9551d7bf6aa979486e34a11d1f26f4909f5

Fonte: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40. O coordenador e o AGENTE-05 documentaram no P7/complete/37 e /65 duas compilações apenas das **N.spec extraídas**, usando snapshots Solidity e CLI 8.19.0. As duas specs CVL globais completas retornaram EXIT 1, em parte por methods, hooks, invoke e outros trechos CVL1. No P7/37, o solc auxiliar reportou Stack too deep e fallback de autofinder, mesmo tendo o CLI encerrado com exit 0.

A execução sobre o fragmento comprova somente que ele atravessou parsing/typechecking na cena efetiva indicada; não fecha hooks, ghosts, methods, summaries ou imports e não reproduz o auditado de janeiro/2022. O SHA auditado aave/aave-v3-core a87d546 não contém as duas rules integrityDelegationWithSig do snapshot posterior. P7/3 continua especialmente sensível a hook sobre balance e summary externo de handleAction; métodos universais e reverts demandam prova de não vacuidade.

**Risco:** chamar P7/37 ou /65 SEMANTIC_PROVEN ou MIGRATED_COMPLETE seria indevido. O PR #40 marca corretamente o caráter provisório e permanece Draft. Não foi identificada promoção indevida nas versões revisadas. Para P7/41,63 e depois 36,47,73, falta análise de selector, method f, global rule e cena.

## PR #46 — HEAD 62754c10e3e9dc23d122aad3333eac2ec60f817d

Fonte: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46. O experimento autorizado alterou exclusivamente os argumentos formais de divPrecisely de uint,uint para mathint,mathint em duas specs derivadas, cada uma com assert diferente. Compilaram em cenário anterior no CLI 8.19.0, mas a definição aritmética divide por um resultado RCPT que **pode ser zero**, sob premissas originais. Em mathint/0, o comportamento operacional relativo CVL1/CVL2 não foi estabelecido com fonte histórica suficiente.

A dedução matemática sob RCPT > 0 comparando dois conjuntos de falhas das assertions distintas (V1 contido estritamente em V2) não demonstra que o universo dos contraexemplos CVL1 é igual ao CVL2 para qualquer uma delas. Além disso, RC multiplicado por 10^18 pode exceder uint256 mesmo quando quociente final é representável, tornando coerção histórica relevante. Não introduzir require RCPT>0 para evitar divisão por zero nem cast que filtre casos.

**Risco:** transformar COMPILE_OK + CI estrutural em VERIFIED/EQUIVALENT seria indevido; a manutenção da categoria 02_unresolved para ambos os exemplos está fundamentada e preserva a ausência de prova. Não houve execução nova de CVL1, CVL2 ou Prover por esta auditoria.

**Conclusão:** 4 compilações anteriores do painel #47 têm escopo restrito e representam 0 equivalências provadas. Essa separação de gates foi observada corretamente nos PRs #40/#46; não requer edição na branch de outro agente.
