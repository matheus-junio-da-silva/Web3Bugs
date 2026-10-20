# Painel de coordenação — Rodada 5 — 20/10/2026

**Escopo:** 23 projetos, 1.386 instâncias de properties (1.390 relações com Bug Labels), oito agentes em branches exclusivas. Este documento é o estado factual de triagem; **não é um certificado de migração CVL1→CVL2**.

**Fontes/artefatos de controle:** [ROUND5_PROGRESS.csv](ROUND5_PROGRESS.csv), [ROUND5_COMPILATION_OBSERVATIONS.csv](ROUND5_COMPILATION_OBSERVATIONS.csv), [verificador Round 5](../../../scripts/check_cvl2_round5_progress.py), [painel anterior Round 4](ROUND4_DASHBOARD.md). Refs fixados por projeto na matriz. PRs agentes: [01/#39](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39), [02/#37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), [03/#36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36), [04/#42](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/42), [05/#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), [06/#38](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38), [07/#41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), [08/#43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43).

## Indicadores que não devem ser confundidos

| Gate / universo | Valor | Percentual | Definição |
|---|---:|---:|---|
| Cadastro histórico preservado | 1.386/1.386 | 100% | Complete/Incomplete refere-se às dependências do fragmento arquivado |
| Linhas individuais nos oito relatórios da Rodada 5 | 1.386/1.386 | 100% | Pesquisa e blockers por instância |
| Projetos com documentação | 23/23 | 100% | Não significa migration ready |
| CVL2 `--compilation_steps_only` exit 0 | 4/1.386 | 0,29% | P7/37,65 fragmentos originais do snapshot; P19/1,2 derivados `mathint`; todos sem equivalência histórica demonstrada |
| CVL2 parser/compilation exit 1 real | 11/1.386 | 0,79% | P10/33,34; P7/36,41,47,63,73; P12/23,25; P18/3,23. Não incluem erros de autenticação |
| Ainda sem execução do typechecker CVL2 documentada | 1.371/1.386 | 98,92% | Nenhum resultado de compilação CVL2 atribuível a essa chave |
| Equivalência CVL1→CVL2 demonstrada | 0/1.386 | 0% | Não provaram mesmo universo de contraexemplos, cena, axiomas ou tratamento de reverts |
| Projetos integralmente migrados e validados | 0/23 | 0% | Não há 100% em nenhum projeto |

## Revisão minuciosa da nova entrega

**AGENTE-01 — Furucombo #39, P10 266:** P10/33–34 por LibParamHarness do commit 2021; CVL2 compile-only **ambos EXIT 1**: selector tipado sem `sig:` e gramática `methods` legada. Driver LibParam dispensa Perl; demais handlers dependem de transformação Perl e ABI pós-script. Rebaixamentos de tokens em comentários são positivos. Nenhum patch em specs aprovado.

**AGENTE-02 — OpenZeppelin #37, P18 181:** solc 0.8.6 gerou quatro ABI do snapshot (AccessControlMock, ERC1155Mock/Burnable/Pausable). Tentativas do agente de `certoraRun` foram bloqueadas por wrapper de `CERTORAKEY`: **não são COMPILE_ERROR nem COMPILE_OK**. Contrateste independente do coordenador usou CLI `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun` diretamente, `solc 0.8.6`, `--compilation_steps_only`, credenciais ausentes e cópias byte-idênticas: **P18/complete/3 EXIT 1** (`methods` sem `function`/`;`, SHA256 `5ca7758775888bd0f8275e7f00a41b3dd8056668bc647bb7478010b1dff702c2`); **P18/complete/23 EXIT 1** (mesmos tipos de erro, SHA256 `3c2ac679b19f75c7777d3221c858337529a4646a18bcb194bf6a812d64ba16c9`). Logs em `/tmp/cvl2-coord-r5-p18-{3,23}-20261020/stdout.log`, fora do repo. Ainda sem conversão admissível `public` internal/external.

**AGENTE-03 — Rocket Joe #36, P24 164:** separação precisa do commit auditado `ef2ef302` e fork `dba90f9`. Hunk de guarda LaunchEvent muda `balance >= reserve` versus `balance-value >= reserve`; não é transformação textual neutra. Dependências OZ 4.4.1/4.4.2 autenticadas por SRI em scratch; patch sem fuzz falha na cena híbrida. 0 compile-only.

**AGENTE-04 — Proof of Reserve/AAVE V2/GHO #42, 157:** P12/complete/23 e /25 **EXIT 1** pelo bloco methods CVL1, enquanto compilação Solidity do snapshot UserConfigurationHarness passou. Assinaturas auditadas exigem `address user`, não presente no snapshot. P15 recuperou pacotes `@aave/core-v3` e compilou ABIs Solidity de targets patchados, mas não reproduziu o Prover. P2 ainda carece de artefatos CVL auditados.

**AGENTE-05 — P3/P6/P7/P19/P21 #40, 148:** P7/36,41,47,63,73 **EXIT 1** por selectors CVL1; seis métodos disallowed existem na ABI snapshot e revertem no contrato, mas a quantificação `method f`/vacuity e hook/ghost globais impedem conclusão semântica. As quatro compilações **já** bem-sucedidas da coordenação não foram repetidas; P19 #46 `02_unresolved`.

**AGENTE-06 — P1/P4/P17/P22 #38, 159:** fork posterior Setembro/2022 recupera `queue2`, `_mock` e scripts, mas PDF da auditoria de Junho/2022 — **não** atribuir o runner posterior à execução anterior. P4 script `applyHarness.patch` aplicado com fuzz=0 ao upstream auditado em scratch, 37 arquivos. P17 Specify 2019 exige tradução semântica por regra; P22 runner parcial. 0 compile-only.

**AGENTE-07 — P8/P9/P11/P20 #41, 156:** relatório independente confirmou contradições formais por substituição W1 em 22/22 extrações P8, W2/W3 em P8/1. Não editar axiomas nem assumir impacto histórico no Prover. P9 Accounts phase2 Solidity ABI compilada; AccountsHarness snapshot tem três imports mento-core faltantes e P9/6 usa selector ausente na ABI phase2. P20 patch altera cinco arquivos, P11 closure Keep textual. 0 CVL2 compile-only.

**AGENTE-08 — P5/P13/P14/P23 #43, 155:** P5 BridgeHarness após patch + npm SHA autenticado compila por **solc 0.8.10** (não CVL2), ABI BridgeHarness 34 funções. P14 controller original/pós-script solc 0.6.10 compilados e comprovada alteração de 39 para 42 funções externas + mudança de lógica; 31 candidaturas rebaixadas corretamente. P23 e P13 continuam sem wrappers/targets exatos. 0 CVL2 compile-only.

## Execução independente e validação do painel

Do WSL remoto, usando arquivos deste PR publicados via URL imutável de branch e catálogo local:

```bash
python3 scripts/check_cvl2_round5_progress.py \
    --catalog results/spec/spec_buglabel.csv \
    --ledger docs/cvl2/coordination/ROUND5_PROGRESS.csv \
    --observations docs/cvl2/coordination/ROUND5_COMPILATION_OBSERVATIONS.csv
```

**Teste positivo:** saída `1.386 exemplos; 1.390 relações; 23 projetos; oito HEADs; 4 COMPILE_OK; 11 COMPILE_ERROR; 1.371 sem teste; zero equivalência; zero projeto finalizado; errors=[]`, exit code **0**.

**Teste negativo:** modificação proposital, **só em cópia temporária do ledger**, do contador P1 COMPILE_OK de 0 para 5; verificador retorna `P1 limited_cvl2_compile_ok=5; expected 0`, exit code **1**. Não houve adulteração dos CSVs versionados.

Todos os oito PRs de agentes estão Draft e oito workflows `validate` da HEAD da Rodada 5 terminaram `SUCCESS`; isso **não** significa provas formais. Nenhum Prover/CVL1 novo foi executado, nenhum merge nem modificação de `results/spec`/contratos/catálogo.
