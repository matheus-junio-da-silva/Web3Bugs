# P2 — Investigacao ABI e ausencia documental (revisao 2)

**B1 auditado:** PDF Proof of Reserve p.1 fixa abreviacao 12296ce, resolvida em SHA `12296ce4c6f9bde6663e1baa02cf19f179c1048b`. O snapshot contem bytes identicos aos quatro Solidity src/contracts do commit (Aggregator, ExecutorBase, ExecutorV2, ExecutorV3). Isso NAO garante os helpers ou scripts Certora.

**Aggregator CVL original:** methods inclui getProofOfReserveFeedForAsset, disableProofOfReserveFeed, enableProofOfReserveFeed, areAllReservesBacked(address[]), getBridgeWrapperForAsset, enableProofOfReserveFeedWithBridgeWrapper, latestRoundData() => NONDET e allBacked(). A especificacao nao prova ABI publica de allBacked. latestRoundData depende de receiver da feed e seu summary global CVL1 nao pode virar currentContract do CVL2 nem wildcard sem prova.

**Executors CVL originais:** usam enableAsset, disableAsset, getAssetState, getAssetsLength, getAsset, _disableBorrowingCalled; nao ha implementacoes de harness comprovadas no tree Solidity auditado. using PORaggregatorDummy as aggregator e em V3 configuratorDummy as configurator sao receivers cujo contrato/ABI exige origem propria. Nao reconstruir mocks.

**B2 PDF integral, seis paginas:** p.2 relata summary arbitrario de areAllReservesBacked para ExecutorV2/V3; p.3 limite de 3 voltas para loops e external effects; p.5–6 apresenta invariants agregadas. Resultado por nome no texto nao e prova identica a N.spec.

**Buscas negativas delimitadas:** git ls-tree auditado nao tem *.spec, *.conf ou harness Certora; snapshot contracts/2 tem tres CVL specs e nenhum .conf. Busca no GitHub por PORaggregatorDummy/areAllReservesBackedCorrelation na fonte PropertyGPT e repositorio Certora nao encontrou os helpers. Nao inferir inexistencia absoluta fora das arvores inspecionadas. Encerramento da pesquisa por esgotamento dessas fontes: falta ABI/config de epoca, 14 incomplete unresolved; complete/1 PoRFeedChange nao pronto.

**A1/A2:** https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html.
