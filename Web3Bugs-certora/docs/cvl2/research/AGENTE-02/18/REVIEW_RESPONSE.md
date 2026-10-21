# Resposta documentada a revisao independente — AGENTE-02 / P18

**Decisao recebida:** devolver a pesquisa; Fase 2 expressamente nao autorizada.

## Adjudicacao individual de alteracoes CVL1-CVL2
- 181 dossies (69 complete, 112 incomplete) mantem o trecho historico e receberam Contrarrevisao de evidencias por propriedade.
- Em cada dossie sao listadas entradas methods referidas literalmente, before/after hipoteticos internal/external, observacao de declaracao Solidity quando presente, selectors e invariant, ghost, hooks e resumo de receivers. O candidato nao presume semantica equivalente.
- Os 57 DOCUMENTED e 12 INDIRECT originais foram revisitados; 7 DOCUMENTED sem chamada textual direta e todos os 12 INDIRECT com summaries apenas no contexto da spec foram rebaixados. IDs dos 7: 7,10,11,26,27,35,36.
- Buckets revisados: DOCUMENTED_CANDIDATE=50, UNRESOLVED_CANDIDATE=131. **DOCUMENTED limita-se a sintaxe observada, nao liberacao de Fase 2.** 181 propriedades continuam sem prova de equivalencia de run.
- P03 selectors: 15 IDs com assinatura tipada no codigo ativo; example 81 contem certorafallback_0().selector, que requer pesquisa de fallback e nao um sig: automatico. Detectores anteriores em comentarios ou parses abrangentes nao constituem prova.

## Proveniencia
- Em commit OpenZeppelin 109778c17c7020618ea4e035efb9f0f9b82d43ca: 12 specs do snapshot ausentes de certora/specs e 4 homonimas presentes mas diferentes em hash Git. Conferir source_comparison.csv.
- Recovery_manifest verifica 5 arquivos upstream com SHA Git real; um arquivo recuperado nao recupera o job, contexto de alvo/constructor, linkings, summaries, patch aplicado, solc ou resultado.
- PDF original de 13 paginas lido diretamente dos streams com ToUnicode, SHA256 em pdf_page_review.md. Quatro findings historicos e sete mutacoes deliberadas continuam distintos. Graficos nao foram deduzidos.

## Verificacoes e bloqueios
- Sem edicao de spec original, Solidity, report historico, configs ou CSV historicos.
- Sem Certora Prover, CVL1, CVL2, harness sintetico, ou alteracao do ambiente global.
- Faltam os dois harnesses Initializable, Supply exists_wrapper/mint wrappers, GovernorPreventLateQuorumHarness, getters/checkpoints e ABI Timelock schedule. Todos bloqueados ate prova de origem e ABI.
- Consulte QA_REPORT.md para saidas reais dos validadores e git diff --check.

**PR #37 permanece DRAFT. Sem merge.**

## Terceira revisao independente — resposta ao coordenador (2026-10-19)
- O feedback sobre o difffull foi reproduzido em HEAD 2f4d6d5: exit 2, com 144 linhas de whitespace final em 86 docs Markdown. Corrigido somente no escopo autorizado; 97.md e 99.md incluidos.
- Commit de correcao 34c4eb3dc73d12e5380034e8bdb2b9054f097ae9: **git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD = exit 0**, sem saida.
- ABI_HISTORICAL_AUDIT.md, abi_resolution_matrix.csv e 181 dossies aprofundam visibilidade, calls, summaries, receivers e proveniencia: 339 registros em 17 targets. Exemplo complete/23 documentado via ERC1155Mock.sol:10 e ERC1155.sol:110/117. Declaracao Solidity public **nao** resolve automatico internal/external do CVL2.
- TimelockController.schedule(bytes32 no spec vs bytes calldata em Solidity) permanece incompatibilidade preexistente. Todas as dependencias de harness e patch ausentes mantidas como bloqueios.
- Nenhuma equivalencia semantica ou readiness aprovada: buckets inalterados 50 apenas lexicais / 131 nao resolvidos. PR DRAFT; sem merge ou Fase 2.
