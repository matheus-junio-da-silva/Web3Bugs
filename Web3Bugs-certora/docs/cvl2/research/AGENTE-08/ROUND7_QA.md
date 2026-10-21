# AGENTE-08 — RODADA 7 / QA de evidência versus execução

PR existente [#43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43), branch `research/cvl2-agente-08`; HEAD inicial conferida `748a8e345061961faf977f78cf9bcce7739e8385`; baseline fixo `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Documentação publicada **exclusivamente via conector GitHub** porque [incidente do WSL](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/948121599b546d61579dc9ecb8c316f9c088e78a/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_WSL_IO_INCIDENT.md) permaneceu sem recuperação administrativa comprovada. **Nenhum comando local foi enviado ao WSL nesta rodada**, em cumprimento da instrução do coordenador.

## Verificações executadas por GitHub — NÃO equivalem a QA de filesystem

1. `get_pr_info` em #43 verificou HEAD anterior exata, branch correta, PR `draft=true`, estado open, baseline correto. Coordenador [revisão R6](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43#pullrequestreview-5590013542) também confirmou EIO/EROFS/SIGBUS.
2. Quatro documentos de catalogação foram recuperados por GitHub e lidos integralmente (`spec_catalog.md`, `spec_catalog_workflow.md`, `spec_catalog_project_1.md`, `standard.md`). Como referência histórica, comparados `complete/1/1.spec`, `incomplete/1/1.spec` e `incomplete/1/1.txt`.
3. `ROUND7_MATRIX_155.csv` foi **recarregado** do GitHub e cruzado por chave `(project_id,original_status,example_id)` com `results/spec/spec_buglabel.csv` do baseline Git SHA `97e20443586540034a4c0305ce1db19b0d2f8cb5`. **EXECUTADO no conector em memória:** 155 linhas distintas (P5=17, P13=58, P14=34, P23=46); **0 mismatch** em Property, Target, Result, Detection Outcome, Original Spec e Original Spec Lines; **155 NOT_RUN CVL2**. Nenhum status histórico ou N.spec foi editado. N.spec SHA256 foi herdado da matriz R6 anteriormente verificada ao catálogo; **não afirmar que 155 SHA256 foram recomputados nesta rodada**.
4. Confronto **independente de provenance por família**: para os 46 P23, `Original Spec` canônico e nome do `certora/specs/N.spec` recuperado estão coerentes (**0 mismatch**); para 41 dos 58 P13 com runner identificado, target declarado no runner corresponde ao Target Contract canônico (**0 divergência**); 17 não possuem runner correspondente nos dez scripts considerados.
5. Recarregado `ROUND7_SOURCE_MANIFEST.csv`, 43 registros SHA Git (8 P5, 11 P13, 1 P14, 23 P23). Com GitHub tree `Certora/drips-contracts@8d1db123...` foi verificada **identidade Git blob** das **seis specs** de P23 e `src/Splits.sol` contra o snapshot, sem baixar binários nem criar código.
6. Os documentos novos foram escritos com verificação estática de whitespace (sem linhas finais com espaços) antes da publicação. Isso **não substitui** o `git diff --check` commitado completo.

## QA pedido após commit: explicitamente NÃO EXECUTADO localmente

Os comandos abaixo são **plano de retomada, não saídas reais da R7**, e só poderão rodar após o administrador comprovar saúde do filesystem WSL e o checkout da branch correta:

```bash
cd Web3Bugs-certora/
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
cd ..
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

| Verificação | Local R7 / execução | Status |
| --- | --- | --- |
| `python3 scripts/check_specs.py .` | WSL: NÃO EXECUTADO | **NOT_RUN_INFRA_BLOCKED** |
| `python3 scripts/check_contests_csv.py .` | WSL: NÃO EXECUTADO | **NOT_RUN_INFRA_BLOCKED** |
| `python3 scripts/check_contracts.py .` | WSL: NÃO EXECUTADO | **NOT_RUN_INFRA_BLOCKED** |
| `git -c core.whitespace=cr-at-eol diff --check BASE...HEAD` | WSL: NÃO EXECUTADO | **NOT_RUN_INFRA_BLOCKED** |
| `certoraRun --compilation_steps_only` P5/14 | WSL scratch: NÃO EXECUTADO | **NOT_RUN_INFRA_BLOCKED** |
| Prover formal, CVL1, Solidity compilation, patch/migration in-place | NÃO EXECUTADO | **NOT_RUN** |

**Não atribuir `exit 0` a esses comandos**; da mesma forma, `PREFLIGHT_AUTH_BLOCKED` requer um erro real de CERTORAKEY, que **não ocorreu**. `COMPILE_ERROR` requer parser/typechecker executado e log atribuível à key, inexistente nos 155 exemplos do AGENTE-08. `INFRA_EIO` é blocker externo separado, não código de erro CVL2. `COMPILE_OK=0, COMPILE_ERROR=0, PREFLIGHT_AUTH_BLOCKED=0, NOT_RUN=155, SEMANTIC_PROVEN=0`.

**CI GitHub Actions:** pode executar `validate` na HEAD publicada. Se retornar `SUCCESS`, seu escopo é somente validação estrutural no GitHub; registrar como **CI remoto** em separado e nunca como execução local dos quatro comandos. `compare_commits` pode certificar paths no PR, mas não executa `git diff --check`.

## Proveniência / fontes recuperadas que NÃO equivalem a compile-only

- P5: 11 inputs/10 links em `verifyBridge.sh`; `BridgeHarness` solc0.8.10 compilado **na R5**, não agora; primeira tentativa de solc da R5 falhou por symlink antes do retry. R7 somente leitura.
- P14: ABI Controller original/postscript 39/42 funções com solc0.6.10 na **R5**; R7 investiga [0] e alcance de reverts documentalmente.
- P13: dez drivers do snapshot com solc7.5 ou solc7.6, 41 cases mapeados/17 sem match; sem solc local novo.
- P23: branch pública `certora@8d1db123` fornece harnesses e scripts SHA exatos + source spec idêntico; **nenhum wrapper CVT gerado e nenhuma execução histórica foi autenticada**, nenhuma ABI Solidity compilada na R7.
- P10/PR #39: apenas auditoria cruzada READ-ONLY; dois errors CVL2 de **outro agente** na R5, sem execução por AG08.

## Saída e condição de desbloqueio humano

Antes de permitir WSL novamente: administrador valida backup/saúde do volume, leitura+escrita em novo diretório temporário, `git status` e HEAD correctos, versões de `python3`/`solc`/`certoraRun` e hashes dos originais; **só então** repetir quatro comandos QA. Para P5/14, fixar target/10 links, 11 seeds, solc8.10, cópia byte-idêntica com SHA256/cmp, stdout/stderr e timeout ~60s, sem credenciais, sem Prover, sem CVL1. Solicitar gate individual se houver proposta derivada.

**Estado operacional AGENTE-08 — RODADA 7: LARANJA / DOCUMENTAÇÃO VERIFICADA PELO GITHUB, QA LOCAL NÃO EXECUTADO.**
