# ECHO — Adjudicação semântica dos Projects 14 e 20 (2026-10-18)

## Escopo, método e base

Revisão de **cinco exemplos**, a partir de `origin/main` SHA `80f551f23bbd86d7901c6a28e7f44c68aebae8fd`. Documentos normativos consultados: `docs/standard.md` (`L2` = rounding/precision; `S3-2` = incorrect state update; `S6-2` = unexpected value), `docs/spec_catalog_workflow.md`, `docs/classification.md`, `docs/contribution.md`, `docs/modifications.md` e `docs/spec_catalog.md`. O arquivo solicitado `instrucoes-obrigatorias.txt` **não consta da árvore do repositório consultada**, nem da raiz da worktree; essa indisponibilidade é registrada, não encoberta.

As especificações CVL foram confrontadas com os arquivos originais de `contracts/<id>`, o alvo Solidity e `N.sol`; foram consultados os relatórios históricos paginados `reports/14.md` e `reports/20.md` (transcrições dos PDFs originais em `resources/14/OpynGammaDec2020.pdf` e `resources/20/SushiBentoboxFeb2021.pdf`). Limite probatório: a leitura textual paginada não é uma nova execução do Prover nem uma inspeção visual independentemente atestada dos símbolos do PDF. Não se fabrica resultado por regra a partir de ✔ agregado/✔* condicionado.

Os arquivos `.spec`, `.sol`, `.txt`, contratos, runners e PDFs foram preservados. `Result` e `Detection Outcome` permanecem `NOT_STATED` para os cinco exemplos. Não há `RESULT_OUTCOME_CHANGE` nem `DEPENDENCY_FIX`; persistem `EVIDENCE_GAP` para equivalência histórica do harness/prover e atribuição individual de PDF.

## Cinco decisões individuais

| Projeto / exemplo | Bug Label anterior → proposto | Decisão / classe | Prioridade |
| --- | --- | --- | --- |
| P14 #1 `orderOfOperations` | `S3-2 → UNMAPPED` | `LABEL_CHANGE` + `DOCUMENTATION_FIX` | P1 |
| P20 #26 `toElasticAndToBaseAreInverse1down` | `S6-2 → L2` | `LABEL_CHANGE` + `DOCUMENTATION_FIX`; contrarrevisão favorável | P2 |
| P20 #27 `toElasticAndToBaseAreInverse1up` | `S6-2 → L2` | `LABEL_CHANGE` + `DOCUMENTATION_FIX`; contrarrevisão favorável | P2 |
| P20 #28 `toElasticAndToBaseAreInverse2down` | `S6-2 → L2` | `LABEL_CHANGE` + `DOCUMENTATION_FIX`; contrarrevisão favorável | P2 |
| P20 #29 `toElasticAndToBaseAreInverse2up` | `S6-2 → L2` | `LABEL_CHANGE` + `DOCUMENTATION_FIX`; contrarrevisão favorável | P2 |

### Project 14 / #1 — scope real e falsificação

**CVL:** `contracts/14/specs/ControllerOrderOfOperations.spec:6-28`, sem `require`. Para `f1.selector > f2.selector` há somente `assert true`. Para `f1.selector <= f2.selector` captura-se `initialStorage`, roda-se `f1(e1,arg1); f2(e2,arg2)`, lê-se `getVaultCollateralAmount(owner,vaultId,0)`, reinicia-se com `f2(e2,arg2) at initialStorage; f1(e1,arg1)` e compara-se **somente** esse getter, no owner/vaultId fornecido. O índice de collateral é `0` fixo; não se comparam arrays completos, owners, pools, índices adicionais ou `vaultLatestUpdate`. Não há hipótese expressa que torne as chamadas independentes ou associe os métodos ao mesmo vault.

