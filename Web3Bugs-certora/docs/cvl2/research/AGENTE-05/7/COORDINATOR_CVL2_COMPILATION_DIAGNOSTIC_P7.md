# Diagnóstico CVL2 de compilação local — P7/37 e P7/65

**Data:** 2026-10-19. **Escopo:** experimentação **sem Prover** e **sem CVL1**, somente `--compilation_steps_only` sobre cópias byte-idênticas, em cenário de Solidity do **snapshot PropertyGPT/Web3Bugs**, não a cena Certora auditada em janeiro/2022. **Branch:** `research/cvl2-agente-05`. Este relatório complementa [a auditoria da import closure](COORDINATOR_CLOSURE_P7_3_37_65.md) e [a comparação com os scripts auditados](COORDINATOR_HISTORICAL_RUNNER_AND_ABI_P7.md).

## 1. Escopo e proteção das fontes

- Dataset original: `results/spec/complete/7/37.spec` e `results/spec/complete/7/65.spec`; foram lidos e copiados **sem trocar um único byte**.
- Specs integrais de origem: `contracts/7/specs/StableDebtToken.spec` e `contracts/7/specs/VariableDebtToken.spec`; igualmente copiadas e comparadas com `cmp`.
- Solidity: cópias isoladas da árvore `contracts/7/contracts/` (1,1 MiB no snapshot), sem alteração. Target `StableDebtToken.sol:StableDebtToken` ou `VariableDebtToken.sol:VariableDebtToken` conforme Example ID.
- Espaço temporário WSL: `/tmp/cvl2_p7_snapshot_diagnostic_20261019/<ID>/`, não adicionado ao repositório. CLI nativo `certora-cli 8.19.0`; Solidity `solc 0.8.10+commit.fc410830.Linux.g++`; processo `timeout --signal=TERM --kill-after=5s 60s`, variáveis `CERTORAKEY`, `CERTORA_TOKEN`, `CERTORA_API_KEY` removidas do subprocesso, `HOME` temporário.
- Foram executadas exclusivamente as **etapas de compilação/typechecking** locais do CLI. Não foi solicitada verificação simbólica formal, execução Prover, CVL1, regras novas, configuração de patches, linkings históricos nem execução de harness de 2022.

### Comando por exemplo

A partir da cópia temporária de seu respectivo Example ID e com `HOME` isolado:

```bash
certoraRun contracts/protocol/tokenization/StableDebtToken.sol:StableDebtToken \
  --verify StableDebtToken:specs/property.spec \
  --compilation_steps_only --solc /home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10

certoraRun contracts/protocol/tokenization/VariableDebtToken.sol:VariableDebtToken \
  --verify VariableDebtToken:specs/property.spec \
  --compilation_steps_only --solc /home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10
```

Os testes das specs completas trocam exclusivamente o argumento `--verify` para `StableDebtToken:specs/full_legacy.spec` ou `VariableDebtToken:specs/full_legacy.spec`; os arquivos de entrada continuam idênticos às suas fontes.

## 2. Validação byte a byte

| Exemplo | SHA-256 do fragmento catalogado e da cópia | SHA-256 da spec completa e da cópia | `cmp` |
| --- | --- | --- | --- |
| P7/complete/37 | `f31e464ce0d28c1ea71dafde572d9b83cf6d82826ebdcb02c3d493e9016edbbd` | `e737e5146477422a2666a6f00cc80344b0f5ba4` | 0 em ambos |
| P7/complete/65 | `ce1539d8bab260852c124f54df56cd78f7758bfc0a26b4c35c912084281c2fe9` | `a21a5649f7b10dd3137cf196a8c81e668f1243` | 0 em ambos |

**Falha preliminar de preparação registrada:** um teste inicial colocou as cópias dos fragmentos em modo filesystem somente leitura (`chmod a-w`). O CLI tentou escrever uma `.0_property.spec.spec` interna e retornou `Permission denied` em ambos os casos, logo os dois códigos de saída 1 iniciais **não constituem erro CVL2 da spec**. O erro foi corrigido **apenas mudando a permissão da cópia temporária, sem tocar no conteúdo**; os `sha256sum` e `cmp` permaneceram iguais. Os resultados abaixo são os da repetição válida.

## 3. Resultado da compilação-only sobre fragmentos N.spec

| Exemplo | Target do snapshot | `--compilation_steps_only` | Observação |
| --- | --- | --- | --- |
| P7/complete/37 | StableDebtToken | **EXIT 0** | `Stack too deep` na tentativa auxiliar de autofinder para variáveis internas; CLI registra `falling back to original file`, continua e encerra 0. Não interpretar a etapa auxiliar como sucesso da instrumentação. |
| P7/complete/65 | VariableDebtToken | **EXIT 0** | Compilação e preparação de informação de funções internas concluídas sem mensagens de erro. |

