# AGENTE-06 — Rodada 6: matriz, QA e proveniência de execuções

**Data 2026-10-20; worktree isolada:** \`/home/mat/agente06-round6-20261020\`, iniciada em \`ad460c288729d881a8adfac212695415809fc07d\`, sem reset nem alterações nos originais. **PR #38 permanece Draft;** documentos desta rodada foram publicados exclusivamente via GitHub na branch existente quando ocorreu falha de I/O no WSL. Isso significa que os comandos finais não puderam ser repetidos sobre o novo checkout; separar **resultado observado** de **resultado não observado**.

## Controle da matriz

A [ROUND6_MATRIX_159.csv](ROUND6_MATRIX_159.csv) foi gerada da fonte versionada [ROUND5_MATRIX_159.csv](ROUND5_MATRIX_159.csv) e dos quatro \`{1,4,17,22}/properties.csv\`. O procedimento de geração verificou (no ambiente do conector GitHub): **159 registros**, **159 chaves distintas**, cobertura P1=70, P4=27, P17=41 e P22=21, correspondência da chave individual e igualdade dos SHA-256 das N.spec **reportados nas duas matrizes anteriores**. Não houve re-hash dos bytes das 159 N.spec nesta execução porque o ambiente local de execução ficou indisponível; a verificação direta desses hashes ocorreu na Rodada 5 e os arquivos originais continuam intocados. As colunas \`historical_result\` e \`historical_detection_outcome\` foram copiadas de \`original_report_result\`/\`original_detection_outcome\` das matrizes preexistentes, **não inferidas** por status de compilação. Todos os 159 registros têm \`cvl2_compile_status=NOT_RUN\` e \`actual_cvl2_exit_code=NOT_OBSERVED\`.

## Comandos e códigos efetivamente observados

| Ação | Escopo | Evidência observada | Classificação |
| --- | --- | --- | --- |
| \`/home/mat/certora-ac-audit/certora_venv/bin/certoraRun --version\` | Preflight local não compilatório | \`certora-cli 8.19.0\`, CLI presente | Ferramenta encontrada; não é CVL2 parser/compilation |
| \`/home/mat/.local/bin/solc --version\` | Preflight Solidity | \`solc 0.8.7\`; scripts P4 requerem \`solc8.17\` | Versão padrão incompatível com runner |
| \`timeout 60s npm install --prefix /tmp/ag06-round6-solidity-20261020/toolchain --no-save --ignore-scripts --no-audit --no-fund --silent solc@0.8.17\` | Scratch externo ao repo, sem scripts npm | **EXIT 0**; \`0.8.17+commit.8df45f5f.Emscripten.clang\` detectado; soljson SHA-256 \`04184dd4a976c37a64c8d6470e25983cfdbb09b10ff371da9178f50d6e132745\` | Compiler adquirido, sem build bem-sucedido |
| \`timeout 60s node compile_p4.js\` | Scratch; Solidity standard-json contendo fontes \`munged\` derivadas e harnesses byte-idênticos | Processo \`Bus error\`, abortou antes do resultado. \`result.json\` não gerado. Código de compilação Solidity **não determinado** | **ENVIRONMENT_FAILURE**; nenhum \`COMPILE_OK\`/ABI; não é COMPILE_ERROR CVL2 |
| \`python3 -c 'print("PYTHON_OK")'\` | Teste runtime WSL | Processo \`Bus error\`, **EXIT 135** | Falha de infraestrutura |
| \`python3 scripts/check_specs.py .\` | Raiz Web3Bugs-certora worktree, tentativa após commits documentais GitHub | Processo \`Bus error\`, **EXIT 135** | Validador **não concluiu**; não relatar PASS nem falha do catálogo |
| \`python3 scripts/check_contests_csv.py .\` | Mesmo local | Processo \`Bus error\`, **EXIT 135** | Validador **não concluiu** |
| \`python3 scripts/check_contracts.py .\` | Mesmo local | Processo \`Bus error\`, **EXIT 135** | Validador **não concluiu** |
| \`timeout 30s git ... fetch origin refs/heads/research/cvl2-agente-06\` | Atualização dos Git objects **sem checkout nem reset** | Processo \`Bus error\`, **EXIT 135**; \`FETCH_HEAD\` não criado | Falha de infraestrutura |
| \`git -c core.whitespace=cr-at-eol diff --check BASE...FETCH_HEAD\` | Tentativa de QA sobre a HEAD remota após fetch | **EXIT 128**: \`FETCH_HEAD\` ausente; **nenhum diff validado** | Não é resultado de whitespace no diff |
| \`certoraRun --compilation_steps_only\` | Nenhuma property deste agente | **NÃO EXECUTADO** | \`NOT_RUN=159\`, \`COMPILE_ERROR=0\`, \`COMPILE_OK=0\`, \`PREFLIGHT_AUTH_BLOCKED=0\` |
| Prover/CVL1/migration script | Nenhum | **NÃO EXECUTADO** | Sem inferência de equivalência |

Os comandos Python/solc que falharam por \`Bus error\` são evidência de pane no ambiente, não diagnóstico semântico nem parser de CVL2. Logs de stdout/stderr do build não contiveram diagnóstico Solidity; nenhuma ABI foi produzida. Arquivos externos em \`/tmp\` não foram copiados para \`contracts/\` ou \`results/\`.

## CI independente no GitHub

Para o commit documental \`95e325aa848db7ac997e25348b02cdd6acf392be\`, a execução [GitHub Actions validate #39473050452](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39473050452) terminou **SUCCESS**. Jobs observados em \`integrity_validation\`: \`check_contests_csv\` SUCCESS, \`check_contracts\` SUCCESS, \`check_git\` SUCCESS. Não se observou um step de nome \`check_specs\` nessa listagem; **não** substituir com isso o comando local que falhou. O workflow não testa migração CVL2 nem equivalência. O estado do workflow da HEAD final deve ser consultado separadamente após o último commit deste QA.

## Gate e remediação operacional

Não executar mais compilação enquanto o WSL apresentar \`Bus error\` e Input/output error em utilitários básicos. Coordenador deve restaurar/inspecionar o runtime, **sem apagar material de outros worktrees**, e reexecutar da raiz Web3Bugs-certora:

\`\`\`bash
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
\`\`\`

Da raiz Git, após sincronizar os objetos da HEAD do PR de pesquisa com cuidado, sem reset, executar:

\`\`\`bash
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
\`\`\`

Até isso ser observado em runtime íntegro, **gate manual de QA local permanece pendente**, apesar de CI estrutural verde. Não promover \`COMPILE_OK\` nem \`SEMANTIC_PROVEN\`, nem fazer merge.

**AGENTE-06 — RODADA 6.**
