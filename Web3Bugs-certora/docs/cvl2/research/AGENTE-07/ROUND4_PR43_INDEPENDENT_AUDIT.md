# AGENTE-07 — contrarrevisão independente, somente leitura, PR #43

**PR:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43
**HEAD examinada:** `8d5734a896119442f3d93f7a6f4b754e22fd344d`
**Baseline:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`
**Método:** checkout independente **detached**, `/home/mat/cvl2-agent07-independent-pr43`, sem qualquer alteração ou commit na branch do AGENTE-08.

## Inspeção independente — veredictos

1. `git -c core.whitespace=cr-at-eol diff --check BASE...HEAD`: **exit 0**, nenhum whitespace incorreto reportado.
2. `git diff --name-only BASE...HEAD`: **196** arquivos, todos sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-08/`; nenhum original/spec/Solidity/CSV histórico alterado.
3. `python3 scripts/check_specs.py .`: **exit 0**, 1.386 exemplos e 1.390 relações; `check_contests_csv.py`: **exit 0**; `check_contracts.py`: **exit 0**.
4. Matrizes `13/historical_status.csv` (58), `23/historical_status.csv` (46), `14/historical_status.csv` (34) e `5/historical_status.csv` (17): **155 registros** e **155 `UNRESOLVED_CANDIDATE`**. Os quatro `properties.csv` mantêm a mesma contagem de unresolved, sem 31 promoções indevidas para Opyn.
5. Spot-check histórico: P13 exemplos 32/34 mantêm `NOT_STATED`, sem aumentar artificialmente os 5 VERIFIED catalogados; P23 #36 mantém `FINDING` e #38 `INCONCLUSIVE`; P14 #1, #19 e #25 continuam bloqueados por ABI/selector, bankruptcy e revert respectivamente; P5 #1 continua bloqueado por import closure/version drift.
6. A distinção descrita pelo AGENTE-08 — falta de evidência em fontes consultadas versus impossibilidade de recuperar historicamente — foi preservada. Matrizes não autorizam migração automática nem `COMPILE_OK`/equivalência CVL2.

## Limites e decisão

A auditoria verifica integridade mecânica, contagens, estados e casos sensíveis; **não** é análise semântica exaustiva das 155 bodies nem certificação de import closure, ABI ou Proof Runner histórico.

**Decisão independente:** nenhuma regressão documental detectada nos gates executados; manter PR #43 **DRAFT**, todos os 155 unresolved e exigir artefatos de run/ABI/solc/harness autenticados antes de qualquer autorização de Fase 2. Não efetuar merge.

## Comandos executados

```sh
cd /home/mat/cvl2-agent07-independent-pr43
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
git diff --name-only 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
cd Web3Bugs-certora
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
```

**AGENTE-07 — RODADA 4**
