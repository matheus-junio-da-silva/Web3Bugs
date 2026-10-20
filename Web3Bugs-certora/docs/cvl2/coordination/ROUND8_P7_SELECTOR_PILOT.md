# Auditoria Round 8 — 20/10/2026 — P7/47 e P7/73: candidaturas com `sig:`

**Fonte canônica intocada:** `Web3Bugs-certora/results/spec/complete/7/{47,73}.spec`, origem `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Regras homônimas `disallowedFunctionalities` mas contratos-alvo **distintos**: StableDebtToken e VariableDebtToken. Análise reconstituída por coordenador, não atribuída ao agente. **Sem CVL1; sem Prover; sem mudança em arquivo original ou no main.**

## Experimento scratch isolado executado após recuperação do WSL

O dispositivo `DESKTOP-5E26TVU` voltou a responder em 20/10/2026. Antes dos experimentos, o checkout histórico `/home/mat/cvl2-agent05-isolated/Web3Bugs` retornou HEAD `470e18be85e74c957783a563d00e454e25f0c510` e `git status --short` vazio. Os validadores do catálogo retornaram 0: `check_specs.py` atestou **1386 exemplos e 1390 relações**; `check_contests_csv.py` e `check_contracts.py` também passaram. Os binários `solc 0.8.10` e `certora-cli 8.19.0` estavam disponíveis.

Para cada `N.spec` original foi criada cópia `original.spec` em `/tmp/cvl2_coordinator_round8_20261020/<N>/specs/`, e `candidate.spec` obtida exclusivamente por **seis substituições** textuais, todas no `definition disAllowedFunctions(method f)`, de `f.selector == transfer(address,uint256).selector` (e cinco outros selectors) para `f.selector == sig:transfer(address,uint256).selector`; mantidos `definition`, `filtered`, `f@withrevert(e,args)`, `assert lastReverted`, `methods` inexistentes no N.spec, comentários, e todo o resto. Um assert no gerador rejeita número de substituições diferente de seis. **Não** é equivalente a migrar a spec global inteira `contracts/7/specs/{StableDebtToken,VariableDebtToken}.spec`, que contém outros métodos/ghosts/hooks.

| Caso | SHA-256 original | SHA-256 da candidata de seis `sig:` | target |
| --- | --- | --- | --- |
| P7/complete/47 | `0cf2150c11cfb9926d3e24eecc1fb7ce0c9ffeb956ec3553dab606d026a8416e` | `409539dbf3a66d5c8877d0d374e7281090ca66ce0fd49c9461c280021e57d996` | StableDebtToken |
| P7/complete/73 | `c82afdd9a07a75c9c6cad9b20eee201cb212017cc4cd01c6266bc90b42c8a76b` | `9719778bf3a91837f3c51ae3d3ce5475350460f29af35d34c286307feff5f99d` | VariableDebtToken |

A árvore `contracts/7/contracts` foi copiada integralmente para cada `/tmp` e compilada em dois jobs isolados:

```bash
# CWD /tmp/cvl2_coordinator_round8_20261020/47
env -u CERTORAKEY -u CERTORA_TOKEN -u CERTORA_API_KEY \
  HOME="$PWD/home" timeout --signal=TERM --kill-after=5s 50s \
  /home/mat/certora-ac-audit/certora_venv/bin/certoraRun \
  contracts/protocol/tokenization/StableDebtToken.sol:StableDebtToken \
  --verify StableDebtToken:specs/candidate.spec --compilation_steps_only \
  --solc /home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10

# CWD /tmp/cvl2_coordinator_round8_20261020/73
# Igual, mas com VariableDebtToken.sol:VariableDebtToken e
# --verify VariableDebtToken:specs/candidate.spec
```

**P7/47: exit code 0.** A geração *auxiliar* de autofinder relatou `CompilerError: Stack too deep`; o CLI explicitamente fez `falling back to original file StableDebtToken.sol` e completou a etapa de compilação. Não confundir esse fallback com sucesso da instrumentação opcional.

**P7/73: exit code 0** na compilação-only do fragmento derivado.

Os logs `stdout.log`, `stderr.log`, `exit_code.txt` permanecem em `/tmp/cvl2_coordinator_round8_20261020/{47,73}/`. São evidências **locais**, que podem se perder se `/tmp` for limpo; hashes/flags/observações foram registrados neste arquivo para revisão. `git status --porcelain` da worktree canônica permaneceu vazio.

## Semântica: gate não satisfeito

1. Os originais P7/47 e /73 já tinham **COMPILE_ERROR** no typechecker CVL2 na Rodada 5 por selectors CVL1 sem `sig:`. A compilação das candidatas **não apaga essas evidências**; no [CSV de 18 tentativas](ROUND8_COMPILATION_ATTEMPTS.csv) há duas linhas adicionais, sem deduplicar os resultados por caminho.
2. Seleção `method f`: lista de seis selectors corresponde a funções ERC20-style que **não são implementadas externamente** por esses tokens de dívida no modelo observado. Isso sugere que o predicado `disAllowedFunctions` pode filtrar exatamente funções ausentes; o universo simbolicamente alcançável e a reação a `f@withrevert` ainda exigem decisão de semantics/ABI/invocabilidade e sanity check independente. Um `assert lastReverted` universal pode passar se nenhum `f` for explorado. **Sem execução Prover e sem comparação CVL1 histórica**, não classificar como prova de revert nem non-vacuity.
3. Os dois targets não compartilham a mesma ABI global: VariableDebtToken e StableDebtToken têm métodos herdados e implementações distintas, hooks/ghosts/summaries presentes nas *specs integrais* CVL1. Não validar apenas o recorte como reprodução do run auditado.
4. `COMPILE_OK` é aceitação do parser/typechecker e compilações auxiliares **do arquivo derivado**, não `VERIFIED`, `SEMANTIC_PROVEN` ou `00_unchanged`. Os destinos CVL2 de outros lotes não são alterados.

## Contagem de progresso sem dupla contagem

- **18 tentativas CVL2 distintas** distribuídas por **16 propriedades**: 6 `COMPILE_OK` (2 novos derived, 2 originais fragmentados, 2 derived P19) e 12 `COMPILE_ERROR` dos fragmentos originais.
- **P7/47 e /73** aparecem duas vezes porque sofreram **tentativas com textos diferentes**. Interseção das propriedades com sucesso e erro = **2**.
- **1.370 propriedades nunca tiveram uma execução CVL2 observada**. A fórmula correta é `1386 - (6 + 12 - 2) = 1370`, não `1386-18`.
- **Zero equivalências CVL1→CVL2 demonstradas; zero projetos integralmente validados.**

Validação por `scripts/check_cvl2_round8_attempts.py` foi **executada no WSL** com catálogo original: 1386 chaves, 1390 relações, 18 tentativas, 16 propriedades, 6/12, 2 intersecções, 1370 não testadas, `errors=[]`, exit 0. Teste negativo em uma cópia temporária marcou indevidamente `semantic_equivalence=PROVEN` e resultou corretamente em **exit 1**; sem alteração dos CSVs originais. O GitHub Actions independente executa a validação e o teste negativo na branch do PR.

**Estado:** os PRs de pesquisa #39/#37/#36/#42/#40/#38/#41/#43 continuam Draft; piloto #46 continua `02_unresolved`. Este relatório somente documental/QA pode ser mesclado após CI, sem autorizar merge de implementação.
