# AGENTE-06 — RODADA 10 / contrarrevisão somente leitura do PR #41

Objeto: PR #41 (AGENTE-07), HEAD 3fcbf9d64af93ef9453abbbb7bee09a8c0dba0f5, Draft, não merged. Lidos revisão mais recente do coordenador de 20/10/2026 e ROUND9_EVIDENCE.md, ROUND9_MATRIX_156.csv, ROUND9_P8_WITNESS_MAP_42.csv e ROUND9_QA.md, na ref imutável. API GitHub listou 244 caminhos alterados, zero fora de Web3Bugs-certora/docs/cvl2/research/AGENTE-07/. Não foram realizados checkout, comentário, commit, push ou edição na branch do AGENTE-07. Nenhuma execução CVL1, CVL2 ou Prover.

## P8 — testemunhas W1/W2/W3 e escopo

[ROUND9_P8_WITNESS_MAP_42.csv](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/3fcbf9d64af93ef9453abbbb7bee09a8c0dba0f5/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND9_P8_WITNESS_MAP_42.csv), Git blob a21c9d13b399c80fd3866bc62e0b19410b8ceb44, classifica 42 exemplos: **22 W1**, **1 W2/W3**, **19 sem essas três testemunhas específicas**. A classificação R9 identifica 12 fragmentos W1 contendo apenas estrutura invariant e 10 fragmentos contendo rules+invariants; contagem textual não significa ativação pelo solver.

- **W1 / incomplete/8/14–35:** [incomplete/8/14.spec:49–54](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/14.spec#L49-L54) apresenta no mesmo ghost rayMul_g as restrições de zero quando x=1,y=0 e o limite x menor ou igual a rayMul_g(x,y). Aplicando x=1,y=0, obtêm-se rayMul_g(1,0)=0 e rayMul_g(1,0)>=1, contraditórios sob a aritmética usual se ambos forem axiomas assumidos.
- **W2 / incomplete/8/1:** [L34–35](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/1.spec#L34-L35) com rounding=1, x=y=denominator=0 exige 0<0.
- **W3 / mesmo N.spec:** [L43–45](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/1.spec#L43-L45) com x=y=0 também exige 0<0, e o termo y/2 é 0/2 válido.

**Não demonstrado:** versão/flags do Prover, ativação dessas ghosts e axiomas nos jobs, summaries de methods, hooks, invariant base/preservation, dispatch method f, alcance de storage/revert. A contradição aritmética do texto não comprova que o VERIFIED histórico fosse vacuamente verdadeiro. O init_state axiom de outra ghost em P8/14 não é o axiom global W1. Ausência desses três padrões nos 19 restantes não implica que seus axiomas sejam consistentes. [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html) e [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html) modernos são referências, não logs antigos.

**Gate proposto, não executado:** reconstruir cena, runner, resumo ghost e seleção de rule/invariant antes de estudo de consistência derivado autorizado pelo coordenador. Não alterar axiomas, require, domínio, nem rodar Prover autonomamente.

## Outros projetos de AGENTE-07, somente leitura

**P9 Celo:** método authorizeSignerWithSignature existe em Accounts.sol snapshot:407, blob ac93720967e0ca762e9f9ff66da34ff558b5e4f9, mas faltava na ABI Accounts phase2 previamente compilada isoladamente. Fonte phase2 e snapshot são diferentes. O gitlink mento-core do monorepo posterior 10c3f192 não prova o run auditado; IStableToken também difere entre revisões.

**P11 Keep:** runner público recuperado em keep-ecdsa@a5cd171.../solidity/scripts/runCertora.sh, blob 948bca9945db5bdf953c7d5e9830348480f9b030, define FullyBackedBondingHarness, solc5.17, structLink e link. Quatro blobs spec/harness idênticos ao snapshot são evidência, mas o SHA do relatório 658b02f... e a cena do Prover continuam sem vínculo temporal comprovado; sem teste CVL2.

**P20 BentoBox:** patch histórico altera cinco Solidity incluindo calls e try/catch. compoundStrategyAdditional.spec:65 chama MAX_INT() não definido no próprio arquivo; definições de specs irmãs não são globais sem import/concatenação do runner. Nenhuma hipótese de equivalência está aprovada.

**Parecer:** contradições condicionais P8 e proveniências P9/P11/P20 estão documentadas com limites apropriados. Não há prova de vacuidade histórica ou equivalência CVL1→CVL2, nenhum projeto integralmente migrado. PR #41 continua Draft e sua branch foi preservada intacta.

**AGENTE-06 — RODADA 10 / CONTRARREVISÃO.**
