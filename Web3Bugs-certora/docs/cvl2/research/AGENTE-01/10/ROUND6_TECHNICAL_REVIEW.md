# AGENTE-01 — RODADA 6 / P10 Furucombo / pesquisa técnica CVL2

**Escopo:** P10 = 266 propriedades (2 complete + 264 incomplete). Pesquisa e QA somente; não é autorização de implementação nem demonstração de equivalência.

**PR Draft:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 · branch `research/cvl2-agente-01` · HEAD inicial `e31e4fee3174bd91b99c2d62135fb095b1e0253a` · baseline imutável `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.

**Referências de coordenação:** revisão do PR #39 `pullrequestreview-5589225959` e `ROUND5_DASHBOARD.md` no PR #47, HEAD `5835165642875f52de43227cb20334bae66edb77`. Contabilidade da coordenação: 4/1386 COMPILE_OK restritos; 11/1386 COMPILE_ERROR; 1.371 sem teste observado; 0 equivalências e 0 projetos migrados. P10 responde por dois erros de compilação das tentativas **anteriores**.

## 1. Política de preservação e referência ao catálogo

Foram examinados os documentos normativos `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md`; os quatro arquivos permanecem intactos. As regras distinguem `complete` (dependências do recorte disponíveis) de CVL2 compilável, e `Result` de `Detection Outcome`.

Comparação dirigida da referência P1:

| Exemplo P1 | Propriedade / evidência | Implicação para P10 |
| --- | --- | --- |
| `complete/1/3` | `independentQueuedActions` inclui definição `stateVariableUpdate`, `methods` e chamadas; `Result=VIOLATED`, `Detection Outcome=FINDING` vêm do relatório, não de recompilação | Não inferir sucesso de CVL2 de `complete` nem eliminar definições/restrições |
| `incomplete/1/1` | `queuePriviliged` depende do `queue2` histórico ausente; `N.txt` declara o símbolo faltante | Não inventar `stack_slot`, getter Perl, target ou ABI em P10 para promover `incomplete` |
| Inventário P1 | 36 complete, 34 incomplete, 70 chaves, 72 relacionamentos | Status do catálogo distinto de compile-only e de equivalência |

Fonte P1: `results/spec/complete/1/3.spec`, `results/spec/incomplete/1/1.spec` e `.txt` em `main@2a03637...`.

Documentação oficial consultada: [CVL2 migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html) e [expressions](https://docs.certora.com/en/latest/docs/cvl/expr.html). `envfree` não autoriza mudar o universo de chamadas ou acrescentar um receiver wildcard.

## 2. P10/complete/33–34 — closure, ABI e recortes versus spec GLOBAL

| Arquivo de 2021 | URL exata / linhas | Hash Git |
| --- | --- | --- |
| `specs/libParam.spec` | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L31 | `096f9f704226a7aa77c3d0da3862644db5051eb3` |
| `specs/harnesses/LibParamHarness.sol` | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L1-L22 | `e31683f3b63a95d3522f897748d0d13159388a15` |
| `contracts/lib/LibParam.sol` | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/lib/LibParam.sol#L1-L72 | `740e8a5ccae25d5e041c9736545c13de7cd3867f` |
| `specs/scripts/libParam.sh` | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/libParam.sh#L1-L4 | `3344316e9569c8292df6d47725126dfa3173c605` |

**Closure textual já fechada na Rodada 5:** `LibParamHarness.sol` importa somente `../../contracts/lib/LibParam.sol`. As funções internas da biblioteca **não** são a ABI do wrapper. No harness do commit auditado, a ABI externa identificável em fonte é:

| Função do harness | Visibilidade Solidity | Retorno ABI |
| --- | --- | --- |
| `isStatic(bytes32)` | `external` | `bool` |
| `isReferenced(bytes32)` | `external` | `bool` |
| `getReturnNum(bytes32)` | `external` | `uint256` |
| `getParams(bytes32)` | `external` | sem retorno |
| `getNumOfReferences(bytes32)` | `external` | `uint256` |

O driver `libParam.sh` usa `--verify LibParamHarness:specs/libParam.spec`, opção histórica `-b=64,-smt_bitVectorTheory=true`, **sem** chamar o Perl dos handlers. O compilador Solidity auditado é 0.6.12 e a CLI observada no teste anterior 8.19.0; não se demonstra identidade do job Certora 2021 por isso. O registro de fonte/byte-copy e hashes das duas execuções de Rodada 5 permanece em `round5/source_manifest.csv` e `round5/diagnostics.csv`.

**Diferença fundamental GLOBAL versus recorte:** `complete/33.spec` tem as duas declarações `methods` do `libParam.spec` original; `complete/34.spec` contém apenas a `rule noRevert`, **sem** o `methods` global. Não inserir as declarações no 34 como se fossem dependências CVL automaticamente ausentes: devem ser comparadas ao target/universo antes de qualquer opção de implementação. A compilação do fragmento original não é a compilação da spec global.

### Hipótese mínima DOCUMENTAL — não aplicada nem executada em R6

No contexto exclusivo de `LibParamHarness`, declarações CVL2 hipotéticas para o `methods` do **33**:

```cvl
methods {
    function LibParamHarness.isStatic(bytes32) external returns (bool) envfree;
    function LibParamHarness.getNumOfReferences(bytes32) external returns (uint256) envfree;
}
```

As duas entradas têm receiver **exato**, em vez de `_.`, para evitar ampliar o universo de métodos; o alvo é também o `currentContract` indicado no `--verify`. A qualificação explícita é uma **hipótese** de sintaxe/escopo, não um patch autorizado nem uma ABI compilada. Não inventar `optional` ou `internal`. `external` é respaldado pela fonte, mas `envfree` e a correlação das rotas do harness ainda exigem avaliação de execução.

Nos dois recortes, o literal tipado ativo `getParams(bytes32).selector` tem hipótese gramatical `sig:getParams(bytes32).selector`. A linguagem CVL2 exige `sig:` para method literals, mas isso não atesta o conjunto de métodos gerados pelo Prover nem a mesma semântica para `f.selector`.

**33 — noThrow:** preservar, sem modificação, `require e.msg.value == 0`, `require !isStatic(x)`, `require getNumOfReferences(x)>0`, `getParams@withrevert(e,x)`, `f@withrevert(e,arg)` e `assert !lastHasThrown`. A variável histórica `lastHasThrown` **não** deve ser trocada silenciosamente por `lastReverted`: o tratamento semântico de throw/revert e o próximo erro de typechecker precisam ser constatados antes. A restrição `getNumOfReferences(x)>0` não garante que a execução de `getParams(x)` cumpra todas as pré-condições internas da biblioteca; pode haver reverts admissíveis sob `@withrevert`.

**34 — noRevert:** manter literalmente `require false;` no ramo `f.selector==getParams(bytes32).selector`. Isso **retira esse ramo do universo admissível**: `assert !lastReverted` recai no `else`, depois de `f@withrevert`. Não proclamar getParams comprovado. Não acrescentar chamadas depois de `f@withrevert` antes da assertion: `lastReverted` reflete a **última** chamada e pode ser sobrescrito. Nenhum cast aritmético se justifica nessa assertion booleana.

**Ghosts/hooks:** `libParam.spec` não declara `ghost` nem `hook`; isso é uma constatação de fonte, não licença para ignorar hooks de uma cena histórica distinta. A semântica de ghosts (revert/havoc/storage snapshot) pode alterar provas em outros clusters; não extrapolar aos handlers.

### Histórico experimental versus R6

| Exemplo | Último teste CVL2 realmente executado | Estado atual | Novo teste R6 |
| --- | --- | --- | --- |
| 33 | Rodada 5: CLI direto 8.19.0 e solc 0.6.12, exit **1**, linhas 5–6: falta `function` e `;` | `COMPILE_ERROR` histórico documental | `NOT_EXECUTED_INFRA_EIO` |
| 34 | Rodada 5: CLI direto 8.19.0 e solc 0.6.12, exit **1**, linha 8: falta `sig:` | `COMPILE_ERROR` histórico documental | `NOT_EXECUTED_INFRA_EIO` |

Nenhum `COMPILE_OK`, `SEMANTIC_PROVEN` nem `MIGRATED_COMPLETE`. **Nenhuma variante temporária chegou a ser executada nesta rodada.** A falha no checkout remoto apresentou `EIO` em leitura de arquivos e `Bus error` até em `python3 -V`; isso é **bloqueio de infraestrutura**, não `COMPILE_ERROR` novo nem `PREFLIGHT_AUTH_BLOCKED`. Não foram consultados tokens, `.env` nem credenciais.

## 3. Bloqueios dirigidos nos demais 264 exemplos

- **Registry/Proxy/ProxyHarness (29):** `Registry.sol` do commit auditado importa OZ 3.3.0 `access/Ownable.sol` e `IRegistry`. `Proxy.sol` usa paths e versão Solidity 0.6 diferentes dos snapshots 0.8.10, inclusive `SafeERC20`. Em `ProxyHarness.getStackLengthSlot()`, `assembly { x := stack_slot }` não tem resolução comprovada na closure pesquisada; os incomplete/15–16 permanecem sem teste. Recuperação de tarball/imports não substitui ABI histórica e linkage.
- **Famílias de handler (234):** 164 registros têm driver identificado com Perl; 70 não. O `_runHandler.sh` auditado injetava getters e aplicava renames somente sob padrões/arquivos específicos; `public` dos getters não equivale automaticamente à rota `internal` ou `external` em CVL2. Não propagar alterações Perl a targets cujo wrapper não as executava. Falta ABI pós-transformação, flags/scene/linking, receiver/summaries, compatibilidade do snapshot e fonte executada.
- **Sanity incomplete/35 (1):** target `UNSPECIFIED` e `sinvoke` legada; não atribuir target/driver arbitrários.
- **Selectors de comentário:** 14 falsos positivos em incomplete/11–12 e um em incomplete/23 foram rebaixados na Rodada 5. Há **13 method literals ativos** comprovados contra o parser de comentários; não reeditar originais. Não foi necessário alterar novamente a matriz desses gates.

Esses registros individualizados estão em `round6_progress_matrix.csv`, com chave `(project_id, original_status, example_id)`, SHA Git do CVL e Solidity extraídos, fonte/target auditados, bloqueio e próximo gate.

## 4. Revisão cruzada SOMENTE LEITURA — PR #37 / P18/3 e P18/23

HEAD verificada do outro PR: `9350a3f9a1ffd5861358a3b085adfa2bd48a8e6b`. Ambos os dossiês continuam como `DOCUMENTED_CANDIDATE`, somente hipótese lexical, com ABI de **snapshot** e não prova do job auditado. **Não foi alterado nenhum arquivo do AGENTE-02.**

| P18 | Source e property | Conclusão independente |
| --- | --- | --- |
| complete/3 | `AccessControl.spec`, `grantRoleEffect`, target `AccessControlMock` | `grantRole` e `hasRole` public em `AccessControl.sol:144,84`; métodos `internal` e wrappers `external` não são intercambiáveis. A regra chama `hasRole` antes/depois de `grantRole`; ABI compilada do snapshot não comprova o mesmo universo/call graph na execução auditada. Sem summary CVL no recorte. |
| complete/23 | `ERC1155.spec`, `noTransferEffectOnApproval`, target `ERC1155Mock` | `safeTransferFrom` é public com parâmetro `bytes memory` na implementação e `bytes calldata` na interface; `isApprovedForAll` também é public. A rota `internal/external` e a assinatura anotada CVL2 devem ser demonstradas para a chamada real. Sem summary CVL no recorte. |

A coordenação já reproduziu com CLI **direto** ambas as tentativas originais de P18: EXIT 1 por gramática `methods`, conforme `ROUND5_DASHBOARD.md`. Essas execuções **não são testes deste AGENTE-01**; os nove preflights anteriores do AGENTE-02 com wrapper e falta de `CERTORAKEY` são `PREFLIGHT_AUTH_BLOCKED`, não erros de compilação. O commit auditado `OpenZeppelin/openzeppelin-contracts@109778c17c7020618ea4e035efb9f0f9b82d43ca` não comprova identidade das specs e harnesses históricos para esses exemplos.

## 5. QA, situação e gates

**Status R6: LARANJA — pesquisa documental publicada, execução local bloqueada por infraestrutura.** Sem novos compiles, sem Prover, CVL1, scripts in-place ou migração em lote. A matriz nova mantém 266 chaves, 2 COMPILE_ERROR anteriores e 264 NOT_RUN; **zero** COMPILE_OK e **zero** PREFLIGHT_AUTH_BLOCKED atribuídos ao P10. Os resultados históricos `Result`/`Detection Outcome` são copiados sem alteração.

**Importante:** a instabilidade do filesystem no WSL remoto impediu executar os três validadores Python e o `git diff --check BASE...HEAD` após os commits desta rodada. Esses checks são **NÃO EXECUTADOS POR INFRA_EIO**, não estão marcados como aprovados; a validação estrutural do Github Actions, caso disponível, deve ser checada separadamente e não substitui afirmações de execução local.

**Próximos gates requeridos:**
1. Recuperar estabilidade do dispositivo WSL/checkout sem reset, rebase automático ou interrupção de outros agentes; conferir novamente HEAD/escopo e executar os três validadores e `git diff --check`.
2. Gate individual para variante **temporária** de 33 com `function`, receiver explícito `LibParamHarness`, `external`, `sig:`, sem mudar guards/assertions; rodar `--compilation_steps_only` com logs, sem confundir typecheck com equivalência.
3. Gate separado para 34, mantendo `require false`, sem tratar ramo excluído como verificado; comparar a spec global e o recorte isolado.
4. Resolver ABI histórica/scene de Registry, Proxy, `stack_slot` e Perl por target/runner antes de outros compile-only. Exigir verificação de vacuity, universe `method f`, reverts, call graph e hooks/ghosts quando aplicáveis.

**Assinatura: AGENTE-01 — RODADA 6.**
