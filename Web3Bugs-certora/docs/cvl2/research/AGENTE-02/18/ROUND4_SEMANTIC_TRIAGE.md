# AGENTE-02 — Rodada 4: diagnóstico semântico por alvo (P18)

Data: 2026-10-20. Branch local isolada `research/cvl2-agente-02-round4-local`, derivada da HEAD do PR #37 `3da04efedfe6d75b049b15fa37a040572260eca4`; baseline imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.

## Regra de evidência e resultados honestos

- **`round4_diagnostic_matrix.csv`**: **181** registros distintos (69 `complete`, 112 `incomplete`) preservando `original_status`, `example_id`, `property` e `target`. `NOT_RUN=50`, `BLOCKED=131`, `COMPILE_OK=0`, `COMPILE_ERROR=0`; separadamente, `SEMANTIC_UNRESOLVED=181`, `SEMANTIC_SUPPORTED=0`. `NOT_RUN` significa teste não invocado, **não** ausência de impedimento: é a fila priorizada de pesquisa lexical. `BLOCKED` significa que faltam dependências ou ambiente histórico material para diagnóstico responsável. Nenhuma célula fabrica saída de compilador.
- **`round4_source_identity.csv`**: dez caminhos Solidity lidos diretamente no repositório `OpenZeppelin/openzeppelin-contracts` no commit auditado `109778c17c7020618ea4e035efb9f0f9b82d43ca`, com Git blob SHA-1 confrontado via `git hash-object` no snapshot. **10/10 byte-idênticos**; não são JSON ABIs nem artefatos de build. O `package.json` local informa a versão 4.6.0 e a fonte auditada pode ter identificadores/versões diversos em arquivos de distribuição: não inferir identidade do runner dessa identidade parcial dos blobs.
- Documentação formal: [Certora CVL2 Migration Guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes Introduced in CVL2](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html). A mudança `function`/`;` nos `methods` é lexical, mas a anotação `internal`/`external`, o receiver e o scope dos summaries têm impacto semântico. A documentação alerta que `public` gera rota externa mais rotina interna, e que summaries em CVL2 deixam de abranger implicitamente todos os contratos.
- O comparativo de specs de origem de `source_comparison.csv` permanece bloqueante: 12 specs não constam no `certora/specs` desse commit e quatro homônimas têm Git blobs diferentes. Não há documento de execução que associe esses arquivos da extração ao ABI, bytecode, solver e resumo de chamadas do job histórico.
- Preservados todos `contracts/`, `results/spec/`, PDFs, arquivos `.spec`, CSV de catálogo e resultados históricos.

## Priorização exaustiva das 50 candidaturas lexicais

| Fila | Chaves `complete/18/N` | Total | Evidência e gate |
|---|---|---:|---|
| A: selector `sig:` | 5, 9, 53 | 3 | 1 + 6 + 2 literais tipados respectivamente em trecho CVL ativo; confirmar assinatura e universo `method f` do ABI compilado antes de converter |
| B: AccessControl | 3, 4 | 2 | `grantRole`, `revokeRole`, `hasRole` definidos no Solidity e base/mock com blobs idênticos, mas as rotas `public` são internal e external |
| C: ERC1155 principal | 6, 8, 12–25, 28–34, 37–45 | 32 | `ERC1155Mock`, `ERC1155`, `mint`, `burn`, transfer e aprovação: source conhecido, porém escolha de método e contracena do runner não demonstradas |
| C: ERC1155Burnable | 46–51 | 6 | `ERC1155BurnableMock` herda `ERC1155Burnable`; diferenciar `burn` `public` da extensão e getters herdados |
| C: ERC1155Pausable | 52, 54–59 | 7 | `ERC1155PausableMock` herda `ERC1155Mock` e `ERC1155Pausable`, e `paused()` é `public` em `Pausable`; `pause`/`unpause` do mock são `external` |

**Soma por fila disjunta:** 3 + 2 + 32 + 6 + 7 = **50**. **Partição por target:** 2 AccessControl, 34 ERC1155Mock, 6 ERC1155BurnableMock e 8 ERC1155PausableMock. A fila A corresponde a um subconjunto dos três targets ERC1155; os IDs 5, 9 e 53 foram retirados das respectivas filas C para impedir contagem dupla.

### Exemplos onde o nome da função não basta

