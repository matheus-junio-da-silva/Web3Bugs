# Painel CVL2 — Rodada 4 (20/10/2026)

**Coordenação:** [CSV por 23 projetos](ROUND4_PROGRESS.csv), [validador contábil](../../../scripts/check_cvl2_round4_progress.py). **Base imutável:** `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. **PRs pesquisados:** [AG01 #39](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39), [AG02 #37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), [AG03 #36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36), [AG04 #42](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/42), [AG05 #40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), [AG06 #38](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38), [AG07 #41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), [AG08 #43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43). Todos Draft, sem merge no momento desta revisão.

## Barras de progresso, critérios diferentes

| Indicador | Valor | Percentual | Interpretação |
| --- | ---: | ---: | --- |
| Catalogação original | 1.386 / 1.386 | 100% | Chaves únicas de properties; 1.390 relacionamentos Bug Label |
| Matrizes de pesquisa Rodada 4 | 1.386 / 1.386 | 100% | Progresso documental e classificação de blockers; **não** migração |
| Projetos com levantamento documental | 23 / 23 | 100% | Documentação de pesquisa entregue |
| CVL2 compilation-only em escopo limitado | 4 / 1.386 | 0,29% | P19/complete/1–2 com mudança `mathint` **em cópias derivadas**, P7/complete/37,65 como **fragmentos** de snapshot |
| Equivalência semântica CVL1→CVL2 provada | 0 / 1.386 | 0% | Não foi demonstrada equivalência de motores/cenas históricas |
| Projetos inteiramente migrados/validados | 0 / 23 | 0% | Nem um projeto integralmente encerrado em Fase 2 |

**Contagem auditada:** agreguei os 23 projetos das oito matrizes ROUND4. Cada projeto tem IDs e quantidades reconciliados ao CSV canônico; campos Property/Target/Result/Detection Outcome, onde presentes, coincidem, sem divergências. Oito workflows `validate` relativos às HEADs atuais foram vistos como SUCCESS. Esses workflows verificam estrutura, não semântica.

### Regra de status

- `catalog_complete`: dependências no recorte histórico disponíveis; não significa pronto para CVL2.
- `DOCUMENTED_CANDIDATE` e `UNCHANGED_CANDIDATE`: hipóteses de investigação; não são compilações ou implementação aprovada.
- `COMPILE_OK`: somente arquivo e target efetivamente usados com CLI/version/flags/logs; não é VERIFIED nem prova de equivalência.
- `02_unresolved`: preserva casos com migração candidata compilada mas sem semântica demonstrada, como P19/1–2.
- `fully_migrated=1`: somente se todas as properties pertinentes foram verificadas com critérios independentes. Bloqueio histórico documentado não eleva esse indicador.

## Revisão técnica da Rodada 4

**AG01 (P10, 266):** 266/266 N.spec auditados por hash, LibParamHarness/33–34 mais fundamentados. 14 ocorrências indevidas de `sig:` em comentários rebaixadas; Preserve `require false`; ABI pós Perl permanece faltante.

**AG02 (P18, 181):** 50 candidatos lexicais, 131 bloqueados. Nenhum compilado na rodada. `public` cria rotas internal/external dependentes da cena; fonte de alguns nomes não está na spec do commit auditado.

**AG03 (P24, 164):** recuperação do fork Certora e patch analisado. `--fuzz=0` falhou num hunk da cena auditada híbrida; `fuzz 2` funcionar não prova ABI equivalente; OZ 4.4.1 vs 4.4.2.

**AG04 (P2/P12/P15, 157):** 18 candidatos documentados sem proof do ABI. P12 UserConfiguration tem assinatura `address user` no auditado que desaparece no snapshot; P15 `@aave/core-v3` e harness exigem fechamento.

**AG05 (P3/P6/P7/P19/P21, 148):** quatro compilações anteriores, exclusivamente P7/37,65 fragmentos e P19/1,2 derivados. Nenhuma equivalência. Mais promissores P7/41,63,36,47,73 após evidência de universo `method f` e não vacuidade; P19 permanece `02_unresolved` no [PR #46](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46).

**AG06 (P1/P4/P17/P22, 159):** todas UNRESOLVED; ausência `queue2`, `_mock`, fontes generated `src/munged`, semântica Specify, runner parcial de Popsicle.

**AG07 (P8/P9/P11/P20, 156):** W1/W2/W3 axiomas de P8 indicam possível inconsistência, ver [contrarrevisão independente](P8_AXIOM_CONSISTENCY_REVIEW.md). P20 patch atingiu cinco Solidity em scratch, mudando semântica; P9 duas fases auditadas não são equivalentes; P11 tarballs autenticados mas run não reproduzido.

**AG08 (P5/P13/P14/P23, 155):** recuperação de tarballs @aave em P5 (40 Solidity, 64 imports sem missing no grafo textual), patch auditável em scratch; Opyn patch injeta funções/getters e altera semântica do Controller; Radicle wrappers CVT ausentes; 155 permanecem sem compilação/semântica demonstradas.

## Portões técnicos antes de novos PRs derivados

1. **Imutabilidade:** não mudar `results/spec`, `contracts`, `results/spec/spec_buglabel.csv`, reports históricos, nem os N.spec extraídos. Preserve hashes e N.txt de incompletude.
2. **Autenticação:** fixar blob e SHA auditado, target Solidity, regras CVL completas, imports transitivos, harness, scripts, compile flags, receiver de summaries, placeholders, links e proxies.
3. **Teste diagnóstico:** `--compilation_steps_only` em scratch, tempo/versões/hash/stdout/stderr/exit. Não executar Prover/CVL1 por iniciativa do agente.
4. **Semântica:** invariants, methods, hooks, ghosts, `using`, casts/overflow, `ecrecover`, reverts, `assert`, `require`, policy `ALL` vs `UNRESOLVED`, satisfatibilidade.
5. **Adjudicação:** resultados conservadores se não houver equivalência; PR Draft, sem merge nem promoção automática. O coordenador não deve contar dados novos duas vezes.

## Verificação local

Dentro de `Web3Bugs-certora`:

```bash
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
python3 scripts/check_cvl2_round4_progress.py --json
git diff --check
```

O validador do progresso compara **somente a consistência contábil do ledger com o CSV histórico**. Não conecta ao GitHub nem valida independentemente os logs de compilação; estes exigem revisão separada por PR.

**Próxima rodada:** trabalho em paralelo dos oito agentes; cada um tem escopo exclusivo e um PR de pesquisa próprio. Auditorias de trabalhos alheios são read-only. Este painel pertence à coordenação e não altera os 1.386 exemplos.
