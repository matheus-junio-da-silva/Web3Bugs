# AGENTE-05 — ROUND7_EVIDENCE: CVL2 histórico, P7 `sig:` e gates

**Data:** 20/10/2026. **PR:** [#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), Draft, sem merge. **HEAD inicial conferida:** `31ce9c427e5aed759c1b04932ed9ebdd76cbe959`. **Baseline imutável:** `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Escopo exclusivo: P7=74, P19=37, P6=32, P3=3, P21=2 (**148**). Pesquisa documental somente leitura, **nenhum trabalho executado no WSL comprometido**. Leia também [ROUND7_MATRIX_148.csv](ROUND7_MATRIX_148.csv) e [ROUND7_QA.md](ROUND7_QA.md).

## Restrições de interpretação confirmadas em documentação primária

[CVL2 Changes, § method literals](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html) exige `sig:` nos literais de método, sem provar equivalência da cena. [CVL2 migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html) exige revisão manual de methods e tipos. [Methods e summaries](https://docs.certora.com/en/latest/docs/cvl/methods.html) podem alterar a resolução de chamadas externas; receivers/dispatch devem ser autenticados. [Statements, § revert](https://docs.certora.com/en/latest/docs/cvl/statements.html) define que uma chamada **sem** `@withrevert` descarta caminhos revertidos, enquanto `@withrevert` os mantém para checar `lastReverted`. [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html) e [invariants](https://docs.certora.com/en/latest/docs/cvl/invariants.html) podem alterar estado de verificação/hipóteses; não presumir que um fragmento extraído incorpora a spec global. Esses guias **não documentam automaticamente a semântica da verificação CVL1/Specify histórica**.

## P7 — auditoria documental de P7/complete/47 e /73

Os arquivos [P7/47](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/7/47.spec) e [P7/73](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/7/73.spec) contêm **a mesma definição textual** de `disAllowedFunctions(method f)` e os mesmos operadores `f@withrevert(e,args)` / `assert lastReverted;`, mas targets e cenas diferentes. Em ambos, o filtro não inclui `!f.isView`, portanto o método `allowance` **view** permanece no conjunto, conforme ABI.

**Diff candidato exclusivamente documental — 6 alterações na definição de P7/47, nenhuma na rule:**

```diff
- f.selector == transfer(address, uint256).selector ||
+ f.selector == sig:transfer(address, uint256).selector ||
- f.selector == allowance(address, address).selector ||
+ f.selector == sig:allowance(address, address).selector ||
- f.selector == approve(address, uint256).selector ||
+ f.selector == sig:approve(address, uint256).selector ||
- f.selector == transferFrom(address, address, uint256).selector ||
+ f.selector == sig:transferFrom(address, address, uint256).selector ||
- f.selector == increaseAllowance(address, uint256).selector ||
+ f.selector == sig:increaseAllowance(address, uint256).selector ||
- f.selector == decreaseAllowance(address, uint256).selector;
+ f.selector == sig:decreaseAllowance(address, uint256).selector;
```

**Não há patch aplicado**, cópia derivada persistente ou nova execução. A lista é um plano estritamente de syntax/selector; preserva integralmente `rule disallowedFunctionalities`, `filtered`, `f@withrevert`, `assert lastReverted`, seus argumentos, ghosts, hooks, require e summaries.

### ABI independente dos dois snapshots — consulta a artefatos R5 + Solidity do baseline em R7

| Seletor / visibilidade ABI | StableDebtToken | VariableDebtToken | Risco de escopo |
| --- | --- | --- | --- |
| `transfer(address,uint256)` — nonpayable | Presente | Presente | Ambos revertem no caminho Solidity visível |
| `allowance(address,address)` — **view** | Presente | Presente | Continua **selecionado** por P7/47,73 |
| `approve(address,uint256)` — nonpayable | Presente | Presente | Não confundir com `approveDelegation` |
| `transferFrom(address,address,uint256)` — nonpayable | Presente | Presente | Identidade de selector distinta |
| `increaseAllowance(address,uint256)` — nonpayable | Presente | Presente | Sem assumir implementação ERC20 |
| `decreaseAllowance(address,uint256)` — nonpayable | Presente | Presente | Sem assumir implementação ERC20 |

As **seis funções** têm `revert(Errors.OPERATION_NOT_SUPPORTED)` no snapshot, em [StableDebtToken.sol:365–386](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/contracts/protocol/tokenization/StableDebtToken.sol#L365-L386) e [VariableDebtToken.sol:127–148](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/contracts/protocol/tokenization/VariableDebtToken.sol#L127-L148). Leitura independente dos arquivos [ABI Stable](7/round5_logs/abi/StableDebtToken.abi) e [ABI Variable](7/round5_logs/abi/VariableDebtToken.abi) confirma respectivamente **33** e **30** funções ABI. Os seis selectors do filtro estão presentes em **ambos**. Isso torna o filtro **não vazio no conjunto estático das assinaturas ABI**, mas **não prova** que o Prover gerou instanciações, executou caminhos satisfatíveis nem tratou a mesma cena/harness da auditoria histórica. Verificação formal de não-vacuidade **não foi executada**.

| Exemplo | CVL global e recorte | Diagnóstico anterior | Semântica ainda não fechada |
| --- | --- | --- | --- |
| P7/47 `disallowedFunctionalities` | [StableDebtToken.spec:14–20 e 338–344](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/StableDebtToken.spec#L338-L344) | N.spec original **EXIT 1 R5**: faltam `sig:`; variante R6 **NOT_RUN** por EIO | `method f`/dispatch real, receivers e cenário global não reproduzidos; `@withrevert` preservado |
| P7/73 `disallowedFunctionalities` | [VariableDebtToken.spec:23–29,252–258](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/VariableDebtToken.spec#L252-L258) | N.spec original **EXIT 1 R5**, **nenhuma variante** | Target Variable separado; não transferir o eventual exit do 47 para 73 |

O **P7/47** é o candidato único permitido para futuro diagnóstico em scratch, mas somente após WSL íntegro e gate individual do coordenador, com SHA/cmp original e variante, cópias byte-idênticas do Solidity, CLI 8.19.0, solc 0.8.10, timeout ~60–65 s, stdout/stderr, exit e manifesto; sem tokens, sem Prover e sem output `results/cvl2`. Não implementar caso falte qualquer precondição. **Nada disso foi executado em R7.**

## P7/41,63,36 — `f(e,args)` sem `@withrevert` e dependências globais

A leitura direta dos arquivos N.spec preservados e do Solidity mostra:

| Exemplo | Source/linhas | `method f` ABI não-view após exclusão dos cinco disallowed nonpayable | Gate semântico |
| --- | --- | --- | --- |
| **41** `nonceChangePermits` | `StableDebtToken.spec:226–236` e definição `:14–20`; [DebtTokenBase.sol:43–68](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/contracts/protocol/tokenization/base/DebtTokenBase.sol#L43-L68) | `approveDelegation(address,uint256)`, `burn(address,uint256)`, `delegationWithSig(address,address,uint256,uint256,uint8,bytes32,bytes32)`, `initialize`, `mint`, `setIncentivesController` | `delegationWithSig` requer prazo válido, EIP-712 e `ecrecover` válido para avançar nonce. `f(e,args)` descarta paths com revert; se `oldNonce==newNonce`, implicação é verdadeira sem testar a situação interessante. |
| **63** `nonceChangePermits` | `VariableDebtToken.spec:89–99` e `:23–29`, base herdada DebtTokenBase | As mesmas seis **famílias**, mas `burn(address,uint256,uint256)` e `mint` Variable diferem do Stable | Não equiparar mudanças de índices e efeitos de mint/burn; hook `_userState.balance` e ghost `sumAllBalance` da spec Variable têm closure global independente. |
| **36** `integrityTimeStamp` | `StableDebtToken.spec:166–174`; getter [StableDebtToken.sol:90–93](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/contracts/protocol/tokenization/StableDebtToken.sol#L90-L93) | Seis famílias Stable não-view, idem 41 | A precondição existente `getUserLastUpdated(e,user)<=e.block.timestamp` e a assert pós `f(e,args)` **não** provam alcance de mint/burn/initialize. Não acrescentar premissas nem forçar sucesso. |

Os globals excluídos dos recortes incluem, na Stable, [`methods`:1–10, ghosts/summaries:22–108, `sumAllBalance`/hooks:114–123](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/StableDebtToken.spec); Variable contém `methods`, `gRNVB` e axiom, `sumAllBalance`/hooks e invariant. O caminho de `f=mint/burn` potencialmente encontra essa instrumentação, diferentemente do caminho direto P7/37,65. **Não transformar summaries de receivers desconhecidos em NONDET genérico sem autorização, não importar axiomas seletivamente.**

A execução anterior isolada de P7/37,65 foi `COMPILE_OK`, mas a **spec global CVL1 falhou no typechecker CVL2**. Também houve aviso secundário `Stack too deep` no autofinder Stable e fallback no diagnóstico anterior: distinguir esse evento auxiliar do erro CVL2 de sintaxe. Sem replay do run janeiro/2022, sem EIP-712 satisfatível demonstrado.

## P3, P6, P19 e P21 — fontes encerradas ao limite disponível; tickets individuais

| Project IDs | Proveniência verificável existente | Bloqueio negativo/necessidade humana |
| --- | --- | --- |
| **P3/incomplete/1–3** | Fork `bgd-labs/rescue-mission-phase-1@33c1aeca28d6d61659c1b28775ad2644b7e2ac6e` aponta gitlink `lib/solidity-utils@49f2bd22950cf8dfe32d3f01e30a221b1f2f95dd`, tree `36cb441858e6d959387713deb832e47e4377efe5`; `LendToAaveMigrator.sol:4` importa IERC20 desse pacote. | Submódulo/pin **resolvido em R5**, mas ainda faltam scene+links LEND/AAVE, harness, `solc_map`, replays por rule. Para stkAAVE não aplicar indiscriminadamente o runner LEND. Sem novos arquivos da auditoria autenticados em R7. |
| **P6/incomplete/1–32** | Transcript [reports/6.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/reports/6.md): PDF arquivado marca `ac92951`; relatório público alternativo marca `51d46b1`; snapshot identificado com commit diferente `13a004738c533f11710400c1757b9570ef1e0466`. | Buscas anteriores de ambos SHAs em aave/aave-v3-periphery, bgd-labs/aave-v3-periphery e aave/aave-v3-core foram negativas; **não repetir nem afirmar inexistência**. Falta SHA completo/repositorio/runner que corresponda ao snapshot e PDF. |
| **P19/incomplete/3–37** | `contracts/19/contracts/yarn.lock:522–530` fixa OZ contracts 2.5.0 e upgrades 2.8.0; tarballs recuperados em R5 com SHA-512 exato e 38+8 imports diretos presentes. `applyHarnesses.sh:1–5` muda fonte, incluindo `require(nonRebasingCreditsPerToken[...] <= 1e18)`. | Não aplicar script ao original. Falta árvore efetiva pós-script, dependências transitivas, receiver/ABI e run por ID. **35 incomplete** e nenhuma compilação nova. P19/complete/1,2 do PR #46 continuam `02_unresolved`: `RCPT=0` permite segunda divisão por zero, equivalência CVL1 não demonstrada. |
| **P21/incomplete/1–2** | `contracts/21/specs/DSM.spec:3–38` usa `DepositSecurityModuleHarness/getGuardianLength`; [DepositSecurityModule.sol:214–235](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/21/0.8.9/DepositSecurityModule.sol#L214-L235) expõe `getGuardianQuorum` e `getGuardians`. | Não há harness/getter original autenticado. A linha 223 permite expressamente quorum maior que tamanho dos guardians, tensionando `quorumLeGuardian` se `Length` for contagem real. **Não** declarar VIOLATED formal nem inventar getter. |

## Auditoria cruzada PR #38 — SOMENTE LEITURA

HEAD examinada: `abdd7d4a9eefc4156d1c4c7d3efc717b8296754d`, PR Draft. Inspeção da [`ROUND6_TECHNICAL_EVIDENCE.md`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/abdd7d4a9eefc4156d1c4c7d3efc717b8296754d/Web3Bugs-certora/docs/cvl2/research/AGENTE-06/ROUND6_TECHNICAL_EVIDENCE.md) e das fontes originais:

- **P1 `queue2`:** contrato [L2BridgeExecutor.sol junho/2022](https://github.com/aave/governance-crosschain-bridges/blob/303bd3e16c8d3465325389a72564126c3bacc4f9/contracts/bridges/L2BridgeExecutor.sol) e setembro/2022 compartilha mesmo Git blob, mas `queue2` só é documentado no [harness público de setembro L45–61](https://github.com/aave/governance-crosschain-bridges/blob/93c39de7065a7dc3bb08cddf7dadb466f9a393b8/certora/harness/L2BridgeExecutorHarness.sol#L45-L61), com **cinco arrays fixos [2]**, ao contrário de `queue` com arrays dinâmicos. Isso não autentica o **job Certora de junho** nem dá permissão de substituir ABI. `OptimismHarness.sol:21` declara `_mock`; runner de setembro faz `--link OptimismHarness:_mock=mockTarget`. Não transferir linkings por rede. Contrateste de proveniência temporal aceita match de Solidity, **não** migração.
- **P17 Specify/2019:** [complete/8:19–28,64–65,114–117](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/17/8.spec) usa havoc env+local, `static_require result==invoke borrowFreshPub(...)`, `lastReverted` e asserts bidirecionais. [complete/9:19–32,67–68](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/17/9.spec) faz repay com payer/borrower/other distintos. [complete/39:21–32,69–80](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/17/39.spec) inclui `havoc doApprove` e `sinvoke approve` condicional, que **pode alterar storage**, antes de `invoke transferFrom` e `lastReverted`. Substituir tokens CVL1 sem motor Specify 2019 e `.spclnk` não demonstra semântica de snapshots/reverts.
- **Parecer limitado:** estes casos devem continuar **UNRESOLVED**; a existência de `queue2` no snapshot posterior não sana diferença temporal; nenhum compile-only CVL2 do PR38 foi atribuído. Nenhuma alteração na branch do AGENTE-06; esta revisão é **amostral por prioridade**, não afirma 159 provas reexecutadas.

## Gates concretos e alerta

1. **Operacional primeiro:** administrador recupera filesystem WSL `DESKTOP-5E26TVU`; coordenação valida scratch RW, Python/git, worktree, SHA, os três validadores e `git diff --check BASE...HEAD`. **Não executar comandos de recuperação automaticamente.**
2. **P7/47:** decisão humana específica sobre cena/ABI/selector/`method f` e autorização de **um** `--compilation_steps_only` em scratch com diff de seis `sig:`. Sem exit 0 real, não usar `COMPILE_OK`. P7/73 e 41/63/36 requerem gates separados.
3. **Outras famílias:** autenticar runner+links P3; SHA/PDF P6; harness pós-script P19; getter/harness e semântica P21; PR38 runner junho e Specify 2019.

**Alerta:** 🟠 investigação semântica/histórica não concluída; 🔴 capacidade operacional WSL/QA local bloqueada. Sem Prover, CVL1, merge, alterações em originais ou `MIGRATED_COMPLETE`. **AGENTE-05 — RODADA 7.**
