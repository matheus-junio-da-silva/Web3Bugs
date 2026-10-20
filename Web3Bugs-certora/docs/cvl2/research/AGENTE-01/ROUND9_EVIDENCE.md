# AGENTE-01 — RODADA 9 / EVIDÊNCIAS TÉCNICAS

**Repositório:** https://github.com/matheus-junio-da-silva/Web3Bugs
**PR exclusivo:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 — DRAFT, sem merge
**Branch:** research/cvl2-agente-01
**HEAD inicial conferida:** 8267dcdf8114dd856e0bffca7c3e6de36b0102d5
**Baseline histórico imutável:** 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3
**Carteira:** P10 Furucombo, 266 propriedades (2 complete, 264 incomplete).

A revisão independente mais recente do PR39 (pullrequestreview-5592623213) autorizou somente diagnósticos restritos, com recuperação do WSL previamente checada. O painel do coordenador PR48 informava **18 tentativas em 16 propriedades distintas**, seis compile-only EXIT 0, doze erros em originais (interseção de dois P7), 1.370 sem compilação CVL2 e zero equivalências históricas antes desta R9. NÃO transportar essa contagem global às duas experiências novas P10 sem ledger atualizado.

## 1. Pré-requisitos e identidades

Antes de modificar qualquer documentação, lidos integralmente spec_catalog.md, spec_catalog_workflow.md, spec_catalog_project_1.md, standard.md, mais P1/complete/3.spec e P1/incomplete/1.spec e /1.txt. Complete no catálogo só atesta closure de dependências do snapshot. Nenhum histórico, fonte, contrato, bug label, require, assert, cast, ghost, hook ou summary foi editado.

Fontes oficiais Certora: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html ; https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html ; https://docs.certora.com/en/latest/docs/cvl/methods.html ; https://docs.certora.com/en/latest/docs/cvl/ghosts.html ; https://docs.certora.com/en/latest/docs/cvl/hooks.html ; https://docs.certora.com/en/latest/docs/cvl/statements.html ; https://docs.certora.com/en/latest/docs/cvl/expr.html .
Solidity 0.6.12: https://docs.soliditylang.org/en/v0.6.12/assembly.html e https://docs.soliditylang.org/en/v0.6.12/internals/layout_in_storage.html .

Origem Solidity: dinngo/furucombo-contract@c90dec1046e5e26edf70f985dd86381403912482; fonte OpenZeppelin: openzeppelin-contracts@6be5ffe54fc8982b7c1d0f45d4cb7bbd313107cd (tag 3.3.0). Pinos confirmados por Git. Certora CLI 8.19.0 e compilador solc 0.6.12+commit.27d51765, digest oficial SHA256 f6cb519b01dabc61cab4c184a3db11aa591d18151e362fcae850e42cffdfb09a.

WSL DESKTOP-5E26TVU respondeu aos comandos simples: bash, Python 3.14.4, Git 2.53.0, filesystem, leitura do catálogo, ABI fonte e estado Git. Checkout AGENTE-01 isolado estava limpo, sem alterações de terceiros, e foi atualizado somente por fast-forward até a HEAD inicial. Não houve reset/rebase.

## 2. Dois resultados CVL2 realmente NOVOS — derivados separados, sem Prover

Fonte GLOBAL: https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L31 ; Git blob 096f9f704226a7aa77c3d0da3862644db5051eb3.
Harness: https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L1-L22 ; blob e31683f3b63a95d3522f897748d0d13159388a15.
Biblioteca: https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/lib/LibParam.sol ; blob 740e8a5ccae25d5e041c9736545c13de7cd3867f.
Driver: specs/scripts/libParam.sh, blob 3344316e9569c8292df6d47725126dfa3173c605, sem script Perl de handlers.

Os wrappers isStatic(bytes32) e getNumOfReferences(bytes32) são external na fonte harness; getParams(bytes32) é external sem retorno. O código da biblioteca usa internal pure, não equivale automaticamente à ABI externa. As anotações envfree dos métodos não são summaries, e o universo method f continua não comprovado.

