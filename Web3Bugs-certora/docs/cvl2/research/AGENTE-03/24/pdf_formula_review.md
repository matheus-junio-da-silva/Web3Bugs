# Rocket Joe — leitura direta do PDF correto em 21 páginas

SHA256: f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4. Parser de texto PDF por página sobre os bytes do arquivo em resources/24, não mera cópia da matriz. Commit formalmente auditado: ef2ef30248661b5509c52ab30af9bd0fc07f6657.

## Escopo por página

- p1: intervalo janeiro a março de 2022, SHA auditado ef2ef302 e quatro contratos.
- pp2-4: achados manuais e distinção entre prova por regra e escopo da especificação.
- p4: símbolos do relatório e interpretação dos Hoare triples e propriedades relacionais.
- pp5-6: modelo LaunchEvent, simplificações (loops no máximo uma iteração, WAVAX confiável, inicialização, libs e Joe-core, bypass de _safeTransferAVAX com risco de reentrância omitida).
- pp7-13: estados sempre/open/closed/openStopped/closedStopped e transições.
- pp13-16: regras de alto nível, incluindo precedências e fronteiras de regras de frontrunning.
- pp16-20: Staking, saldos, recompensa, propriedade temporal, emergência.
- p21: regras não implementadas, premissas de init/emergency e timeouts.

## Divergências e verificações individuais

- **#2**: p13 same-sender deposit equivalence vs CVL different-sender and equal-start-balances.
- **#5**: p14 deposit front-run PDF includes a withdraw-oriented postcondition, unlike CVL deposit +msg.value.
- **#7**: pp14-16 mention withdrawAVAX front-running only, not withdrawLiquidity; source ID7 no named PDF counterpart.
- **#147**: p17 equality == in PDF vs >= in CVL, with preserved sender guard.
- **#150**: pp17-18 printed userBalance_ variables within RJPS proof vs RJPS_pre/post used in source.
- **#12**: No report name; active exists dt implication can be vacuous.
- **#13**: No report name; exists dt temporal implication can be vacuous.
- **#152**: pp18-19 reward exists t, p21 timeout footnote; commented min-interval assertion inactive.
- **#154**: p19 active exists dt implication; direct strict-reward comparison commented.
- **#163**: p20 footnote nonreversion cannot be independently proven; source requires lastReverted false.
- **#164**: No report name; reachability assert false probe.
- **#1**: p13 formula; CVL adds preserved safeAssumptions and equal sender restriction.

Preservar fórmulas literais no N.spec, sem promover Result ou Detection Outcome a partir do PDF. Detalhes por exemplo em properties/incomplete/N.md e source_provenance_matrix.csv.
