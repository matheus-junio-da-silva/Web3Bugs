# AGENTE-01 — RODADA 10 / QA observado, incidentes e limites

PR #39: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 (DRAFT). Branch: research/cvl2-agente-01. HEAD de partida realmente conferida: fc668ccdfa825266952b9daca9cc08432ad8ccf6. Baseline imutável: 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3.

## Pré-condições inicialmente executadas e aprovadas

- WSL DESKTOP-5E26TVU on-line; processo simples bash /bin/true funcionou.
- Python 3.14.4 e Git 2.53.0 responderam, volume inicial montado (df /home/mat: 1007G, 44G usados).
- git rev-parse HEAD inicial respondeu fc668ccdfa825266952b9daca9cc08432ad8ccf6; git status --short --branch indicou research/cvl2-agente-01, limpa.
- Ferramentas localizadas: Certora CLI 8.19.0; solc 0.6.12+commit.27d51765. Furucombo c90dec1046e5e26edf70f985dd86381403912482 e OpenZeppelin 3.3.0 6be5ffe54fc8982b7c1d0f45d4cb7bbd313107cd.
- Leitura completa dos quatro documentos normativos da pasta docs/ e referências P1; linhas: spec_catalog 79, spec_catalog_workflow 487, spec_catalog_project_1 90 e standard 270.
- Busca somente leitura na spec global Furucombo 2021: apenas uma ocorrência de lastHasThrown, na assertion L18; métodos L1–4 e noThrow L6–19 não fornecem declaração; noRevert L21–31 usa lastReverted e exclui getParams por require false.

## Incidente em tempo real: EXECUÇÃO INTERROMPIDA

Durante a preparação de scratch, ainda antes de uma compilação de R10, a consulta de integridade do Git deixou de funcionar: "fatal: not a git repository" para o checkout AGENTE-01 embora a pasta .git estivesse visível. Verificação pontual somente de leitura mostrou EIO real na listagem de .git/objects e .git/refs; Python também falhou com OSError [Errno 5] Input/output error ao carregar módulos. **Nenhum contrato foi corrigido e nenhum processo de teste foi iniciado após este EIO.** Não houve git reset, rebase, shutdown, reparo, exclusão de outro checkout ou gravação adicional nesse WSL. **A infraestrutura inicialmente saudável tornou-se NÃO ÍNTEGRA.**

A conclusão técnica é INFRA_EIO, não COMPILE_ERROR, PREFLIGHT_AUTH_BLOCKED nem falha Solidity. A Rodada 10 prosseguiu exclusivamente com documentação por GitHub e referências públicas já fixadas.

## Execuções CVL2 e outros testes nesta R10

| Operação | R10 real | Saída/exito atribuído |
| --- | --- | --- |
| certoraRun --compilation_steps_only P10/33 | **NOT_RUN_INFRA_EIO** | Nenhum log novo |
| certoraRun --compilation_steps_only P10/34 | **NOT_RUN_INFRA_EIO** | Nenhum log novo |
| solc original ProxyHarness | **NOT_RUN_INFRA_EIO** | Erros de override pertencem à R9, não à R10 |
| solc --abi cena handler pós-Perl | **NOT_RUN_INFRA_EIO** | Sem ABI e sem ambiente íntegro |
| Perl transformações HMaker/HBalancer/HSCompound | **NOT_RUN_INFRA_EIO** | Os 18 arquivos alterados referem-se à R9 |
| Prover formal e CVL1 | **PROIBIDO / NÃO EXECUTADO** | Nenhuma prova |

## Validadores históricos e diff commitado

| Comando exato exigido | Status R10 | Motivo |
| --- | --- | --- |
| python3 scripts/check_specs.py . (raiz Web3Bugs-certora) | **NOT_RUN_INFRA_BLOCKED** | Git/Python no WSL apresentaram EIO |
| python3 scripts/check_contests_csv.py . | **NOT_RUN_INFRA_BLOCKED** | Mesmo incidente |
| python3 scripts/check_contracts.py . | **NOT_RUN_INFRA_BLOCKED** | Mesmo incidente |
| git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD | **NOT_RUN_INFRA_BLOCKED** | Checkout local não íntegro; não inventar exit 0 |

Na R9, os quatro comandos tinham sido executados com EXIT 0 na HEAD fc668cc... antes do incidente, mas **aquela rodada NÃO substitui QA local após os commits R10**. GitHub Actions validate, se passar na HEAD R10, é apenas CI estrutural, nunca CVL1/CVL2 Prover nem substituto para os quatro comandos neste dispositivo.

## Verificações alternativas via conector GitHub

- PR #39 HEAD inicial e estado DRAFT conferidos antes das escritas. Nenhuma branch ou arquivo de AGENTE-02 modificado.
- Usada matriz R9 de 266 chaves e CSV baseline do catálogo (266 P10). Reconciliador CSV em memória pelo conector confirmou 266 identidades únicas e igualdade em Property, Target Contract, Result, Detection Outcome, Bug Label e path Spec; Git blob SHA-1 dos N.spec e N.sol preservados da auditoria byte-exata R9 (não recalculados sobre filesystem EIO).
- Nova ROUND10_MATRIX_266.csv contém 266 identidades e estado separado ORIGINAL R5 (2 COMPILE_ERROR + 264 NOT_RUN), DERIVADO R9 (1 COMPILE_OK, 1 COMPILE_ERROR + 264 NOT_RUN), EXECUÇÕES R10 (0), SEMANTIC_EQUIVALENCE (0).
- Após os commits, repetir via conector a comparação dos CSVs e revisar o escopo completo BASE...HEAD, whitespace textual dos arquivos novos e CI Github. A validação em memória **NÃO** executa os scripts históricos nem git diff --check.

## Gate humano e operacional

**Alerta infraestrutura VERMELHO:** administrador recuperar filesystem mantendo worktrees e logs; verificar saúde Git/Python e checksum dos arquivos, sincronizar sem reset e executar os quatro checks na HEAD R10. **Alerta semântico VERMELHO:** nenhuma equivalência histórica comprovada. Não permitir nova compilação, uso do Perl, Prover ou mudança de source até o host estar comprovadamente íntegro e o coordenador aprovar cenário por property.

**AGENTE-01 — RODADA 10.**