**Ambiente:** duas árvores scratch separadas fora do repositório. Cada N.spec original foi copiado e comparado byte a byte contra o snapshot. CLI direto certoraRun --compilation_steps_only, solc pinado, timeout 65s com margem SIGKILL 5s, HOME/XDG_CACHE_HOME individuais e CERTORAKEY/CERTORA_TOKEN/CERTORA_API_KEY/CERTORA_USER_ID removidos. Não foi executado Prover completo, CVL1 ou migração em lote.

| ID P10 | Original SHA256 | Derivado SHA256 | Única variação sintática em scratch | R9 resultado real |
| --- | --- | --- | --- | --- |
| complete/33 noThrow | cfc9c3350c09d9e26dda514568628d339bfb6def8e851c7cb8b929d005101f5b | adfa4b07964bd31a14d1461d0fca711af62f99d1ca503dcf74fb853637d4776d | nas duas entradas methods: function LibParamHarness.* external e ; ; no selector de getParams: sig: | **COMPILE_ERROR, EXIT 1**, typechecker em 33.derived.spec:21:10: variável lastHasThrown não declarada |
| complete/34 noRevert | 617fd020e9ed8344af651f1286dde672feb07c7c5ea8f6444e54e2904fda8f8d | 6e27246dc38c51f16c5777b766e2f449531610109e00f5f0590b09e1d00e3e54 | SOMENTE sig: na comparação getParams(bytes32).selector | **COMPILE_OK, EXIT 0**, estritamente para recorte CVL2 DERIVADO |

O arquivo original complete/33.spec permanece blob e55057a90f641156538f732c0fe172c28cd86dad; complete/34.spec blob 3e180d5f3a046f2e63192cd1a464cadff5b8775a. N33 deriva do GLOBAL noThrow com methods; N34 é noRevert extraída sem methods da spec GLOBAL. Estas duas compilações não reproduzem o job auditado completo com suas regras e flags.

**Nova observação 33:** function, external, ; e sig: passaram do erro gramatical da R5 ao próximo erro de tipo: lastHasThrown não declarado. O CVL2 atual documenta lastReverted, mas NÃO está demonstrada a equivalência histórica com lastHasThrown no CVL1. Não alterar a assertion por conveniência. Não acrescentar premissas, getters intermediários ou restringir method f.

**Nova observação 34:** somente sig: bastou para o recorte derivado passar compilation_steps_only. A instrução require false; está **literalmente preservada** e exclui o ramo getParams da regra; assert !lastReverted verifica somente o ramo else após f@withrevert. Não há prova de satisfatibilidade deste ramo, de não-vacuidade, de equivalência nem de não-reversão de getParams. Nunca classificar como VERIFIED, SEMANTIC_PROVEN ou 100% migrado.

Diferenças unificadas exatas: ROUND9_ARTIFACTS/33_exact_diff.txt e 34_exact_diff.txt. Logs CVL completos: ROUND9_ARTIFACTS/33_derived_cvl2.txt e 34_derived_cvl2.txt; bytes originais recuperáveis nos arquivos .raw.b64. Os SHA256 de ambos os formatos, comandos sanitizados, exit codes e SHA de Solidity são fornecidos por ROUND9_LOG_MANIFEST.csv e ROUND9_DIAGNOSTICS.csv.

## 3. Compilação Solidity de ProxyHarness original em scratch — eixos separados

Seeds auditados: https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/ProxyHarness.sol#L13-L90 ; https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/Proxy.sol#L116-L237 ; Storage.sol; OpenZeppelin 3.3.0 pinado. A primeira invocação solc com remapping de caminho absoluto gerou erro de localização de import SafeERC20/Address, **bloqueio da montagem da cena**, não erro sintático CVL2.

Uma segunda compilação solc 0.6.12 usou cópias de fontes Furucombo e OZ pinadas sem alteração, incluindo a árvore local @openzeppelin/contracts, com cmp das sementes. RESULTADO REAL **SOLC EXIT 1**:

