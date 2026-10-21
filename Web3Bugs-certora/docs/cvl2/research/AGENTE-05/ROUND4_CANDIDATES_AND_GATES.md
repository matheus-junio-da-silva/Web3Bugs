# AGENTE-05 — Rodada 4: seleção de candidaturas, 148 exemplos e gates

Data: 2026-10-20. Branch `research/cvl2-agente-05`. Base imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
Esta atualização é **somente documental**. Estado detalhado individual, por chave `project_id/original_status/example_id`, em [ROUND4_148_EXAMPLE_PROGRESS.csv](ROUND4_148_EXAMPLE_PROGRESS.csv).

## Reconciliação de escopo e natureza dos testes

| Projeto | Exemplos | Complete | Incomplete | Compilação CVL2 comunicada anteriormente | Gate semântico |
| --- | ---: | ---: | ---: | --- | --- |
| 7 AAVE V3 | 74 | 46 | 28 | 37 e 65: `N.spec` fragmentados compilam no snapshot; specs globais integrais falham | ABI/runner histórico, EIP712, ghosts/summaries, vacuity |
| 19 Origin OUSD | 37 | 2 | 35 | 1 e 2: somente derivadas `mathint` de #46 compilam | equivalência histórica `divPrecisely`, inclusive divisão por zero |
| 6 Static AToken LM | 32 | 0 | 32 | nenhuma demonstrada | versões de fontes/PDF e dependências ausentes |
| 3 AAVE Rescue Mission | 3 | 0 | 3 | nenhuma demonstrada | submódulo histórico e link/runner/targets |
| 21 Lido DSM | 2 | 0 | 2 | nenhuma demonstrada | harness/helper faltante e divergência do PDF |
| **Total** | **148** | **48** | **100** | **4 casos com evidência limitada prévia, 144 sem compilação** | **zero casos com equivalência CVL1→CVL2 estabelecida** |

Na versão da matriz de pesquisa existente: 12 `DOCUMENTED_CANDIDATE`, 5 `UNCHANGED_CANDIDATE`, 131 `UNRESOLVED_CANDIDATE`; tais nomes não são buckets migrados. Os dois `P19/complete/1,2` são **`02_unresolved` na implementação experimental**, mesmo que o antigo `properties.csv` os registre com hipótese textual `UNCHANGED_CANDIDATE`. Nenhum `properties.csv`, CSV canônico ou resultado formal histórico foi modificado. Foram verificados os SHA256 dos 148 `N.spec` contra o ledger prévio; total e unicidade são asserts do script que gerou a nova matriz.

## Prioridade 1 — P7 closures locais, não migração autorizada

1. `P7/complete/41 nonceChangePermits` StableDebtToken e `P7/complete/63 nonceChangePermits` VariableDebtToken: ambos trazem `definition disAllowedFunctions` e seletor `delegationWithSig(...).selector`; mudança `sig:` é documentada no guia CVL2, porém a rule usa `method f` e `f(e,args)` paramétricos, requer confirmação de universo não vazio das funções elegíveis, ABI completa e interpretação de reverts, especialmente quando `f` chama `delegationWithSig`. Nada foi compilado.
2. `P7/complete/36 integrityTimeStamp` StableDebtToken: nenhuma definição de ghost ou `methods` incorporada ao recorte; depende da mesma definição de filtro e chamadas ao getter `getUserLastUpdated`. Exige confrontar ABI, `method f`, tempo simbólico e implantação; o recorte não substitui a spec original, que contém blocos globais.
3. `P7/complete/47` Stable e `73` Variable, `disallowedFunctionalities`: fonte de recorte local simples e `f@withrevert` explícito, mas os selectors `transfer/approve/allowance` podem não existir na ABI concreta. Se o conjunto filtrado for vazio, o `assert lastReverted` é vacuamente verdadeiro. Confirmar domínio de method-filter e não inventar ABI ou inserir métodos. Não promover por compilação isolada.
4. `P7/complete/33,40,43,61,62,70` contêm selectors adicionais, hooks, summaries, accounting e/ou `invoke`; `P7/complete/10` inclui `invoke`. Parecem transformações textuais localizáveis, mas têm closure global mais complexa: prioridade abaixo das regras 41/63/36/47/73.
5. `P7/complete/37,65` permanecem os únicos fragmentos P7 com compilação CVL2 observada; veja [ROUND4_INDEPENDENT_GLOBAL_CLOSURE.md](7/ROUND4_INDEPENDENT_GLOBAL_CLOSURE.md). `P7/complete/3` é **bloqueio de contexto concreto**, não `compile_ok`.

