# AGENTE-06 P17 — QA de inventário, ainda NÃO de equivalência semântica

- Baseline Web3Bugs 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 confirmado; PropertyGPT 687f654c679ed45ab127b7949e2a29c8f5e491b9 confirmado.
- Árvores Git conferidas: 31 complete e 10 incomplete N.spec; 41 chaves canônicas = 41 dossiês e 41 linhas properties.csv.
- Relações Bug Label 41, excedentes de multi-label 0, sem duplicar exemplos.
- Caminhos e blob SHAs de N.spec/N.md/N.sol/N.txt recuperados da árvore Git imutável e incluídos em cada dossiê.
- Limitação IMPORTANTE: 159 corpos CVL e Solidity NÃO foram todos lidos semanticamente. Este inventário por metadata NÃO encerra a tarefa da fase 1 e não justifica candidaturas específicas de edição.
- Versões de solc e CLI não inventariadas; Remote Desktop Commander offline e container local inacessível.
- Validadores Python, git diff --check, PDF page-by-page, CVL1, CVL2, Prover NÃO executados.
- Bloqueio crítico: Specify .cvl is not equivalent to ordinary CVL1 .spec. The .spclnk aliases and modeled ABI are historical context, not property instances.
- Próximo passo obrigatório antes de revisão para Fase 2: leitura individual dos N.spec, N.md, N.sol e transitive imports, reconstrução histórica com hashes upstream auditados, motivos N.txt e pesquisa official per-case.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## Atualização auditada 2026-10-19

Identificado commit upstream e 5 arquivos byte-idênticos aos archived originals; detalhes em [AUDITED_SOURCE_PROVENANCE.md](AUDITED_SOURCE_PROVENANCE.md). O status incomplete de dez exemplos permanece; sem CVL2 ou Prover.