- ProxyHarness.sol:45:21, função _parse: override especificado, mas não sobrescreve nenhuma função com a mesma assinatura.
- ProxyHarness.sol:62:21, função _trim: mesmo erro.
- Proxy.sol:233:5 / ProxyHarness.sol:68, _exec: base não marcada virtual.
- Proxy.sol:116:5 / ProxyHarness.sol:78, _execs: base não marcada virtual.

Log integral: ROUND9_ARTIFACTS/proxy_solc_unpatched.raw.b64 (legível no .txt). **Falha Solidity, NÃO CVL2 COMPILE_ERROR.** Não há ABI ProxyHarness compilada. Sem qualquer patch nos contratos para adicionar virtual ou alterar arrays 2 vs 256.

Separadamente solc --storage-layout contracts/Storage.sol em scratch retornou **EXIT 0**: Storage.stack, array dinâmico bytes32[], ocupa o slot inicial 0; Storage.cache ocupa slot 1. A notação stack_slot para storage em inline assembly é documentada em Solidity 0.6.x. O log de erro do ProxyHarness não menciona stack_slot, mas a compilação global falhou antes de validar toda cena. Conclusão: a ausência de declaração literal stack_slot não demonstra por si só ausência de símbolo, e os N.txt históricos /15 e /16 permanecem **inalterados**. Ainda falta provar que o job histórico solucionou as quatro incompatibilidades de override; não inventar patch.

## 4. Reencenação dos comandos Perl do HMaker — transformação somente, sem compilação Certora

O script auditado https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L1-L108 (blob b603b618b4e85782cc63b9b97101a928c350636b) é invocado por runHMakerSpecific.sh com HMaker maker specs/hmaker.spec e B=3. As linhas 104–108 chamam certoraRun e **não foram executadas**.

Foi feita cópia byte-idêntica dos contratos de 2021 (116 arquivos Solidity) em scratch. Apenas as linhas **1–102** com os comandos Perl efetivos foram reproduzidas com os argumentos históricos; transformação-only **EXIT 0**, stderr vazio. **18 dos 116** arquivos Solidity tiveram SHA256 alterado, com inventário antes/depois e lista de 18 mudanças em ROUND9_ARTIFACTS/hmaker_before_tree.txt, hmaker_after_tree.txt e hmaker_changed_tree.txt (mais versões .raw.b64).

- HandlerBase.sol: _revertMsg(string,string) passa a virtual internal.
- HMaker.sol: injeta getSlot, getStackLengthSlot, getStackLength, getSender, getCubeCounter, ethBalance, isHandler; adiciona override _revertMsg que executa revert(); troca import SafeERC20.sol por ERC20.sol; chamadas safeApprove por approve; alguns endereços deixam de ser constant.
- 16 outros Solidity sofrem modificações globais, incluindo HSCompound.sol claimComp→unique_claimComp, Aave, Kyber, Mooniswap, YVault e WETH. Não afirmar que apenas o handler alvo foi transformado.

O runner COMPLETO, que NÃO foi executado, teria seis seeds Solidity HMaker, Registry, DummyERC20A, DummyERC20B, ProxyHarness, Summary, verificação HMaker:specs/hmaker.spec e flags -assumeUnwindCond,-b=3,-ciMode=true. A GLOBAL hmaker.spec contém using, DISPATCHER(true), NONDET, envfree, filtro method f e selector legado. **Não há ABI pós-Perl compilada nem prova de correspondência com o job Certora de 2021.** Os 11 N.spec HMaker, 11 HBalancer e 11 HSCompound permanecem incomplete, NOT_RUN de CVL2 nesta R9.

## 5. Contrarrevisão somente leitura — AGENTE-02 PR #37

PR https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37 na HEAD f13481755eeac310aac7f930022faa522c7b8fce, Draft. Lidas revisão de coordenação mais recente, ROUND8_EVIDENCE.md e ROUND8_METHOD_RECEIVER_MATRIX.csv do AGENTE-02. **Nenhuma escrita em sua branch.**

