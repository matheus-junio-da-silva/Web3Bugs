# Auditoria de ABIs historicas e receivers — AGENTE-02, terceira rodada

**Escopo:** Evidencia source-only, sem ABI json compilada, sem migracao CVL, Prover ou replay CVL1. Cada linha da matriz abi_resolution_matrix.csv esta associada a ID, status, target, method de spec e declaracao do grafo de imports do Solidity do snapshot, quando encontrada. Imports nao provam heranca, override, dispatcher ou identidade de job.

## Matriz por target; nao agrega resultados individuais

| Target | IDs | Source observada | Bloqueio |
|---|---:|---|---|
| AccessControlMock | 4 | getRoleAdmin, grantRole, hasRole, revokeRole | Solidity public; duas rotas internal/external, sem call graph |
| ERC1155Mock | 41 | balanceOf, burn, burnBatch, isApprovedForAll, mint, mintBatch ... | Solidity public; duas rotas internal/external, sem call graph |
| ERC1155BurnableMock | 6 | balanceOf, isApprovedForAll | Solidity public; duas rotas internal/external, sem call graph |
| ERC1155PausableMock | 8 | balanceOf, paused | Solidity public; duas rotas internal/external, sem call graph |
| ERC1155Supply (historical verification harness) | 4 | balanceOf, exists_wrapper, owner, totalSupply | Harness historico nao identificado; ABI nao reconstruida |
| ERC20FlashMintMock | 1 |  | Apenas texto fonte; nao se deduz ABI efetivamente usada |
| ERC20Votes (historical voting harness) | 16 | _delegate, _delegates, _maxSupply, burn, ckptFromBlock, delegate ... | Harness historico nao identificado; ABI nao reconstruida |
| ERC20Wrapper (historical underlying-token harness) | 9 | _recover, depositFor, underlying, underlyingBalanceOf, underlyingTotalSupply, withdrawTo | Harness historico nao identificado; ABI nao reconstruida |
| ERC721Votes (historical voting harness) | 11 | _delegate, ckptFromBlock, delegate, delegateBySig, delegates, getVotes ... | Harness historico nao identificado; ABI nao reconstruida |
| Governor (historical ERC20VotesHarness) | 13 | execute, hasVoted, isCanceled, isExecuted, proposalDeadline, proposalSnapshot ... | Harness historico nao identificado; ABI nao reconstruida |
| GovernorCountingSimple (historical governor harness) | 8 | getExecutor, ghost_sum_vote_power_by_id, quorumNumerator, timelock | Harness historico nao identificado; ABI nao reconstruida |
| GovernorPreventLateQuorumHarness | 11 | getExtendedDeadline, lateQuorumVoteExtension, latestCastVoteCall | Harness historico nao identificado; ABI nao reconstruida |
| Initializable / flat verification harness (historical name not stated) | 13 | a, b, initialize, initialized, initializing, reinitialize ... | Harness historico nao identificado; ABI nao reconstruida |
| Initializable / multi-inheritance verification harness (historical name not stated) | 13 | a, b, initialize, initialized, initializing, reinitialize ... | Harness historico nao identificado; ABI nao reconstruida |
| Governor (RulesInProgress; historical ERC20VotesHarness) | 2 | proposalVotes | Harness historico nao identificado; ABI nao reconstruida |
| TimelockController | 20 | PROPOSER_ROLE, _DONE_TIMESTAMP, _minDelay, cancel, execute, executeBatch ... | Solidity public; duas rotas internal/external, sem call graph |
| UNRESOLVED (generic method probe) | 1 |  | Apenas texto fonte; nao se deduz ABI efetivamente usada |

## Evidencias especificas e implicacoes

**complete/23, ERC1155Mock:** contracts/18/contracts/mocks/ERC1155Mock.sol:10 declara heranca ERC1155. contracts/18/contracts/token/ERC1155/ERC1155.sol:110 define isApprovedForAll(address,address) public view e retorna bool; :117 define safeTransferFrom(address,address,uint256,uint256,bytes memory) public. O spec ERC1155.spec:2 e :9 contem respectivamente entradas isApprovedForAll(address,address) returns(bool) envfree e safeTransferFrom(address,address,uint256,uint256,bytes). O corpo da rule noTransferEffectOnApproval consulta a aprovacao, chama safeTransferFrom(e,...) e compara aprovacao apos a chamada. Solidity public produz implementacao internal e wrapper external, e a escolha em methods CVL2 depende do call graph real. Nao foi gerado ABI json; nenhuma das duas traducoes hipoteticas foi aprovada.

