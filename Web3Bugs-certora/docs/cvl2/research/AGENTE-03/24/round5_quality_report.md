# AGENTE-03 — RODADA 5 — QUALIDADE CVL2 / Rocket Joe P24

**Decisão:** 164/164 exemplos permanecem incomplete e UNRESOLVED_CANDIDATE. COMPILE_OK=0; SEMANTIC_PROVEN=0; MIGRATED_COMPLETE=0. Compile-only NÃO executado: identidade da cena auditada (target, ABI, harness e links) não comprovada, apesar de progresso na closure estática OpenZeppelin. Nenhum Prover ou CVL1.

## Fontes separadas e referências exatas

| Fonte | Identificador e linha | Evidência | Limite |
| --- | --- | --- | --- |
| Relatório Certora | resources/24/Certora_Formal_Verification_Report_Rocket_Joe.pdf, 21 pp., SHA256 f223d83ad55ec79376126a18219c0f417b732fea7d53cf4a743738840cdd43b4, pp.1 e 6 | Commit Solidity auditado ef2ef30248661b5509c52ab30af9bd0fc07f6657 | Não fornece bytes exatos da execução de cada regra, harness, ABI, Prover |
| Fork histórico | Certora/rocket-joe-1@dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10:certora/ | Oito arquivos CVL completos com Git blobs idênticos aos do snapshot, scripts, helper erc20, patch e harnesses | Fork posterior não é a cena auditada |
| Snapshot catalogado | Web3Bugs-certora/results/spec/incomplete/24/N.*, baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 | 164 extratos e resultados originais preservados | Cada N.spec é extração do CVL, não blob idêntico à spec upstream inteira |
| Documentação CVL2 | https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html (Step 4), https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html | Methods exige internal/external e receiver explícito; wildcard e casts requerem semântica | Não autoriza conversão lexical como prova |

## Hunk #7 — achado semântico novo

O patch está em certora/applyHarness.patch:96–104 (Git blob abfb1eae851307c9a3e7d17a7b3e913962952845, SHA256 e06f5a9d5503e82310ffccfab55214b9cb847d2146656f2558271e0777e27fdb). O patch espera o guard do fork e altera a assinatura do método para virtual internal:

| Blobs imutáveis | Referência | Condição exata |
| --- | --- | --- |
| Solidity auditado, blob 2af4cfe5472decc22ab3dd361d0117893a61539e | ef2ef302:contracts/LaunchEvent.sol:673–679 | address(this).balance >= avaxReserve |
| Solidity fork, blob 2656eb863a83ca2a53714eb0ed336f420f952dae | dba90f9:contracts/LaunchEvent.sol:673–679 | address(this).balance - _value >= avaxReserve |
| Harness do fork, blob 1b6a42c5e397d03c921d18217364c7e67878621a | dba90f9:certora/harness/LaunchEventHarness.sol:114–116 | Override da função com IReceiver(_to).receiveETH{value: _value}(), sem o mesmo guard |

No estado aritmético abstrato balance=100, reserve=80 e valor=30, a primeira condição é verdadeira e a segunda falsa; isso mostra diferença das guardas, **não** um contraexemplo alcançável comprovado por Prover. O override ainda troca o mecanismo de transferência. Por isso nem o patch nem o harness podem ser considerados equivalentes ao run do PDF.

Teste histórico em SCRATCH somente, preservado em round4_patch_scene.log: patch --dry-run --batch --fuzz=0 -p0 no fork exit 0; híbrido auditado exit 1, Hunk #7 FAILED at 670; híbrido com fuzz padrão exit 0, Hunk #7 succeeded at 670 with fuzz 2; aplicação em scratch do fork exit 0. A Rodada 5 investigou a diferença textual e a regra de transferência, sem forçar patches sobre originais.

## OpenZeppelin autenticação nova e imports

Em ef2ef302:yarn.lock:581–589, contracts e contracts-upgradeable estão em **4.4.1**. Em dba90f9:yarn.lock:672–680, ambos são **4.4.2**. Recuperei em scratch, via npm pack --ignore-scripts, os quatro tarballs das versões exatas. O SHA512 calculado sobre os bytes de cada tarball coincidiu com integrity SHA512 no lock correspondente: **4 MATCH**. Arquivo round5_oz_package_provenance.csv traz cada versão, URL implícita no lock, SHA256, SRI e quantidade de fontes Solidity (134 + 128 por versão).

O grafo apenas de imports OpenZeppelin estáticos foi rechecado em round5_import_resolution.csv (6 scripts × 2 versões):
- verifyLEHighLevel.sh, verifyLEValidStates.sh, verifyLEVarTran.sh e sanity.sh: 10 caminhos OZ diretos e 15 arquivos OZ distintos transitivos, 0 ausências dentro desses tarballs.
- verifyStaking.sh e stakingRule.sh: 6 diretos e 11 arquivos distintos transitivos, 0 ausências dentro desses tarballs.
- Isto **não** autentica os pacotes realmente instalados no job Certora, outros imports/paths, versão/binário do solc, ABI/harness ou o diretório munged no run. O Owner.sol do verifyLEVarTran continua ausente; stakingRule.sh continua apontando para certora/spec/staking.spec, casing divergente. Nenhum mock inserido, nenhuma troca silenciosa 4.4.1/4.4.2.

