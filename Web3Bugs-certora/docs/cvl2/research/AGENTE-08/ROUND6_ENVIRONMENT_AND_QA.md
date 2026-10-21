# AGENTE-08 — Rodada 6 / preflight, logs e QA sem falsos PASS

Data: 2026-10-20. Branch `research/cvl2-agente-08`. HEAD anterior conferida `97924c06366bacc260a8adebfa0c3754887248c2`, sem reset. PR #43 DRAFT.

## Experimentos verdadeiramente executados

| Momento / chamada | Local | Saída observada | Exit/classificação |
| --- | --- | --- | --- |
| `git rev-parse HEAD`; `git status --porcelain` antes dos testes | checkout isolado WSL R5 | `97924c06366bacc260a8adebfa0c3754887248c2`; worktree inicialmente sem arquivos alterados | leitura OK |
| `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun --version` | WSL CLI direto de coordenação | `certora-cli 8.19.0` | **exit 0**; somente versão, não compila CVL |
| `mkdir -p /home/mat/cvl2-agente08-round4-20261020/scratch/round6/p5-14` | WSL, preparação de cópia `incomplete/5/14.spec` | `mkdir: Read-only file system` | **exit 1**, somente filesystem; **nenhum** `certoraRun` foi iniciado |
| `mkdir -p /home/mat/cvl2-agente08-round6-isolated/scratch` | tentativa alternativa WSL | `mkdir: Read-only file system` | **exit 1**, somente filesystem |
| `touch /home/mat/cvl2-agente08-round6-isolated/scratch/write-test` | tentativa de gravar arquivo | `No such file or directory` porque diretório não pôde ser criado | **exit 1**; não é parser/CLI |
| `git -C /home/mat/cvl2-agente08-round4-20261020/repo rev-parse HEAD` após falha | checkout isolado WSL | `fatal: couldn't read .git/packed-refs: Input/output error` | **exit 128** |
| `git ls-remote https://github.com/matheus-junio-da-silva/Web3Bugs.git refs/heads/research/cvl2-agente-08` | WSL, rede independente da pasta corrompida | `97924c06366bacc260a8adebfa0c3754887248c2 refs/heads/research/cvl2-agente-08` | **exit 0**, HEAD inicial remota |
| Busca GitHub no `Certora/drips-contracts` por `Splits2.spec`, `CVT`, `splitResults` | índice GitHub | 0 resultados indexados nesse escopo | documentação de busca negativa, não prova de ausência absoluta |
| Consulta do CLI P5/14 `certoraRun --compilation_steps_only` | Scratch P5/14 | **NÃO EXECUTADA**, pois pré-condição de cópia gravável falhou | **NOT_RUN**, exit `N/A` |
| Verificações CVL de P13, P14, P23 | Worktree/scratch | **NÃO EXECUTADAS** | **NOT_RUN**, exit `N/A` |

**Classificações sem misturar:** `PREFLIGHT_AUTH_BLOCKED=0` — nenhum erro de CERTORAKEY foi observado no CLI direto nesta rodada. `COMPILE_ERROR=0` — um erro de parser CVL requer que uma compilação seja executada; não ocorreu. `COMPILE_OK=0`, `NOT_RUN=155`. Solc histórico executado nas rodadas anteriores pertence ao diagnóstico **Solidity**, não é novo resultado CVL2.

## Limite de entrega e publicação

A falha do dispositivo WSL impediu criação de cópias novas, logs `certoraRun` e qualquer `git commit/push` local confiável. **Documentação publicada por GitHub Contents API** diretamente na mesma branch de pesquisa, sem force push e sem edição de arquivos de outros agentes; este mecanismo cria commits versionados na mesma PR. Matrizes foram checadas antes do upload com parsing CSV e 155 chaves únicas (P5 17/P13 58/P14 34/P23 46). Não inventar um SHA de arquivo temporário inexistente, pois a cópia `N.spec` não chegou a ser criada.

**QA solicitado APÓS a publicação:** os comandos exatos são

```bash
cd Web3Bugs-certora
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
cd ..
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

**Não foram executados nesta rodada após commit**, pois o WSL falhou em leitura de objetos Git e em escrita de scratch. Não atribuir a eles exit 0 por inferência. Se o GitHub Actions `validate` executar, registrar separadamente como CI remoto estrutural, nunca como execução local dos quatro comandos. O retorno do CI não comprova semântica CVL2, e a matriz não representa uma migração realizada.

## Referências e checks anteriores (não repetidos nesta rodada)

- R5 `ROUND5_SOLIDITY_FULL_COMPILER_LOGS.txt`: logs integrais das **sete** tentativas Solidity anteriores, seis exit 0, uma primeira falha de symlink por `--allow-paths`. Não são compilação CVL2.
- R5 `ROUND5_SOLIDITY_ABI_REGISTER.csv`: 40 ABI P5, 71 ABI P14, incluindo dependências; não confundir quantidade de ABI com propriedades CVL.
- Os três validadores e `git diff --check` tiveram exit 0 **na Rodada 5** no commit `97924c06366bacc260a8adebfa0c3754887248c2`, mas isso não é QA pós-commit da R6.

**Bloqueio operacional:** recuperar filesystem WSL gravável ou novo ambiente isolado; então executar os quatro checks e teste P5/14 em scratch com logs e timeout. Não executar Prover, CVL1 nem alterar originais para solucionar esse bloqueio.
