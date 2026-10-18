# DELTA — auditoria semântica cruzada, rodada 2

**Escopo:** 177 decisões de instâncias CVL/target (Project 19: 37; Project 13: 58; Project 14: 34; Project 11: 16; Project 10: IDs 33–64: 32). **Data:** 18 de outubro de 2026. **Artefato auditável:** `delta_review.csv`, separador CSV padrão, UTF-8 com BOM.

## Escopo da conclusão

A matriz diferencia **avaliação do predicado CVL**, **classificação técnica proposta** e **atribuição histórica de resultado de prova**. `CONFIRMED` significa que a interpretação **limitada ao recorte recuperado** coincide com as evidências examinadas; não é nova prova nem aprovação do programa. `CORRECTION_REQUIRED` solicita decisão humana para mudança especificada. `INCONCLUSIVE` não significa falso, não significa livre de bugs e não constitui autorização para alterar o catálogo primário.

## Fontes e isolamento de versões

- **VM:** ZIP fornecido (`Web3Bugs.zip`), HEAD local `4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82`, **defasado** da atual main. Foram extraídos *read-only* os snapshots históricos das branches remotas do ZIP: `origin/catalog/p10-gaia-furucombo` (`16a0eb0...`), `origin/catalog/p11-helix-keep-fully`, `origin/catalog/p13-atlas-notional-finance-v2` (`d520dde...`), `origin/catalog/p14-boreal-opyn-gamma-protocol` (`b2de6ff...`). Não alegar que estas HEADs são iguais às HEADs atuais do GitHub.
- **GitHub via conector:** consulta da `main` atual aos índices `docs/spec_catalog_project_19.md`, `docs/spec_catalog_project_10.md`, às nove especificações CVL originais sob `contracts/19/spec/` e aos N.md de Furucombo IDs 37–64; consulta amostral a vários N.md de Origin. Sem clone local atual das fontes Solidity P19 e sem cópia binária do PDF Origin. Por isso P19 com evidência de PDF em várias linhas fica condicional e a coluna `cvl_sha256` deliberadamente não inventa hash local.
- **Relatórios PDF analisados da VM:** FurucomboMay2021.pdf (31 pp.), KeepFullyBackedBondingNov2020.pdf (12 pp.), Notional1Nov2021.pdf (16 pp.), OpynGammaDec2020.pdf (19 pp.). Texto extraído via `pdftotext -layout` para alinhamento com descrição, com atenção a ✔, ✔*, ✍ e 🔁; fonte PDF histórica continua prevalecendo sobre os resumos em `N.md`. O PDF OriginFeb2021.pdf (9 pp.) não estava no ZIP; as referências P19 usam reconciliação do catálogo e texto remoto, não um exame independente pixel a pixel.
- **Categorias:** `docs/standard.md`: O (fora de escopo), L (oracles gerais), S (oracles semânticos). `UNMAPPED` é sentinela de ausência de classe defensável e não categoria oficial da taxonomia. Não classificar uma property diagnóstica como vulnerabilidade sem falha normativa.

## Totais por projeto e decisão

| Projeto | Escopo | CONFIRMED | CORRECTION_REQUIRED | INCONCLUSIVE |
|---|---:|---:|---:|---:|
| 19 — Origin OUSD | 37 | 12 | 1 | 24 |
| 13 — Notional Finance V2 | 58 | 0 | 0 | 58 |
| 14 — Opyn Gamma Protocol | 34 | 19 | 1 | 14 |
| 11 — Keep Fully Backed Bonding | 16 | 12 | 0 | 4 |
| 10 — Furucombo | 32 | 0 | 4 | 28 |
| **Total** | **177** | **43** | **6** | **128** |

## Adjudicações prioritárias

