# AGENTE-04 — ROUND7 QA e gate de infraestrutura

## 1. O que foi realmente EXECUTADO nesta Rodada 7

- GitHub get_pr_info: branch research/cvl2-agente-04 HEAD inicial 3cd8f72c35d94b4a48cb6155628cba4bea378c67; PR #42 DRAFT e não mergeado.
- GitHub fetch_file: os quatro documentos normativos, as quatro fontes da coordenação R6, ABI e import CSV de R5, casos originais/specs/harnesses P15/P12/P2, e exemplos P1 para a semântica de complete/incomplete.
- Reconciliação IN-MEMORY via JavaScript do conector: original results/spec/spec_buglabel.csv contém 1390 relações e 1386 IDs; **blob SHA1 idêntico** no baseline 2a03637... e HEAD 3cd8f72... = 97e20443586540034a4c0305ce1db19b0d2f8cb5.
- Round6 matriz 157 chaves distintas, P2=15 / P12=26 / P15=116, comparadas contra todas as relações do CSV canônico, incluindo duplicatas Bug Label; zero divergências em (Project ID, Status, Example ID, Property, Target Contract, Result, Detection Outcome, N.spec path).
- Round7 matriz nova 157 chaves distintas, contadores reconciliados a R6: 3 COMPILE_ERROR **herdados** (P12/23,25; P15/36), 154 NOT_RUN, 0 COMPILE_OK, 0 PREFLIGHT_AUTH_BLOCKED. **Nenhuma execução CLI nova R7.** N.spec/source SHA256 foram preservados do ledger histórico já auditado; **não recalculados** na máquina comprometida.
- Sources versionadas upstream aave/gho-core@ce49fb0 e aave/protocol-v2@7509203 recuperadas somente leitura via GitHub; documentação Certora oficial atual consultada.
- Auditoria cruzada dos PRs #40 e #46 exclusivamente read-only.

## 2. Scripts oficiais — STATUS NA HEAD R7

| Controle | Diretório / comando exigido | STATUS | Explicação |
| --- | --- | --- | --- |
| Catálogo specs | Web3Bugs-certora/: python3 scripts/check_specs.py . | **NOT_RUN_INFRA_BLOCKED** | WSL DESKTOP-5E26TVU SIGBUS/EIO/EROFS, sem recuperação humana comprovada |
| Contests CSV | Web3Bugs-certora/: python3 scripts/check_contests_csv.py . | **NOT_RUN_INFRA_BLOCKED** | Mesmo gate; GitHub CI de outra HEAD não substitui validação local |
| Contratos | Web3Bugs-certora/: python3 scripts/check_contracts.py . | **NOT_RUN_INFRA_BLOCKED** | Mesmo gate |
| Whitespace commitado | Git root: git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD | **NOT_RUN_INFRA_BLOCKED** | Não simular git diff por JS nem presumir exit 0 |
| Certora CLI --compilation_steps_only | scratch, cenário individual P15/36 ou P12/23,25 | **NOT_RUN_INFRA_BLOCKED** | Os 3 COMPILE_ERROR são de R5/R6, não novos |

**Importante:** validação da nova matriz por JavaScript e GitHub Actions, se houver, são controles DIFERENTES dos quatro comandos acima. Não inventar COMPILE_ERROR, COMPILE_OK, SUCCESS local ou logs de R7. Nenhum arquivo de log novo, porque nenhum compile-only foi executado.

## 3. Gate humano obrigatório para retomar WSL

Antes de tentar novos comandos nesse host, o administrador deve assegurar backup e recuperação do filesystem Windows/WSL. Após confirmação externa de saúde, em primeiro lugar verificar filesystem leitura/escrita em diretório temporário novo; depois Python, Git, HEAD, worktree, integridade de cache e versões/hashes sem expor tokens; só então executar os três validadores e diff exato na HEAD atualizada e registrar stdout, stderr, exit. Nenhum reset, rebase, patch, reinstalação nem compilação pelo agente enquanto esse gate estiver fechado.

**QA textual realizado no conector GitHub:** matriz contábil/identidade verificada em memória e arquivos novos examinados contra trailing whitespace, blank EOF e space-before-tab (checagem JavaScript de conteúdo; NÃO o git diff obrigatório). Todos os caminhos novos limitados a Web3Bugs-certora/docs/cvl2/research/AGENTE-04/. PR permanece Draft, sem merge.

## 4. Comunicação ao coordenador

Status sinal: **LARANJA, BLOQUEIO HUMANO DE INFRAESTRUTURA**. Gate de Fase 2 fechado, zero equivalências. Próximo passo depende (i) WSL recuperado e QA reproduzido e (ii) decisão por property quanto a método external, envfree/static checks e source global P15/36; ABI histórica P12/23,25; receiver de feed Chainlink P2.

AGENTE-04 — RODADA 7
