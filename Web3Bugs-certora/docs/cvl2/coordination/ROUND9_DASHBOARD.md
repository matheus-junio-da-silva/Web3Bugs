# Coordenação Certora CVL2 — Rodada 9 (20 de outubro de 2026)

**Escopo:** 23 projetos, 1.386 propriedades individuais e 1.390 relações Bug Label. Fontes históricas congeladas no baseline `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Os oito agentes atualizaram seus próprios PRs de pesquisa #39, #37, #36, #42, #40, #38, #41 e #43; PR experimental #46 permanece Draft e `02_unresolved`. PRs de coordenação #47 e #48 já foram integrados somente como documentação/QA.

## Indicadores sem dupla contagem

| O que é contado | Valor | Interpretação |
| --- | ---: | --- |
| Excertos catalogados, 23 projetos | 1.386 / 1.386 | Cobertura histórica e documental; não migração concluída |
| Relações de Bug Label | 1.390 | Algumas properties têm mais de uma relação |
| **Execuções** CVL2 compilação-only registradas até R9 | **33** | Inclui testes originais, derivados, repetições, preflight de compilação Solidity |
| Propriedades individuais com ao menos uma execução registrada | **20 / 1.386** | Não é a soma de execuções, pois uma property pode ter vários resultados |
| Execuções `COMPILE_OK` | **11** | Aceitação de fragmentos/variantes derivadas, sem prova formal |
| Propriedades distintas com algum `COMPILE_OK` | **11 / 1.386 ≈ 0,79%** | Não implica `VERIFIED` nem equivalência CVL1 |
| Execuções `COMPILE_ERROR` de parser/typechecker | **21** | Inclui repetições da mesma property original |
| Propriedades distintas com algum `COMPILE_ERROR` | **16 / 1.386 ≈ 1,15%** | Falha de sintaxe/tipagem não é violação da property |
| Interseção propriedades com original que falhou e derivado que compilou | **7** | P7/47,73; P10/34; P15/36; P18/4,46,53 |
| Falhas de setup/remapping Solidity | **1** | P15/36 scratch sem `@aave/core-v3`; não é parser CVL2 |
| Nunca tiveram teste CVL2 observado | **1.366 / 1.386 ≈ 98,56%** | `1386-(11+16-7)=1366` |
| Equivalência semântica CVL1→CVL2 demonstrada | **0** | Domínio, ABI/harness, assumptions e resultados de prova não reconstituídos |
| Projetos integralmente migrados e validados | **0 / 23** | Não aprovar merge de código derivado |

O [ledger de 33 execuções](ROUND9_ATTEMPT_EVENTS.csv) registra uma linha por **evento**, com projeto/status/ID, tipo de entrada, saída, executor e evidência. Um mesmo original pode ter sido executado mais de uma vez e cada linha mantém sua identidade `event_id`; a coluna `semantic_equivalence` permanece `NOT_DEMONSTRATED`. O [verificador do ledger](../../../scripts/check_cvl2_round9_events.py) reconcilia as chaves contra o catálogo e usa inclusão-exclusão. Foi executado no WSL contra `spec_buglabel.csv` real: `errors=[]`, saída 0. Teste negativo alterou **somente cópia temporária** para `semantic_equivalence=PROVEN` e foi corretamente rejeitado com exit 1.

## Auditoria por agente — Rodada 9

| PR | Novidade técnica observável | Gate restante |
| --- | --- | --- |
| [#39 — AG01 / P10](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39) | P10/33 **derivada EXIT 1**: `lastHasThrown` não declarado; P10/34 **derivada EXIT 0** usando `sig:`, preservando `require false`. `solc` ProxyHarness **EXIT 1** por incompatibilidade `override`; `storage-layout` confirmou `stack` slot 0, `cache` 1. 18/116 contratos HMaker alterados pela transformação Perl em scratch | Documentar `lastHasThrown` da spec integral sem inventar variável; reconstruir ABI pós-patch e Perl; P10/34 pode ser vacuous |
| [#37 — AG02 / P18](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37) | P18/4,46,53 **originais EXIT 1** (`methods` antigos); três **derivadas EXIT 0** em solc 0.8.6, logs originais compactados por gzip, patches e SHA256 por caso | Receivers `public` vs `internal/external`, summaries, `method f`, full CVL; specs do commit auditado não equivalentes |
| [#36 — AG03 / P24](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36) | `patch --fuzz=0` dry-run e apply **EXIT 0** somente em cena fork Rocket Joe; nenhum solc ou CVL2 | Compile Solidity fork-only ou scene auditada autêntica separadamente; patches alteram comportamento e não comprovam execução original |
| [#42 — AG04 / P2/12/15](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/42) | P15/36 **derivada com remapping EXIT 0**; P15/36 original com remapping mantém parser EXIT 1; P12/23 e 25 originais repetem errors. Uma tentativa derivada P15 sem remapping falhou em **SOLC IMPORT**, não é erro CVL2 | `GhoDiscountRateStrategyHarness` six methods e `envfree`, variáveis globais/reverts; P12 com ABI `address user` diferente; P2 feed/summaries |
| [#40 — AG05 / P3/6/7/19/21](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40) | AG05 auditou os dois pilotos P7/47,73 do coordenador já integrados no PR #48 e a presença dos seis métodos ERC20-style na ABI estática; sem nova chamada do CLI do agente | A presença na ABI não garante entrada `method f`, `@withrevert` nem não-vacuidade; P19 #46 continua `02_unresolved` |
| [#38 — AG06 / P1/4/17/22](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38) | ABI Solidity isolada do StakedToken P4 `solc-js 0.8.17` compilou; FullMathWrapper P22 `solc-js 0.7.6` compilou; PoolActions wrapper falhou em TypeErrors **Solidity**, não CVL2. Junio/Setembro bridge runner permanecem distintos | Cena histórica por propriedade; Specify 2019 não é CVL1 genérico; P22 FullMath não implica proof |
| [#41 — AG07 / P8/9/11/20](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41) | Testemunhas W1/W2/W3 documentadas; fato novo: `authorizeSignerWithSignature` **existe no snapshot P9** mas não na ABI phase2 que foi testada; runner original Keep e deps fixadas | Escopo de axiomas no job, Mento-core SHA exato; solc5.17 ainda não disponível; P20 MAX_INT e patch |
| [#43 — AG08 / P5/13/14/23](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43) | P5/incomplete/14 **original EXIT 1** no parser CVL2 com 11 seeds/10 links. P14 Controller pós-patch muda lógica e risco de arrays `[0]`; P23 harness Certora posterior não reproduz produção | Cenas/ABI/summaries e patch/compiladores individuais por propriedade |

**Decisão de merge:** documentação de coordenação isolada pode ser integrada com CI positivo e teste negativo; esta integração **não aprova os oito PRs de pesquisa nem o PR #46 como migração final**. Qualquer release de migração requer evidência por propriedade de contexto CVL global, target/ABI, assumptions, revert behavior, reachability, versões, testes e equivalência semântica. Não alterar originais, CSV, reports ou merges dos agentes sem gate próprio.