## Índice individual e N.txt: 164/164

round5_example_evidence.csv contém 164 chaves únicas (24,incomplete,N), de N=1..164. Seus 52 campos incluem nome, hash do blob da spec fonte, linhas no arquivo original, SHA256 de N.spec, N.sol, N.md e N.txt, todas as importações CVL transitivas e blobs do fork, roots Solidity/hash, script/hash, target auditado/fork, Result, Detection Outcome, Bug Label original, bloqueio, versão, prioridade, próximo passo e gate individual. O novo arquivo foi reconciliado com results/spec/spec_buglabel.csv, sem modificá-lo.

Todos os **164 N.txt** originais foram lidos. **161** registram ausência de ../helpers/erc20.spec no snapshot; **3** (LEInProgress IDs 11–13) não declaram essa importação. Isso continua válido para o snapshot mesmo com helper encontrado no fork. Os 164 N.txt possuem 7 linhas e permanecem intactos. As oito specs upstream completas são Git-blobs idênticos entre snapshot e fork, mas **a identidade do Solidity não existe**: LaunchEvent auditado 2af4cfe5472decc22ab3dd361d0117893a61539e versus fork 2656eb863a83ca2a53714eb0ed336f420f952dae; Staking auditado 6f970060b271826b98c70f58131211454c3682a6 versus fork ae45dd7493c87c9451118c687e1ce77db8668bc3.

No CSV original, **164/164 Result=NOT_STATED**, Detection Outcome 161 NOT_STATED e 3 INCONCLUSIVE. VERIFIED do PDF não é resultado da property extraída. Grupos que exigem cuidado: IDs 2/5/7/147/150 diferem de fórmula ou guarda apresentada; IDs 12/13/152/154 são sensíveis à existência/vacuity; ID 163 usa require como filtro depois de @withrevert, não assert; ID 164 é sonda com assert false. Nada foi promovido.

## Causas dominantes por família

| Status de bloqueio | Casos | Evidência negativa | Próxima ação |
| --- | ---: | --- | --- |
| SPEC_WITHOUT_RECOVERED_RUNNER (LaunchEvent 76, LEPreset 1) | 77 | Sem runner específico que prove o target correto | Recuperar comando/ABI dessas specs |
| NO_RUNNER_OR_IMPORT_PROVEN (LEInProgress IDs 11–13) | 3 | Não declara import; nenhum runner | Recuperar driver exato, não inferir helper |
| OZ_EXTERNAL_BYTES_AND_ABI (LEHighLevel 10, LEValidStates 35, sanity 1) | 46 | OZ público recuperado, mas ABI da execução e patch-scene auditada não | Confirmar runner/target/ABI, começar por sanity |
| OWNER_SOL_ROOT_ABSENT (LEVarTran) | 19 | Owner.sol ausente no script | Localizar SHA correto; não substituir OwnerA/B |
| STAKING_TWO_RUNNERS_DIFFERENT_TARGETS | 19 | Targets harness vs munged, erro de casing e versões | Fixar qual runner/ABI é histórico |
| **TOTAL** | **164** | **0 COMPILE_OK** | Gate do coordenador |

### Compile-only: gate fechado com razão concreta

Prioridade isolada **N=164, sanity.spec**: N.spec byte-original preservado; script sanity.sh e import helper erc20 no fork; pacotes OZ autenticados e grafo interno OZ completo. Mas o script verifica LaunchEventHarness, que sobrescreve transferência AVAX; seu contrato base é diferente do auditado e o patch exige fuzz na cena auditada. Sem target/harness/ABI históricos comprovados não há teste diagnóstico que represente o relatório. O N.spec extraído ainda usa sintaxe CVL1, a qual não foi editada. **certoraRun --compilation_steps_only NÃO EXECUTADO**, por gate insuficiente; nem solc isolado, CVL1 ou Prover.

## Contrarrevisão somente leitura do PR #42

HEAD dc5f710cd1ef02ded3cb37dd0bb01362406d8e33 lida com git show, incluindo ROUND4_REVIEW.md e matrizes dos projetos 2,12,15. Resultado separado no arquivo round5_crossreview_pr42.md. Branch e originais AGENTE-04 não foram alterados.

## Requisitos dependentes do coordenador

1. Evidência do run (target, ABI compilada, harness e patch de mesma versão, binários/flags solc, logs/prover e linkings) para poder falar de execução auditada.
2. Se houver autorização para compilar **cena exclusivamente do fork** como experimento separado da auditoria, definir por escrito escopo e aprovação de runner para N=164; isso jamais comprovará o PDF.
3. Adjudicar as diferenças de guard em LaunchEvent: auditado versus fork e efeito do override do harness. Não converter resultados históricos.
4. Autorizar gate individual antes de qualquer saída results/cvl2; manter PR de pesquisa DRAFT, sem merge.

**Alerta LARANJA. AGENTE-03 — RODADA 5 — QUALIDADE CVL2.**
