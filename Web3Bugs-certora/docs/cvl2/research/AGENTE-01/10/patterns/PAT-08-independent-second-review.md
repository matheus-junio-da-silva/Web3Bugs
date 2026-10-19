# Furucombo P10 — adjudicação semântica da segunda revisão independente

Estado: **Fase 1, sem migração**. Baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3; audited c90dec1046e5e26edf70f985dd86381403912482. A matriz detalhada por N.spec/linha está em semantic_candidate_gate_matrix.csv.

## Autoridade da decisão

- A1: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#step-4-review-your-methods-blocks — a escolha de internal/external e o receiver precisa ser revista, não deduzida apenas de CVL.
- A1: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#step-3-fix-type-errors — casts require podem esconder counterexamples; não adicionar sem justificação.
- A2: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#function-and-required-for-methods-block-entries — function e ponto e vírgula obrigatórios.
- A2: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#required-internal-or-external-annotation — deve haver uma visibilidade, que depende do entrypoint Solidity.
- A2: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#summaries-only-apply-to-one-contract-by-default — summary CVL1 por assinatura versus CVL2 no currentContract; wildcard possui restrições e não implica equivalência automática.
- A2: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#optional-methods-block-entries — optional pode omitir regras; NÃO adicionar onde método histórico ausente ou incerto.
- A2: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#method-literals-require-sig — sig prefix é alteração de sintaxe localizada e não muda f.selector.

## Contagem de decisões por ocorrência, não por propriedade única
- BLOCKED_UNTIL_ABI: 513
- NO_ARITHMETIC_CAST_INDICATED: 271
- REQUIRED_SYNTAX_VISIBILITY_SOURCE_SUPPORTED: 108
- VISIBILITY_PUBLIC_CHOICE_BLOCKED: 42
- REQUIRED_SIG_LITERAL_SYNTAX: 28
- ARITHMETIC_SEMANTICS_REVIEW_ONLY: 25
- REQUIRED_PRESERVE_EXCLUSION: 1

Essas contagens são diagnósticos léxicos conservadores; não equivalem a compilação, provas ou 988 propriedades únicas. Um mesmo N.spec pode ter mais de um bloqueio.

## Correção pontual 33 — noThrow
- Fontes B1: https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L19 ; https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L1-L24 ; https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/libParam.sh#L1-L4 .
- N.spec:5 isStatic(bytes32) returns(bool) envfree => candidato function isStatic(bytes32) external returns(bool) envfree; fundamento: harness auditado linha 10 external.
- N.spec:6 getNumOfReferences(bytes32) returns(uint256) envfree => candidato function getNumOfReferences(bytes32) external returns(uint256) envfree; fundamento: harness linha 14 external.
- Não trocar esses getters pelas rotinas internal da biblioteca LibParam (contrato/receiver distinto). Getter histórico está no target auditado, não é função Perl injetada.
- N.spec:13 selector getParams(bytes32).selector => sig:getParams(bytes32).selector; getParams é external no harness auditado linha 13. Preservar os dois require dentro do ramo, getParams@withrevert e assert !lastHasThrown. Compilação não executada.

## Correção pontual 34 — noRevert
- Fontes B1: https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L21-L31 ; https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L10-L14 .
- N.spec:8 selector getParams(bytes32).selector => sig:getParams(bytes32).selector (mudança lexical).
- N.spec:9 require false; deve permanecer EXATAMENTE: torna inacessível o ramo getParams ao contraexemplo. A asserção só vale para f no ramo else e sujeita a require e.msg.value == 0. Nenhuma afirmação de que getParams nunca reverte.
- N.spec:13 assert !lastReverted; é booleano; não possui soma/subtração/multiplicação/divisão: diagnóstico genérico mathint/cast RETIRADO. Preserve o comentário only fallback may revert como histórico, sem transformá-lo em prova.
- O N.spec:34 não possui methods block: isso é recorte do catálogo, não ausência da declaração compartilhada no libParam.spec original.

## Getters Perl e target histórico
- B1: https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L38-L108 (commit 2021). O runner altera HandlerBase._revertMsg, injeta getSlot(uint), getStackLengthSlot(), getStackLength(), getSender(), getCubeCounter(), ethBalance(address), isHandler() e faz substituições por handler.
- No código auditado, getSender/getCubeCounter/isHandler são public sem view. O snapshot posterior adiciona view, outras substituições e muda a lista de handlers, inclusive HOneInchExchange/HWeth. Usar snapshot como driver histórico mudaria o modelo.
- A injeção acontece por regex na cláusula is HandlerBase, e não automaticamente em qualquer herdeiro indireto. HBProtocol herda HMaker; a coincidência no arquivo que o runner seleciona precisa ser examinada separadamente. Não afirmar getter no ABI sem verificação.
- Há renames 2021 unique_repay, unique_claimComp, unique_swap, unique_withdraw, compoundredeem, yvault_withdraw e changes de transfer para Nothing(...).nop; representam transformação no modelo, não substituição autorizada na fonte preservada.
- Em método public, o CVL2 distingue implementação internal e wrapper external; não há prova de que uma única marcação preserve todos os efeitos. Por isso essas entradas permanecem BLOCKED.
- Em summary DISPATCHER/NONDET, receiver precisa ser o contrato que define o método (inclusive supercontrato), não necessariamente o target escolhido; wildcard underscore pode mudar a cobertura e as restrições de returns/envfree. Não propor wildcard em massa.

## Busca negativa reproduzível e alcance do bloqueio
- Diretório pesquisado: clone literal dinngo/furucombo-contract no commit c90dec1046e5e26edf70f985dd86381403912482; log externo QA em /home/mat/cvl2-agent01-isolated/qa_logs/negative_historical_search.log.
- Comandos: find . -type f -name *.abi; find . -type f -name *.bin; padrões *certora*.json, *certora*.conf, *certora*.log, package-lock.json, yarn.lock; git ls-tree -r --name-only AUD com filtros de ABI, bin e lock. **Resultado zero** para esses nomes no tree auditado consultado.
- Os scripts com certoraRun, --verify e --settings foram encontrados (log lista caminhos): existem launchers em texto, mas não ABI compilada, linking executado, logs individuais nem pin exato do certora-cli.
- Reproduzir GNU Perl no workspace ORIGINAL seria uma mutação não autorizada; nenhum Perl foi executado. A leitura estática de pattern match NÃO é validação da ABI final.
- O package.json pin solc 0.6.12 e OZ 3.3.0 é evidência de dependência, não compilação. A tag OZ oficial não comprova identidade de todos os bytes de um pacote NPM histórico.
- Bloqueio formal que resta: artefatos compiled ABI/symbol table/post-transformação, resolution por receiver e chamadas de outros contratos, mapping de summaries/links e Prover histórico. Fase 2 não autorizada.
