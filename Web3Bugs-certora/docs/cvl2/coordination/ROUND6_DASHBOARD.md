# CVL2 — painel de evidências / Rodada 6 / 20-10-2026

**Coordenação:** [PR #47](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/47), exclusivamente documentação e validação estrutural. **Fontes originais:** `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` imutável. **Oito agentes:** PRs #39, #37, #36, #42, #40, #38, #41, #43; heads pinados e exemplos por projeto em [ROUND6_PROGRESS.csv](ROUND6_PROGRESS.csv). Não houve merge, Prover nem teste CVL1 autorizado.

## Contabilidade por exemplo, sem misturar níveis de prova

| Gate | Valor | % | Interpretação |
| --- | ---: | ---: | --- |
| Catalogado e com registro de pesquisa | **1386 / 1386** | 100% | 1390 relações de Bug Label; documentação até casos não reproduzíveis |
| 23 projetos com relatório de pesquisa | 23 / 23 | 100% | Cobertura documental |
| CVL2 `--compilation_steps_only` **EXIT 0** | **4 / 1386** | 0,29% | P7/37,65 recortes originais do snapshot; P19/1,2 cópias derivadas e restritas |
| CVL2 parser/typecheck **EXIT 1** com logs atribuídos à property | **12 / 1386** | 0,87% | P7/36,41,47,63,73; P10/33,34; P12/23,25; P15/incomplete/36; P18/3,23 |
| Sem execução CVL2 atribuível à property | **1370 / 1386** | 98,85% | Falha de autenticação, solc ABI, SIGBUS e `--version` **não contam** como parser |
| Equivalência semântica CVL1→CVL2 demonstrada | **0 / 1386** | 0% | Não reconstituído mesmo conjunto de contraprovas na cena auditada |
| Projetos completamente migrados/validados | **0 / 23** | 0% | Não confundir `complete` do catálogo histórico com Fase 2 completa |

**Artefatos:** [ROUND6_COMPILATION_OBSERVATIONS.csv](ROUND6_COMPILATION_OBSERVATIONS.csv) registra as 16 chaves distintas com status e evidência; [check_cvl2_round6_progress.py](../../../scripts/check_cvl2_round6_progress.py) reconcilia os 23 projetos e 16 observações com o catálogo histórico. A prova independente contra CSV real pelo conector GitHub deu 1390 relações, 1386 chaves, 23 projetos, oito heads, 4 OK/12 erro/1370 sem teste, nenhum mismatch; teste negativo alterou **somente em memória** o contador compilado de P1 e confirmou a detecção de anomalia. **Esta verificação não executa nem substitui os três validadores históricos no WSL.**

## Novidade realmente atribuível à Rodada 6

**AGENTE-04, P15/incomplete/36 `limitOnDiscountRate`:** N.spec byte-original e target `GhoDiscountRateStrategyHarness`; CLI Certora 8.19.0 direto, Solidity 0.8.10, `--compilation_steps_only` em scratch com exit **1 por seis entradas de `methods` sem `function` e `;`** (linhas 7–12), log [#42/round6/P15_36_CVL2_COMPILE_LOG.txt](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/3cd8f72c35d94b4a48cb6155628cba4bea378c67/Web3Bugs-certora/docs/cvl2/research/AGENTE-04/round6/P15_36_CVL2_COMPILE_LOG.txt). Essa observação somada aos 15 casos de R5 produz a contagem acima. **Não demonstra** equivalência nem libera migração da spec completa.

Os outros sete agentes **não registraram execuções novas de `certoraRun --compilation_steps_only` com diagnóstico do parser nesta Rodada 6**. Em especial, a proposta `sig:` P7/47 do AGENTE-05 não chegou à execução; os P18/3 e /23 do AGENTE-02 continuam duas **execuções anteriores do coordenador**, não da Rodada 6; ABI Solidity `solc` não se contabiliza como CVL2; tentativa `--version` que sofre SIGBUS é falha ambiental.

## Auditoria técnica e próximos gates por agente

| Agente (PR) | Avanço verificável | Gate estrito seguinte |
| --- | --- | --- |
| 01 [#39](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39), P10/266 | P10/33–34 dependências LibParam, driver separado do Perl; relatório de métodos `envfree` e `require false` | Closure CVL global/harness+receiver, variantes `function`/`sig:` **somente scratch**, sem promover |
| 02 [#37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), P18/181 | ABI solc de quatro mocks; 2 erros CVL2 históricos atribuídos ao coordenador | Retomar P18/4,46,53 com CLI direto após recuperação de FS, avaliar `public` internal/external |
| 03 [#36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36), P24/164 | Hunk 7 do LaunchEvent troca guarda `balance >= reserve` por `balance-value >= reserve`; import graph parcial | Target e run auditados, pacotes OZ 4.4.1/4.4.2 e `Owner.sol` sem substitutos |
| 04 [#42](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/42), P2/12/15 157 | **Novo P15/36 parser EXIT 1**; GHO remappings e ABI; P12/23,25 errors anteriores | Analisar visibilidade/receiver dos seis methods de P15/36 e novos requires do harness, sem alterar originals |
| 05 [#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), P3/6/7/19/21 148 | Variante proposta **não executada** de P7/47 com seis `sig:` e universo method-f ABI | Testar exclusivamente variante scratch P7/47 depois do FS, preservar `@withrevert` e asserção, não inferir não-vacuidade |
| 06 [#38](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38), P1/4/17/22 159 | junho vs setembro bridge distinta, `munged` P4, Specify 2019 | Compilar solc harness P4 com toolchain correto somente após recuperação; não extrapolar era histórica |
| 07 [#41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), P8/9/11/20 156 | P8 W1 para 22 N.spec, W2/W3 outros; P9 phase2 ABI parcial, imports Mentocore missing | Plano de satisfatibilidade sem executar Prover até autorização; reconstruir Mentocore via SHA |
| 08 [#43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43), P5/13/14/23 155 | P5 BridgeHarness solc ABI e P14 Controller pós-patch 39→42 funções, sem Prover | P5 regra individual com scene íntegra; P14 mudanças de lógica de `getExcessCollateral`, getters e runner |

## Bloqueio técnico externo: WSL `spawn EIO`

Vários agentes R6 registraram `Bus error`, `SIGBUS`, `EROFS`, falhas de `df` e I/O em checkout; o coordenador reproduziu `spawn EIO` mesmo ao executar `df -h`, `ls` e `python3 --version` via Remote Desktop Commander. O dispositivo estar **online** não implica filesystem íntegro. **Nenhum novo teste CLI WSL foi executado pelo coordenador nesta rodada.** Ver [ROUND6_WSL_IO_INCIDENT.md](ROUND6_WSL_IO_INCIDENT.md) para gate de recuperação. Correções de documentação foram feitas pelo conector GitHub sem mexer no filesystem remoto.

**Estado geral:** os oito PRs mantidos Draft e sem merge; nenhuma modificação em `results/spec/`, `contracts/` ou `spec_buglabel.csv`. PR #46 experimental P19 permanece `02_unresolved`. O trabalho continua nos oito chats, priorizando pesquisa/source closure e QA read-only até ambiente de compilação confiável.
