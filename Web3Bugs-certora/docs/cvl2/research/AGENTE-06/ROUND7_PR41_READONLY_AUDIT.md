# AGENTE-06 — Rodada 7 / auditoria independente SOMENTE LEITURA do PR #41

**HEAD observada e fixada:** \`0224fa9ab258f0faca0aef54b5fb31c77157320b\` no [PR #41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), Draft, em 20/10/2026. Baseline do catálogo: \`2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3\`. **Nenhum checkout, patch, commit, comentário, push ou modificação da branch AGENTE-07.** GitHub leitura por ref imutável.

## Escopo mecânico realmente conferido

- Conector de PR listou **235 caminhos alterados**, **zero** fora de \`Web3Bugs-certora/docs/cvl2/research/AGENTE-07/\`; a comparação API \`BASE...HEAD\` listou os mesmos 235. **Isso é comparação de nomes, NÃO execução local de \`git diff --check\`**, nem reanálise dos conteúdos integrais desses 235 arquivos.
- Consultados e lidos [\`ROUND7_EVIDENCE.md\`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/0224fa9ab258f0faca0aef54b5fb31c77157320b/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND7_EVIDENCE.md), [\`ROUND7_MATRIX_156.csv\`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/0224fa9ab258f0faca0aef54b5fb31c77157320b/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND7_MATRIX_156.csv), e a R6 [\`ROUND6_MATRIX_156.csv\`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/104f6deef80ac95ab5fec75c3e5ebb01f075f6fe/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND6_MATRIX_156.csv). 156 linhas R6 e 156 linhas R7 declaradas (P8 42, P9 61, P11 16, P20 37); os relatórios de AG07 mantêm **156 NOT_RUN CVL2** e **zero equivalência**. **Nenhum SHA-256 de N.spec recalculado nesta auditoria**; os hashes são evidência anterior preservada.

## P8 — W1, W2 e W3: contradições das fórmulas, não prova de vacuidade histórica

Reabri diretamente os N.spec imutáveis [P8/incomplete/14, L49–54](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/14.spec#L49-L54) e [P8/incomplete/1, L24–45](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/1.spec#L24-L45):

| Grupo documental de AG07 | Testemunha e mecanismo |
| --- | --- |
| **W1**: 22 extrações IDs 14–35 | No mesmo \`ghost rayMul_g\`, \`forall x,y\` supõe \`(x==0 || y==0) => rayMul_g(x,y)==0\` e \`x <= rayMul_g(x,y)\`. \`x=1,y=0\` implica \`rayMul_g(1,0)=0\` e \`rayMul_g(1,0)>=1\`, incompatíveis em inteiros. AG07 mapeou 22 IDs; eu confirmei diretamente a fórmula representativa ID14, **não reabri nesta rodada os outros 21 bytes**. |
| **W2**: P8/incomplete/1 | Axioma global de \`mulDiv_g\` para \`rounding==1\`, L34–35: \`x=0,y=0,denominator=0\` força \`0 < mulDiv_g(...)*0\`, isto é, \`0<0\`. |
| **W3**: mesma ID1, independente de W2 | Axioma \`rayDiv_g\` L43–45 com \`x=y=0\` força \`0*RAY()-0/2 < rayDiv_g(0,0)*0\`, isto é, \`0<0\`; denominador do termo \`0/2\` é válido. |

**Condição lógica:** se axiomas globais inteiros são assumidos como premissas, esse conjunto é inconsistente. **Condição operacional ainda NÃO provada:** que as cláusulas foram todas ativadas naquele run/propriedade, de acordo com a semântica/versão antiga de ghost, summaries, dispatch, invariants, hooks e scope. O Prover histórico poderia ter configurado seleção/instanciação diferente, desconhecida. Logo, não classificar automaticamente \`VERIFIED\` como vacuous; não extrapolar W1/W2/W3 aos **outros 19 P8**. AG07 corretamente pede um teste derivado e autorizado de satisfatibilidade **somente após** reconstituir runner, sem alterar axiomas históricos; **nenhum teste foi executado**.

## P9 — conferência independente dos blobs Mento candidatos da R7

O PR #41 recuperou candidato [celo-org/mento-core@4ceb4f0ed3e24163617e9da2b5bfc4c5a2b722b8](https://github.com/celo-org/mento-core/tree/4ceb4f0ed3e24163617e9da2b5bfc4c5a2b722b8). Verifiquei por \`GitHub fetch_file\` na SHA fixada, com os seguintes **Git blobs SHA-1 exatos**:

| Arquivo no commit candidato | Blob SHA-1 confirmado | Conteúdo delimitado |
| --- | --- | --- |
| \`contracts/interfaces/IExchange.sol\` | \`968158a26512cb4bcf479af85cb11d9c4f301b88\` | \`pragma solidity ^0.5.13\` |
| \`contracts/interfaces/IReserve.sol\` | \`2fc72df0a4937bfabd2fc76de624a2d8763f4c4b\` | \`pragma solidity ^0.5.13\` |
| \`contracts/interfaces/IStableToken.sol\` | \`b62d7fe7169cb591f704242ee9bfa904ef90d58d\` | \`pragma solidity ^0.5.13\` |
| \`contracts/common/UsingRegistry.sol\` | \`e3bca1e6bb2ffe86dd656fb7b79de429d69ab690\` | Importa \`../interfaces/...\`, não o caminho do snapshot Celo |

**Boa evidência de fonte histórica concreta; ainda NÃO é uma dependência provada do audit run.** O snapshot Celo espera \`lib/mento-core\`; falta o **gitlink** de seu superproject na revisão verificada, import closure e target. A phase2 \`celo-monorepo@a46ce55e...\` usa outro \`UsingRegistry\` e ABI Solidity Accounts de 40 funções da R5; \`P9/6\` chama \`authorizeSignerWithSignature\`, ausente da ABI phase2 compilada. Não copiar interfaces ou introduzir mock para completar ABI antes do gitlink de auditoria.

## P20 e P11: escopo corroborado, testes não reproduzidos

**P20:** o relatório AG07 identifica os cinco patches históricos e riscos de \`try/catch\` removido de \`CompoundStrategy\`, redirecionamento de chamada e expansão de interface. Isso afeta potencialmente o universo de reversões e não autoriza transformar summaries; \`MAX_INT()\` isolado segue sem import/definição provados. A classificação de alcance por grupos de target é **documental**; nenhuma ABI pós-patch R7 executada. **P11:** closure textual de 104 nós/204 imports e seis pacotes com SRI verificados antes; SHA de audit \`658b02f...\` não reconciliada ao \`a5cd171...\` e nenhum runner/formal replay autenticado. Ambos ainda \`NOT_RUN\` CVL2.

## Parecer e intervenção humana

**PASS restrito à consistência documental das fontes examinadas e escopo de caminhos do PR #41 na HEAD citada.** \`COMPILE_OK=0\` e \`SEMANTIC_PROVEN=0\` no AG07. **NÃO** executei Python, Git CLI \`diff --check\`, solc, CVL2 ou Prover nesta revisão, nem reexecutei todos os hashes da matriz. Auditoria cruzada não valida execução histórica.

**P8 alerta VERMELHO** para modelo de axiomas; **P9/P20/P11 LARANJA** para cena sem target/ABI/run demonstrados. Próximo gate: coordenador identificar versão de Prover e ativação das ghosts, gitlink exato Mento, runner/harness Celo, build patch BentoBox e audit SHA Keep; aprovação específica antes de testes derivados. PR #41 permanece Draft sem merge.

**AGENTE-06 — RODADA 7.**