Essas prioridades são escolhas de **pesquisa**, não autorizações de criar specs derivadas nem de modificar `methods`, summary, `sig:`, receiver ou target. Uma atualização estritamente sintática não demonstra conservação do universo de contraexemplos.

## Prioridade cruzada: P6, P3, P21 e outros 35 P19

| Grupo | Melhor pista verificável | Fechamento faltante / decisão |
| --- | --- | --- |
| P3/1–2 Rescue LEND | Fork `bgd-labs/rescue-mission-phase-1@33c1aeca` com cinco Git blobs históricos comprovados (helpers, harness, scripts, patch). | Submódulo transitivo `lib/solidity-utils`, links LEND/AAVE, solc_map e correspondência com o target auditado não autenticados. Alto valor de pesquisa após recuperação exata, sem mock substituto. |
| P3/3 stkAAVE | Mesmo fork e PDF que distingue caso stkAAVE de LEND. | `StakedTokenV2Rev4`, token/reward links, configurações de runner e commit correto por fase ainda sem closure; não combinar resultados de fases. |
| P6/1–32 StaticATokenLM | Fonte `StaticATokenLM.spec` com 32 declarações, famílias agrupáveis para análise de aliases. | 0 complete; commit `ac92951` no transcript arquivado versus `51d46b1` em PDF público, ABI/harness e imports ausentes. Identidade de revisão deve preceder conversões de `methods`. |
| P21/1–2 DSM | Duas regras localizadas em `contracts/21/specs/DSM.spec`, inclusive `quorumLeGuardian`. | `DepositSecurityModuleHarness` e getter `getGuardianLength` ausentes; nenhum dos 18 nomes do PDF corresponde às duas regras. A desigualdade sobre quorum precisa de revisão do comportamento pretendido; não preencher getter nem alterar assertion por intuição. |
| P19/incomplete/3–37 | `ousd.spec` e demais fontes originais preservadas, `package.json/yarn.lock` fixam versões `@openzeppelin/contracts@2.5.0` e `@openzeppelin/upgrades@2.8.0`. | Reconstruir bytes das dependências fixadas, import closure e alterações exatas do harness OUSD antes de qualquer `--compilation_steps_only`. Diferentes targets devem continuar separados. |

**Ranking condicionado à evidência disponível**: P7/41 e 63 (local, com selector `sig:` verificável), P7/36, P7/47 e 73 para levantamento ABI/vacuity; P3 somente após baixar o submódulo autenticado; P19 incomplete somente após dependências versionadas; P6 e P21 permanecem historical_blocked. Nenhum deles recebe status de compilação positiva sem log de execução.

## P19 não repetir piloto encerrado

As duas fontes originais retornaram erro de tipo no CVL2 CLI 8.19.0; as duas cópias de #46 compilaram com **apenas** a assinatura `divPrecisely(mathint,mathint)` em lugar de `divPrecisely(uint,uint)`. Isso é somente typechecking: `RCPT=0` continua permitido nas precondições originais e torna a segunda divisão indefinida. Sem regra histórica confiável para tratamento `mathint/0` e sem equivalência de operações inteiras CVL1, os casos permanecem `02_unresolved`. Não inserir `require RCPT>0`, casts, nem executar Prover/CVL1.

## Ações condicionantes e encerramento conservador

- Obter commit da spec, build graph, solc, ABI, deployment, `--link` e receiver-policy do **mesmo** run histórico, em vez de compilar apenas fonte posterior que lhe parece semelhante.
- Para qualquer teste permitido no futuro: sandbox/scratch fora do repositório, input SHA256 e `cmp`, CLI/solc version, timeout, HOME/token isolados, `--compilation_steps_only`, logs stdout/stderr e exit code, uma spec por target. Até isso ocorrer, `NOT_TESTED` é o único registro correto.
- Evidência de compilação de uma rule extraída não substitui scripts da auditoria nem transforma rótulos originais VERIFIED/VIOLATED/NOT_STATED em resultados do CLI moderno.
- Preservar PR #40 e #46 como Draft, nenhuma integração ou alteração em originais, CSV de catálogo, resultados, contracts, configs ou código de migração.

Fontes de linguagem: [Certora Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [CVL2 Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Statements](https://docs.certora.com/en/latest/docs/cvl/statements.html).