**Contraexemplo lógico:** ordem com `f1.selector <= f2.selector` e `vaultCollateralAmount1 != vaultCollateralAmount2` em chamadas/modelo viáveis. Se operações forem legitimamente não comutativas, o contraexemplo pode não representar bug. A rule não prova atualização incorreta nem comutatividade sobre storage, tornando `S3-2` excessivo; **UNMAPPED** conserva a natureza parcial/diagnóstica. S3-2 poderia ser reconsiderado somente após provar obrigação de comutatividade do par e erro de update. Não se presume intenção privada do autor.

**Solidity:** `contracts/14/specs/harness/ControllerHarness.sol`, getter `getVaultCollateralAmount` implementado por `cheapGetVault(owner,vaultId).collateralAmounts[i]`; `contracts/14/contracts/core/Controller.sol` contém `mapping(address => mapping(uint256 => MarginVault.Vault)) vaults` e `operate/_runActions`. O target histórico é `ControllerHarness`, com mocks e linking segundo `contracts/14/specs/scripts/runOrderOfOperations.sh`.

**PDF:** `reports/14.md`, property 18, página 12, `✔*`, relata ordem global independente de operações bem-sucedidas **sob simplificações**, mas a rule fonte tem predicado muito mais restrito. Não transferir o marker ao resultado individual: `NOT_STATED/NOT_STATED`.

### Project 20 — quatro conversões distintas

Pré-condição **comum**: `base1=getBase() != 0` e `elastic1=getElastic() != 0`; entrada `amount:uint256` simbólica, sem outra restrição declarada. Target `RebaseWrapper`; wrapper view lê `rebase`, com `base` em shares e `elastic` em montante. O helper `only_slightly_larger_than(x,y,ε)` é `y <= x && x <= y+ε` e `only_slightly_smaller_than(x,y,ε)` é `x <= y && y <= x+ε`.

| ID | Entrada → retorno intermediário → retorno final | roundUp | Assertion efetiva (ret = resultado final; a = amount) | Tolerância |
| --- | --- | --- | --- | --- |
| 26 | shares → elastic → shares | false | `ret <= a` e `a - ret <= floor(base1/elastic1)+1` | `base1 / elastic1 + 1` |
| 27 | shares → elastic → shares | true | `ret >= a` e `ret - a <= floor(base1/elastic1)+2` | `base1 / elastic1 + 2` |
| 28 | elastic → shares → elastic | false | `ret <= a` e `a - ret <= floor(elastic1/base1)+1` | `elastic1 / base1 + 1` |
| 29 | elastic → shares → elastic | true | `ret >= a` e `ret - a <= floor(elastic1/base1)+2` | `elastic1 / base1 + 2` |

O **contraexemplo** de cada linha exige inversão de direção ou exceder a tolerância, não mera desigualdade entre entrada e saída. Todas as divisões do bound são inteiras. A primeira conversão é `toElastic` nos exemplos 26–27 e `toBase` nos 28–29. `roundUp` é fixado identicamente nas duas etapas.

**Causa e label:** `RebaseLibrary.toBase` calcula aproximadamente `elastic * total.base / total.elastic` e `toElastic` o dual, efetuando divisões inteiras; `roundUp=true` tenta compensar o resto com incremento. A propriedade define um oráculo de precisão/arredondamento, e `L2` é preferível para desvios aritméticos de conversão que excedem o bound. **Limite crucial:** um resultado errado pode provir de fórmula/operandos diferentes, não necessariamente do mecanismo de rounding; o CVL por si só não prova a raiz causal de todo contraexemplo. `S6-2` permanece alternativa argumentável nesse cenário e depende de trace causal. Por isso a proposta ECHO é documentada, não imposta como consenso prévio do BOREAL.

**PDF:** `reports/20.md` página 6, `Identity ✔ (rule: toElasticAndToBaseAreInverse*)`, um resultado **agregado** que não certifica nominalmente cada variante #26–29; todas permanecem `NOT_STATED/NOT_STATED`. O target tem imports históricos de `@boringcrypto` ausentes na snapshot: `incomplete` é preservado. **IDs #30–31 não alterados:** casos `base/elastic=0` são qualitativamente distintos.

