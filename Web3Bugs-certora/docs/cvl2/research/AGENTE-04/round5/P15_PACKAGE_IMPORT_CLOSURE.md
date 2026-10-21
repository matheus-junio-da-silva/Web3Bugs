# P15 GHO — provenance npm, closure de imports e ABI pós-patch

**Fonte auditada:** aave/gho-core commit ce49fb0c94cfebf0159222ceb288e4f9a55d305f, checkout Git em scratch com HEAD verificada. package-lock.json possui lockfileVersion 2 e 895 entradas. Foram recuperados somente três pacotes npm, todos com URL resolved fixada e SHA512 comparado ao SRI do lockfile. Esta operação foi executada na Rodada 5, não apenas citada da Rodada 4.

| Pacote npm | Versão | SHA256 tarball obtido | SRI SHA512 |
| --- | --- | --- | --- |
| @aave/core-v3 | 1.17.2 | 1a1307d7cfae3027fd475fa76dd251206c1c65fd2466b60036da6cadc8ef54e9 | MATCH |
| @aave/periphery-v3 | 2.0.1 | b48e664f06dbbc34e3e3af2dc13fd6dc4fd34fa116e5bfc98362d62f6c741320 | MATCH |
| @openzeppelin/contracts | 4.8.1 | d45d540b9b1c60707b01c8981ccfb1ce9b7e156492c9ab85a46fa520960da065 | MATCH |

Log original de verificação dos três pacotes: evidence/gho_package_sri.log. Bundle foi extraído apenas em scratch/node_modules. O restante do lockfile de 895 entradas NÃO foi instalado/reproduzido: SRI de três tarballs não é hash da instalação do Prover.

## Patch histórico verificável, não equivalência

O commit fixa certora/Makefile e certora/applyHarness.patch, SHA256 do patch 5bd7efa57de87e8c325d24b44a7ac37d89d2906f9d333fbc14efaafb807de325. Como make não estava instalado no WSL, a execução de make munged foi tentada, mas não chegou a ser executada com sucesso. Reproduzi MANUALMENTE em scratch a mesma sequência de cópia src→munged e patch -p0 usando o PATCH ORIGINAL, sem qualquer edição de hunks. Aplicação do patch EXIT 0, log evidence/gho_original_patch.log. Uma tentativa inicial com cópia aninhada munged/src falhou e foi abandonada; não há alegação de sucesso dessa tentativa.

Hash gerado em scratch de certora/munged/contracts/gho/GhoToken.sol = db7c06317fd74b5f1ec501ac2985dbddecd5f52236232c75ff0f1740d65d2cc5; para certora/munged/contracts/gho/interfaces/IGhoToken.sol = 2ea007113309e3778df73e8b12bdcfef826a67a5afba05922a3bdfce85e10d75. Esses hashes foram comparados byte a byte contra cenário scratch preparado independentemente dos mesmos hunks.

Patch introduz requires em addFacilitator, removeFacilitator e setFacilitatorBucketCapacity, campo booleano isLabelNonempty, e transforma getters getFacilitatorBucket e getFacilitatorsList de external para public. Mudam possibilidades de revert, layout de estado e chamadas internas, mesmo quando os selectors públicos não mudam. Não tratar hash ou patch que aplica como preservação semântica.

## Fechamento de imports de Solidity POR FAMÍLIA, sem misturar propriedades

Lidas as cinco invocações de certoraRun do commit auditado em certora/scripts/verify*.sh. Raízes Solidity explícitas do primeiro comando de cada script (no total 19 inputs com repetições) e imports de Solidity recursivos sobre arquivos de cena, src original, munged e os pacotes autenticados. O algoritmo não sintetiza arquivos, não transpila imports nem substitui interfaces.

| Script | Inputs explicitos | Arquivos Solidity alcançados | Import edges | Missing path |
| --- | ---: | ---: | ---: | ---: |
| verifyFlashMinter.sh | 4 | 51 | 111 | 0 |
| verifyGhoAToken.sh | 6 | 50 | 97 | 0 |
| verifyGhoDiscountRateStrategy.sh | 1 | 4 | 4 | 0 |
| verifyGhoToken.sh | 2 | 15 | 17 | 0 |
| verifyGhoVariableDebtToken.sh | 6 | 32 | 55 | 0 |
| SOMA POR CENAS (inclui imports repetidos) | 19 | 152 | 284 | 0 |

evidence/gho_import_closure_families.csv e evidence/gho_import_closure_edges.csv preservam cada source, path importado, destino, classificação e hash SHA256. O zero significa apenas **zero arquivos importados ausentes dentro das cenas e bundles SCRATCH escolhidos**; não demonstra deploy/bytecode efetivo, links, ABI de todo target, configuração ou semântica. Os totais 152 e 284 têm duplicação entre scripts.

## Compilações executadas, separadas de CVL2

Compilador solc 0.8.10+commit.fc410830, comando --base-path . --include-path node_modules --allow-paths . --combined-json abi, timeout 70. Todos em cenário GHO auditado reconstruído e SCRATCH, sem certoraRun nem Prover. Resultados reais:
- GhoDiscountRateStrategyHarness.sol: EXIT 0, ABI de 6 métodos externos.
- GhoTokenHarness.sol + munged/GhoToken.sol: EXIT 0; ABI do GhoTokenHarness com 37 entradas e da GhoToken patched com 30.
- src/contracts/gho/GhoToken.sol sem patch: EXIT 0, ABI com 30 funções.

evidence/solc_compiled_abi_signatures.csv contém 111 entradas, separadas por source scene, sem fabricar resultado CVL. GhoToken patched e original possuem mesmas **30 assinaturas externas**, mas regras internas são alteradas pelos novos requires e visibilidade; não equivalência.

**Alerta de identidade do target:** o CSV histórico P15 aponta 55 exemplos para GhoToken, mas verifyGhoToken.sh verifica GhoTokenHarness com GhoToken presente na cena. Outros 47 exemplos são target catalogada GhoVariableDebtToken e script verifica GhoVariableDebtTokenHarness. O único GhoDiscountRateStrategy utiliza script que verifica GhoDiscountRateStrategyHarness. Não corrigir rótulos históricos por conveniência. GhoAToken 7 e GhoFlashMinter 6 têm nomes alinhados ao runner, mas cena completa continua pendente.

**Próximo gate do coordenador:** seleção individual (target + spec integral + flags + links + patch + versões da execução auditada). Nenhuma das 116 propriedades foi submetida a Certora CVL2 nesta rodada; todas permanecem unresolved, sem nova conclusão sobre os 63 VERIFIED do CSV original.