1. **`complete/3` e `complete/4` — AccessControlMock.** `grantRole(bytes32,address)` e `revokeRole(bytes32,address)` são `public` em `AccessControl.sol`, e `hasRole(bytes32,address)` igualmente. Acrescentar `function` e `;` à declaração é necessário em CVL2; converter automaticamente para `internal` pode resumir/interceptar o corpo onde o outer wrapper não o faria. Marcar como `external` parece plausível para chamada de regra, mas não é prova da mesma exposição e dispatch do runner auditado. Nenhum summary direto consta da source spec; não adicionar um.
2. **`complete/5` — `unexpectedAllowanceChange`.** Filtro `f.selector != setApprovalForAll(address,bool).selector` tem literal tipado ativo; `sig:` é exigência sintática oficial. A população de `f` no ABI do mock importa; sem ela não se demonstra que o filtro exclui o mesmo conjunto de métodos em CVL1 e CVL2.
3. **`complete/9` — `unexpectedBalanceChange`.** Seis ocorrências de literais tipados ativos de selector (não seis propriedades independentes). Não alterar a quantificação ou o conjunto dos métodos ao migrar.
4. **`complete/23` — `noTransferEffectOnApproval`.** `safeTransferFrom` é `public` em `ERC1155.sol`; a análise do coordenador sobre as duas rotas compiladas permanece aplicável. A igualdade da source não prova a resolução para `internal`/ `external`.
5. **`complete/46`–`51` — Burnable.** O mock estende `ERC1155Burnable`, cuja `burn` é `public` e verifica titular ou aprovação; já `ERC1155Mock.burn` chama `_burn` diretamente, sem essa mesma guarda. Trocar os targets homônimos alteraria o universo de contraexemplos. `balanceOf` é herdado. O contexto de receiver é necessário mesmo sem summary direto na spec.
6. **`complete/53` — Pausable.** Filtro para `safeTransferFrom(...,bytes)` e `safeBatchTransferFrom(...,bytes)` tem dois literais tipados. O mock implementa `pause` e `unpause` como `external`, mas `paused` é `public` herdado; anotar todos os métodos com uma só regra de visibilidade seria incorreto.

### Famílias adiadas sem promover status

- **ERC1155Supply (4):** `exists_wrapper` e harness histórico não comprovados. `ERC1155Supply.sol` byte-idêntico não equivale ao wrapper nem ao target da verificação.
- **ERC20/ ERC721 Votes, Wrapper, FlashMint (37):** `_delegate`, getters de checkpoints, `ckptFromBlock`, `_recover`, `unsafeNumCheckpoints`, mock token e patch de exposição podem exigir ABI não presente. Getter homônimo não autoriza síntese.
- **Governor (34):** `ERC20VotesHarness` recuperável tem hash, mas não o job; `GovernorPreventLateQuorumHarness` ausente; `getVotes`, `getPastVotes`, `getPastTotalSupply` com `DISPATCHER(true)` exigem conferir *todos* os call sites e receivers. Em CVL2, um resumo `Governor.getVotes` restringiria o alvo, enquanto `_.getVotes` expande a qualquer contrato com assinatura correspondente; nenhuma dessas opções foi demonstrada como equivalente ao summary global CVL1.
- **Initializable (26):** duas cenas (flat e herança múltipla) não são identificadas por um contrato `Initializable.sol` sozinho. Mesmo nome de rule não autoriza colapsar as instâncias.
- **TimelockController (20):** `schedule(address,uint256,bytes32,bytes32,bytes32,uint256)` na spec conflita com `schedule(address,uint256,bytes,bytes32,bytes32,uint256)` Solidity; não converter o parâmetro `bytes32` para `bytes` sem fonte histórica que prove a intenção. A summary `_checkRole(bytes32) => DISPATCHER(true)` pode ter receiver/scope diferente.
- **Sanity (1):** target de probe genérico indefinido.

## Gate de compilação local

O usuário autorizou *somente* `--compilation_steps_only`, em pequenos lotes, sobre **arquivos originais copiados para scratch, um target por vez, se a cena estiver comprovada**. A igualdade dos dez blobs Solidity é evidência positiva de código; **não** comprova config, ABI de target, `--link`, spec idêntica ou scope dos summaries na época. Nenhuma das 17 cenas do inventário tem no momento essa associação histórica completa; portanto **nenhum compilador foi invocado**, não existem stdout/stderr de compilação a interpretar. A tentativa de consulta à wrapper local de `certoraRun --version` foi interceptada por sua checagem de `CERTORAKEY` ausente, anterior a qualquer compilação; **não** é classificada como `COMPILE_ERROR`.

Não executar a ferramenta de migração que edita os arquivos in-place, não adicionar `require_`, `assert_`, mocks, summaries, receivers `_`, casts nem premissas para eliminar contraexemplos.

## Artefatos pendentes para nova rodada executável

Manifest por *job*: comando e working directory originais; blobs de spec e imports; contratos/harnesses usados e seus patches aplicados; compilador, `--solc_map`, `--link`, flags; ABI/bytecode alvo; funções mapeadas; call-resolution e scope efetivo dos summaries; semântica tipada da fórmula e domínio de inputs. Depois disso, um único target e um arquivo de spec original em scratch poderia receber diagnóstico compilador, sem afirmação de prova de equivalência automática.

**Decisão:** 50 candidaturas lexicalmente motivadas, **zero autorizadas para implementação**. Todas as 181 propriedades continuam `SEMANTIC_UNRESOLVED`; nenhum resultado histórico foi reexecutado ou transferido. PR exclusivamente documental, DRAFT.

**AGENTE-02 — RODADA 4.**
