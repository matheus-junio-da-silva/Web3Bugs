# AGENTE-01 — RODADA 9 / QA REAL

PR #39, branch research/cvl2-agente-01, DRAFT, baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. HEAD inicial 8267dcdf8114dd856e0bffca7c3e6de36b0102d5.

## Pré-condições executadas

1. Saúde do WSL: bash, Python 3.14.4, Git 2.53.0, volume, leitura dos quatro docs normativos, P1 reference, checkout limpo. Sincronização exclusiva por fast-forward, sem reset/rebase. Furucombo upstream c90dec1046 e OpenZeppelin 3.3.0 6be5ffe54 pinados. CLI Certora 8.19.0 e solc 0.6.12 SHA256 f6cb519b01dabc61cab4c184a3db11aa591d18151e362fcae850e42cffdfb09a.
2. N.spec 33/34 originais copiados e comparados byte a byte. Variantes apenas scratch e diffs exatos. Require false, calls, envfree e assertions preservados. HOME e caches isolados, credenciais removidas, timeout -k 5s 65s. Dois COMPILE-ONLY executados por AGENTE-01 na R9: derivado 33 EXIT 1 por lastHasThrown undeclared; derivado 34 EXIT 0. Originais R5 não reexecutados.
3. Solc ProxyHarness scratch com fontes originais copiados: tentativa inicial de remapping encontrou paths OZ não resolvidos (erro da cena), depois cópia local de bytes OZ 3.3.0 resultou EXIT 1 com 4 erros de override (não parser CVL2). Solc --storage-layout Storage.sol EXIT 0, stack slot 0, cache slot 1. Sem patch de source histórico.
4. Fase Perl HMaker reproduzida SOMENTE com linhas 1-102 do runner, sem certoraRun 104-108: 116 arquivos Solidity em scratch, 18 transformados, exit 0 e stderr vazio. SHA256 por arquivo antes/depois documentado. Isto não é ABI histórica e não conta como CVL2.
5. Programaticamente reconciliadas 266 chaves distintas ROUND9_MATRIX_266.csv e todos os campos Property, Target, Result, Detection Outcome, Bug Label, Spec e hashes Git de TODOS os N.spec e N.sol individuais com o CSV original. Status R9: um COMPILE_OK derivado, um COMPILE_ERROR derivado, 264 NOT_RUN, zero equivalências semânticas.
6. Cross-review somente leitura PR #37 HEAD f13481755eeac310aac7f930022faa522c7b8fce, incluindo matriz de 18 métodos e revisão mais recente. Nenhuma branch alheia alterada.

## Logs preservados

ROUND9_DIAGNOSTICS.csv registra os comandos sanitizados, input hashes, versões, target, execuções e resultados dos dois CVL2. ROUND9_LOG_MANIFEST.csv relaciona 11 artefatos com SHA256 bruto e legível. ROUND9_ARTIFACTS/*.raw.b64 preserva bytes originais íntegros. As versões .txt legíveis tiveram apenas quebras terminais vazias removidas para o whitespace gate e possuem hashes diferentes documentados. Não há log inventado nem Prover executado.

## QA estrutural pós-commit

Três comandos Python oficiais e git -c core.whitespace=cr-at-eol diff --check BASE...HEAD deverão ser executados sobre o commit atual. Registrar abaixo HEAD e exits reais depois que ocorrerem; a passagem em GitHub Actions não substitui testes locais e não demonstra equivalência.

**AGENTE-01 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO.**

- Para evitar falsos positivos de git diff --check, somente as versões legíveis de 33_exact_diff, 34_exact_diff e storage_layout receberam prefixo [raw] por linha; as versões raw.b64 preservam integralmente os bytes do diff/layout original. O manifesto registra os dois SHA256 distintos.

## Primeira bateria QA após commit d4aba118488518e3878a39ddd51d8339155c73bc

- EXECUTADO: python3 scripts/check_specs.py . — EXIT 0, 1.386 exemplos / 1.390 relações Bug Label.
- EXECUTADO: python3 scripts/check_contests_csv.py . — EXIT 0.
- EXECUTADO: python3 scripts/check_contracts.py . — EXIT 0.
- EXECUTADO: git -c core.whitespace=cr-at-eol diff --check BASE...HEAD — EXIT 2: apenas três trailing whitespaces em arquivo documental antigo desta mesma pasta AGENTE-01/10/ROUND6_QA_EXECUTION.md, linhas 3 a 5, incorporadas no diff histórico. Artefatos novos R9 haviam passado no diff staged. Corrigidos somente espaços de fim dessas três linhas, sem alteração de resultados, specs ou interpretação. Será executada nova bateria após o commit dessa correção.

Logs de QA realmente executados em scratch isolado: /home/mat/cvl2-agent01-isolated/round9-scratch/logs/qa_postcommit/ .
