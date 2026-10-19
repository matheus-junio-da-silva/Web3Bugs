# P19 — Implementação derivada CVL2 do exemplo 1

**Classificação:** `02_unresolved`. Original: `results/spec/complete/19/1.spec`; derivada: `results/cvl2/02_unresolved/19/1.spec`.

## Evidências exatas

- Baseline: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- SHA-256 original: `279c6c956d9084cb576f9e3f99dba63936d27b6e07401f9878751ac22808016a`.
- SHA-256 da candidata: `6dff6a352b42887fbf8c8679a16cb35c20489fefd668ce960146e701fe4ff4af`, igual ao registrado pelo coordenador na [terceira revisão do PR #44](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176).
- Target preservado: `contracts/19/spec/harnesses/Dummy.sol` (SHA-256 `11f334db4012673cfb05cd9d1aca8904e9f3a822080a4d3c1c52ed474665c875`).
- Nome da regra: `mathOfChangeSupply`. Assertion intacta: `assert T2 <= MAX_SUPPLY();`.
- Alteração **única**, na linha 4:

```diff
-definition divPrecisely(uint x, uint y) returns mathint 
+definition divPrecisely(mathint x, mathint y) returns mathint 
```

O corpo matemático `= x*1000000000000000000 / y ;`, os requisitos e a assertion acima permanecem idênticos aos bytes da origem. Os demais campos não foram normalizados ou reformatados.

## Justificativa CVL2

[Certora Changes — Mathematical operations return mathint](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#mathematical-operations-return-mathint): a expressão `T-NR` tem tipo `mathint` e `RCPT` também; a assinatura original com `uint` rejeitava essas duas entradas. A alteração autorizada amplia os tipos auxiliares sem impor casts restritivos. [Migration Guide — Type errors in arithmetic and casts](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts).

Os parâmetros da própria regra `uint T, uint NR, uint RC` não mudaram. Sob as precondições, `1<=T-NR<=2^128-2`; após a primeira divisão bem definida, `RCPT>=0` e o `require RCPT<=MAX_UINT256()` limita seu teto, portanto os argumentos concretos permanecem representáveis por `uint256`. **Isto não demonstra equivalência da operação nos casos excepcionais.** Por exemplo, `T=2^128-1, NR=1, RC=1` dá `RCPT=0` sob divisão inteira usual; a segunda chamada divide por zero. O original não proíbe isso. Ver [análise de domínio](DOMAIN_ANALYSIS.md).

## Compilação: evidência e limites

A revisão independente do coordenador relata **exit 0**, `certora-cli 8.19.0`, `solc 0.8.7`, `--compilation_steps_only`, timeout 60 segundos, com esta exata SHA-256. O AGENTE-05 **não conseguiu repetir a compilação nesta retomada**, porque o Remote Desktop Commander/WSL deixou de responder e passou a offline. **Não existem novos logs, duração ou exit code locais**; ver [VALIDATION.md](VALIDATION.md). Isto não é um resultado VERIFIED nem comprova semântica CVL1/CVL2. Não foi executado Prover completo nem CVL1.
