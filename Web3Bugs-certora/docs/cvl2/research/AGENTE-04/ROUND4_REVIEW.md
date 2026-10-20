# AGENTE-04 — Rodada 4: portas de compilação e confronto histórico

Data: 2026-10-20. Branch exclusivamente documental: `research/cvl2-agente-04`; baseline imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. PR #42 Draft. **Nenhuma Fase 2 foi autorizada.**

## Método e denominadores

Antes das ações, foram lidos os documentos `Web3Bugs-certora/docs/spec_catalog.md`, `spec_catalog_workflow.md`, `spec_catalog_project_1.md` e `docs/standard.md`. Fontes A1 e A2: [Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html) e [Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html). Examinei também as revisões do PR #42 até a terceira revisão do coordenador e os documentos anteriores de provenance.

`ROUND4_PROGRESS.csv` contém **157 linhas únicas**, com chaves (`project_id`, `status`, `example_id`): P12 **26** (17 complete / 9 incomplete), P2 **15** (1 complete / 14 incomplete), P15 **116** (0 complete / 116 incomplete). Todos os **157/157** arquivos originais `.spec` e todos os **157/157** exemplos extraídos existem no checkout. Foram confrontados os **157 nomes exatos** com os textos `reports/{12,2,15}.md`: 77 nomes literais localizados, 80 não localizados como token exato. **Isto não é contagem de propriedades comprovadas, nem leitura independente das 157 execuções, nem prova de ausência no PDF**. Cada linha retém o resultado/outcome do índice anterior sem corrigir ou extrapolar o CSV histórico. O índice anterior indicava páginas nominais de PDF por instância; suas referências constam na matriz, com estados NÃO LOCALIZADO preservados. Fontes primárias: `resources/12/AaveV2Dec2020.pdf` (25 páginas, exame da rodada anterior), `resources/2/Aave-Proof-of-Reserve-Formal-Verification-Report.pdf` (6 páginas, conferidas nesta rodada), `resources/15/Aave_Gho_Formal_Verification_Report.pdf` (13 páginas, rodada anterior). Não se supõe execução por simples presença textual.

**Total de 18 DOCUMENTED_CANDIDATE = 17 de P12 e 1 de P2.** Todos permanecem `UNRESOLVED_ABI_TARGET_SEMANTICS` no índice anterior. Os outros 139 não recebem promoção; `local_compilation=NOT_RUN_HISTORICAL_CLOSURE_GATE` e `semantic_preservation=NOT_DEMONSTRATED` em 157/157 linhas.

## P12: nova contraprova de identidade histórico/snapshot

