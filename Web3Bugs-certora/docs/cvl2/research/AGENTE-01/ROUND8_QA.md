# AGENTE-01 — RODADA 8 / QA reproduzível e bloqueio local

PR existente https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 · branch `research/cvl2-agente-01` · HEAD inicial **verificada** `a9f881bf5cb6158b6614554cd4d0250f34ca340a` · baseline imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.

## O que ocorreu nesta rodada (checks remotos, NÃO parser CVL)

1. Pelo conector GitHub, lidos os quatro documentos normativos do dataset na baseline, exemplos P1 complete e incomplete, revisão mais recente do PR #39 e painel `ROUND7_DASHBOARD.md` integrado em main pelo PR #47.
2. Fontes Certora atuais migration/changes/methods/ghosts/hooks/statements e Solidity 0.6.12 assembly + Solidity 0.6.0 virtual/override consultadas via documentação oficial. Nova adjudicação da origem `stack_slot`: sintaxe `x_slot` historicamente válida de storage em Solidity 0.6.x, mas compilação da cena ainda ausente.
3. Resultados históricos de P10 **copiados sem alteração** do `results/spec/spec_buglabel.csv` original para `ROUND8_MATRIX_266.csv`. Gerada a matriz de **266 propriedades únicas**, incluindo os rótulos Bug Label e os campos `Property`, `Target Contract`, `Result`, `Detection Outcome` e path `Spec`; reconciliador via conector compare em memória (confirmação pós-publicação no comentário PR).
4. Colunas disjuntas: `source_or_report_fact`, `inference`, `missing_proof`, `cvl2_compile_observed_status`, `cvl2_observation_executor`, `cvl2_observed_round`, `cvl2_observed_exit_code`, `r8_compile_attempt_status`. **Não transportar duas saídas R5 como se fossem novas R8**. O campo `audited_target_git_blob_sha1` dos onze HBalancer foi atualizado especificamente para `f1d09c9f4c4c55d1ec5f3f28f60a1f6068c2e797` (fonte upstream 2021), sem alterar os `incomplete` do catálogo.
5. Auditoria read-only do PR #37, HEAD R7 `4ceac5d5e988dba5b54c44d5678f486a6dabc5af`: P18/3 e /23, ambos erros anteriores **do coordenador**, plus proposta R7 do AGENTE-02 para /4,/46,/53 que continua NOT_RUN. Nenhum arquivo de outros agentes editado.
6. Fonte Furucombo 2021, tagged OpenZeppelin 3.3.0 e fontes adicionais em `ROUND8_CLOSURE_DELTA.csv` recuperadas por GitHub; sem rodar Perl ou construir ABI. Propostas de sintaxe somente em `ROUND8_MINIMAL_DIFF_PROPOSAL.md`.

## O que não se executou

Por ordem do coordenador, o WSL DESKTOP-5E26TVU permanece **INFRA_EIO / EROFS / SIGBUS**, sem recuperação humana atestada. **Nenhum** comando foi enviado ao WSL na R8; sem worktree novo, scratch, `solc`, `certoraRun`, Perl, patch ou prover. Portanto:

| Comando originalmente solicitado | Status local R8 | Exit code |
| --- | --- | --- |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | **NOT_RUN_INFRA_BLOCKED** | **NÃO EXECUTADO** |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_BLOCKED** | **NÃO EXECUTADO** |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_BLOCKED** | **NÃO EXECUTADO** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NOT_RUN_INFRA_BLOCKED** | **NÃO EXECUTADO** |
| `certoraRun --compilation_steps_only` P10/33,34 ou quaisquer incompletos | **NOT_RUN_INFRA_BLOCKED** | **NÃO EXECUTADO** |

Nenhum log R8 de compilação foi criado; versões/flags/exit de R5 estão documentados em `10/round5/diagnostics.csv` e são **históricos**, não renovados. Nenhum `PREFLIGHT_AUTH_BLOCKED` de P10 foi observado nesta R8. Não confundir `SIGBUS`, `solc --abi`, falha de `CERTORAKEY`, `--version` ou CI com diagnóstico do parser ou prova de equivalência.

## QA remoto, escopo, CI e pendências

- O PR deve permanecer **DRAFT** e conter mudanças apenas em `Web3Bugs-certora/docs/cvl2/research/AGENTE-01/`. A comparação via listagem GitHub de arquivos alterados BASE...PR HEAD não equivale ao comando local `git diff --check BASE...HEAD`.
- A ação GitHub `validate`, quando `completed/success`, é uma verificação de **integridade estrutural**, não `COMPILE_OK`, equivalência de contraexemplos ou execução dos quatro comandos locais. Confirmar separadamente o status real na HEAD final após esta adição.
- Controlar toda a matriz P10: **266 com registro de pesquisa; 2 COMPILE_ERROR prévios de R5; 264 NOT_RUN histórico; 0 COMPILE_OK; 266 sem execução R8 por infraestrutura; 0 SEMANTIC_PROVEN; 0 MIGRATED_COMPLETE**.
- Os incidentes `ROUND6_WSL_IO_INCIDENT.md` e painel R7 do PR #47 descrevem pré-condições para liberar qualquer processo WSL.

### Gate dependente de intervenção humana

Recuperação controlada do volume pelo administrador: preservar e verificar backups/worktrees, testar leitura+escrita em scratch novo, obter saúde estável dos executáveis Git/Python/CLI/solc, reconciliar a HEAD com origin **sem reset/rebase automático** e conferir hashes das fontes. Somente depois executar localmente os quatro comandos exatos **na HEAD final** e registrar os exits/stdout/stderr. Para experimentos CVL2, autorização individual separada do coordenador por P10/33 ou P10/34, sem tocar originales; comparação de domínio/vacuity ainda necessária após compile-only.

**Alerta infra: VERMELHO. Alerta semântico: LARANJA.**

**AGENTE-01 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.**
