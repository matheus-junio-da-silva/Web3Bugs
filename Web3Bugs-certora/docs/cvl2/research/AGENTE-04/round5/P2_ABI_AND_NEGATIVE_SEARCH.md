# P2 — Proof of Reserve, source auditada versus ABI/receivers faltantes

## Auditoria de commit e buscas negativas

Checkout Git independente de Certora/aave-proof-of-reserve@12296ce4c6f9bde6663e1baa02cf19f179c1048b, hash inteiro correspondente ao abreviado 12296ce mencionado no PDF de seis páginas. git ls-tree -r HEAD revela 99 arquivos. Buscas por extensões .spec, .conf e nomes harness, PORaggregatorDummy ou configuratorDummy na árvore desse SHA não retornaram arquivos. Não inferir que os artefatos nunca existiram fora desse commit.

Verificados com cmp a source src/contracts/ contra o snapshot imutável:
- ProofOfReserveAggregator.sol SHA256 152b0f8c77ba6d4629828afb4e82bd355cde7acc865cd89fd8315a640465fecd: bytes iguais.
- ProofOfReserveExecutorBase.sol SHA256 2d4421c5e7d6034f9b8dca71a4f017d3d99e66d167aae09f4e5500a7baff12e4: bytes iguais.
- ProofOfReserveExecutorV2.sol SHA256 b08f5fc3eeacd19dab91a06f225e7da117495f0d723c8bbd3020e121ff713015: bytes iguais.
- ProofOfReserveExecutorV3.sol SHA256 fb1ad3e412b6cb83735dfdc655d3c5787fe06f8ca3763ca1e6207347d79d40b4: bytes iguais.

## ABI observável e origem do receiver da feed

Em contracts/2/contracts/ProofOfReserveAggregator.sol, L21–35 estão getProofOfReserveFeedForAsset(address) e getBridgeWrapperForAsset(address), externals view; as operações de ativar/desativar alimentam mappings sob onlyOwner nas linhas seguintes. Em L89–122, areAllReservesBacked(address[]) chama AggregratorV3Interface(feedAddress).latestRoundData() no contrato da **FEED EXTERNA**, não um método da ABI do ProofOfReserveAggregator.

No CVL original contracts/2/specs/aggregator.spec L1–16, há summary latestRoundData() => NONDET, entradas de getters e selectors; helper call_f_with_params L18–28 e rule PoRFeedChange L35–54. O programa CVL1 aplicava summaries por assinatura genericamente; CVL2 exige receiver explícito ou corrente, sem equivalência garantida. Converter latestRoundData para currentContract estaria tecnicamente errado quanto ao alvo da chamada externa; usar wildcard também precisa de prova sobre o conjunto de contratos resumidos. A rule quantifica method f, o que aumenta o risco de diferença no universo de métodos e nos reverts.

Imports do Aggregator original em linhas 4–6: solidity-utils/.../Ownable.sol, solidity-utils/.../IERC20.sol e chainlink-brownie-contracts/.../AggregatorV3Interface.sol. No snapshot P2 esses pacotes externos não estão vendorizados, e seus bytes auditados não foram recuperados de maneira autenticada. **ABI Solidity integral de P2 não foi compilada**, precisamente por closure externa faltante; não basta recriar getters methods pela assinatura textual do CVL.

## Por ID e próximos gates

- P2/complete/1 PoRFeedChange: é o único DOCUMENTED_CANDIDATE do projeto. O target nominal ProofOfReserveAggregator está presente, mas spec summary de feed, métodos elegíveis e setup remoto não fechados. **Não executado** Certora compile-only. Não transferir marcação de PDF por nome sem instância executada.
- P2/incomplete/1–14: executors e aggregator correlation referenciam helpers PORaggregatorDummy, configuratorDummy, _disableBorrowingCalled, getAssetsLength, getAssetState ou areAllReservesBackedCorrelation (conforme instância). Ausência do harness/prover job impede reconstrução; não sintetizar getters ou mock.
- PDF p.2–3 assume arbitrariedade de summaries externas e unrolling limitado a três iterações; p.5–6 contém propriedades agregadas. Contagens antigas não são provas individuais.
- Depende do coordenador: recuperar specs CVL do job original, versões históricas de pacotes importados, wrappers/receivers, links e flags; então adjudicar P2/complete/1 isoladamente.

**Gate:** P2 possui 15/15 unresolved, zero compilações CVL2 novas, zero equivalência semântica e zero Solidity histórico editado.
