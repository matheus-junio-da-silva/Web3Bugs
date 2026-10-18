# ECHO — Auditoria semântica independente, rodada 2

**Data:** 18/10/2026. **Fonte:** snapshot Git local de Web3Bugs, origin/main em 80f551f23bbd86d7901c6a28e7f44c68aebae8fd. **Escopo:** exatamente 174 instâncias CVL; não foi aberto merge nem editado catálogo de outros agentes.

## Resultado quantitativo

| Projeto | Instâncias | CONFIRMED | CORRECTION_REQUIRED | INCONCLUSIVE |
|---|---:|---:|---:|---:|
| 20 — Sushi BentoBox | 37 | 29 | 4 | 4 |
| 9 — Celo Governance | 61 | 51 | 0 | 10 |
| 4 — AAVE Staked Token | 27 | 23 | 0 | 4 |
| 5 — AAVE Starknet Bridge | 17 | 8 | 0 | 9 |
| 10 — Furucombo, IDs 65–96 | 32 | 24 | 0 | 8 |
| **Total** | **174** | **135** | **4** | **35** |

**CONFIRMED** significa que a interpretação documentada é compatível com a formulação técnica observável e com os qualificadores recuperáveis, não que a prova Certora foi reproduzida. **CORRECTION_REQUIRED** significa divergência classificatória para a qual há recomendação concreta de ajuste. **INCONCLUSIVE** significa falta de vínculo/harness histórico, precondição possivelmente insatisfatível ou limitação técnica material que impede atestar a semântica completa do target. Essas três decisões não substituem os campos Result e Detection Outcome.

## Método e integridade

Foi lido o corpo integral da declaração original selecionada em cada N.spec, com extração de assert, invariante e require (inclusive requires após a chamada), nomes dos helpers, methods, definitions, using e requireInvariant. A matriz aponta o arquivo de origem CVL e o N.spec e compara símbolos chamados com declarações de funções no N.sol preservado. A ausência de um entrypoint coincidente recebe marcação explícita SEM_MATCH_DIRETO: não se toma uma citação de contexto contratual como prova de correspondência funcional. Em seguida foram cotejados N.md, docs/standard.md, reports e scripts/harnesses documentados.

A intenção reconstruída é **uma descrição da propriedade tecnicamente observável**, nunca uma atribuição de pensamento privado ao autor. O contraexemplo é a condição lógica que falsearia a assertion, sob as premissas exatas do código; não é um trace do Prover que não foi fornecido. Os predicados CVL e restrições constam, por exemplo, das colunas Assertion_Efetiva e Requires_e_Filtros da matriz, e não são substituídos por sumários genéricos. Fechamento por nome de CVL não demonstra reconstrução de imports Solidity e de transformação do target; estes limites estão indicados individualmente.

Os campos atuais e propostos de Bug Label, Result e Detection Outcome são separados. O resultado histórico é preservado quando documentado individualmente; um ✔, ❌, ✔*, None, N/A ou 🔎 em tabela agregada não é automaticamente tratado como status de outra source rule, versão ou handler. Não foi feita nova execução do Prover, compilação equivalente, migração CVL2, nem inspeção visual adicional de diagramação dos PDFs: foram utilizadas as transcrições paginadas preservadas em reports/4.md, reports/5.md, reports/9.md, reports/10.md e reports/20.md e as citações individuais dos catálogos. O PDF binário permanece a autoridade final sobre o conteúdo histórico.

## Correções concretas propostas

**P2 — Project 20, IDs 26, 27, 28 e 29.** Proposta de Bug Label **S6-2 → L2**. São comparações de round-trip entre base e elastic, com o sinal de roundUp e tolerâncias de erro base/elastic explícitas. O problema detectável pela assertion é perda de precisão/arredondamento, coberto pelo oráculo geral L2 em docs/standard.md antes de uma categoria semântica S6-2. As condições base != 0 e elastic != 0 devem ser preservadas. O relatório marca Identity ✔ para o grupo, mas não permite inferir VERIFIED por cada uma das quatro variantes: permanecem NOT_STATED/NOT_STATED.

**IDs 30 e 31 não são incluídos na correção.** Os casos de base ou elastic zero verificam que o round-trip devolva o valor original ou zero. Não há perda de arredondamento necessariamente presente; a categoria atual S6-2 continua defensável, e o status é igualmente NOT_STATED/NOT_STATED.

## Achados por prioridade

**P0 — nenhum erro P0 comprovado.** Uma hipótese de vacuidade ou falta de fonte histórica não é automaticamente um exploit crítico no Solidity implantado.

**P1 — defeitos/limitações materiais da especificação original:**

- **P20 #20, #32 e #35:** as regras integrityHarvest exigem amountAdded < MIN_INT(), enquanto MIN_INT é definido no CVL como literal 0x8000... de tipo int256. Se for o mínimo signed, não há int256 estritamente menor: o caminho de verificação é possivelmente vazio. Os rótulos e o Result do catálogo são preservados; o histórico VERIFIED dos alvos SymbolicStrategy/SushiStrategy não demonstra não-vacuidade. Confirmar tipagem de CVL1 e satisfatibilidade antes de atestar o resultado. Decisão INCONCLUSIVE; não gerar trace imaginário.
- **P10 #67, #71, #75, #79, #83, #87, #91 e #95:** tokenMovementCorrectness atribui a origGeneratedTokenBalance o getter de saldo **sem** at initialStorage. UpdatedGeneratedTokenBalance lê o mesmo pós-estado. Quando expectedConsumedAmount > 0 e generated != 0, a segunda assertion exige x > x; se a condição nunca ocorre, o ramo pode ser vacuamente verdadeiro. A primeira assertion sobre tokens consumidos continua independente. A falha histórica já está reconhecida nos N.md, portanto não se duplicou uma correção catalográfica inexistente.
- **P9 #36 e #37:** getVoteRecord é declarado no CVL com três valores de retorno contra seis na assinatura Solidity consultada. Sem adaptador/ABI do harness histórico confirmado, a interpretação de execução é INCONCLUSIVE; manter incomplete.
- **P9 #50:** constitution_change_legal tem b1/b2 e os asserts de maioria dentro de comentário de bloco. A única assertion ativa é assert true; nenhum contraexemplo a falseia. UNMAPPED está correto. Não atribuir ao CVL uma verificação de constitucionalidade efetiva.

