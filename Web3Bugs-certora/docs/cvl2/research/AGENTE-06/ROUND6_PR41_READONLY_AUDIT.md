# AGENTE-06 — Rodada 6 / auditoria cruzada SOMENTE LEITURA — PR #41

**Data 2026-10-20**. Objeto imutável: HEAD **\`a4a9a32d0c320189ffbab0faf05fd0a506e10a32\`** do [PR #41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), confirmado no GitHub, PR Draft. Baseline \`2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3\`. Nenhuma escrita, checkout, push ou commit no AGENTE-07; pesquisa feita por leitura do conector GitHub e fontes originais em SHA fixado. **Não** executados CVL2, Prover ou CVL1.

**Escopo documental efetivamente lido:** [ROUND5_TECHNICAL_EVIDENCE.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/a4a9a32d0c320189ffbab0faf05fd0a506e10a32/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND5_TECHNICAL_EVIDENCE.md), [ROUND5_MATRIX_156.csv](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/a4a9a32d0c320189ffbab0faf05fd0a506e10a32/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND5_MATRIX_156.csv), [ROUND5_P8_AXIOM_42.csv](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/a4a9a32d0c320189ffbab0faf05fd0a506e10a32/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND5_P8_AXIOM_42.csv), [ROUND5_P9_ACCOUNTS_ABI_1_7.csv](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/a4a9a32d0c320189ffbab0faf05fd0a506e10a32/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND5_P9_ACCOUNTS_ABI_1_7.csv) e [PR #47: P8 consistency](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/705641e9f8920da648c724ce4c3361f03b8ac821/Web3Bugs-certora/docs/cvl2/coordination/P8_AXIOM_CONSISTENCY_REVIEW.md).

## P8 — testemunhas distintas e limites

| Família e N.spec original | Testemunha verificável na expressão literal | Status |
| --- | --- | --- |
| W1, 22 IDs \`incomplete/8/14–35\` | Em [P8/14](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/14.spec#L49-L54), \`x=1,y=0\` impõe simultaneamente \`rayMul_g(1,0)=0\` e \`1<=rayMul_g(1,0)\`. Matriz do AG07 possui 22 entradas \`W1\`, com linhas e SHA específicos e flag \`W1_same_ghost=true\`. | Contradição textual de axiomas globais sob inteiros usuais. Isso NÃO prova que o run histórico instanciou os axiomas dessa maneira ou foi vacuous. |
| W2, \`incomplete/8/1\` | [L24–35](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/1.spec#L24-L35): \`x=y=denominator=0, rounding=1\` obriga \`0 < 0\`. | Contradição por quantificador/implicação da própria fórmula. |
| W3, mesmo \`incomplete/8/1\` | [L43–45](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/1.spec#L43-L45): \`x=y=0\` implica \`0*RAY()-0/2 < rayDiv_g(0,0)*0\`, equivalente a \`0<0\`. \`0/2\` é divisão válida. | Independente de W2; não é prova empírica do Prover. |

Outros **19 IDs** da P8 não apresentam estes três padrões específicos no levantamento, **não** são declarados satisfatíveis. W1/W2/W3 recomendam teste de satisfatibilidade/vacuity autorizado por coordenador e versionado, sem alterar axiomas originais; não reinterpretar \`VERIFIED\` como validação semântica.

## P9 — fases distintas e ABI de Accounts

Phase 1: \`9d2ec0d9399a6959565062f57efa037d03fd4fbc\`; phase 2: \`a46ce55ebd3867fa69290bf3be040846d433525d\`. A análise de AG07 tem evidência de que \`Governance.sol\` e ferramentas são versões diferentes, \`Accounts.sol\` não aparece nos caminhos da árvore phase1 examinados, e phase2 possui um \`Accounts.sol\` com **ABI Solidity de 40 funções** compilada com \`solc-js 0.5.13\` sobre 24 fontes. Isso é compilação de **Solidity base**, não de CVL2 ou do \`AccountsHarness\`. O último falhou em três imports \`mento-core\` ausentes, que não devem ser substituídos por stubs.

Detalhe individual **P9/6** em [ROUND5_P9_ACCOUNTS_ABI_1_7.csv](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/a4a9a32d0c320189ffbab0faf05fd0a506e10a32/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND5_P9_ACCOUNTS_ABI_1_7.csv): a regra chama \`authorizeSignerWithSignature\`, **não encontrada na ABI compilada phase2**. Os IDs 1–7 requerem exame independente da ABI do harness, selectors, inheritance, wrapper de execução, mapping run→fase e dependências mento-core. **50 DOCUMENTED_CANDIDATE** permanecem apenas hipóteses.

## Restantes e gate

**P20 BentoBox:** hashes do \`BentoBox.sol\` snapshot e upstream divergem; patch muda cinco arquivos e resumo de chamadas; \`MAX_INT()\` não se resolve automaticamente pelos siblings. **P11 Keep:** 6/6 SRI, 104 nós e 204 imports textuais documentados, mas SHA do run, ABI e compiler auditados continuam ausentes. Nenhum dos dois justifica \`COMPILE_OK\`.

**Escopo do diff:** o conector GitHub identificou **230 caminhos** na HEAD \`a4a9a32d\`, **zero fora de \`Web3Bugs-certora/docs/cvl2/research/AGENTE-07/\`**. A documentação de QA do agente informa validators/diff EXIT 0; nesta auditoria cruzada **não reexecutei** os comandos Git/Python devido a falha de I/O do WSL desta sessão. Este limite é distinto da confirmação anterior, realizada na Rodada 5 sobre HEAD \`96257f02\`. Não declarar que executei o diff contra \`a4a9a32d\` nesta Rodada 6.

**Conclusão:** PR #41 permanece **Draft**, integridade documental referenciada, W1/W2/W3 semântica histórica não demonstrada, ABI/fase Celo parcialmente reconstruídas, zero equivalência comprovada e nenhum merge/edição externa.

**AGENTE-06 — RODADA 6.**
