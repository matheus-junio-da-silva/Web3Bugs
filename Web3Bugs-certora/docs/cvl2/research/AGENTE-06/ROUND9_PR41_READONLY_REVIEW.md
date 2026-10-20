# AGENTE-06 — RODADA 9 / PR #41 CONTRARREVISÃO SOMENTE LEITURA

Repositório https://github.com/matheus-junio-da-silva/Web3Bugs; PR #41 AGENTE-07. HEAD lida **dc737f6470041d1422ca86e4c4594607fdb57a28**, Draft, sem merge. Revisão de coordenação de 20/10/2026 confirmou 156 casos (P8 42, P9 61, P11 16, P20 37), documentação íntegra e nenhuma compilação CVL2 R8. Apenas leitura de GitHub: **nenhum checkout, edição, comentário, push ou alteração da branch AGENTE-07**. Não executar Prover nem atribuir vacuity histórica com base em fórmulas isoladas.

## P8 / três testemunhas documentadas

- **W1, 22 originais incomplete/8/14–35** (uma amostra textual relida na R8/9): N.spec incomplete/8/14.spec linhas 49–54 tem no MESMO ghost rayMul_g dois axiomas universais. Substituindo x=1 e y=0, rayMul_g(1,0)==0 e 1<=rayMul_g(1,0): contradição matemática. Fonte original informada pelo AGENTE-07: contracts/8/specs/fees_LEQ_ATokenBal.spec:26–33, lastVaultBal_LEQ_ATokenBalThis.spec:20–27, positiveSupply_imply_positiveAssets.spec:29–36. Os 22 exemplos são atribuídos por sua matriz R8, não se reexecutaram 22 funções.
- **W2, incomplete/8/1.spec linhas 34–35:** axioma universal de mulDiv_g no ramo rounding=1, x=y=denominator=0 implica 0 < 0, independentemente do valor do ghost.
- **W3, mesmo N.spec linhas 43–45:** axioma rayDiv_g com x=y=0 implica 0<0; o termo y/2 é 0/2 válido, NÃO é divisão por zero.

**Fatos estabelecidos:** as fórmulas, se axiomas globais universais assumidos simultaneamente nos seus domínios, são inconsistentes. **Não demonstrado:** que o job histórico carregou/ativou estes axiomas no mesmo scope de cada rule, que ghosts foram invocados pelo resumo de methods, nem que a propriedade VERIFIED foi provada vacuamente. A versão e flags do Prover, hooks, invariant base/preservation, init_state, summons de método f, summaries e alcance dos paths precisam ser reconstruídos. Em especial init_state axiom de outro ghost no N.spec W1 não equivale ao axiom global da testemunha W1. Os outros 19 P8 estão sem essas testemunhas específicas, mas não se provaram consistentes.

**Próximo experimento exclusivamente proposto:** coordenador autorizar estudo de alcance de axiomas por scene versionada; distinguir teste derivado de consistência aritmética de execução Certora histórica. Nunca modificar axiomas, require ou domínio em originais para tornar satisfatível; não rodar Prover sem gate.

## Outros riscos do peer review

P9: arquivos candidatos Mento-core com três Git blobs de interfaces e remapping da revisão Celo posterior não fixam o gitlink no audit runner. Accounts phase2 ABI Solidity (40 funções) não é a ABI autenticada do AccountsHarness. P20: applyHarnesses.sh edita cinco Solidity, inclusive try/catch e chamadas externas; MAX_INT de compoundStrategyAdditional.spec:65 sem definição no próprio arquivo não herda automaticamente definitions de arquivos irmãos. P11: closure textual do lock não autentica report SHA, hooks e execução. Nenhum dos quatro projetos recebeu equivalência CVL1→CVL2 ou status MIGRATED_COMPLETE.

**Parecer:** CONTRADIÇÕES FONTE confirmadas condicionadas à ativação; **VACUIDADE HISTÓRICA NÃO PROVADA**; 156 exemplos continuam sem CVL2 validado. PR #41 permanece Draft e intocado por este agente. A integridade deste parecer é documental, não revisão de solc/Prover.

AGENTE-06 — RODADA 9 / CONTRARREVISÃO.
