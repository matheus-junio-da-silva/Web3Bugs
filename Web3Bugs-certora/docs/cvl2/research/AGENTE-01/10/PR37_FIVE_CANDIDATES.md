# Auditoria cruzada independente — cinco candidaturas DOCUMENTED_CANDIDATE do AGENTE-02

Somente leitura do PR https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37, referência fixa 2c32e08521a1a709cad9f86f4c9d2c7cb0954251. Leitura via git show da ref do PR no checkout próprio AGENTE-01; branch research/cvl2-agente-02 não foi alterada.

Os cinco pares status/ID possuem DOCUMENTED_CANDIDATE no properties.csv do AGENTE-02 e foram confrontados com o spec_buglabel.csv da mesma HEAD em Property, Target, Result e Detection Outcome (zero divergência); N.spec e dossiês foram lidos. Sem supor ABI compilada, summaries ou contrato definidor.

| Exemplo | Property / Target | Observação auditável e bloqueio |
| --- | --- | --- |
| complete/3 | grantRoleEffect / AccessControlMock | N.spec methods grantRole e hasRole; AccessControl.sol :144 e :84 têm source public. A documentação considera explicitamente as duas rotas internal/external; sem compiled ABI/harness ou call graph. Não existe summary nas entradas do recorte. |
| complete/5 | unexpectedAllowanceChange / ERC1155Mock | N.spec filtered escolhe métodos com selector diferente do literal ativo setApprovalForAll(address,bool).selector. Prefixo sig: é hipótese lexical; setApprovalForAll e isApprovedForAll public no grafo Solidity. Seleção de wrappers, métodos do universo f e ABI não certificada. |
| complete/23 | noTransferEffectOnApproval / ERC1155Mock | safeTransferFrom toma bytes memory na implementação public e bytes calldata na interface external. O N.spec tem chamada explícita e uma declaração methods para isApprovedForAll. Dossiê corretamente não escolhe internal/external, location nem receiver. |
| complete/46 | onlyHolderOrApprovedCanReduceBalance / ERC1155BurnableMock | Calls balanceOf/isApprovedForAll herdadas de ERC1155 e f paramétrico não dão ABI de job nem definição completa do conjunto de métodos. Não há summary CVL1 no recorte, e não se deve fabricar receiver wildcard. |
| complete/53 | transferMethodsRevertWhenPaused / ERC1155PausableMock | Dois literais de selector ativos em filtered (safeTransferFrom e safeBatchTransferFrom); paused() é public em Pausable.sol:64 segundo a seção ABI do próprio dossiê. Ressalva documental: a seção anterior declara “Sem declaracao Solidity localizada”; essa frase é conflitante com a evidência final de Pausable.sol:64. Precisa corrigir ou qualificar a seção, sem promover ABI compilada. |

Verificação da documentação Certora: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html (Step 4) e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html (methods, visibilidade, retorno, local de referência e summaries). As cinco candidaturas são apenas textuais; todas estão em SNAPSHOT_IMPORT_GRAPH_ONLY e não em COMPILE_OK ou SEMANTIC_PROVEN. As cinco specs homônimas não foram afirmadas idênticas à cena do commit auditado OpenZeppelin 109778c17c7020618ea4e035efb9f0f9b82d43ca.

Registro estruturado em round5/pr37_five_candidate_audit.csv. Nenhum arquivo do AGENTE-02, fonte, summary ou config foi editado. Amostra limitada a cinco instâncias, não representa reauditoria de 181 exemplos.

**AGENTE-01 — RODADA 5 — QUALIDADE CVL2 — auditoria read-only.**