**AccessControlMock:** contratos mocks/AccessControlMock.sol e access/AccessControl.sol documentam metodos public. Nao assumir que a visibilidade da declaracao herde automaticamente o alcance de summaries CVL1. Os IDs 3-4 permanecem apenas lexicalmente documentados.

**ERC1155BurnableMock e ERC1155PausableMock:** BurnableMock herda ERC1155Burnable; PausableMock herda ERC1155Mock e ERC1155Pausable. No PausableMock, pause e unpause sao external, enquanto paused em Pausable.sol e balanceOf em ERC1155.sol sao public. Declaracoes em contratos diferentes no mesmo grafo de imports NAO substituem resolucao de override/dispatch. Ambos permanecem com contexto semantico historico nao comprovado.

**TimelockController:** contracts/18/specs/TimelockController.spec tem schedule(address,uint256,bytes32,bytes32,bytes32,uint256), divergente de contracts/18/contracts/governance/TimelockController.sol:214-221 cujo terceiro argumento e bytes calldata. Trata-se de desacordo historico de ABI ANTES de qualquer hipotese CVL2. O summary _checkRole(bytes32) => DISPATCHER(true) envolve contrato definidor AccessControl e alcance de chamada; receiver exato versus wildcard nao pode ser fixado sem closure. Os 20 IDs permanecem distintos e bloqueados.

**GovernorBase e GovernorPreventLateQuorum:** GovernorBase.spec contem getVotes(address,uint256), getPastTotalSupply(uint256) e getPastVotes(address,uint256) com DISPATCHER(true). GovernorPreventLateQuorum.spec contem getMinDelay com DISPATCHER(true) e executeBatch/scheduleBatch com CONSTANT. No CVL2 o receptor implicito resume apenas currentContract; underscore wildcard amplia outras definições, sendo necessario comprovar contrato definidor e graph of calls. O PDF pp. 10-11 descreve GovernorPreventLateQuorumHarness, override de _castVote, getters, flag latestCastVoteCall e _execute no-op, nao reproduziveis sem harness fonte exata.

**Initializable, Supply e Votes:** os 26 exemplos Initializable distribuem-se entre flat e multi-heranca nao recuperados. Supply depende de exists_wrapper e wrappers mint/burn. Votes depende de getters/checkpoints nao recuperados e de patch/harness; mesmo um blob de ERC20VotesHarness existente nao prova vinculo entre job, patch e specs originais. Nenhum resultado do PDF substitui ABI do job individual.

## Regras oficiais e status

Certora A1 CVL2 Migration Guide: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html
Certora A2 Changes Introduced in CVL2: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html ; Required internal or external annotation; optional entries; reference memory/calldata/storage; summaries only apply to one contract by default; requirements on returns. Guia Methods Block: https://docs.certora.com/en/latest/docs/cvl/methods.html , Visibility modifiers e Summary resolution.

A2 explicita que public cria rota internal e wrapper external e que funcoes chamadas diretamente de CVL nao tem necessariamente os mesmos summaries das chamadas Solidity internas. Wildcard underscore corresponde a todas definicoes da assinatura sem returns e sem optional/envfree; preferencia e sobreposicao com entradas exatas importam. Quando referencia tem arrays/bytes, locations dependem da rota. Nao converter optional, receiver, envfree, requires ou casts para satisfazer parser sem prova de semantica.

**Decisao:** 50 DOCUMENTED_CANDIDATE comprovam somente mudanca lexical candidata, nunca readiness; 131 UNRESOLVED_CANDIDATE e zero instancias liberadas para Fase 2. Para desbloquear: job exato com ABI artefato, solc, patch, remappings, imports, linkings, target/constructor, method universe, dispatch e prova de source identity; nenhum desses foi reproduzido.
