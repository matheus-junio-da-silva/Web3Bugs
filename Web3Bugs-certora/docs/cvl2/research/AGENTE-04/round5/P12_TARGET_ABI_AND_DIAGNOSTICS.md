# P12 — diagnóstico de UserConfigurationHarness (P12/23 e P12/25)

## Origem e identidade

Upstream aave/protocol-v2 commit 750920303e33b66bc29862ea3b85206dda9ce786, checkout Git fixado e versionado. Arquivo auditado specs/harness/UserConfigurationHarness.sol: SHA256 965afb5a3ea8dfc4a34a77ac53cea1079adc9ee9f603971e14f62d174e88a0ee. Snapshot contracts/12/specs/harness/UserConfigurationHarness.sol: SHA256 0bbda4db0ee80986a3c63672d50bd5858ab7fe62cb7a28d440a0e7320846c116. A source auditada usa parâmetro address user; a source snapshot remove o argumento nas sete operações principais. Hashes upstream e snapshot constam também de evidence/historic_source_hashes.csv.

Os dois N.spec foram copiados com preservação byte-a-byte e comparados com cmp (exit 0). SHA256 P12 complete/23 = a8b6271f0d0d5030fbe78e48becf28c1a66ad6754f70e5a9e722cf4690449560; complete/25 = b91c97498f1b60f7664e279ca1520193c03644887463df4df7145a64ce85876b.

## ABI medida por Solidity 0.6.12 do snapshot

Executado no scratch com cwd p12-snapshot: solc 0.6.12 --base-path . --allow-paths . --combined-json abi specs/harness/UserConfigurationHarness.sol. **EXIT 0.** ABI compilada e documentação da assinatura auditada (apenas source-text) em evidence/p12_snapshot_vs_audited_source_abi.csv.

| ID | Snapshot ABI comprovada | Source auditada (NÃO compilada) |
| --- | --- | --- |
| 12/complete/23 setBorrowing | setBorrowing(uint256,bool); isBorrowing(uint256) returns bool | setBorrowing(address,uint256,bool); isBorrowing(address,uint256) |
| 12/complete/25 setUsingAsCollateral | setUsingAsCollateral(uint256,bool); isUsingAsCollateral(uint256) returns bool | setUsingAsCollateral(address,uint256,bool); isUsingAsCollateral(address,uint256) |

Importância: parâmetros e selectors mudam; não inferir que estado/mapeamento muda automaticamente, pois o harness upstream ainda usa usersConfig único.

Contrateste na árvore upstream EXATA: solc 0.6.12 sobre specs/harness/UserConfigurationHarness.sol original retornou **EXIT 1** porque o import relativo contracts/libraries/configuration/UserConfiguration.sol não existe naquela árvore. O arquivo de biblioteca está em contracts/protocol/libraries/configuration/UserConfiguration.sol. Nenhum import ou harness foi reescrito para forçar compilação upstream. Evidência integral: evidence/p12_upstream_solc_stderr.log. Logo, a tabela upstream é declaração textual da fonte, NÃO ABI compilada da execução auditada. O script auditado runUserConfigCLI.sh usa target nominal UserConfigurationHarness e solc6.8 literal; o binário de época não foi comprovado.

## Dois resultados reais do Certora CLI 8.19.0, modo compilação apenas

CWD: /home/mat/cvl2-agent04-round5/scratch/p12-snapshot, solc 0.6.12+commit.27d51765, ambiente sem CERTORAKEY/CERTORA_TOKEN/CERTORA_API_KEY, HOME temporário por execução, timeout --signal=TERM --kill-after=5s 90, sem Prover nem CVL1. Comando para cada n igual a 23 e 25:

    certoraRun specs/harness/UserConfigurationHarness.sol:UserConfigurationHarness
      --verify UserConfigurationHarness:specs/n.spec
      --solc /home/mat/.solc-select/artifacts/solc-0.6.12/solc-0.6.12
      --compilation_steps_only

P12/23: **EXIT 1**. L5:2 e L6:2: cada methods entry deve começar com function; L5:37 e L6:43: cada methods entry deve terminar em ;. Log STDOUT/STDERR integral evidence/p12_23_compile.log.

P12/25: **EXIT 1**. L5:2 e L6:2: falta function; L5:45 e L6:51: falta terminador ;. Log integral evidence/p12_25_compile.log.

Ambas classificadas **COMPILE_ERROR_CVL2_LEGACY_METHODS**, NÃO COMPILE_OK. Nenhum token de source foi alterado, nenhuma spec derivada foi construída. Não há prova de equivalência e não se pressupõe que a falha do parser seja a única futura falha; ela impede testar as etapas posteriores.

## Restante dos 26 exemplos

- complete/19–22,24,26: mantidos DOCUMENTED_CANDIDATE, mas mesma família com user argument ausente no snapshot; não executar lote.
- complete/10–18: VariableDebtToken contém 2/9 corpos semelhantes em tokens (IDs 10 e 16), 7/9 diferentes; linking POOL e cenas/seletores não fechados.
- incomplete/1–9: StableDebtToken auditado com superclass constructor de cinco argumentos e getter diferente da variante initialize do snapshot; não substituir ou reparar.
- Relatórios PDF usam, por vezes, nomes/agregados e fórmulas com argumentos de usuário; NÃO propagados resultados para cada source por similaridade.

**Pedido de gate:** adjudicar se a referência semântica é o harness auditado ou a variante do snapshot para cada ID, e autorizar explicitamente qualquer futura cópia derivada CVL2. O diagnóstico atual é sobre **snapshot**, não replay histórico.
