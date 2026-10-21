# AGENTE-01 — RODADA 4 / Furucombo: investigação e gates

**PR:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 (DRAFT; sem merge)
**Baseline imutável:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`
**HEAD documental de entrada:** `763f3f38d28f1b37a4686c812e2bfc6699bbc35a`
**Commit auditado:** `dinngo/furucombo-contract@c90dec1046e5e26edf70f985dd86381403912482`
**OZ 3.3.0 (fontes etiquetadas):** `OpenZeppelin/openzeppelin-contracts@6be5ffe54fc8982b7c1d0f45d4cb7bbd313107cd`. Identidade do tarball npm e ABI binária **não demonstradas**.

## Metodologia e significado de status

As regras de `docs/spec_catalog.md`, `spec_catalog_workflow.md`, `spec_catalog_project_1.md` e `standard.md` foram relidas. Os resultados históricos NÃO equivalem a status de compilação. O inventário da revisão anterior (266 N.spec, 266 N.sol, 266 N.md, 264 N.txt) foi novamente conferido **por leitura programática e hash Git blob** nesta rodada: 1.062 de 1.062 hashes coincidiram com `individual_source_audit.csv`; isso não se apresenta como nova leitura semântica humana linha a linha dos 1.062 documentos.

A nova `round4_progress_matrix.csv` possui exatamente 266 linhas, chave `(status, example_id)`; contém links fixados ao baseline, blob SHA por fonte, URL ao commit auditado, seed/runner, diferenças de target, dependências e gates por exemplo, status de compilação explicitamente `NOT_RUN_COORDINATOR_GATE_REQUIRED`, blocker e próxima ação. Assim, cada exemplo tem registro independente; grupos similares NÃO são convertidos em um único job histórico.

## Prova da separação entre mudança lexical e ABI / universo semântico

Documentação oficial:
- https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html — simple migration script, `invoke`/`sinvoke`, `sig:`, métodos; **script pode errar** e escreve in place (NÃO executado).
- https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html — methods `function`/`;`, anotação `internal`/`external`, tipos de referência, `optional`, scopes de summaries, receiver, `mathint` e casts.

Do **não** inferir de "mudança obrigatória de gramática" que todos os métodos do Solidity resolvem para a mesma ABI, que o receiver permaneceu o mesmo ou que os mesmos contraexemplos sejam possíveis. `public` pode gerar rotas internal e external distintas; CVL2 restringe summary por default ao `currentContract`, diferentemente do alcance global em CVL1. O uso de `_` só pode ser justificado por evidência de cada contrato definidor/dispatch, não pelo nome de função.

### complete/33 — noThrow

- [spec auditada `libParam.spec:1–19`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L19).
- [`LibParamHarness.sol:10–18`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L10-L18): `isStatic(bytes32)` e `getNumOfReferences(bytes32)` têm wrappers **external** no target, distintos dos helpers internos da biblioteca `LibParam`.
- [`libParam.sh:1–4`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/libParam.sh#L1-L4): executa somente esse harness com `--verify LibParamHarness:specs/libParam.spec`; não usa `_runHandler.sh`, logo a ressalva de ABI pós-Perl dos handlers não é aplicável.
- N.spec:5,6: `function`, `external` e `;` são candidatos **textuais com visibilidade de fonte**. N.spec:13 requer `sig:getParams(bytes32).selector` por regra lexical. Preservar `require e.msg.value == 0`, `require !isStatic(x)`, `require getNumOfReferences(x)>0`, `getParams@withrevert`, `f@withrevert` e `assert !lastHasThrown`.
- Mesmo caso delimitado não tem prova de ABI compilada, CLI/solc/flags reproduzidos, linkings, resolução de chamadas ou equivalência; **sem autorização para experimento derivado**.

### complete/34 — noRevert

- [spec auditada `libParam.spec:21–31`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L21-L31) e a mesma fonte de harness/driver sem Perl.
- N.spec:8 contém método literal ativo `getParams(bytes32).selector`: sintaxe candidata `sig:getParams(bytes32).selector`.
- N.spec:9 `require false;` **exclui** o ramo desse selector da avaliação da asserção; N.spec:13 `assert !lastReverted;` recai no ramo `else` sob `require e.msg.value == 0`. É incorreto chamar isso de prova de não-reversão de `getParams`. Não alterar exclusão, preconditions, calls nem assert; não introduzir cast aritmético onde não há aritmética.
- Esta decisão é exclusivamente documental. Nenhuma compilação/Prover foi executado.

### incomplete/11–12 — 14 falsos positivos de `sig:`; cinco operações legadas

- [`privileged.spec:1–31`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/privileged.spec#L1-L31): sete selectors tipados aparecem em `/* ... */` e não são código CVL ativo; cada um reaparece no recorte N.spec de **dois targets**, totalizando 14 registros anteriormente indevidamente marcados `REQUIRED_SIG_LITERAL_SYNTAX`. Reclassificação pontual: `COMMENT_ONLY_NO_CVL2_CHANGE`. Manter o `definition knownAsNonPrivileged(...) = false` literal.
- N.spec:24 e :30 contêm, respectivamente, `invoke f(e1,arg)` e `invoke f(e2,arg2) at initialStorage`; são **ativas**, agora documentadas como quatro ocorrências `LEGACY_INVOKE_*` com gates diferentes. Não assumir que migração direta preserva armazenamento, efeitos de reversão e universo de métodos sem runtime histórico.
- Incomplete/11 Registry precisa de OZ Ownable e prova do target; /12 Proxy tem divergência substancial entre dependências OZ do snapshot 0.8.10 e fonte auditada 0.6.x. Dados nos N.txt originais mantidos.

### incomplete/15–16 — ProxyHarness / missing `stack_slot`

- [`ProxyHarness.sol` no commit auditado](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/ProxyHarness.sol#L1-L30) expõe getters, mas a própria árvore histórica/snapshot preservada não fornece resolução demonstrada de `stack_slot` na cadeia examinada (ver N.txt de cada ID). A fonte de wrapper, ainda que external, **não fecha** a dependência; sem compilação local.
- As entradas `REQUIRED_SYNTAX_VISIBILITY_SOURCE_SUPPORTED` identificam **apenas** declaração de método e requisito gramatical, nunca prontidão experimental.

### incomplete/35 — sanity

- Fonte: `contracts/10/specs/sanity.spec`; N.spec:7 contém `sinvoke f(e,arg)` (quinta ocorrência legada acrescentada). Assert `false` é diagnóstico; o target está **UNSPECIFIED** e não existe runner individual atribuível. Não compilar nem supor um target arbitrário.

## Perl, ABI e diferenças históricas

- [Runner auditado `_runHandler.sh:38–108`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L38-L108): alterações regex de `HandlerBase`, getters injetados e renames por família. A aplicação textual ao source não equivale à ABI compilada.
- O runner antigo define `getSender/getCubeCounter/isHandler` `public`, sem `view`; o snapshot posterior diverge. `getSlot/getStackLength` são wrappers `external`; a classe derivada só recebe a injeção por match real na declaração alvo. Classes com herança indireta não são automaticamente cobertas.
- `target_revision_matrix.csv` e `perl_getter_scope_matrix.csv` preservam 28 contextos, diferenças de blob/pragma/import e alcance estimado; 22 source paths distintos diferem entre snapshot e commit auditado, e o script de 2021 tem blob `b603b618b4e85782cc63b9b97101a928c350636b` versus snapshot posterior `c31b728ca03d3a4e3c8bc53fa27c2eb23e0fe6a7`.
- A recuperação da tag OZ 3.3.0 supre evidência textual de imports, **não** comprova npm tarball, ABI pós-Perl, solc/CLI efetivos e multicontract linkings. Falhas de atribuição do relatório PDF não foram promovidas a prova por exemplo: 138 células das páginas físicas 26–31 eram `None`, sem trace individual.

## Resultado da triagem para compilação isolada

**Compilação CVL2: zero.** Apenas complete/33–34 formam o menor grupo com source/harness/driver documentados em um target sem Perl; porém nenhuma implementação derivada foi autorizada individualmente pelo coordenador e não há modelo histórico executado equivalente. Todos os outros 264 são `incomplete` na base: não se deve usar o diagnóstico lexical de 36 exemplos sem bloqueio na matriz como substituto de closure de dependências; `15/16` e `35` exemplificam isso.

**Nenhum `--compilation_steps_only`, Prover, CVL1, solc ou scripts de mutação foi executado.** Status `NOT_RUN` não é falha nem sucesso de compilação. O próximo avanço seguro é prova material de ABI/harness/runner do commit auditado ou gate individual expresso para cópias temporárias, preservando todos os `require` e `assert`.

**AGENTE-01 — RODADA 4.**
