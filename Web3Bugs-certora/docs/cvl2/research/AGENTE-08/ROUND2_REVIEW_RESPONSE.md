# AGENTE-08 — segunda auditoria: resposta documental ao coordenador
Comentario original: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43#pullrequestreview-5577013034

## Decisao aceita e mantida
O coordenador considerou a pesquisa historicamente aproveitavel, mas fixou **155/155 UNRESOLVED_CANDIDATE**, proibiu Fase 2 e manteve o PR Draft. Nao houve reclassificacao para DOCUMENTED_CANDIDATE nem 01_documented.

## P13
HISTORICAL_BLOCKERS.md, historical_status.csv, RECOVERY_SEARCH_LOG.md: 48 casos com import closure incompleta, dez Balances sem target historico e diferenca 7 vs 5 VERIFIED (IDs #32/#34). Scripts fixam solc7.5 e Brownie packages, sem provar pacote/hash do auditor. Ausencia em busca publica limitada, nao impossibilidade.

## P23
Os 46 exemplos receberam status por instancia. Original Results: 15 VERIFIED, 1 VIOLATED, 30 NOT_STATED; #36 e #38 preservados. CVT generated wrappers/harnesses em falta; busca publica retorna citacoes as specs, nao implementacao. Splits2 nao recebe resultado de Splits.

## P14
Todos 34 continuam unresolved, inclusive as 31 candidaturas retiradas. applyHarnesses.sh muda fontes; runOrderOfOperations usa solc6.10, enquanto runNoBankruptcy e runMarginVault usam um binario nomeado solc (sem versao explicita no comando); ABI/receiver/summary continuam incertos. Placeholders nos antigos dossies sao apenas texto ilustrativo, nao codigo compilavel, e nenhum assert foi alterado.

## P5
Blobs upstream 4c010c18 de erc20.spec, BridgeHarness, mocks, Makefile, patch e scripts sao recuperaveis com proveniencia. Remappings e imports transitivos, ambiente do compiler solc8.10, tree munged e bytes da revisao efetivamente auditada nao fechados. Nao atribuir a erc20.spec implementacoes de getters de BridgeHarness.

## Disposicao final
A pesquisa delimitada das fontes enumeradas foi fechada como bloqueio documental enquanto nenhuma nova pista surgir. Os logs por projeto registram consultas e resultados; nenhuma conclusao de impossibilidade global foi feita. Sem specs, Solidity, CSV historico, asserts, assumes, method universe, Prover ou compilacao CVL2. Nova fonte historica ou deliberacao humana e indispensavel antes de qualquer fase seguinte.