**P2 — qualidade documental e limites do ambiente:**

- **P20 #23:** exitRevert chama MAX_INT() ausente como definition/import na compoundStrategyAdditional.spec. Trata-se de sonda de não-reversão restrita e UNMAPPED, não teste de conservação. A origem está corretamente incomplete.
- **P9 #27:** o GovernanceHarness faz dequeueProposalsIfReady ser no-op, o que pode tornar um teste sobre dequeued vacuamente verdadeiro. #30, #48, #49 e #58–61 apresentam lacunas de dependência, mapeamento de getter, runner ou harness; não atribuir prova individual da tabela do PDF.
- **P4:** o alvo StakedAaveV3Harness depende de ../munged gerado a partir de ../src, não incluído no snapshot. Os 27 CVLs são objetos de avaliação estática; a implementação disponibilizada de StakedTokenV3 não substitui o alvo compilado. Preservar hipóteses do relatório: staked e reward token iguais, rewards vault distinto, loop unrolled três vezes e permit nondeterminístico. Particularmente stake mede taxa de conversão **depois** da chamada.
- **P5:** BridgeHarness, BridgeL2Harness e mocks L2/messaging não estão preservados localmente, enquanto Bridge.sol fornecido pertence a revisão posterior ao relatório. IDs #3/#16 e #13/#17 são variantes de specs distintas sem atribuição individual do ✔* agregado. A regra integrityOfWithdraw só protege direção dos saldos: saída zero não é falha necessária. #12 S2-3 codifica duplicação do L2 ID, sem exigir que os dois tokens L1 sejam distintos. #4–6 pertencem à categoria L2 de precisão ray.
- **P10 #65–96:** cada quádrupla corresponde a um handler distinto, não a uma prova intercambiável de ProxyHarness. HBalancer (#65–68) e HGasTokens (#93–96) não têm fonte concreta preservada. Scripts de handler podem alterar a implementação e Summary modela comportamentos externos. O universo de métodos e suas precondições muda por target; 8 instâncias são INCONCLUSIVE. Todos os 32 resultados individuais são NOT_STATED/NOT_STATED.

## Evidência histórica por projeto

**BentoBox:** shares em balanceOf[token][account], base de rebase, elastic como montante devido, ERC20.balanceOf como saldo externo e strategyData.balance como registro de estratégia são grandezas distintas. noChangeToOthersBalances proíbe apenas diminuição de shares de terceiro. additivity dos exemplos BentoBox efetivamente exercita **deposit**, apesar da descrição de withdrawal no relatório, portanto não herda a prova. A fonte bentoBoxCompoundStrategy.spec (#9–16) não herda VERIFIED do BentoBox original, e as seis variantes de inverse do Rebase não herdam o ✔ coletivo. A distinção entre 12 VERIFIED/NO_FINDING, 3 VERIFIED/FINDING e 22 NOT_STATED/NOT_STATED decorre da atribuição atual e não implica falha na versão final.

**Celo:** 61 casos preservam NOT_STATED/NOT_STATED por falta de correspondência individual entre resumo de Accounts/Governance e rule/harness. Regras privilegedOperation com dois callers verificam impossibilidade de sucesso simultâneo, **não** demonstram identidade do autorizado. Tautologias, getters e aplicações de applyHarness limitam generalização.

**AAVE Staked Token:** o relatório histórico distingue resultados atribuídos a propriedades e achados em versões anteriores. Outcome FINDING não prova que a revisão final está vulnerável. Sem munged e dependências ERC20 não se reconstrói o Prover de 2023.

**AAVE Starknet Bridge:** report de simplificações (L2 não verificado diretamente) e Solidity posterior impedem equiparar todas as variantes à prova original. A conversão ray e cancelamento/deposito usam modelos cujo material de execução falta.

**Furucombo:** report de 2021 apresenta observações por função/handler e abstrações DeFi, mas não fornece certificado individual de cada instância transcrita. Não converter None/N/A e marcadores de investigação em VERIFIED.

## Verificações da entrega

Matriz em docs/semantic_review_round2/echo_review.csv, CSV UTF-8 com BOM, com **174** linhas de dados e chaves exclusivas (Project_ID, Example_ID). Faixa do Project 10 estritamente de #65 a #96. Há colunas de provenance do CVL, predicados originais, target, Solidity e match, contraexemplo, Bug Label, Result e Outcome atuais/propostos, PDF, confiança, decisão e prioridade.

Os dois arquivos desta pasta são os únicos acrescentados pela auditoria. As fontes originais, N.spec/N.sol/N.md de outros agentes, contratos, resources, reports e resultados históricos foram mantidos sem alteração. Sem merge e sem autoaprovação.

**Conclusão: 135 CONFIRMED, 4 CORRECTION_REQUIRED, 35 INCONCLUSIVE (174/174).**
