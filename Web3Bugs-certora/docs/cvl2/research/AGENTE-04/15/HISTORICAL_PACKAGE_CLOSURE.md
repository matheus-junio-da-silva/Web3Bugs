# P15 — Pacotes, harnesses e exclusoes da pesquisa (revisao 2)

**B1 fonte primaria:** https://github.com/aave/gho-core/blob/ce49fb0c94cfebf0159222ceb288e4f9a55d305f/package-lock.json commit `ce49fb0c94cfebf0159222ceb288e4f9a55d305f`. Foram baixados apenas tarballs publicos indicados pelos objetos resolved do lock, sem instalacao. **C1 checksum reproduzivel:** os tres SHA512 calculados correspondem aos campos integrity do lockfile (nenhum ambiente Certora executado).

| Package | Version | SHA256 tarball | SHA512 = SRI committed |
|---|---|---|---|
| `@aave/core-v3` | 1.17.2 | `1a1307d7cfae3027fd475fa76dd251206c1c65fd2466b60036da6cadc8ef54e9` | sim |
| `@aave/periphery-v3` | 2.0.1 | `b48e664f06dbbc34e3e3af2dc13fd6dc4fd34fa116e5bfc98362d62f6c741320` | sim |
| `@openzeppelin/contracts` | 4.8.1 | `d45d540b9b1c60707b01c8981ccfb1ce9b7e156492c9ab85a46fa520960da065` | sim |

Os 3 arquivos foram validados na distribuicao historica, mas 895 entradas do lock e os node_modules instalados pelo auditor NAO foram reproduzidos. Identidade SRI de tarball nao equivale a SHA de commit Git nem a ambiente efetivo de compilacao.

**Harness e patch B1:** https://github.com/aave/gho-core/blob/ce49fb0c94cfebf0159222ceb288e4f9a55d305f/certora/Makefile descreve munged como copia de src seguida de patch. https://github.com/aave/gho-core/blob/ce49fb0c94cfebf0159222ceb288e4f9a55d305f/certora/applyHarness.patch tem SHA256 `5bd7efa57de87e8c325d24b44a7ac37d89d2906f9d333fbc14efaafb807de325` e altera contratos GhoToken.sol, IGhoToken.sol: getFacilitatorBucket e getFacilitatorsList external viram public; ha novas condicoes require nas diferencas. O Solidity analisado no Prover pode ter semantica distinta do source original. O arquivo munged gerado e os logs historicos NAO estao preservados.

**Scripts B1 (apenas leitura):** verifyGhoVariableDebtToken.sh usa GhoVariableDebtTokenHarness, DummyPool e tokens ERC20 simulados, links para desconto/POOL e solc8.10 com loop_iter 2. verifyGhoToken.sh usa GhoTokenHarness, patch e loop_iter 3. verifyFlashMinter.sh traz links GhoToken/AToken/borrower e limite de recursao. verifyGhoAToken.sh traz links AToken/debt token. verifyGhoDiscountRateStrategy.sh usa GhoDiscountRateStrategyHarness e loop_iter 2. O VariableDebtToken.spec e o set.spec participam como imports, nao ha prova de target autônomo.

**Buscas negativas limitadas:** nao foi localizado .conf sob certora na tree auditada. A tree nao identifica binario do Certora Prover, versao real CLI, node_modules efetivo nem logs remotos; nao gerar reconstrucao otimista. Conclusao P15: all 116 cases continuam UNRESOLVED_HISTORICAL_RUNTIME/ABI; CSV fixado permanece 63 VERIFIED, nao 64.

**A1/A2:** https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html; sintaxe de methods e sig: pode estar documentada, mas receiver/visibility e resumo de chamadas exigem prova do target.
