# AGENTE-01 — Rodada 6 / Registro fiel do QA

**PR:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39 (Draft)  
**Base:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`  
**Local WSL:** `/home/mat/cvl2-agent01-isolated/Web3Bugs` (branch local observada `research/cvl2-agente-01`, HEAD `e31e4fee3174bd91b99c2d62135fb095b1e0253a`).  
**Motivo do uso alternativo de GitHub Contents API para documentação:** falha de leitura `EIO` em arquivos do WSL e `Bus error` ao invocar Python/alguns comandos Git. Não foi aplicado reset, shutdown de WSL, merge ou rebase; nenhum arquivo histórico foi editado.

## QA solicitado: tentativa executada, check NÃO concluído

O comando foi invocado no WSL a partir de `Web3Bugs-certora` para os validadores e a partir da raiz Git para o diff:

| Comando | Observação efetiva | Status confiável de validação |
| --- | --- | --- |
| `python3 scripts/check_specs.py .` | `Bus error`, shell exit **135** | **NÃO CONCLUÍDO — INFRA_EIO** |
| `python3 scripts/check_contests_csv.py .` | `Bus error`, shell exit **135** | **NÃO CONCLUÍDO — INFRA_EIO** |
| `python3 scripts/check_contracts.py .` | `Bus error`, shell exit **135** | **NÃO CONCLUÍDO — INFRA_EIO** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | `Bus error`, shell exit **135** | **NÃO CONCLUÍDO — INFRA_EIO** |

A HEAD local do WSL permaneceu em `e31e4fee...` porque as atualizações R6 foram feitas diretamente na branch remota via GitHub, em vez de escrever em um checkout que apresentava EIO. Assim, essa tentativa **não** constitui o check da nova HEAD remota. Não chamar exit 135 de falha de CVL2, prova de compilação, `PREFLIGHT_AUTH_BLOCKED` ou check negativo do diff.

## Verificações executadas fora do WSL

1. No repositório GitHub, `round6_progress_matrix.csv` foi parseada como CSV com aspas e comparada ao `results/spec/spec_buglabel.csv` fixado na baseline: **266 chaves únicas** `(project_id,original_status,example_id)`, contra 266 linhas/266 chaves canônicas P10; **0 divergências** em Property, Target, Result, Detection Outcome. Estado: 2 COMPILE_ERROR **observados na Rodada 5**, 264 NOT_RUN; 0 COMPILE_OK, 0 SEMANTIC_PROVEN e 0 PREFLIGHT_AUTH_BLOCKED do P10.
2. O workflow remoto GitHub Actions `validate` foi consultado na HEAD documental já publicada e retornou `status=completed`, `conclusion=success`. **CI estrutural não prova equivalência CVL1→CVL2** nem substitui os quatro comandos locais solicitados.
3. O PR foi confirmado `draft=true`. Alterações R6 feitas exclusivamente em `Web3Bugs-certora/docs/cvl2/research/AGENTE-01/10/` por chamadas de escrita para arquivos documentais; nenhuma spec/contrato/catalogação histórica alterada.

## Fechamento operacional

O bloqueio operacional da Rodada 6 é **infraestrutura do WSL**. Quando houver estabilidade de leitura/executáveis, conferir a HEAD remota por fetch não destrutivo, repetir os três validadores e o `BASE...HEAD` real; só então reportar saída local 0 ou falha concreta de conteúdo.

Nenhuma variante CVL2 temporária foi executada em R6. O status de `complete/33–34` preserva exclusivamente os logs integrais anteriores de `round5/logs/`. O progresso documental não cria `COMPILE_OK`.

**AGENTE-01 — RODADA 6.**