- P18/complete/3 grantRoleEffect e P18/complete/23 noTransferEffectOnApproval tinham COMPILE_ERROR anteriores de methods CVL1 (execução do **COORDENADOR**, não deste agente), sem novo parser executado por mim. Em AccessControl, grantRole/hasRole são public; a ABI wrapper external não substitui a rota internal do corpo em chamadas indiretas. ERC1155.safeTransferFrom é public, com bytes memory no corpo e bytes calldata na interface; o método N.spec não garante que a mesma rota seja resumida.
- A nova matriz de 18 métodos documenta P18/4 revokeRole public nonpayable e hasRole public view envfree, nenhum summary explícito; a cadeia _checkRole interna não se confunde com a chamada CVL externa.
- P18/46: ERC1155Burnable.burn exige titular/aprovado, enquanto ERC1155Mock.burn chama diretamente _burn: selector igual não implica comportamento igual.
- P18/53: dois selectors filtrados, paused() e @withrevert; uma hipótese sig: não prova não-vacuidade do require paused() nem os resultados do Prover.
- A diferença PER_CALLEE_CONSTANT versus DISPATCHER(true) na spec GovernorBase entre versão auditada e snapshot é um risco de semântica efetivo, não simples gramática.

P18/4, /46 e /53 estavam NOT_RUN do parser na HEAD examinada. Os preflights por CERTORAKEY de outras rodadas são eixo distinto. Sem modificação de PR alheio.

## 6. Totais, evidências e próximos gates

| Métrica de P10 | R9 |
| --- | ---: |
| Registros documentados com chaves únicas | 266/266 |
| Novas tentativas CVL2 efetivas em derivados | 2 |
| Derivados COMPILE_OK | 1 (P10/complete/34) |
| Derivados COMPILE_ERROR | 1 (P10/complete/33, lastHasThrown) |
| NOT_RUN CVL2 na R9 | 264 incompletos |
| N.spec ORIGINAIS previamente COMPILE_ERROR (R5) | 2 (mesmos IDs 33/34; não somar como propriedades novas) |
| PREFLIGHT_AUTH_BLOCKED na R9 | 0 |
| Equivalências semânticas demonstradas | 0 |
| Projetos P10 integralmente migrados | 0 |
| Solc ProxyHarness, cena original scratch | EXIT 1 (override), NÃO CVL2 |
| Solc Storage layout scratch | EXIT 0, NÃO CVL2 |
| Perl transformação-only scratch | EXIT 0, 18 arquivos alterados, NÃO Certora |

**Próximos dois gates de propriedade, para aprovação independente do coordenador:** (1) P10/complete/33 — adjudicar a semântica histórica de lastHasThrown contra a variável suportada em CVL2 e preservar o conjunto de contraexemplos antes de qualquer nova variante. (2) P10/complete/34 — avaliar satisfatibilidade do ramo else e universo de method f com require false intocado, comparando GLOBAL versus N.spec e possível impacto de summaries. Nenhuma compilação exit 0 autoriza merge de implementação.

**Riscos vermelhos:** lastHasThrown alterado sem evidência CVL1; violação de require false; restringir f/receivers, envfree ou summaries para forçar sucesso; corrigir manualmente overrides Solidity da fonte histórica; tratar 18 mutações Perl como apenas ABI; dupla contagem de originais e derivados. Resultado CI estrutural não prova equivalência.

**Matriz:** ROUND9_MATRIX_266.csv (identidade, Property/Target/Result/Detection Outcome/Bug Label, SHA N.spec/N.sol, origem, execução antiga/atual, log, source_or_report_fact, inference, missing_proof, vacuity e próximo gate). **Diagnósticos e hashes:** ROUND9_DIAGNOSTICS.csv, ROUND9_LOG_MANIFEST.csv, ROUND9_ARTIFACTS/. **QA pós-commit:** ROUND9_QA.md. PR permanece Draft, originais intocados.

**AGENTE-01 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.**