## Contrarrevisão independente — BOREAL

**PARECER RECEBIDO: CONCORDÂNCIA FUNDAMENTADA PARA OS QUATRO EXEMPLOS.** O BOREAL, responsável pela catalogação original do Project 20, publicou [contrarrevisão técnica independente no PR #14](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/14#issuecomment-6255736378) antes deste PR corretivo. O parecer confere os requires, helpers, flags, sentidos das desigualdades, limites e a implementação Solidity por regra. Conclui que **L2** é a categoria mais específica para os limites genéricos de erro de arredondamento/precisão conforme a precedência do `docs/standard.md`.

- **#26:** L2, shares → elastic → shares, roundDown, resultado <= entrada, erro <= floor(base/elastic)+1.
- **#27:** L2, shares → elastic → shares, roundUp, resultado >= entrada, erro <= floor(base/elastic)+2.
- **#28:** L2, elastic → shares → elastic, roundDown, resultado <= entrada, erro <= floor(elastic/base)+1.
- **#29:** L2, elastic → shares → elastic, roundUp, resultado >= entrada, erro <= floor(elastic/base)+2.

BOREAL confirma que o PDF BentoBox p.6 registra apenas **Identity ✔ agregado**, sem veredicto individual por variante; importa módulos de `@boringcrypto` ausentes e não alega replay do Prover. Os quatro Result/Outcome seguem **NOT_STATED/NOT_STATED**.

**Ressalva causal:** L2 descreve o oráculo de precisão da assertion, não prova que qualquer futura violação foi causada por rounding. Se um trace evidenciar erro diferente de fórmula ou de inputs/harness, S6-2 pode tornar-se a interpretação mais adequada **para aquela falha específica**; isso não contradiz a concordância sobre a intenção formal da propriedade. [Pedido posterior do ECHO no PR original](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/14#issuecomment-6255791795). Não houve divergência entre os pareceres acerca da classificação destas quatro assertions; eventual evidência contrária deverá ser submetida ao orquestrador.

## Risco e controle de mudança

- **P0:** nenhum confirmado.
- **P1 — #1:** documentação poderia promover um teste parcial a garantia geral de comutatividade e imputar equivocadamente `S3-2`.
- **P2 — #26–29:** seleção entre oráculo genérico `L2` e `S6-2` depende de diferenciar mecanismo aritmético de erro semântico; a regra permite tolerâncias explícitas. Mudança recomendada **com contrarrevisão favorável**, sem inventar falha real.
- **EVIDENCE_GAP:** versão/harness exatos e resultados individuais não reproduzidos.
- **RESULT_OUTCOME_CHANGE:** nenhum. **DEPENDENCY_FIX:** nenhum. **DOCUMENTATION_FIX:** cinco. **LABEL_CHANGE:** cinco.
- **CSV compartilhado:** somente as cinco relações por (Project ID, Status, Example ID) foram alteradas. Outras linhas, inclusive todos os demais projetos e P20 #30–31, conservadas.
- **Validação real:** na VM, dentro de Web3Bugs-certora, os três comandos oficiais foram executados com o alias PATH local temporário python → /usr/bin/python3: check_specs.py exit **0** (1222 exemplos, 1227 relações), check_contests_csv.py exit **0**, check_contracts.py exit **0**. Na raiz Git, diff --check da worktree exit **0**. Após o commit, o diff oficial origin/main...HEAD deve ser executado novamente e seu exit code documentado no PR.
- **Tentativa inicial antes de materializar sparse checkout:** check_specs=0, check_contests=1, check_contracts=1 por FileNotFoundError de ./reports (ausência local de diretório, não erro no CSV); após git sparse-checkout add de reports e contracts, repetição passou com exit 0. Nenhum arquivo histórico foi reescrito. A CI do PR ainda será conferida no GitHub; não presumir sucesso nem SHA final.

Nenhum merge autorizado.
