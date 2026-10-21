# AGENTE-01 — RODADA 5 — QUALIDADE CVL2 / P10

## Escopo e controles

Projeto 10 — 266 exemplos, 2 complete e 264 incomplete; branch research/cvl2-agente-01 no PR https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 (DRAFT, sem merge).
Baseline imutável: 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3.
Origem Furucombo auditada: dinngo/furucombo-contract@c90dec1046e5e26edf70f985dd86381403912482.
Fonte OpenZeppelin 3.3.0: OpenZeppelin/openzeppelin-contracts@6be5ffe54fc8982b7c1d0f45d4cb7bbd313107cd.
Painel de coordenação lido sem modificações: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/47 — HEAD 705641e9f8920da648c724ce4c3361f03b8ac821, zero equivalências provadas.

Antes de editar, consultados integralmente os quatro documentos de políticas do catálogo: docs/spec_catalog.md, docs/spec_catalog_workflow.md, docs/spec_catalog_project_1.md, docs/standard.md; também os comentários/revisões do PR #39, incluindo a revisão da Rodada 4 que autoriza exclusivamente diagnose compile-only no ambiente recuperado. Nenhuma alteração nos originais de results/spec, contratos, scripts, PDF, relatórios, CSV de Bug Labels ou arquivos da branch do AGENTE-02.

Status da rodada: **LARANJA** — duas compilações diagnósticas individuais EXECUTADAS com exit 1 por sintaxe histórica; COMPILE_OK=0, SEMANTIC_PROVEN=0, MIGRATED_COMPLETE=0. Não executar Prover nem CVL1; sem implementação derivada até gate individual do coordenador.

## Evidências fixadas: fonte, destino e hashes

| Objeto | Fonte com linha/caminho | Commit ou SHA de blob |
| --- | --- | --- |
| LibParamHarness.sol | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L1-L22 | Git blob e31683f3b63a95d3522f897748d0d13159388a15 |
| LibParam.sol (único import) | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/lib/LibParam.sol#L1-L72 | Git blob 740e8a5ccae25d5e041c9736545c13de7cd3867f |
| libParam.sh | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/libParam.sh#L1-L4 | Git blob 3344316e9569c8292df6d47725126dfa3173c605 |
| libParam.spec compartilhada | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L31 | Git blob 096f9f704226a7aa77c3d0da3862644db5051eb3 |
| complete/33.spec extraída | https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/10/33.spec#L1-L22 | Git blob e55057a90f641156538f732c0fe172c28cd86dad |
| complete/34.spec extraída | https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/10/34.spec#L1-L14 | Git blob 3e180d5f3a046f2e63192cd1a464cadff5b8775a |
| Perl antigo; não usado por LibParamHarness | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/scripts/_runHandler.sh#L38-L108 | blob b603b618b4e85782cc63b9b97101a928c350636b |
| Registry.sol, auditado 2021 | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/Registry.sol#L1-L9 | blob 7fd035af411724057297a8bfd234eda9f024e14c |
| Proxy.sol, auditado 2021 | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/contracts/Proxy.sol#L1-L15 | blob e0b6030be761dc559489448817c6a15ba2a776e1 |
| ProxyHarness.sol, auditado 2021 | https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/ProxyHarness.sol#L1-L30 | blob 61afe55c5681a50c943ae770a951f58637e86bf6 |
| Documentação de sintaxe CVL2 | https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html | fonte oficial consultada nesta rodada |
| Manifesto compilador | https://binaries.soliditylang.org/linux-amd64/list.json | solc 0.6.12+commit.27d51765, SHA256 f6cb519b01dabc61cab4c184a3db11aa591d18151e362fcae850e42cffdfb09a |

A árvore auditada de LibParamHarness fecha exatamente em dois arquivos Solidity: specs/harnesses/LibParamHarness.sol -> ../../contracts/lib/LibParam.sol. Sem import externo nesse subgrafo; **zero arquivos OpenZeppelin alcançados** por esse target específico. Isso não comprova a identidade da distribuição npm nem toda a cena original de um job de Prover.

