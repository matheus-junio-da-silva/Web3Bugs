# ATLAS — adjudicação P8 #1, P19 #35 e P15 balance_after_burn

**Data:** 2026-10-18. **Baseline:** Web3Bugs main commit 80f551f23bbd86d7901c6a28e7f44c68aebae8fd. **Branch:** fix/semantic-p08-p15-p19-atlas. **Status:** parecer independente DELTA recebido e aceito para OUSD #35; validação da branch atualizada em andamento; sem merge.

## Inventário de alterações e tipologia

| Projeto/ID | Tipo de intervenção | Antes | Depois | Fundamento |
|---|---|---|---|---|
| P8 #1 accrueYieldCheck | RESULT_OUTCOME_CHANGE; DOCUMENTATION_FIX; EVIDENCE_GAP | Result VERIFIED; Outcome NO_FINDING | Result VERIFIED; Outcome INCONCLUSIVE | W2/W3 contraditórios quando as fórmulas são quantificadas literalmente; não-vacuidade e configuração histórica não demonstradas |
| P19 #35 privilegedOperation | LABEL_CHANGE confirmado por DELTA; DOCUMENTATION_FIX; EVIDENCE_GAP | S5-1; Result/Outcome NOT_STATED | UNMAPPED; Result/Outcome NOT_STATED | f arbitrário sem filter, três chamadas de senders distintos; nenhuma assertion de storage privilegiado; contrarrevisão DELTA confirmada |
| P15 #59 balance_after_burn (PDF #54) | RESULT_OUTCOME_CHANGE; DOCUMENTATION_FIX; EVIDENCE_GAP | VERIFIED / NO_FINDING | NOT_STATED / NOT_STATED para a rule do snapshot | PDF diz aumento após burn; CVL e Solidity exigem diminuição |
| Três itens | DEPENDENCY_FIX | fontes originais incompletas | **nenhuma mudança de dependência** | Não preencher stubs, nem alterar scripts, bibliotecas, CVL, Solidity ou PDF |