Commit primário do relatório: [aave/protocol-v2@750920303e33b66bc29862ea3b85206dda9ce786](https://github.com/aave/protocol-v2/tree/750920303e33b66bc29862ea3b85206dda9ce786). Recuperadas por URL imutável, apenas para comparação em scratch (não substituídas no snapshot), as sources:

- `specs/UserConfiguration.spec`, `specs/harness/UserConfigurationHarness.sol`;
- `specs/VariableDebtToken.spec`, `specs/harness/LendingPoolHarnessForVariableDebtToken.sol`;
- `contracts/protocol/libraries/configuration/UserConfiguration.sol` e `contracts/protocol/libraries/types/DataTypes.sol`.

### P12 / complete/19–26: nome idêntico não é a mesma ABI

**O snapshot alterou estruturalmente a fonte CVL e o harness de época.** Na source auditada, o methods `setBorrowing(address,uint256,bool)`, `isBorrowing(address,uint256)`, `isEmpty(address)` etc. recebe `address user`; no snapshot tais funções são `setBorrowing(uint256,bool)`, `isBorrowing(uint256)` e `isEmpty()`. A source CVL da época também possui `user` nos argumentos de regras e invariants; o snapshot o elimina. O harness original expõe métodos públicos com argumento `address user`; o snapshot utiliza a versão pública sem esse argumento e reescreve imports.

Evidências por hash SHA256: upstream `UserConfigurationHarness.sol` = `965afb5a3ea8dfc4a34a77ac53cea1079adc9ee9f603971e14f62d174e88a0ee`; snapshot = `0bbda4db0ee80986a3c63672d50bd5858ab7fe62cb7a28d440a0e7320846c116`. A biblioteca `UserConfiguration.sol` difere em formatação da função `isUsingAsCollateralOrBorrowing`; `DataTypes.sol` foi idêntico byte a byte nos caminhos comparados. Logo, os 8 corpos de property P12/19–26 divergem da source upstream. A função `user` adicional pode não acessar um mapa distinto neste harness; **não presumimos que removê-la é mudança de comportamento de estado**; é certamente mudança de assinatura, conjunto de argumentos e potencial método/selector. O PDF apresenta notação com usuário. Nenhuma equivalência de universo de contraexemplos foi estabelecida.

O exemplo **complete/23 — `setBorrowing`** é a prioridade lexical mais compacta no snapshot: target único `UserConfigurationHarness`, `setBorrowing(uint256,bool)` e `isBorrowing(uint256)` são públicos e presentes; o require `reserveIndex < 128` e a assertion devem permanecer. O **complete/25 — `setUsingAsCollateral`** é caso semelhante. Ambos são **apenas candidatos à futura decisão**, jamais ao diagnóstico local da rodada, porque a assinatura auditada diverge. Há ainda divergência textual histórica entre a propriedade #29 do PDF (postcondição impressa de borrowing) e a assertion de collateral no CVL, já corretamente isolada em `reports/12.md`.

### P12 / complete/10–18: versão de spec e harness

Comparação individual da declaração e corpo por normalização **apenas de comentários/espaços** entre os arquivos `VariableDebtToken.spec` upstream e snapshot: **2/9 idênticos em tokens** (IDs 10 `balanceOfChange` e 16 `integrityBurn`), **7/9 diferentes** (11, 12, 13, 14, 15, 17, 18). Exemplos objetivos: em `integirtyBalanceOfTotalSupply` o filtro de selector para mint usa assinatura distinta; outras regras apresentam mudanças nos argumentos, corpo e condições. `LendingPoolHarnessForVariableDebtToken.sol` também diverge por SHA256. Mesmo 10 e 16 **não** estão semanticamente reconstituídos, porque contexto, linking `POOL`, target binário, compiler e settings não têm closure auditável. O relatório PDF não lista automaticamente cada uma dessas regras de supply: preserva-se a distinção entre a regra visível e o agregado.

### P12 / incomplete/1–9: StableDebtToken

Não usar versão recente. O `StableDebtTokenHarness` auditado invoca superclass constructor de cinco argumentos; o snapshot de `StableDebtToken.sol` utiliza `initialize(...)`, getter de tipo incompatível e alterações de virtualidade. O bloqueio é de fonte/ABI de Solidity **antes** de CVL2. A script `runStableTokenCLI.sh` do commit mostra o target; seu literal `solc6.8` não prova que o binário correto para `pragma 0.6.12` esteja disponível. Zero dos nove são elegíveis.

## P2: uma target de catálogo não fecha receivers externos

A source `contracts/2/specs/aggregator.spec` e o exemplo `complete/2/1.spec` contêm `PoRFeedChange`, target `ProofOfReserveAggregator`. O relatório [Proof of Reserve](../../../../resources/2/Aave-Proof-of-Reserve-Formal-Verification-Report.pdf) p.6 marca nominalmente `PoRFeedChange`, mas o texto declara hipóteses de external effects, simplificações e loops limitados a três iterações. O Solidity principal auditado foi anteriormente reconciliado byte a byte ao commit [Certora/aave-proof-of-reserve@12296ce4](https://github.com/Certora/aave-proof-of-reserve/commit/12296ce4c6f9bde6663e1baa02cf19f179c1048b).

O método `latestRoundData() => NONDET` da spec original representa chamadas de feed/oráculo; migrá-lo a `currentContract` em CVL2 perde o receiver externo, enquanto trocar para `_.latestRoundData` pode alterar o conjunto de contratos resumidos. A documentação A1/A2 exige decisão explícita de visibilidade e receiver; **não há prova que `PoRFeedChange` preserva o mesmo universo de chamadas com qualquer substituição textual automática**. A regra ainda usa `f.selector` com caminhos específicos e `f(e,args)` no default; uma migração de `sig:` e de call semantics deve ser analisada em conjunto.

Para os **14 incomplete**, `PORaggregatorDummy`, `configuratorDummy`, helpers `_disableBorrowingCalled` e a ABI histórica necessária não estão comprovados; não inventar equivalentes. Zero de P2 selecionados para compilação nesta rodada.

## P15: versões fixadas versus ambiente efetivo

O pacote auditado [aave/gho-core@ce49fb0](https://github.com/aave/gho-core/tree/ce49fb0c94cfebf0159222ceb288e4f9a55d305f) registra `package-lock.json` e scripts `certora/scripts/verify*.sh`. A rodada anterior verificou SRI de três tarballs com hashes: `@aave/core-v3@1.17.2` (`1a1307d7cfae3027fd475fa76dd251206c1c65fd2466b60036da6cadc8ef54e9`), `@aave/periphery-v3@2.0.1` (`b48e664f06dbbc34e3e3af2dc13fd6dc4fd34fa116e5bfc98362d62f6c741320`) e `@openzeppelin/contracts@4.8.1` (`d45d540b9b1c60707b01c8981ccfb1ce9b7e156492c9ab85a46fa520960da065`); estes checksums são **evidência anterior, não uma nova reexecução deste turno**. Nenhuma inferência de `node_modules` instalado, restante das dependências transitivas ou versão CLI histórica.

A Makefile e `applyHarness.patch` geram a árvore `munged` com alterações de visibilidade e novas cláusulas `require` para `GhoToken`. Sem hash dos artefatos munged usados na execução, argumentos `--verify`, linkings e scripts não bastam para fixar a mesma ABI/semântica. Por isso nenhum dos **116 incomplete** é selecionado para compilação. **63 VERIFIED** provenientes do CSV histórico ficam intactos; o relato antigo de 64 não vira uma property adicional.

## Candidaturas por ordem de potencial lexical, mas bloqueadas para execução

| Prioridade documental | IDs | Uma target indicada? | Gate efetivamente bloqueante | Ação |
|---|---|---|---|---|
| P12 UserConfiguration simples | complete/23, /25 | Sim, snapshot `UserConfigurationHarness` | upstream acrescenta `address user` nas sources; sem identidade entre ambientes | Não compilar; aguardar adjudicação individual da versão |
| P12 UserConfiguration demais | complete/19–22, /24, /26 | Sim, no snapshot | mesma divergência histórica, invariants e variáveis de domínio | Não compilar |
| P12 VariableDebt | complete/10–18 | Target nominal `VariableDebtToken` | linking `POOL`, harness e mudanças de fonte, 7/9 bodies distintos | Não compilar |
| P2 Aggregator | complete/1 | Sim, catálogo `ProofOfReserveAggregator` | receiver/scope da summary `latestRoundData` sem closure histórica | Não compilar |
| P12 StableDebt | incomplete/1–9 | Nominal `StableDebtTokenHarness` | constructor/getter/Solidity incompatíveis | Não compilar |
| P2 Executors | incomplete/1–14 | Targets nominais dos Executors | mocks/ABI externa ausentes | Não compilar |
| P15 GHO | incomplete/1–116 | Família histórica de scripts, sem binário alvo único reconstruído por regra | transitive deps, munged e execution provenance | Não compilar |

**Compilações novas: 0; diagnósticos `--compilation_steps_only`: 0; Prover: 0; CVL1: 0; specs/contratos/CSV histórico alterados: 0; equivalências afirmadas: 0.** Esta ausência de compilação é uma escolha de integridade: faltam os requisitos mínimos de closure.

## Contrarrevisão independente somente leitura de AGENTE-05 (PRs #40 e #46)

Realizada depois da triagem dos três projetos, **sem alterar as branches do AGENTE-05**. No [PR #40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), o diagnóstico do coordenador para P7/37 e P7/65 registra `EXIT 0` de CVL2 em **fragmentos** sobre o snapshot, mas as specs CVL **integrais** de StableDebtToken e VariableDebtToken retornam `EXIT 1` (methods, hooks e invoke). O relatório explicita diferenças para a cena auditada de 2022 e até fallback de autofinder por `Stack too deep` em P7/37. Risco de claim: promover `SNAPSHOT_FRAGMENT_CVL2_COMPILE_OK` a replay histórico, equivalência semântica ou prova seria indevido. Registro factual: não foi essa a promoção adotada pelo autor; o bloqueio é corretamente declarado.

No [PR #46](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46), li o `SEMANTIC_REVIEW.md` na HEAD `62754c10e3e9dc23d122aad3333eac2ec60f817d` e a quarta revisão independente. As duas cópias `mathOfChangeSupply` mudam somente os tipos formais de `divPrecisely` para `mathint` e possuem assertions **diferentes**. O caso matemático `RCPT=0` ainda admite segunda divisão por zero; há lacunas documentais de coerção de CVL1 e da semântica operacional de `mathint/0`. Risco de claim: confundir `V1⊊V2` das duas assertions sob **um mesmo** modelo matemático definido (`RCPT>0`) com equivalência CVL1→CVL2, ou usar CI estrutural/compilação como `VERIFIED`. A documentação do AGENTE-05 mantém ambas `02_unresolved`, o que é adequado às fontes consultadas. Nenhum novo resultado experimental foi produzido por esta contrarrevisão.

**Sem pedido de merge, sem revisão formal submetida aos outros PRs e sem afirmar equivalência.**

## Reprodutibilidade e alertas

Checkout isolado da branch HEAD inicial `4abce59bc2be6930766be761b6d1d5392f6b22c8` em `/home/mat/cvl2-agent04-round4/repo`. As comparações upstream foram feitas apenas em `/home/mat/cvl2-agent04-round4/scratch/upstream-v2`; o script de matriz e logs de QA ficam fora do Git. Os quatro documentos normativos foram lidos antes da investigação. Os validadores e a integridade do diff foram executados e serão novamente executados após commit; seus exit codes finais devem constar da mensagem de entrega.

Avisos: comparação de tokens **não** é equivalência semântica; resultado em relatório **não** demonstra recompilação desta extração; arquivo `N.sol` é trecho de evidência, não entrada de compilação; patches, `require_`, `assert_` e wildcard summaries podem mudar os contraexemplos; nenhuma substituição de dependência foi efetuada. Status **BLOQUEADO / DRAFT**, nenhuma Fase 2, nenhum merge.

**AGENTE-04 — RODADA 4**