Excertos representativos de stdout:

```text
P7/37: Encountered an exception generating autofinder ...
CompilerError: Stack too deep, try removing local variables.
... falling back to original file StableDebtToken.sol
Compiling ... to expose internal function information...
[process exit 0]

P7/65: Compiling contracts/protocol/tokenization/VariableDebtToken.sol...
Compiling ... to expose internal function information and local variables...
[process exit 0]
```

**Interpretação rigorosa:** o typechecker/compilation path aceitou ambos os **fragmentos**, com o target indicado do snapshot; isso não prova que sejam provas completas, semanticamente equivalentes à CVL1 original, livres de vacuity, nem que o instrumento auxiliar de StableDebtToken foi gerado sem fallback.

## 4. Contrateste — specs CVL integrais, sem qualquer modificação

| Origem completa | `--compilation_steps_only` | Incompatibilidades observadas |
| --- | --- | --- |
| `contracts/7/specs/StableDebtToken.spec` | **EXIT 1** | 6 entradas `methods` sem palavra `function` + 6 sem terminador `;`; `if (x == 0) || (y == 0)` em linha 47, rejeitado perto de `||`; hook `Sstore` com `STORAGE` redundante em linha 118. |
| `contracts/7/specs/VariableDebtToken.spec` | **EXIT 1** | 5 entradas `methods` sem palavra `function` + 5 sem `;`; hook `Sstore` com `STORAGE` redundante em linha 36; `invoke burn(e,u,0,index)` na linha 205, rejeitado perto de `(`. |

Esses são os **erros concretamente emitidos pelo compilador nesta primeira tentativa**, não uma lista exaustiva de todas as alterações CVL1→CVL2 necessárias. Os diagnósticos foram lidos diretamente de `/tmp/cvl2_p7_snapshot_diagnostic_20261019/{37,65}/full_stdout.log`, sempre com `--compilation_steps_only`.

**Constatação substantiva:** a compatibilidade textual e de tipagem de uma **rule extraída** não significa que sua **spec integral de origem** compila em CVL2. As declarações de `methods`, ghosts, summaries, hooks e invariants globais omitidas no recorte exigem análise de pertinência e preservação de semântica por cenário e versão. Uma tradução de `methods` apenas para satisfazer o parser, sem fechar receiver e política `ALL/UNRESOLVED`, poderia alterar o significado da verificação.

## 5. Por que não é reprodução da auditoria de 2022

O relatório Certora 2022 fixa [`aave/aave-v3-core@a87d546`](https://github.com/aave/aave-v3-core/tree/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee), cujas specs `StableDebtToken.spec` e `VariableDebtToken.spec` não contêm a rule `integrityDelegationWithSig` deste dataset posterior. Os scripts arquivados incluem `solc6.12` e harnesses de `pragma 0.6.12`, enquanto os contratos auditados naquele SHA já indicam Solidity `0.8.10`. Seus blobs diferem do snapshot PropertyGPT. A execução deste estudo usou explicitamente **solc 0.8.10 do snapshot**, sem harness ou script auditado.

Logo o resultado é exclusivamente `SNAPSHOT_FRAGMENT_CVL2_COMPILE_OK`, **não** `HISTORICAL_REPLAY`, `VERIFIED`, `EQUIVALENT` nem `UNCHANGED_SEMANTICS`.

## 6. Próximo gate e decisão

- **P7/37 e P7/65:** ambos permanecem `00_unchanged (PROVISIONAL)` **somente como hipótese textual de pesquisa**; não promover para categoria final `00_unchanged`. Nenhuma nova cópia CVL2 em `results/cvl2` foi criada.
- **P7/3:** não foi incluído neste diagnóstico; permanece bloqueado por `Sstore` hook e summary externo de `handleAction`, além da ausência de `SimpleERC20` no snapshot.
- **Próximo passo legítimo:** documentar, por cada um dos dois targets de dívida, a equivalência do recorte `N.spec` versus o contexto global da spec original; mapear summaries `methods`, hooks e efeitos diretos/indiretos em Solidity, EIP-712 e riscos de poda por revert. Antes de qualquer Prover ou mudança de bucket, exigir cena/assumptions/runners explícitos e revisão semântica independente. Se tal prova continuar faltando, preservar `02_unresolved` como destino conservador em futuras cópias derivadas.
- **Sem `require` extra, sem cast restritivo, sem transformação da assinatura, sem atualização do CSV histórico e sem merge.** O experimento foi totalmente read-only para o repositório.

Documentação Certora: [CVL2 Migration Guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes Introduced in CVL2](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods Block](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Statements/Reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html).
