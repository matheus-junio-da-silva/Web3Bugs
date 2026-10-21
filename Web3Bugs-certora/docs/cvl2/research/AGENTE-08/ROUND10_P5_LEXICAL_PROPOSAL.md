# P5/incomplete/14 — proposta lexical exclusivamente documental, Rodada 10

Esta é uma **hipótese não aprovada** para análise por propriedade, **não uma especificação CVL2 aprovada** e **não um arquivo executável versionado**. Nada de `results/spec/`, `contracts/`, `results/cvl2/` ou do N.spec original foi alterado.

**Origem:** `results/spec/incomplete/5/14.spec`, SHA256 `0c0e05b80677a46deccfe1494e205cf09b966efab14785e6206c37a0a92e2031`; fonte upstream `aave-starknet-project/aave-starknet-bridge@4c010c18b08703e4f367db1e0c642c76c25e551b`. Log original de R9 [stdout Base64](ROUND9_P5_N14_stdout.log.b64) SHA256 da decodificação `cbf24143137931fcd317c00fd3c175e440fcbf5a16b9efc945ce21f49e4269f8`, CVL2 parser exit 1 por entradas `methods` sem `function` e `;`.

**Proveniência R10 da candidata em scratch:** `/home/mat/cvl2-agente08-round10-20261020/scratch/P5_14_lexical/spec/14_derived_lexical.spec` (fora do Git). A variante foi escrita e seu SHA256 calculado **antes** do EROFS: `f246fe4490c92102fdc1fd91634bf4f7506f3a6c42e9124ae7d37aa61530c804`. A comparação linha a linha revelou **quatro linhas** alteradas, sem inserções ou exclusões de linhas, preservando o resto da property byte a byte:

```diff
-    withdraw(address, uint256, address, uint256, uint256, bool)
-    receiveRewards(uint256, address, uint256)
+    function withdraw(address, uint256, address, uint256, uint256, bool) external;
+    function receiveRewards(uint256, address, uint256) external;
@@
-    f.selector != receiveRewards(uint256, address, uint256).selector
+    f.selector != sig:receiveRewards(uint256, address, uint256).selector
@@
-    f.selector != withdraw(address, uint256, address, uint256, uint256, bool).selector;
+    f.selector != sig:withdraw(address, uint256, address, uint256, uint256, bool).selector;
```

**Base normativa:** [CVL2 Changes — function, terminador, visibilidade e sig](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [CVL2 Migration — revisar métodos/receivers](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Methods Block](https://docs.certora.com/en/latest/docs/cvl/methods.html). `external` foi escolhido provisoriamente por serem métodos externos herdados de `Bridge.sol:153,232`, mas **a resolução receiver→ABI executada pelo Prover não foi autenticada**. A variante não altera `invariant alwaysUnSent`, `messageSentFilter`, `filtered`, ghost/hook, calls, assert/require ou state constraints. Uma mudança lexical pode mesmo assim mudar semântica se o target/métodos não forem os mesmos.

**Estado de execução:** `NOT_RUN` do derivado em CVL2. Ao tentar configurar os logs de execução, o shell retornou `Read-only file system`; o redirecionamento `stdout/stderr` falhou antes de iniciar `certoraRun`. O código `1` que apareceu é do **shell** no pré-flight, **não `COMPILE_ERROR` do parser/typechecker**. Nenhum log CLI derivado existe. Não reexecutar antes de intervenção humana e autorização específica.

**Gate:** verificar 11 seeds, 10 links, compilador exato solc0.8.10, SHA de originais/variante, `HOME` isolado e logs graváveis; somente então novo `--compilation_steps_only` com timeout, cenário N.spec fragmentado distinto da full `bridge.spec` que importa `setup.spec` e `erc20.spec`. Mesmo eventual `COMPILE_OK` derivado não comprovaria universo global de contraexemplos ou equivalência CVL1→CVL2.
