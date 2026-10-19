# Project 4 — auditoria original e fontes recuperáveis

**AGENTE-06 / FASE 1 — não alterar originais.**

- PDF oficial em resources/4/Aave-Staked-Token-v1.5.pdf, página 1: último commit revisado pelo Prover `4cf8837`. Render da página 1 conferido; SHA-256 do PDF no ZIP fornecido: `2c1bf00f39ac48973e4cfea4b190adfd5dc103cc7247f4a49247770dde326f67`.
- Upstream [Certora/aave-stk-v1-5](https://github.com/Certora/aave-stk-v1-5/commit/4cf8837121a4351cc0e21703bb1df76036205114), SHA completo `4cf8837121a4351cc0e21703bb1df76036205114`, árvore auditada `61a8c68add4e31190507f0ff751b0cc8f53e91b6`.
- Na página 3, o PDF explicita tokens stake/reward iguais, reward vault distinto, loops limitados a 3 iterações e permit resumido por nondeterminismo válido.
- A árvore no commit auditado contém `src/contracts`, `src/interfaces`, `src/lib`, `src/utils`, porém **não contém diretório `certora/` com harness gerado**. O `src/` de base é recuperável com proveniência; `certora/munged` e execução original ainda NÃO reconstruídos.

## SHA dos blobs, comparação com contracts/4 do snapshot

| Path upstream auditado | Git blob upstream | Git blob arquivado | Observação |
|---|---|---|---|
| `src/contracts/StakedAaveV3.sol` | `a7d65c9137fe890db274c7072181d45548e87353` | `eaaa398430d3e1ab9f5398718c7e2fb1d566071b` | DIFFERENT_SOURCE |
| `src/contracts/StakedTokenV3.sol` | `d066ac0745d2e7ae06c03c71829302fa3eb7251b` | `43e6a6ffb54e51441369c4f1f47791c8646c24e5` | DIFFERENT_SOURCE |
| `src/contracts/StakedTokenV2.sol` | `e7ccc525b3292e5f4d4cbdbd9a5c2c78328e2121` | `422e660f902e7e3f6f844a7d4bc1be65470e0f23` | DIFFERENT_SOURCE |
| `src/contracts/AaveDistributionManager.sol` | `7b98c0f248ef0f7ab57f5be89848e1950f899ecf` | `7b98c0f248ef0f7ab57f5be89848e1950f899ecf` | EXACT_MATCH |
| `src/interfaces/IERC20.sol` | `27885bf1e33776eae95a17f4703ff569d0ec8088` | `Não comparado no arquivo raiz` | UPSTREAM_SOURCE_PRESENT |
| `src/interfaces/IStakedAaveV3.sol` | `5a1550bf46a7336bd25c746bb5adbe605611d21a` | `Não comparado no arquivo raiz` | UPSTREAM_SOURCE_PRESENT |

Em especial StakedAaveV3.sol tem diferenças além de whitespace/import: versão auditada possui 245 linhas e o snapshot 261, com divergência inicial em import de hook GHO. Não presumir equivalência semântica nem substituir snapshot.

**Original_status das 27 propriedades continua incomplete.** A recuperação de `src` não comprova geração de `munged` idêntica nem seleção do mesmo harness e flags. Nenhum Prover, CVL1, CVL2 ou solc foi executado.