## Experimentos individuais CVL2 (sem patch)

Diretório scratch isolado: /home/mat/cvl2-agent01-isolated/round5-scratch/scene. Arquivos CVL e Solidity foram copiados, comparados byte a byte contra originais e identificados em round5/source_manifest.csv. Os scripts históricos foram inspecionados, não executados; o target é o harness original sem transformação Perl. As duas tentativas usaram Certora CLI 8.19.0 do venv instalado, solc 0.6.12 oficial com digest verificado pelo manifesto, timeout -k 5s 85s e a flag --compilation_steps_only. Variáveis de chave Certora explicitamente não fornecidas; nenhuma credencial lida.

| Exemplo | Arquivo byte-idêntico | Resultado real | Diagnóstico literal no log |
| --- | --- | --- | --- |
| complete/33 — noThrow | results/spec/complete/10/33.spec | **EXIT 1, COMPILE_ERROR_ORIGINAL_CVL1_SYNTAX** | 33.spec:5:2 e :6:2: methods block entries must begin with function; :5:42 e :6:55: must end with ; |
| complete/34 — noRevert | results/spec/complete/10/34.spec | **EXIT 1, COMPILE_ERROR_ORIGINAL_CVL1_SYNTAX** | 34.spec:8:30: Variable bytes32 has not been declared. Did you forget to use sig: for a method selector? |

Os logs completos são round5/logs/33_compile_only.log e round5/logs/34_compile_only.log, hashes em round5/diagnostics.csv. Não são resultados de sucesso da compilação, muito menos de equivalência CVL1/CVL2. Na tentativa 34 a CLI registrou compilação da fonte Solidity antes do typechecker CVL falhar; isso não significa scene histórica comprovada. Nenhuma spec derivada foi criada ou aplicada. Nenhum Prover foi rodado.

### Complete/33 — noThrow

No N.spec:5–6 são declarações legadas sem function/external/semicolon; no harness 2021 linhas 10 e 14 estão as funções external correspondentes, distintas das internas da biblioteca. N.spec:13 é selector ativo getParams(bytes32).selector, candidato gramatical sig:getParams(bytes32).selector. Não alterar os guards e.msg.value == 0, !isStatic(x), getNumOfReferences(x) > 0, a chamada getParams@withrevert ou a assertion !lastHasThrown. A compilação do recorte ORIGINAL falhou antes de aprovar tradução; nenhuma decisão automática sobre envfree, métodos elegíveis ou equivalência.

### Complete/34 — noRevert

N.spec:8 contém selector ativo de getParams(bytes32); o erro lexical direto confirma a ausência de sig:. N.spec:9 inclui **require false;**, que elimina o ramo getParams do universo admissível. N.spec:13 avalia assert !lastReverted apenas depois de f@withrevert no ramo else sob e.msg.value == 0. Não inferir que getParams foi provado sem reversão. Sem casts novos; assertion booleana. O recorte N.spec:34 não contém o methods block global do libParam.spec original; não criar nem inserir um sem gate.

## Parser de comentários: uma correção adicional, todos os 266 recortes

Foi executado parser de máscara com estados code, line comment, block comment e string literal, preservando linha/coluna. Depois, confronto entre selectors com assinatura tipada realmente ativos e registros METHOD_LITERAL da semantic_candidate_gate_matrix.csv: **13 ativos = 13 entradas gramaticais**, nenhuma divergência. **15 entradas em comentários** corretamente excluídas, incluindo as 14 já corrigidas na Rodada 4 dentro de incomplete/11–12.

Nova correção desta rodada em incomplete/23, N.spec:21: o texto certorafallback_0().selector encontra-se DENTRO de /* ... */, não requer sig: nem reabilitação do fallback, que não é uma referência ativa em CVL2. A assertion usa desigualdade de selectors e lastReverted; não contém operação matemática que motive cast. Dois registros documentais foram ajustados (COMMENT_ONLY_NO_CVL2_CHANGE e NO_ARITHMETIC_CAST_INDICATED). O selector ativo proxy.batchExec(address[],bytes32[],bytes[]).selector da mesma linha permanece classificado como candidato lexical, dependente de ABI/receiver. Nenhuma alteração de source, assertion ou comentário original.