Os valores Result/Detection Outcome no CSV compartilhado foram reconciliados com os respectivos N.md em exatamente três instâncias. Não houve alteração das 22 entradas W1 (Vault #14–35), nem das 115 outras propriedades GHO.

## P8 #1 — prova histórica versus soundness da teoria

Arquivo original: contracts/8/specs/accrueYieldCheck.spec (rule linhas 39–45). Target nominal ATokenVault. O relatório AAVE Vault menciona verificação histórica; não contém replay por rule e por conjunto de axiomas na versão disponível. A propriedade demanda monotonicidade de getAccumulatedFees depois de accrueYield(e). Isso seria falsificado por um decréscimo concreto sob execução elegível.

* **W2, no mesmo arquivo:** ghost mulDiv_g e summary mulDiv envfree, axioma universal estrito x*y < mulDiv_g(x,y,denominator,rounding)*denominator+denominator. Com x=y=denominator=0 e rounding=0, reduz a 0<0. O ramo rounding=1 também força 0<0 com o mesmo denominador zero.
* **W3, no mesmo arquivo:** ghost rayDiv_g e summary rayDiv envfree. O axioma x*RAY()-y/2 < rayDiv_g(x,y)*y, para x=y=0, exige 0<0. Isso não depende de RAY.
* **W1, em outras três specs:** em fees_LEQ_ATokenBal, lastVaultBal_LEQ_ATokenBalThis, positiveSupply_imply_positiveAssets, o axioma ((x==0||y==0)=>rayMul_g(x,y)==0) E x<=rayMul_g(x,y) exige simultaneamente rayMul_g(1,0)=0 e >=1. É um risco para os contextos arquivados dos exemplos #14–35, não um axioma inserido na rule #1.

A contradição prova que uma interpretação universal irrestrita desses axiomas é insatisfatível; NÃO prova que o Prover histórico efetivamente executou a rule com exatamente esse modelo nem que o Solidity incorre em bug. Portanto manter **Historical result reported: VERIFIED**, mas substituir NO_FINDING por **INCONCLUSIVE** para a atribuição atual de Detection Outcome. O label S3-2 e o status incomplete não mudam. Pendências P0: config/CLI e target efetivo; satisfiability check dos axiomas; Prover model check não-vácuo; versionamento/harness e logs originais.

## P19 #35 — ausência de ligação ao estado privilegiado

Source: contracts/19/spec/PrivilegedVaultAdmin.spec:1–26. Target histórico declarado VaultAdmin (report Origin OUSD, review SHA 5c702edbefb451287805918c3275535c11654074). Regra sem filtered methods: f pode designar selector que não requer privilégio. Require privileged1 != privileged2, sender1=privileged1, sender2=privileged2, sender3 diferente de ambos. Embora arg2 seja declarado, a segunda chamada reutiliza arg da primeira. Terceira usa arg3. Armazena preestado initialStorage=lastStorage; a primeira chamada não explicita at initialStorage; segunda e terceira explicitam.

A assertion nega firstSucceeded && secondSucceeded && thirdSucceeded, em que cada succeeded é !lastReverted. Não há leitura ou comparação de strategistAddr, governor, nem de pós-estados. Um f público que conclua para três remetentes distintos oferece um contramodelo compatível com ausência de falha de privilégios. O Solidity VaultAdmin contém onlyGovernor, onlyGovernorOrStrategist e onlyVaultOrGovernor, mas nenhum está vinculado a f por filter na regra.

O label S5-1 em docs/standard.md exige mutação arbitrária de estado privilegiado por usuário. A regra não demonstra tal mutação. Proposta defendida: **S5-1 → UNMAPPED**, classificação de diagnóstico sem oráculo de exploit. Resultado histórico NOT_STATED e Outcome NOT_STATED permanecem. **Adjudicação final de rótulo:** DELTA realizou contrarrevisão independente e concordou expressamente com UNMAPPED no comentário https://github.com/matheus-junio-da-silva/Web3Bugs/pull/31#issuecomment-6256562964. A concordância é restrita a P19 #35; não implica reprodução histórica do Prover.

## P15 #59 — divergência adicional CERES, PDF #54

Arquivo original contracts/15/ghoToken.spec:425–438, rule balance_after_burn. Target GhoToken; revisão oficial ce49fb0c94cfebf0159222ceb288e4f9a55d305f; relatório original de 13 páginas, página **11**, regra numerada **54**. O PDF tem marca ✔ nominal mas afirma na prosa que burn aumenta saldo e supply. O predicado real requer:

~~~cvl
assert initBalance == finBalance + amount;
assert initSupply == finSupply + amount;
~~~

Isso implica diminuição de ambos por amount. A regra também aplica requireInvariant inv_balanceOf_leq_totalSupply(e.msg.sender). Solidity GhoToken.burn(uint256) decrementa bucketLevel e chama ERC20._burn(msg.sender, amount). O PDF e a CVL discordam na direção da mudança. Um match de nome e commit não sana a divergência sem a captura individual do Prover/errata.

**Decisão:** preservar o fato de que o **PDF reporta ✔ na propriedade #54**, mas classificar **Result=NOT_STATED e Outcome=NOT_STATED** na atribuição à source rule #59 até que se demonstre qual fórmula o Prover realmente executou. Não reescrever o CVL. Não deduzir vulnerabilidade Solidity. Trata-se de divergência CERES adicional, não integrante dos 114 apontamentos originais de outras revisões.

## Quadro individual de 64 atribuições VERIFIED originais

Arquivo de evidências: [atlas_gho_verified_64.csv](./atlas_gho_verified_64.csv), com **64 linhas únicas** para source rules do GHO que tinham originalmente VERIFIED; cada linha contém: ID de exemplo e item numerado PDF, marca nominal, página e descrição extraída do PDF original, predicado executável CVL, require/requireInvariant, contextos CVL importados, target/contrato Solidity, SHA de versão histórica, assumptions, driver e harness ausentes, relação semântica da fórmula, suficiência probatória, Result atual, Outcome e decisão.

**64/64 correspondências de nome ao PDF comprovadas** (incluindo a linha #65 quebrada no PDF). **63** continuam com Result VERIFIED como **atribuição histórica nominal e qualificada**, não como execução reproduzida; **1** (#54) foi reclassificada NOT_STATED por contradição de fórmula. O status semântico global dos outros 63 permanece INCONCLUSIVE quanto à equivalência total da fórmula/harness; isso **não** converte 63 VERIFIED em erros. Por padrão, o modelo do dataset mantém a versão final historicamente auditada, distingue resultados do PDF de bugs anteriores e não inventa findings.

Condições adicionais documentadas pela CERES em branch review/ceres-p15-gho-core-provenance: os 22 arquivos Solidity correspondem ao commit revisado; 8/9 specs correspondem, com ghoDiscountRateStrategy reduzida; harness, scripts, mock contracts, links, Makefile/munged patches e configuração de Prover não foram preservados no snapshot; Aave V3 Pool correto, setter-linked dependências e loops limitados são assumptions materiais. O confronto automatizado oferece CVL original e prosa individual do PDF para auditor humano, **não certifica sozinho a equivalência semântica** dos 63 itens.

## Evidências ainda faltantes / plano de encerramento

1. P0 Vault: scripts exatos da execução histórica e solver consistency check; runs por rule/target/versão; rastreio dos axiomas globais para a verificação #1 e 14–35.
2. P1 GHO: outputs do Prover e arquivos de configuração originais para as 64 propriedades; validação de cada fórmula/summaries/harness/versão; errata para #54 ou prova de que a própria fórmula da source foi verificada.
3. P1 OUSD: **DELTA CONCLUIU E CONCORDOU**: f não filtrado, arg2 declarado mas não usado, chamadas sobre preestado salvo, sem assertion sobre storage; possível falsificador benigno por getter público governor(). Sem execução Certora histórica; classificação UNMAPPED ratificada por DELTA.
4. P2: fechar bibliotecas externas não vendorizadas e reproduzir os drivers/munged, sem alterar sources históricas.

## Validações e CI

A evidência reproduzível dos comandos obrigatórios com SHA, data/hora UTC e códigos de saída está no arquivo [atlas_validation.log](./atlas_validation.log). Os quatro comandos do projeto são controladores estruturais; sucesso neles não implica Prover replay nem conformidade histórica da fórmula. PR draft separa correções do PR review-only da matriz de 192 casos. Nenhum merge solicitado.

## ATLAS — reconciliação com main após 14 merges (2026-10-18)

Main de referência: 9d0a65faf2ba378c131c956605580ee540da4cdc. A branch de correção incorporou essa main preservando integralmente os novos catálogos (inclusive P24 Rocket Joe). A comparação do CSV compartilhado com parser CSV mostrou 1.390 relações contra 1.390 na main, 17 colunas idênticas, ordem de linhas idêntica e somente três diferenças de valores:

- P8 #1: Detection Outcome NO_FINDING -> INCONCLUSIVE; Result VERIFIED histórico intacto; label S3-2 intacto.
- P19 #35: Bug Label S5-1 -> UNMAPPED; Result e Outcome NOT_STATED intactos; contrarrevisão DELTA inicialmente ausente, depois **PUBLICADA E FAVORÁVEL** no comentário #6256562964.
- P15 #59: Result VERIFIED -> NOT_STATED e Detection Outcome NO_FINDING -> NOT_STATED; label S6-4 intacto; marca ✔ histórica no PDF #54 p.11 preservada em documentação.

Outros 1.387 registros do CSV são idênticos à main, inclusive as 164 relações do Project 24. results/contests.csv contém 23 dados, results/bugs.csv contém 97 dados, ambos idênticos à main e não modificados pelo PR. Nenhum projeto fora dos três registros recebeu atualização do CSV nesta branch. O check_specs.py informa 1.386 exemplos e 1.390 relações; não confundir exemplos de spec com relações do CSV. Todas as 3 tabelas CSV têm a quantidade de colunas original em todas as linhas. Campos vazios já existentes no CSV grande referem-se a dados opcionais de dependência/contrato (nunca colunas extras).

A contrarrevisão DELTA foi recebida e sustenta a decisão UNMAPPED. A verificação final exige novo SHA, quatro comandos exit 0 e CI da nova HEAD antes de solicitar aceite do orquestrador. A ausência de Prover histórico, não-vacuidade Vault e vínculo de job individual GHO continuam limitações formais.

## DELTA — confirmação independente e resposta ATLAS

A contrarrevisão independente da DELTA foi recebida no PR #31: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/31#issuecomment-6256562964. DELTA leu PrivilegedVaultAdmin.spec, VaultAdmin.sol, VaultStorage.sol, Governable.sol e docs/standard.md e **concordou com S5-1 -> UNMAPPED**. O falsificador indicado é o getter público herdado governor(), selecionável como f no modelo sem restrição explícita de seletor: para três endereços distintos e calldata sem argumentos, as três chamadas podem não reverter embora nenhuma altere estado privilegiado. Mesmo sem reproduzir essa execução no Prover histórico, a rule não exige a mutação privilegiada necessária a S5-1. A ausência de filtro de métodos, o reuso de arg na segunda call (arg2 não usado), a semântica at initialStorage em calls 2 e 3 e o único assert de não-revert conjunto foram confrontados independentemente. Concordância DELTA abrange somente P19 #35, não as decisões P8/P15. **Resposta ATLAS: parecer aceito e label UNMAPPED ratificado sem exceções**. Result=NOT_STATED, Detection Outcome=NOT_STATED e status incomplete permanecem. Nenhuma prova de exploit foi produzida.