1. **Opyn #1, `orderOfOperations` — CORRECTION_REQUIRED, P1.** O ramo `f1.selector > f2.selector` executa `assert true`. Somente o outro ramo verifica igualdade de `getVaultCollateralAmount(owner,vaultId,0)` ao inverter duas invocações. A propriedade não afirma equivalência de todo o storage, nem vale para todos os pares/sequências; classificar como `S3-2` sem esta ressalva confunde um *campo* com todo o estado. A revisão propõe `UNMAPPED` até o orquestrador estabelecer uma classificação derivada da propriedade restrita. O ✔* textual de ordem não dá `VERIFIED` individual a esta instância.
2. **Origin #35, `privilegedOperation` — CORRECTION_REQUIRED, P1.** `!(firstSucceeded && secondSucceeded && thirdSucceeded)` restringe três coexecuções em *mesmo pré-estado*, mas não comprova que um usuário arbitrário controla `VaultStorage.strategistAddr` ou `governor`. Rotular automaticamente `S5-1` seria erro de causa-raiz. Proposto `UNMAPPED` até mapear métodos, identidade de roles e consequência de sucesso. A versão com dois usuários (#32–34) também não identifica o autorizado.
3. **Keep #11, `noFrontRunningOnWithdraw` — CONFIRMED com limite explícito, P1.** `succSceanrio1` é calculado e descartado, `assert succSceanrio2` é incondicional. A segunda chamada pode reverter por caller não autorizado, amount maior que saldo ou locks e `f` pode modificar também o operador original. O ✔ da formulação relacional no PDF **não** se propaga à rule. Resultado individual preservado como `NOT_STATED`, rótulo `UNMAPPED`.
4. **Origin #17–22, wrappers de transferência — INCONCLUSIVE, P1.** `assert true` final é somente wrapper. As condições materiais se encontram em `transferCheckEffects` e nos helpers especializados, que dependem de ratio, sender, nonrebasing e métodos simulados. Não catalogar a tautologia como prova nem descartar as assertions internas.
5. **Origin #6 — CONFIRMED (divergência necessária de relatórios), P1.** A propriedade ativa testa `totalSupply() >= rebasingCredits*ONE()/rebasingCreditsPerToken + nonRebasingSupply`; a declaração violada no PDF afirma **igualdade**, logo não é o mesmo teste. Manter `NOT_STATED`, não projetar `VIOLATED`.
6. **Origin #27, `additiveBurnRanges` — INCONCLUSIVE, P1.** A assertion admite `diff < 1000000`, não additivity exata; seus bounds de créditos são indispensáveis à interpretação. `UNMAPPED` não é automaticamente necessário, mas a tese de igualdade irrestrita seria incorreta.
7. **Origin #30, `sum1Test` — CONFIRMED como diagnóstico não normativo, P1.** Após `require c1` significando saldo alterado, exige que seja igual ao anterior. Se o preestado e f tornam c1 alcançável, há contradição lógica deliberada; não é uma propriedade de conservação de saldo demonstrada.
8. **Furucombo #37–64 — INCONCLUSIVE, incluindo 8 casos P1.** São quatro regras (`transferredTokensMeanThatStackIsUpdated`, `approvedTokensAreTemporary`, `tokenMovementCorrectness`, `noOtherPartyModified`) repetidas nos 7 targets HMaker, HAaveProtocol, HAaveProtocolV2, HSCompound, HFunds, HOneInchExchange e HBProtocol. `HAaveProtocol` e `HOneInchExchange` não têm a implementação histórica no snapshot; versões V2/V5 são substitutos inválidos. Um resultado de tabela do PDF não se transfere ao par propriedade × handler. A spec usa mocks/summaryInstance, e o driver altera fonte e interfaces; ABI e contexto `delegatecall` devem ser verificados.
9. **Furucombo #33–36 — CORRECTION_REQUIRED, P1.** As quatro fontes em `N.md` não apresentam seção independente `Why the Solidity excerpt is relevant`, confirmada também na main atual. #33 verifica `lastHasThrown` (não `lastReverted`), #34 verifica `lastReverted` mas exclui `getParams(bytes32)`, #35 é diagnóstica `assert false` sem target/driver, #36 verifica `summaryInstance.checkDelegated(getProxyActions())` além do limite de três pushes. A main atual mantém #33–34 como complete restrito e #35–36 como incomplete; o ZIP antigo ainda exibe os dois últimos como complete, e isso **não** foi propagado aos caminhos da matriz.
10. **Notional #1, #37 e #58 — INCONCLUSIVE, diagnósticos.** `assert false` após método simbólico testa alcançabilidade, não corrupção contábil. Regras no PDF são descritas em linguagem de negócios e há alternativas de mock de mercado; as 7 marcações `VERIFIED` catalogadas não são novas execuções nem garantias independentes da instância extraída.
11. **Keep #3–7, ✔*.** O símbolo designa simplificações/hypotheses e não prova de produção; fontes `@keep-network` e OpenZeppelin externas ausentes. Mesma cautela para os demais 16 exemplos `incomplete`.

## Próximas decisões para o orquestrador

- Adjudicar `UNMAPPED` para Opyn #1 e Origin #35 ou substituir por rótulo estritamente vinculado a assertions específicas, sem mudar os arquivos originais nesta rodada.
- Em P19, descarregar a `main` atual com `.spec`, `.sol`, scripts e PDF com SHA auditável; conferir todos os 37 `N.spec` e os nós de helpers por execução da análise estática. Esta rodada realizou leitura das nove fontes CVL originais e dos metadados por propriedade, mas **não** a verificação integral de cada fechamento de Solidity ou PDF visual.
- Em P10, recuperar build e scripts históricos de 2021, testar ABI após o harness/driver, estabelecer para cada target se `summaryInstance` foi corretamente associado. Não converter 23 handlers em 23 resultados verificados.
- Para Notional/Keep, exigir o conjunto completo de imports e versões compiláveis antes de promover `incomplete` a `complete`; não confundir ausência de solc com fonte externa realmente ausente.

**Nenhuma alteração foi feita nos `N.md`, specs, contratos, PDFs ou classificações primárias do repositório. Nenhum Prover foi executado. Nenhum merge foi realizado.**