## Dependências históricas dos 264 incomplete

Matriz round5_progress_matrix.csv: 266 chaves (status, ID) únicas, Property/Target/Result/Detection Outcome imutáveis, baseline/blob, prioridade, estado experimental, risco e ação individual.

- **P1 — Registry/Proxy/ProxyHarness: 29 exemplos.** Registry.sol 2021 importa Ownable.sol da OZ 3.3.0 e IRegistry; Proxy.sol 2021 importa SafeERC20.sol no caminho antigo, Address, IProxy/IRegistry, Config, Storage e LibParam. O snapshot posterior 0.8.10 usa imports e lógica diferentes; não o substituir. Em incomplete/15–16, a expressão assembly stack_slot no ProxyHarness 2021 não encontra declaração nos arquivos alvo Registry/Storage/ProxyHarness pesquisados: persistência do bloqueio original, não remendar harness.
- **P2 — famílias de handlers: 234 exemplos.** Desses, 164 são indicados na matriz como usando driver Perl e 70 não; são populações distintas, não aplicar getters injetados indiscriminadamente. O script 2021 altera virtualidade de _revertMsg, aplica regex de herança direta de HandlerBase, injeta getSlot/getStackLength/getSender/getCubeCounter/isHandler com visibilidades específicas, renomeia métodos em famílias selecionadas e modifica transfers. Source transformada não equivale a ABI compilada. A busca no tree auditado por *.abi, *.bin, *certora*.json/conf/log, package-lock.json e yarn.lock segue negativa para os nomes procurados; nenhum job completo atestável, nem conclusões sobre outras localizações não pesquisadas.
- **P3 — target UNSPECIFIED: incomplete/35.** A regra sanity usa sinvoke f(e,arg), sem target/driver individual atribuível; não escolher contrato arbitrário.
- **P0 — complete/33–34: 2.** Diagnósticos executados, falha sintática explícita, sem aumento de COMPILE_OK.

Os 264 incomplete não foram compilados nesta rodada; cada bloqueio histórico mantém sua fonte e razão da Rodada 4. Não promover conclusão de irreversibilidade universal: recuperar build artifacts específicos ou o target e continuar por outra família quando surgir evidência.

## Próximo gate requerido da coordenação

1. Gate **individual** para propor uma cópia derivada mínima do complete/33, com métodos external comprovados e selector sig:, preservação literal de todos os guards, assertions, universo de f, import graph, target, versão CLI, compilador, flags e log; depois avaliação semântica independente.
2. Gate **individual e separado** para complete/34, preservando require false, selector e exclusão do ramo getParams. Não reutilizar aprovação do 33 para o 34.
3. Para Registry/Proxy e handlers, somente após prova do material compilado/ABI pós-transformação, byte hashes do runner/seed, getters efetivamente injetados e resolução de receiver, definir candidato e novo teste. Não gerar results/cvl2 nem relatório VERIFIED com erro de parser.

**AGENTE-01 — RODADA 5 — QUALIDADE CVL2.**
### Integridade dos logs e check de whitespace

Os stdout/stderr brutos de cada tentativa são preservados **byte a byte** em round5/logs/33_compile_only.log.b64 e round5/logs/34_compile_only.log.b64. Sua decodificação Base64 reproduz exatamente os arquivos gerados pela execução (digests raw_log_sha256 em round5/diagnostics.csv). Os arquivos .log são versões legíveis, apenas com linhas vazias terminais removidas para satisfazer git diff --check; seus hashes separados constam da coluna readable_log_sha256. Nenhum conteúdo de erro foi removido. O registro do comando e exit code permanece no CSV de diagnósticos.
