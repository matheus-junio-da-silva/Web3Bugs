# AGENTE-08 — Rodada 9 / QA local e evidência de execução

**PR:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43, branch `research/cvl2-agente-08` (Draft).
**HEAD de partida, verificada antes de editar:** `f38d9089e6ceeb85b1c54d2df07a44f7cea577ce`.
**Baseline imutável:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
**Checkout isolado e scratch exclusivos R9:** `/home/mat/cvl2-agente08-round9-20261020/repo` e `.../scratch/P5_N14`; checkout do AGENTE-01 ou de outros agentes não utilizado para escrita.

## Preflight realmente executado antes de compilar

- `date -Is`, `uname -sr`, `df -h /home/mat /tmp`, `git rev-parse HEAD` e `git status --porcelain` no checkout antigo, tudo respondeu. Scratch `/tmp/agent08-health-20261020` criado, gravado, relido e comparado via `cmp`: **PASS**. Nem EIO, SIGBUS nem EROFS observados.
- Clone **novo e isolado** criado a partir da cópia anterior, `git fetch` da branch existente e checkout exclusivo. `git rev-parse HEAD` = `f38d9089e6ceeb85b1c54d2df07a44f7cea577ce`; `git status --porcelain` vazio antes das mudanças; commit baseline resolvível como objeto Git.
- Pastas de origem e patch: `aave-starknet-bridge` upstream `4c010c18b08703e4f367db1e0c642c76c25e551b`; `git hash-object certora/applyHarness.patch` = `f806c1e6957b164a0a8419fa6f5c8015de5dd95c`. `Bridge.sol` patched no scratch copiado tem SHA256 `f7852c1be61e44e70a46be76606c4a8d9dbdb6ecd9441d2e2bce9df00709058d`, igual ao anterior. N.spec original 14 SHA256 `0c0e05b80677a46deccfe1494e205cf09b966efab14785e6206c37a0a92e2031` com `cmp` byte-idêntico antes e depois.
- Binários disponíveis: `certora-cli 8.19.0` diretamente no venv e `solc 0.8.10+commit.fc410830.Linux.g++` no caminho versionado. A versão da CLI é preflight, **não** compilação em si.
- Os 11 seeds Solidity, 10 `--link`, full `setup.spec`, `bridge.spec`, `erc20.spec` hashes e o patch estão em [ROUND9_P5_N14_INPUT_MANIFEST.csv](ROUND9_P5_N14_INPUT_MANIFEST.csv). A cena usa fontes preexistentes e o patch histórico fixo, não um patch executado in-place nesta rodada.

## Compilação realmente executada — uma única tentativa ORIGINAL

**Comando executado:** [ROUND9_P5_N14_command.txt](ROUND9_P5_N14_command.txt). Entrada: `results/spec/incomplete/5/14.spec` **byte-idêntica**, target `BridgeHarness`, 11 Solidity seeds, 10 `--link`, compilador solc 0.8.10 com caminho absoluto. `env -i HOME=<scratch-home> PATH=... timeout -k 5s 68s certoraRun ... --compilation_steps_only`. Nenhuma credencial herdada, Prover formal/CVL1 desativados por tipo de execução. A spec executada é o **fragmento N14**, não a global `bridge.spec`; flags de solver `--settings` e `--cloud` do runner auditado não foram utilizadas, pois não há prova. Um bom resultado do fragmento, se houvesse, não atestaria a full spec.

**RESULTADO REAL:** `exit code = 1` (não timeout), 10 linhas de stdout, 0 linhas de stderr. O stdout bruto termina com linha em branco; `ROUND9_P5_N14_stdout.log.b64` preserva os bytes originais sem inserir whitespace inválido no diff Git; decodificar com `base64 -d`. O stdout apresenta erros do typechecker CVL2 em `14.spec:8:5` e `:9:5` (`methods` exige `function`) e `14.spec:8:64` e `:9:46` (`methods` exige `;`). Log original integral [stdout](ROUND9_P5_N14_stdout.log.b64) SHA256 `cbf24143137931fcd317c00fd3c175e440fcbf5a16b9efc945ce21f49e4269f8`; [stderr](ROUND9_P5_N14_stderr.log) SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. A origem do erro é o **parser/typechecker CVL2**, não token/infra/solc; `COMPILE_ERROR` atribuível somente ao exemplo P5/incomplete/14. Nenhuma variante derivada foi criada ou executada.

**Integridade da classificação R9:** `ROUND9_MATRIX_155.csv` foi criada a partir de `ROUND8_MATRIX_155.csv` sem mudar Property, Target, Bug Label, Result, Detection Outcome, Original Spec e N.spec SHA256. Requer exatamente 155 chaves únicas `(project_id,original_status,example_id)`: P5 17, P13 58, P14 34, P23 46. Um `COMPILE_ERROR` P5/14, **154 `NOT_RUN`**, 0 `COMPILE_OK`, 0 equivalências demonstradas. Tentativas originais = **1**, derivadas = **0**, não somar essas contagens como duas properties.

## Verificações após a publicação

As verificações obrigatórias estão planejadas para **depois do primeiro commit/push** da R9 e devem ser registradas na revisão final do PR e no complemento deste arquivo. Os resultados abaixo **não serão presumidos**, só declarados após comandos concluídos:

```bash
cd Web3Bugs-certora
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
cd ..
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

CI GitHub `validate` é separado: estrutural, nunca prova CVL2. Após HEAD final, confirmar por GitHub que o PR #43 está Draft e que `BASE...HEAD` contém somente arquivos em `Web3Bugs-certora/docs/cvl2/research/AGENTE-08/`, com worktree limpa.

**Alerta semântico:** VERMELHO para equivalência não demonstrada, filtros e reverts; **QA de catálogo não equivale a migração CVL2**.
